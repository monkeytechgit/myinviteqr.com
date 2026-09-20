# MyInviteQR marketing website

Static HTML/CSS/JS site (no framework). Deploy the folder as is to Cloudflare Pages, Netlify or any static host.

## Build
- `python3 build.py` regenerates every page, `sitemap.xml`, `robots.txt`, `llms.txt`, `feed.xml`, `site.webmanifest`, `_headers`, `_redirects` and `IMAGES.md`.
- Copy + SEO metadata: `content.py` (base) and `content_extra.py` ("Free" titles, long-form copy, extra landing pages, more blog posts).
- Layout, JSON-LD and page structure: `build.py`. Set `SITE`, `APP` (Flutter app URL used by every "Create invitation" button) and `EMAIL` at the top.

## Images
- `python3 tools/make_images.py` regenerates the feature scenes, OG images (`assets/img/og/`), blog covers and converts template thumbnails.
  It needs the rendered template screenshots in `assets/img/templates/*.png` and `assets/img/phones/*.png`
  (produced with `tool/site_render.dart` in the Flutter repo) plus the real screenshots `templates.png`, `edit-inv.png`, `create-inv.png`, `dashboard.png`.
- Replace any generated file with your own artwork at the same path and size and it will be used as is.

## After going live
Verify the domain in Google Search Console and Bing Webmaster Tools, submit `https://myinviteqr.com/sitemap.xml`, and redirect `www` to the apex domain in Cloudflare.
