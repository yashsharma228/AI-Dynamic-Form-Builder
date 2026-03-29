import api from "./api";

export async function submitResponse(payload) {
  const { data } = await api.post("/responses", payload);
  return data;
}

export async function getResponsesByForm(formId) {
  const { data } = await api.get(`/responses/${formId}`);
  return data;
}
