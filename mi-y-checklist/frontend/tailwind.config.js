/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: { 50: "#fff5ed", 500: "#e85d1a", 600: "#c84a0d", 700: "#9c380a" },
      },
    },
  },
  plugins: [],
};
