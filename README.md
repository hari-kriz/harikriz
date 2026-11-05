# harikriz.netlify.app

Personal portfolio of Harikrishnan N. Static, no build step.

## Files

- `index.html`, `css/style.css`, `script.js`: the site. One page, one stylesheet, one small script (menu, section highlight, local time).
- `404.html`, `_headers`: Netlify not-found page and security/cache headers.
- `resume_data.json` -> `generate_resume.py` -> `Harikrishnan_2026.docx` and `.pdf`. Edit the JSON, run `python generate_resume.py`. PDF uses Word if installed, otherwise headless Chrome.
- `robots.txt`, `sitemap.xml`, `google*.html`: search console.
- `preview.py` serves the folder on http://localhost:8000; `push.py` commits and pushes.

## Design

Redesigned with the [unslop](https://github.com/heydamir/unslop) process by Damir Sokolovsky (CC BY 4.0): ink neutral ramp, one amber accent reserved for the live dot and the chart, Inter 400/500 with IBM Plex Mono for figures, no gradients, glows, emoji or looping motion. The hero visual is an illustrative audit panel built in HTML and SVG, not an image.

## Deploy

Push to `main`. Netlify publishes the repository root with no build command.
