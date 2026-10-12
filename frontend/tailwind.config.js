/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f4f9',
          100: '#d9e2ed',
          200: '#b3c5db',
          300: '#8da8c9',
          400: '#678bb7',
          500: '#436fa5',
          600: '#1D3557', // Primary color
          700: '#17294a',
          800: '#111e38',
          900: '#0a1326',
        },
        secondary: {
          50: '#edf8f6',
          100: '#d1ebe7',
          200: '#a3d7d0',
          300: '#75c3b8',
          400: '#47afa1',
          500: '#2A9D8F', // Secondary color
          600: '#227d72',
          700: '#1a5e55',
          800: '#133e39',
          900: '#0b1f1c',
        },
        accent: {
          50: '#fdf8e9',
          100: '#faefc8',
          200: '#f5df92',
          300: '#E9C46A', // Accent color
          400: '#e4b43d',
          500: '#d9a41b',
          600: '#ae8316',
          700: '#826210',
          800: '#57420b',
          900: '#2b2105',
        },
        success: {
          500: '#10B981',
        },
        warning: {
          500: '#F59E0B',
        },
        error: {
          500: '#EF4444',
        },
        neutral: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '0': '0',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
        '20': '80px',
        '24': '96px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-light': 'pulseLight 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseLight: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}