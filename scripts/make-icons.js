#!/usr/bin/env node
/**
 * Recorta los iconos de la marca desde logo.png.
 *
 * logo.png es el fuente. De aqui salen el favicon de 32 px y el
 * apple-touch-icon de 180 px, mas el favicon.svg, que se dibuja
 * vectorialmente para que se vea nitido a cualquier tamaño.
 *
 * Requiere sharp. Se ejecuta solo cuando cambias el logo:
 *
 *   npm install --no-save sharp
 *   node scripts/make-icons.js
 */
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const DIR = path.join(__dirname, "..", "assets", "img");
const SRC = path.join(DIR, "logo.png");

/** El logo como SVG: el escudo pixelado necesita ser vectorial para
    que la pestaña se vea limpia en pantallas HiDPI, donde un PNG de
    32 px se ve borroso. Las formas son las del logo. */
const LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="s" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7fd4ff"/>
      <stop offset=".5" stop-color="#3d7dff"/>
      <stop offset="1" stop-color="#1a3fd6"/>
    </linearGradient>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d6f4ff"/>
      <stop offset="1" stop-color="#2f6fd0"/>
    </linearGradient>
  </defs>
  <path d="M32 3 58 11v20c0 15-11 26-26 30C17 57 6 46 6 31V11L32 3z" fill="url(#s)"/>
  <path d="M32 7 54 14v17c0 13-9.5 22.5-22 26.2C19.5 53.5 10 44 10 31V14L32 7z" fill="url(#g)" opacity=".45"/>
  <path d="M32 11 50 17v14c0 11-7.8 19.5-18 23-10.2-3.5-18-12-18-23V17l18-6z" fill="#0f2a6b"/>
  <g fill="#a8ecff">
    <path d="M20 44 24 40l4 4-4 4-4-4zM26 38l4-4 4 4-4 4-4-4zM32 32l4-4 4 4-4 4-4-4zM38 26l4-4 4 4-4 4-4-4z"/>
  </g>
  <g fill="#3aa8e8">
    <path d="M24 48l4-4 4 4-4 4-4-4zM30 42l4-4 4 4-4 4-4-4zM36 36l4-4 4 4-4 4-4-4z"/>
  </g>
  <g fill="#c98a4b">
    <path d="M40 50l4-4 4 4-4 4-4-4zM46 44l4-4 4 4-4 4-4-4z"/>
  </g>
</svg>
`;

(async () => {
  if (!fs.existsSync(SRC)) {
    console.error("falta assets/img/logo.png");
    process.exit(1);
  }
  const cut = (size, file) =>
    sharp(SRC)
      .resize(size, size, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png({ quality: 88, compressionLevel: 9, palette: true, effort: 10 })
      .toFile(path.join(DIR, file));

  await cut(32, "favicon-32.png");
  await cut(180, "apple-touch-icon.png");
  fs.writeFileSync(path.join(DIR, "favicon.svg"), LOGO_SVG);

  for (const f of ["favicon-32.png", "apple-touch-icon.png", "favicon.svg"]) {
    const kb = (fs.statSync(path.join(DIR, f)).size / 1024).toFixed(1);
    console.log(`  ${f.padEnd(24)} ${kb} KB`);
  }
})();
