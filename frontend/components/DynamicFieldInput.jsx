function DynamicFieldInput({ field, value, onChange, onBlur, error }) {
  const requiredMark = field.is_required ? <span style={{ color: "#c0392b", marginLeft: "2px" }}>*</span> : null;
  const borderStyle = error ? { borderColor: "#c0392b" } : {};

  const errorMsg = error ? (
    <span style={{ color: "#c0392b", fontSize: "0.82rem", display: "block", marginTop: "2px" }}>{error}</span>
  ) : null;

  const handleBlur = () => onBlur && onBlur(field.label);

  if (field.type === "checkbox") {
    return (
      <div className="form-row">
        <label>
          <input
            type="checkbox"
            checked={Boolean(value)}
            onChange={(event) => onChange(field.label, event.target.checked)}
            onBlur={handleBlur}
            style={{ width: "auto", marginRight: "0.5rem" }}
          />
          {field.label}{requiredMark}
        </label>
        {errorMsg}
      </div>
    );
  }

  if (field.type === "select") {
    return (
      <div className="form-row">
        <label>{field.label}{requiredMark}</label>
        <select
          value={value ?? ""}
          onChange={(event) => onChange(field.label, event.target.value)}
          onBlur={handleBlur}
          style={borderStyle}
        >
          <option value="">Select one</option>
          {(field.options || []).map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        {errorMsg}
      </div>
    );
  }

  if (field.type === "textarea") {
    return (
      <div className="form-row">
        <label>{field.label}{requiredMark}</label>
        <textarea
          value={value ?? ""}
          onChange={(event) => onChange(field.label, event.target.value)}
          onBlur={handleBlur}
          placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
          rows={4}
          style={borderStyle}
        />
        {errorMsg}
      </div>
    );
  }

  if (field.type === "date" || field.type === "time" || field.type === "datetime-local" || field.type === "datetime") {
    const inputType = field.type === "datetime" ? "datetime-local" : field.type;
    return (
      <div className="form-row">
        <label>{field.label}{requiredMark}</label>
        <input
          type={inputType}
          value={value ?? ""}
          onChange={(event) => onChange(field.label, event.target.value)}
          onBlur={handleBlur}
          style={borderStyle}
        />
        {errorMsg}
      </div>
    );
  }

  return (
    <div className="form-row">
      <label>{field.label}{requiredMark}</label>
      <input
        type={
          field.type === "email" ? "email" :
          field.type === "tel" ? "tel" :
          field.type === "number" ? "number" : "text"
        }
        value={value ?? ""}
        onChange={(event) => onChange(field.label, event.target.value)}
        onBlur={handleBlur}
        placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
        style={borderStyle}
      />
      {errorMsg}
    </div>
  );
}

export default DynamicFieldInput;
