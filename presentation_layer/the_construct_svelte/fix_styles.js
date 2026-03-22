import fs from 'fs';
import path from 'path';

function walk(dir) {
	let results = [];
	const list = fs.readdirSync(dir);
	list.forEach((file) => {
		file = path.join(dir, file);
		const stat = fs.statSync(file);
		if (stat && stat.isDirectory()) {
			results = results.concat(walk(file));
		} else if (file.endsWith('.svelte')) {
			results.push(file);
		}
	});
	return results;
}

const svelteFiles = walk('./src');
const appCssPath = path.resolve('./src/app.css');

svelteFiles.forEach((file) => {
	let content = fs.readFileSync(file, 'utf-8');
	if (content.includes('<style>') && content.includes('@apply')) {
		const relativePath = path.relative(path.dirname(file), appCssPath).replace(/\\/g, '/');
		const reference = `@reference "${relativePath.startsWith('.') ? relativePath : './' + relativePath}";`;

		if (!content.includes('@reference')) {
			content = content.replace('<style>', `<style>\n  ${reference}`);
			fs.writeFileSync(file, content, 'utf-8');
			console.log(`Updated ${file} with ${reference}`);
		}
	}
});
