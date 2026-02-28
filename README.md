# Personal Brand Website

Static personal brand website for Harikrishnan N.

## Structure

- `index.html`
- `style.min.css` (production CSS)
- `script.min.js` (production JS)
- `images/` (profile and tech icons)
- `Harikrishnan_N_Resume.pdf`
- `favicon.ico`

## Local Preview

Open `index.html` directly in a browser, or serve with any static server.

## Netlify Deployment

1. Push this folder to a Git repository.
2. In Netlify, create a new site from that repository.
3. Keep build settings empty:
   - Build command: _(none)_
   - Publish directory: `/` (root)
4. Deploy.

## Contact Form

The contact form uses Netlify Forms:

- `<form name="contact" method="POST" data-netlify="true">`
- Includes `form-name` hidden input.
- JavaScript validates fields before submission and posts to `/`.
