/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        card: "#111827",
        hover: "#162038",
        deep: "#0A0F1C",
        dim: "#1E2D45",
        glow: "#00F5FF",
        primary: "#E5E7EB",
        secondary: "#6B7FA3",
        cyan: "#00F5FF",
        red: "#FF3B3B",
        orange: "#FFA500",
        green: "#00FF9C",
      },
      fontFamily: {
        display: ["Orbitron", "sans-serif"],
        mono: ["Syne Mono", "monospace"],
      },
    },
  },
  plugins: [],
};