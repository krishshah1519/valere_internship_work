
module.exports = {
  darkMode: 'media', // or 'class'
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bgSecondary: 'var(--bg-secondary)',
        textPrimary: 'var(--text-color)',
      },
    },
  },
  plugins: [],
}
