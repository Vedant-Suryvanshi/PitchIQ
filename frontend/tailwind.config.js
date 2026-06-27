/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        pitch: {
          black:          '#07070D',
          surface:        '#0F0F1A',
          card:           '#14141F',
          border:         '#1E1E2E',
          muted:          '#2A2A3D',
          purple:         '#7C3AED',
          'purple-light': '#A78BFA',
          lavender:       '#C4B5FD',
          emerald:        '#10B981',
          'emerald-dim':  '#059669',
          cream:          '#F1EDE4',
          'cream-dim':    '#9C9589',
          gold:           '#F59E0B',
          red:            '#EF4444',
          blue:           '#3B82F6',
        },
      },
      fontFamily: {
        display: ['Georgia', 'Times New Roman', 'serif'],
        body:    ['Inter', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4,0,0.6,1) infinite',
        'fade-in':    'fadeIn 0.5s ease-out forwards',
        'slide-up':   'slideUp 0.6s ease-out forwards',
        'glow':       'glow 2s ease-in-out infinite alternate',
        'spin-slow':  'spin 8s linear infinite',
      },
      keyframes: {
        fadeIn:  { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { opacity: '0', transform: 'translateY(24px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        glow:    { from: { boxShadow: '0 0 20px #7C3AED33' }, to: { boxShadow: '0 0 40px #7C3AED88' } },
      },
    },
  },
  plugins: [],
}