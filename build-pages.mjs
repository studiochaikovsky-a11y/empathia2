import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { dirname, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = dirname(fileURLToPath(import.meta.url));
const outputRoot = resolve(projectRoot, 'dist');
if (outputRoot === projectRoot || !outputRoot.startsWith(projectRoot + sep)) {
  throw new Error('Refusing to clear a directory outside this project');
}

const publicExtensions = new Set([
  '.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp',
  '.gif', '.ico', '.woff', '.woff2', '.ttf', '.mp4', '.webm', '.xml', '.txt',
]);
const publicDirectories = ['ar', 'assets', 'crm', 'fr', 'optimized'];
const specialFiles = ['_headers', '_redirects', 'data/project-facts.json'];
let copied = 0;

function copyPublicFile(relativePath) {
  const source = join(projectRoot, relativePath);
  if (!existsSync(source)) throw new Error(`Missing required public file: ${relativePath}`);
  const destination = join(outputRoot, relativePath);
  mkdirSync(dirname(destination), { recursive: true });
  copyFileSync(source, destination);
  copied += 1;
}

function copyPublicDirectory(relativeDirectory) {
  const source = join(projectRoot, relativeDirectory);
  if (!existsSync(source)) return;
  for (const entry of readdirSync(source, { withFileTypes: true })) {
    const relativePath = join(relativeDirectory, entry.name);
    if (entry.isDirectory()) copyPublicDirectory(relativePath);
    else if (entry.isFile() && publicExtensions.has(extname(entry.name).toLowerCase())) {
      copyPublicFile(relativePath);
    }
  }
}

rmSync(outputRoot, { recursive: true, force: true });
mkdirSync(outputRoot);

for (const entry of readdirSync(projectRoot, { withFileTypes: true })) {
  if (entry.isFile() && publicExtensions.has(extname(entry.name).toLowerCase())) {
    copyPublicFile(entry.name);
  }
}
for (const directory of publicDirectories) copyPublicDirectory(directory);
for (const file of specialFiles) copyPublicFile(file);

for (const required of [
  'index.html', 'faq.html', 'project-facts.html', 'robots.txt', 'sitemap.xml',
  '_headers', '_redirects', 'data/project-facts.json',
  'assets/images/brand/logo-emblem.webp',
]) {
  if (!existsSync(join(outputRoot, required))) {
    throw new Error(`Public build is incomplete: ${required}`);
  }
}

console.log(`Built ${copied} public files in dist/; development files stay in Git.`);
