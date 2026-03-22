import daisyui from 'daisyui';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: {
					DEFAULT: '#00FFE1',
					focus: '#00D4B8',
					content: '#0F0F0F'
				},
				secondary: {
					DEFAULT: '#00D4FF',
					focus: '#00A8CC',
					content: '#0F0F0F'
				},
				accent: {
					DEFAULT: '#39FF14',
					focus: '#2ECC11',
					content: '#0F0F0F'
				},
				neutral: {
					DEFAULT: '#2C2C2C',
					focus: '#1A1A1A',
					content: '#E0E0E0'
				},
				base: {
					100: '#0F0F0F',
					200: '#1A1A1A',
					300: '#2C2C2C',
					content: '#E0E0E0'
				},
				info: {
					DEFAULT: '#00D4FF',
					content: '#0F0F0F'
				},
				success: {
					DEFAULT: '#39FF14',
					content: '#0F0F0F'
				},
				warning: {
					DEFAULT: '#FFD700',
					content: '#0F0F0F'
				},
				error: {
					DEFAULT: '#FF073A',
					focus: '#CC0529',
					content: '#FFFFFF'
				}
			},
			animation: {
				'fade-in': 'fadeIn 0.5s ease-in-out',
				'slide-up': 'slideUp 0.3s ease-out',
				glow: 'glow 2s ease-in-out infinite',
				'pulse-border': 'pulse-border 2s ease-in-out infinite',
				'hexagon-rotate': 'hexagon-rotate 20s linear infinite'
			},
			keyframes: {
				fadeIn: {
					from: { opacity: '0' },
					to: { opacity: '1' }
				},
				slideUp: {
					from: {
						transform: 'translateY(10px)',
						opacity: '0'
					},
					to: {
						transform: 'translateY(0)',
						opacity: '1'
					}
				},
				glow: {
					'0%, 100%': {
						boxShadow:
							'0 0 5px var(--robotic-glow), 0 0 10px var(--robotic-glow), 0 0 15px var(--robotic-glow)'
					},
					'50%': {
						boxShadow:
							'0 0 10px var(--robotic-glow), 0 0 20px var(--robotic-glow), 0 0 30px var(--robotic-glow)'
					}
				},
				'pulse-border': {
					'0%, 100%': {
						borderColor: 'var(--robotic-border)'
					},
					'50%': {
						borderColor: 'var(--robotic-glow)'
					}
				},
				'hexagon-rotate': {
					from: { transform: 'rotate(0deg)' },
					to: { transform: 'rotate(360deg)' }
				}
			}
		}
	},
	plugins: [daisyui, forms],
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
					'error-content': '#ffffff'
				}
			},
			'dark',
			'light'
		],
		darkTheme: 'dark',
		base: true,
		styled: true,
		utils: true,
		rtl: false,
		prefix: '',
		logs: true
	}
};
