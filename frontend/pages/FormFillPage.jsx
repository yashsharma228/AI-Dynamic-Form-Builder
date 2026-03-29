import { useEffect, useMemo, useState } from "react";
import DynamicFieldInput from "../components/DynamicFieldInput";
import { getFormById } from "../services/formService";
import { submitResponse } from "../services/responseService";
import useForms from "../hooks/useForms";

function liveDate() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function liveTime() {
  return new Date().toTimeString().slice(0, 5); // HH:MM
}

function liveDatetime() {
  const now = new Date();
  return new Date(now - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16); // YYYY-MM-DDTHH:MM local
}

function buildInitialAnswers(fields) {
  const values = {};
  for (const field of fields) {
    if (field.type === "date") {
      values[field.label] = liveDate();
    } else if (field.type === "time") {
      values[field.label] = liveTime();
    } else if (field.type === "datetime-local" || field.type === "datetime") {
      values[field.label] = liveDatetime();
    } else if (field.type === "checkbox") {
      values[field.label] = false;
    } else {
      values[field.label] = "";
    }
  }
  return values;
}

function validateField(field, value) {
  // Checkbox: required means must be checked
  if (field.type === "checkbox") {
    if (field.is_required && !value) return `${field.label} must be checked.`;
    return "";
  }

  const isEmpty = value === "" || value === null || value === undefined || String(value).trim() === "";

  if (field.is_required && isEmpty) return `${field.label} is required.`;
  if (isEmpty) return ""; // optional field, no further checks

  if (field.type === "email") {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value)))
      return "Enter a valid email address.";
  }

  if (field.type === "tel") {
    if (!/^[\d\s()\-+]{7,15}$/.test(String(value).trim()))
      return "Enter a valid phone number (7–15 digits).";
  }

  if (field.type === "number") {
    if (isNaN(Number(value))) return "Enter a valid number.";
  }

  if (field.validation_rules) {
    const rules = field.validation_rules;
    const num = Number(value);
    const str = String(value);
    if (rules.min !== undefined && num < rules.min)
      return `Minimum value is ${rules.min}.`;
    if (rules.max !== undefined && num > rules.max)
      return `Maximum value is ${rules.max}.`;
    if (rules.minLength !== undefined && str.length < rules.minLength)
      return `Minimum ${rules.minLength} characters required.`;
    if (rules.maxLength !== undefined && str.length > rules.maxLength)
      return `Maximum ${rules.maxLength} characters allowed.`;
    if (rules.pattern) {
      try {
        if (!new RegExp(rules.pattern).test(str))
          return rules.patternMessage || "Invalid format.";
      } catch {}
    }
  }

  return "";
}

function validateAnswers(fields, answers) {
  const errors = {};
  for (const field of fields) {
    const msg = validateField(field, answers[field.label]);
    if (msg) errors[field.label] = msg;
  }
  return errors;
}

function FormFillPage() {
  const { forms, loading: formsLoading } = useForms();
  const [selectedFormId, setSelectedFormId] = useState("");
  const [selectedForm, setSelectedForm] = useState(null);
  const [answers, setAnswers] = useState({});
  const [fieldErrors, setFieldErrors] = useState({});
  const [status, setStatus] = useState({ error: "", success: "" });
  const [submitting, setSubmitting] = useState(false);
  const [loadingForm, setLoadingForm] = useState(false);

  // Live readiness check — true only when every field passes validation
  const isFormValid = useMemo(() => {
    if (!selectedForm) return false;
    return selectedForm.fields.every(
      (field) => validateField(field, answers[field.label]) === ""
    );
  }, [selectedForm, answers]);

  useEffect(() => {
    if (!selectedFormId) {
      setSelectedForm(null);
      setAnswers({});
      return;
    }

    const loadForm = async () => {
      setLoadingForm(true);
      setStatus({ error: "", success: "" });
      try {
        const form = await getFormById(selectedFormId);
        setSelectedForm(form);
        setAnswers(buildInitialAnswers(form.fields));
        setFieldErrors({});
      } catch (err) {
        setStatus({ error: err?.response?.data?.error || "Failed to load form", success: "" });
      } finally {
        setLoadingForm(false);
      }
    };

    loadForm();
  }, [selectedFormId]);

  const handleAnswerChange = (label, value) => {
    setAnswers((prev) => ({ ...prev, [label]: value }));
    // Clear error on change so user gets instant feedback
    setFieldErrors((prev) => ({ ...prev, [label]: "" }));
  };

  const handleBlur = (label) => {
    if (!selectedForm) return;
    const field = selectedForm.fields.find((f) => f.label === label);
    if (!field) return;
    const msg = validateField(field, answers[label]);
    setFieldErrors((prev) => ({ ...prev, [label]: msg }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedForm) return;

    const errors = validateAnswers(selectedForm.fields, answers);
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      setStatus({ error: "Please fix the errors before submitting.", success: "" });
      return;
    }

    setFieldErrors({});
    setSubmitting(true);
    setStatus({ error: "", success: "" });
    try {
      await submitResponse({ form_id: selectedForm.id, answers });
      setStatus({ error: "", success: "Response submitted" });
      setAnswers(buildInitialAnswers(selectedForm.fields));
      setFieldErrors({});
    } catch (err) {
      setStatus({ error: err?.response?.data?.error || "Submission failed", success: "" });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="card">
      <h2>Fill Form</h2>
      <div className="form-row">
        <label>Select Form</label>
        <select value={selectedFormId} onChange={(event) => setSelectedFormId(event.target.value)}>
          <option value="">Select a form</option>
          {forms.map((form) => (
            <option key={form.id} value={form.id}>
              {form.title}
            </option>
          ))}
        </select>
      </div>

      {formsLoading ? <p>Loading forms...</p> : null}
      {loadingForm ? <p>Loading selected form...</p> : null}

      {selectedForm ? (
        <form onSubmit={handleSubmit}>
          <p className="muted">{(selectedForm.description || "No description").replace(/\bbelow\b/gi, "").replace(/\s{2,}/g, " ").trim()}</p>
          {selectedForm.fields.map((field) => (
            <DynamicFieldInput
              key={field.id}
              field={field}
              value={answers[field.label]}
              onChange={handleAnswerChange}
              onBlur={handleBlur}
              error={fieldErrors[field.label]}
            />
          ))}
          <button type="submit" disabled={submitting || !isFormValid}>
            {submitting ? "Submitting..." : "Submit Response"}
          </button>
          {!isFormValid && (
            <p style={{ color: "#c0392b", fontSize: "0.85rem", marginTop: "0.4rem" }}>
              Fill in all required fields correctly before submitting.
            </p>
          )}
        </form>
      ) : (
        <p className="muted">Pick a form to start answering.</p>
      )}

      {status.error ? <p className="notice error">{status.error}</p> : null}
      {status.success ? <p className="notice">{status.success}</p> : null}
    </section>
  );
}

export default FormFillPage;
