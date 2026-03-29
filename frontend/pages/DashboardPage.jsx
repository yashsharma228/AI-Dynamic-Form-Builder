import { useState } from "react";
import useForms from "../hooks/useForms";
import { getResponsesByForm } from "../services/responseService";

function DashboardPage() {
  const { forms, loading: formsLoading } = useForms();
  const [selectedFormId, setSelectedFormId] = useState("");
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleViewResponses = async (formId) => {
    if (!formId) {
      setResponses([]);
      setError("");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const data = await getResponsesByForm(formId);
      setResponses(data);
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to fetch responses");
      setResponses([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Responses Dashboard</h2>
      <p className="muted">Admin view for submitted form data.</p>

      <div className="form-row">
        <label>Form</label>
        <select
          value={selectedFormId}
          onChange={(event) => {
            const value = event.target.value;
            setSelectedFormId(value);
            handleViewResponses(value);
          }}
        >
          <option value="">Select a form</option>
          {forms.map((form) => (
            <option key={form.id} value={form.id}>
              {form.title}
            </option>
          ))}
        </select>
      </div>

      {formsLoading ? <p>Loading forms...</p> : null}
      {loading ? <p>Loading responses...</p> : null}
      {error ? <p className="notice error">{error}</p> : null}

      <div className="list">
        {responses.map((response) => (
          <article key={response.id} className="list-item">
            <strong>Response #{response.id}</strong>
            <p className="muted">Submitted at: {new Date(response.submitted_at.endsWith('Z') ? response.submitted_at : response.submitted_at + 'Z').toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })}</p>
            <pre className="answers">{JSON.stringify(response.answers, null, 2)}</pre>
          </article>
        ))}
      </div>

      {!loading && responses.length === 0 && selectedFormId ? (
        <p className="muted">No responses yet for this form.</p>
      ) : null}
    </section>
  );
}

export default DashboardPage;
