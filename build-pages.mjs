import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runInNewContext } from 'node:vm';

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

// Fail the build if a page loses the shared layout. Render villa cards from the
// current project data before delivery, avoiding late content/layout shifts.
const contentPages = readdirSync(projectRoot).filter(file => file.endsWith('.html'))
  .concat(['fr/index.html', 'ar/index.html']);
for (const file of contentPages) {
  const destination = join(outputRoot, file);
  let html = readFileSync(destination, 'utf8');
  if ((html.match(/id="site-header"/g) || []).length !== 1 ||
      !html.includes('site-header-20261005.css') || !html.includes('site-mobile-20261005.css') ||
      html.includes('<nav class="nav"') || html.includes('static.cloudflareinsights.com/beacon')) {
    throw new Error(`Shared layout or analytics regression: ${file}`);
  }
  if (html.includes('data-lead-form') && !['lead-name', 'lead-email', 'lead-phone', 'lead-villa'].every(id => html.includes(`id="${id}"`))) {
    throw new Error(`Incomplete enquiry form: ${file}`);
  }
  if (html.includes('data-villa-grid')) {
    const lang = file.startsWith('fr/') ? 'fr' : file.startsWith('ar/') ? 'ar' : 'en';
    const context = { window: {}, location: { pathname: '/' + file }, document: { readyState: 'loading', addEventListener() {} } };
    runInNewContext(readFileSync(join(projectRoot, 'assets/js/project-data.js'), 'utf8'), context);
    html = html.replace(/(<div class="upgrade-villa-grid" data-villa-grid>)[\s\S]*?(<\/div><\/div><\/section>)/,
      '$1' + context.window.EmpathiaRenderVillaCards(lang) + '$2');
    writeFileSync(destination, html);
  }
}

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
