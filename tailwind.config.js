/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'react-blue': '#23272F;',
        'navbar-blue': '#1F2329;'
      },
      boxShadow: {
        'custom': '0 20px 25px -5px rgb(255 255 255 / 0.1), 0 8px 10px -6px rgb(255 255 255 / 0.1);'
      },
      gridTemplateRows: {
        'layout': 'repeat(7, 100px);'
      }
    },
  },
  plugins: [],
}