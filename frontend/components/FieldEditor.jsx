const FIELD_TYPES = ["text", "email", "select", "checkbox"];

function FieldEditor({ field, index, onChange, onRemove }) {
  return (
    <div className="list-item">
      <strong>Field {index + 1}</strong>
      <div className="form-row">
        <label>Type</label>
        <select
          value={field.type}
          onChange={(event) => onChange(index, "type", event.target.value)}
        >
          {FIELD_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="form-row">
        <label>Label</label>
        <input
          value={field.label}
          onChange={(event) => onChange(index, "label", event.target.value)}
          placeholder="Field label"
        />
      </div>

      {field.type === "select" && (
        <div className="form-row">
          <label>Options (comma separated)</label>
          <input
            value={field.options}
            onChange={(event) => onChange(index, "options", event.target.value)}
            placeholder="Option A, Option B"
          />
        </div>
      )}

      <button type="button" className="danger" onClick={() => onRemove(index)}>
        Remove Field
      </button>
    </div>
  );
}

export default FieldEditor;
