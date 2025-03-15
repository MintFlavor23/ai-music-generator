/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        'cartoon': ['"Baloo 2"', 'cursive'],
        'sora': ['Sora', 'sans-serif']
      },
    },
  },
  plugins: [],
}
