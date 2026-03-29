import { useMemo, useState } from "react";
import FieldEditor from "../components/FieldEditor";
import useForms from "../hooks/useForms";
import { createForm, deleteForm, updateForm } from "../services/formService";
import { generateFormFromPrompt } from "../services/aiService";

function blankField() {
  return { type: "text", label: "", options: "" };
}

function toApiFields(fields) {
  return fields.map((field) => {
    const payload = {
      type: field.type,
      label: field.label.trim()
    };

    if (field.type === "select") {
      payload.options = field.options
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    }

    return payload;
  });
}

function FormBuilderPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [fields, setFields] = useState([blankField()]);
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState({ error: "", success: "" });
  const [saving, setSaving] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [editingFormId, setEditingFormId] = useState(null);

  const { forms, refreshForms, loading: formsLoading } = useForms();

  const canSubmit = useMemo(() => {
    if (!title.trim()) {
      return false;
    }
    if (fields.length < 1) {
      return false;
    }
    return fields.every((field) => {
      if (!field.label.trim()) {
        return false;
      }
      if (field.type === "select") {
        return field.options.split(",").map((v) => v.trim()).filter(Boolean).length > 0;
      }
      return true;
    });
  }, [title, fields]);

  const onFieldChange = (index, key, value) => {
    setFields((prev) => prev.map((field, i) => (i === index ? { ...field, [key]: value } : field)));
  };

  const onRemoveField = (index) => {
    setFields((prev) => prev.filter((_, i) => i !== index));
  };

  const onAddField = () => {
    setFields((prev) => [...prev, blankField()]);
  };

  const clearForm = () => {
    setTitle("");
    setDescription("");
    setFields([blankField()]);
    setEditingFormId(null);
  };

  const handleEditForm = (form) => {
    setEditingFormId(form.id);
    setTitle(form.title);
    setDescription(form.description || "");
    setFields(
      (form.fields || []).map((f) => ({
        type: f.type,
        label: f.label,
        options: (f.options || []).join(", "),
      }))
    );
    setStatus({ error: "", success: "" });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCreateForm = async (event) => {
    event.preventDefault();
    setStatus({ error: "", success: "" });
    setSaving(true);

    try {
      if (editingFormId) {
        await updateForm(editingFormId, {
          title: title.trim(),
          description: description.trim() || null,
          fields: toApiFields(fields),
        });
        setStatus({ error: "", success: "Form updated successfully" });
      } else {
        await createForm({
          title: title.trim(),
          description: description.trim() || null,
          fields: toApiFields(fields),
        });
        setStatus({ error: "", success: "Form created successfully" });
      }
      clearForm();
      await refreshForms();
    } catch (err) {
      setStatus({ error: err?.response?.data?.error || "Failed to save form", success: "" });
    } finally {
      setSaving(false);
    }
  };

  const handleGenerateWithAi = async () => {
    setStatus({ error: "", success: "" });
    setGenerating(true);
    try {
      const generated = await generateFormFromPrompt(prompt.trim());
      setTitle(generated.title || "");
      setDescription(generated.description || "");
      setFields(
        (generated.fields || []).map((field) => ({
          type: field.type,
          label: field.label,
          options: (field.options || []).join(", ")
        }))
      );
      setStatus({ error: "", success: "AI generated a form draft" });
    } catch (err) {
      setStatus({ error: err?.response?.data?.error || "AI generation failed", success: "" });
    } finally {
      setGenerating(false);
    }
  };

  const handleDeleteForm = async (formId, formTitle) => {
    if (!window.confirm(`Delete "${formTitle}"? This cannot be undone.`)) return;
    try {
      await deleteForm(formId);
      await refreshForms();
    } catch (err) {
      setStatus({ error: err?.response?.data?.error || "Failed to delete form", success: "" });
    }
  };

  return (
    <section className="grid two">
      <div className="card">
        <h2>{editingFormId ? "Edit Form" : "Create Form"}</h2>
        <form onSubmit={handleCreateForm}>
          <div className="form-row">
            <label>Title</label>
            <input value={title} onChange={(event) => setTitle(event.target.value)} required />
          </div>

          <div className="form-row">
            <label>Description</label>
            <textarea value={description} onChange={(event) => setDescription(event.target.value)} />
          </div>

          <div className="button-row" style={{ marginBottom: "0.8rem" }}>
            <button type="button" className="secondary" onClick={onAddField}>
              Add Field
            </button>
          </div>

          <div className="list">
            {fields.map((field, index) => (
              <FieldEditor
                key={`${field.type}-${index}`}
                field={field}
                index={index}
                onChange={onFieldChange}
                onRemove={onRemoveField}
              />
            ))}
          </div>

          <div className="button-row" style={{ marginTop: "0.9rem" }}>
            <button type="submit" disabled={!canSubmit || saving}>
              {saving ? "Saving..." : editingFormId ? "Update Form" : "Create Form"}
            </button>
            <button type="button" className="warn" onClick={clearForm}>
              Reset
            </button>
          </div>
        </form>

        {status.error ? <p className="notice error">{status.error}</p> : null}
        {status.success ? <p className="notice">{status.success}</p> : null}
      </div>

      <div className="card">
        <h2>AI Assistant</h2>
        <p className="muted">Generate fields from a prompt and edit before saving.</p>

        <div className="form-row">
          <label>Prompt</label>
          <textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Example: Create a customer feedback form with email and rating"
          />
        </div>

        <div className="button-row">
          <button type="button" onClick={handleGenerateWithAi} disabled={!prompt.trim() || generating}>
            {generating ? "Generating..." : "Generate Fields"}
          </button>
        </div>

        <hr style={{ border: 0, borderTop: "1px solid #e5ddce", margin: "1rem 0" }} />

        <h3>Existing Forms</h3>
        {formsLoading ? <p>Loading forms...</p> : null}
        <div className="list">
          {forms.map((form) => (
            <article key={form.id} className="list-item">
              <strong>{form.title}</strong>
              <p className="muted">{form.description || "No description"}</p>
              <small>{form.fields.length} fields</small>
              <div className="button-row" style={{ marginTop: "0.5rem" }}>
                <button
                  type="button"
                  className="secondary"
                  onClick={() => handleEditForm(form)}
                >
                  Edit
                </button>
                <button
                  type="button"
                  className="warn"
                  onClick={() => handleDeleteForm(form.id, form.title)}
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
          {forms.length === 0 && !formsLoading ? <p className="muted">No forms yet.</p> : null}
        </div>
      </div>
    </section>
  );
}

export default FormBuilderPage;
