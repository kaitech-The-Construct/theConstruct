import daisyui from 'daisyui';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {},
  },
  plugins: [
    daisyui,
    forms,
  ],
  daisyui: {
    themes: [
      {
        construct: {
          primary: '#3b82f6',
          'primary-focus': '#2563eb',
          'primary-content': '#ffffff',
          secondary: '#64748b',
          'secondary-focus': '#475569',
          'secondary-content': '#ffffff',
          accent: '#10b981',
          'accent-focus': '#059669',
          'accent-content': '#ffffff',
          neutral: '#1e293b',
          'neutral-focus': '#0f172a',
          'neutral-content': '#ffffff',
          'base-100': '#ffffff',
          'base-200': '#f8fafc',
          'base-300': '#e2e8f0',
          'base-content': '#1e293b',
          info: '#06b6d4',
          'info-content': '#ffffff',
          success: '#10b981',
          'success-content': '#ffffff',
          warning: '#f59e0b',
          'warning-content': '#ffffff',
          error: '#ef4444',
          'error-focus': '#dc2626',
          'error-content': '#ffffff',
        },
      },
      'dark',
      'light',
    ],
    darkTheme: 'dark',
    base: true,
    styled: true,
    utils: true,
    rtl: false,
    prefix: '',
    logs: true,
  },
};
