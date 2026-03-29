import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/forms": "http://localhost:5000",
      "/responses": "http://localhost:5000",
      "/ai": "http://localhost:5000",
      "/health": "http://localhost:5000"
    }
  }
});
