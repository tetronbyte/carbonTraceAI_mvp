import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      colors: {
        ink: {
          50:  '#f5f7fa',
          100: '#e1e6ee',
          200: '#c4cdd9',
          300: '#9aa5b6',
          400: '#6c7689',
          500: '#3f4759',
          600: '#272d3c',
          700: '#171b27',
          800: '#0d1018',
          900: '#070910',
        },
        emerald: {
          400: '#34d399',
          500: '#10b981',
        },
        accent: {
          DEFAULT: '#6366f1',
          glow:    '#818cf8',
        },
      },
      boxShadow: {
        'glow-accent': '0 0 0 1px rgba(99, 102, 241, 0.35), 0 8px 32px -8px rgba(99, 102, 241, 0.45)',
        'glow-emerald': '0 0 0 1px rgba(16, 185, 129, 0.25), 0 6px 24px -8px rgba(16, 185, 129, 0.35)',
      },
      animation: {
        'pulse-soft': 'pulse-soft 2.4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'pulse-soft': {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
