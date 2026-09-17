/**
 * Post-build: rewrite relative asset references in dist/index.html to absolute
 * paths.
 *
 * Cloudflare Workers serves a SPA fallback for unmatched paths, so landing on a
 * deep link such as `/practice/` would resolve `./index-<hash>.js` to
 * `/practice/index-<hash>.js` and get back index.html (HTML) instead of the
 * JavaScript bundle. Absolute paths are route-independent.
 */
const indexPath = new URL("../dist/index.html", import.meta.url).pathname;
const html = await Bun.file(indexPath).text();

const rewritten = html.replace(/(\s(?:src|href)=")\.\//g, "$1/");

if (rewritten !== html) {
  await Bun.write(indexPath, rewritten);
  console.log("postbuild: rewrote relative asset paths in dist/index.html");
} else {
  console.log("postbuild: no relative asset paths found");
}
