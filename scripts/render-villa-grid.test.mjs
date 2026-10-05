import test from 'node:test';
import assert from 'node:assert/strict';
import { renderVillaGrid } from './render-villa-grid.mjs';

test('prices remain literal; nested divs and neighbouring legal content stay intact', () => {
  const prefix = '<main><section><div class="upgrade-villa-grid" data-villa-grid>';
  const suffix = '</div></section><section id="buyer-confidence">Taxes payable separately.</section></main>';
  const original = prefix + '<article><div><div>Old card</div></div></article>' + suffix;
  const cards = '<article><div>$990,000</div></article><article><div>$1,500,000</div></article><article><div>$2,100,000</div></article>';
  const actual = renderVillaGrid(original, cards);
  assert.equal(actual, prefix + cards + suffix);
  assert.equal(renderVillaGrid(actual, cards), actual);
  assert.equal((actual.match(/data-villa-grid/g) || []).length, 1);
});

test('missing or unclosed grids fail the build instead of corrupting the page', () => {
  assert.throws(() => renderVillaGrid('<main></main>', ''), /missing/);
  assert.throws(() => renderVillaGrid('<div data-villa-grid><div></div>', ''), /closing/);
});
