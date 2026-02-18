# my personal website

├── content/
│   └── now.md              ← edit this to update your /now page
├── public/
│   ├── .nojekyll           ← tells GitHub Pages to skip Jekyll
│   ├── operius/            ← existing static content (preserved)
│   ├── spotify-project/
│   ├── photos/
│   ├── projects/
│   ├── spiral.html         ← archived old pages
│   └── v1.html
├── src/
│   ├── app/
│   │   ├── layout.tsx      ← root layout (wraps all pages)
│   │   ├── globals.css     ← shared styles (same theme/colors)
│   │   ├── page.tsx        ← home page (/ route)
│   │   ├── now/page.tsx    ← reads content/now.md at build time
│   │   ├── library/page.tsx
│   │   └── blog/page.tsx
│   └── components/
│       └── Spiral.tsx      ← client component ('use client')
├── next.config.mjs         ← output: 'export' for static HTML
├── package.json
└── tsconfig.json