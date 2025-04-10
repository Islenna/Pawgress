/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",  // Make sure it looks through your React components
  ],
  darkMode: 'class',  // This enables dark mode using the 'class' strategy
  theme: {
    extend: {},
  },
  plugins: [],
}
