// /** @type {import('tailwindcss').Config} */
// export default {
//   content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// };

// /** @type {import('tailwindcss').Config} */
// export default {
//   content: [
//     "./index.html",
//     "./src/**/*.{js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {
//       animation: {
//         'fade-in': 'fade-in 0.5s ease-out forwards',
//         'float': 'float 3s ease-in-out infinite',
//         'glow': 'glow 2s ease-in-out infinite',
//       },
//       keyframes: {
//         'fade-in': {
//           '0%': {
//             opacity: '0',
//             transform: 'translateY(10px)',
//           },
//           '100%': {
//             opacity: '1',
//             transform: 'translateY(0)',
//           },
//         },
//         'float': {
//           '0%, 100%': {
//             transform: 'translateY(0px)',
//           },
//           '50%': {
//             transform: 'translateY(-10px)',
//           },
//         },
//         'glow': {
//           '0%, 100%': {
//             'box-shadow': '0 0 10px rgba(99, 102, 241, 0.3)',
//           },
//           '50%': {
//             'box-shadow': '0 0 20px rgba(99, 102, 241, 0.6)',
//           },
//         },
//       },
//     },
//   },
//   plugins: [],
// }

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}", // adjust if using other structure
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

