/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files : ['./src/pages/*.{html,js}',
    './src/components/*.{html,js}'
  ]},
  theme: {
    container: {
    },
    extend: {},
  },
  plugins: [],
}

