import api from "./api";

export async function createForm(payload) {
  const { data } = await api.post("/forms", payload);
  return data;
}

export async function getForms() {
  const { data } = await api.get("/forms");
  return data;
}

export async function getFormById(formId) {
  const { data } = await api.get(`/forms/${formId}`);
  return data;
}

export async function deleteForm(formId) {
  const { data } = await api.delete(`/forms/${formId}`);
  return data;
}

export async function updateForm(formId, payload) {
  const { data } = await api.put(`/forms/${formId}`, payload);
  return data;
}
