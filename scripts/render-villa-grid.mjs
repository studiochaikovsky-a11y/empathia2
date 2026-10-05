// Replace only the grid's contents. Never use generated HTML as a String.replace
// replacement string: prices such as $1,500,000 would be interpreted as $1.
export function renderVillaGrid(html, cards) {
  const opening = /<div\b(?=[^>]*\bdata-villa-grid\b)[^>]*>/i.exec(html);
  if (!opening) throw new Error('Villa grid is missing');
  const start = opening.index + opening[0].length;
  const tags = /<!--[\s\S]*?-->|<\/?div\b[^>]*>/gi;
  tags.lastIndex = start;
  let depth = 1;
  for (let tag; (tag = tags.exec(html));) {
    if (tag[0].startsWith('<!--')) continue;
    depth += /^<\/div/i.test(tag[0]) ? -1 : 1;
    if (depth === 0) {
      return html.slice(0, start) + cards + html.slice(tag.index);
    }
  }
  throw new Error('Villa grid has no closing tag');
}
