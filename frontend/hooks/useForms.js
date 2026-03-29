import { useCallback, useEffect, useState } from "react";
import { getForms } from "../services/formService";

export default function useForms() {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const refreshForms = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const items = await getForms();
      setForms(items);
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to load forms");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshForms();
  }, [refreshForms]);

  return { forms, loading, error, refreshForms };
}
