import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	compilerOptions: {
		warningFilter: (warning) => {
			if (warning.code === 'css_unknown_at_rule' && warning.message.includes('@reference'))
				return false;
			return true;
		}
	},
	kit: {
		adapter: adapter(),
		alias: {
			$lib: './src/lib',
			$components: './src/lib/components',
			$stores: './src/lib/stores',
			$services: './src/lib/services',
			$types: './src/lib/types',
			$utils: './src/lib/utils'
		}
	}
};

export default config;
