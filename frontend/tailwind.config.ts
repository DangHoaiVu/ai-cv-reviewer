import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#10231e",
        cream: "#f7f6ef",
        mint: "#dff4e8",
        green: "#157a55",
        coral: "#e66c50"
      },
      boxShadow: { soft: "0 22px 70px rgba(16, 35, 30, 0.10)" },
      fontFamily: { sans: ["var(--font-manrope)", "sans-serif"], serif: ["var(--font-lora)", "serif"] }
    },
  },
  plugins: [],
};

export default config;
