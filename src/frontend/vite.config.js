import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // غير هذا الرقم إلى المنفذ المطلوب
    proxy: {
      "/api": "http://localhost:5000", // تأكد من أن هذا يطابق منفذ الخادم الخلفي
    },
  },
});
