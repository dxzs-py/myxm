/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,vue}",
    "./index.html"
  ],
  darkMode: false,
  theme: {
    extend: {
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      screens: {
        'xs': '480px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
      },
      colors: {
        primary: {
          light: '#f0f9ff',
          DEFAULT: '#3b82f6',
          dark: '#1d4ed8'
        }
      }
    }
  },
  variants: {
    extend: {
    }
  },
  plugins: [

  ]
};
