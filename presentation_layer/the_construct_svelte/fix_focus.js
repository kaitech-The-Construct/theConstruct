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
		} else if (file.endsWith('.svelte') || file.endsWith('.css')) {
			results.push(file);
		}
	});
	return results;
}

const files = walk('./src');

files.forEach((file) => {
	let content = fs.readFileSync(file, 'utf-8');
	let changed = false;

	if (content.includes('-focus')) {
		content = content.replace(/primary-focus/g, 'primary');
		content = content.replace(/secondary-focus/g, 'secondary');
		content = content.replace(/accent-focus/g, 'accent');
		content = content.replace(/neutral-focus/g, 'neutral');
		content = content.replace(/info-focus/g, 'info');
		content = content.replace(/success-focus/g, 'success');
		content = content.replace(/warning-focus/g, 'warning');
		content = content.replace(/error-focus/g, 'error');
		changed = true;
	}

	if (changed) {
		fs.writeFileSync(file, content, 'utf-8');
		console.log(`Removed -focus from ${file}`);
	}
});
