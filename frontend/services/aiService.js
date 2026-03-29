import api from "./api";

export async function generateFormFromPrompt(prompt) {
  const { data } = await api.post("/ai/generate-form", { prompt });
  return data;
}
