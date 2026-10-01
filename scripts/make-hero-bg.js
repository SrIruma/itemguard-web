#!/usr/bin/env node
/**
 * Genera el fondo pixel-art del hero, en dos variantes: noche y dia.
 *
 * Es arte original hecho pixel a pixel, no un asset de Minecraft: la
 * textura y los sprites de Mojang son propiedad suya y no pueden
 * usarse en la web de un plugin de pago. Lo que sale aqui son dos
 * escenas, con la misma cuadricula de bloques y la misma silueta,
 * dibujadas desde cero.
 *
 * El modo claro necesita la suya: con la de noche encima, un velo
 * claro la deja casi blanca y el fondo se pierde. Dia es un cielo
 * alto, con sol, nubes y terreno mas claro.
 *
 *   node scripts/make-hero-bg.js
 */
const sharp = require("/tmp/opencode/domtest/node_modules/sharp");
const fs = require("fs");
const path = require("path");

const W = 1280;
const H = 640;
const BLOCK = 16;

const ROOT = "/mnt/d/Workspace/itemguard-web";
const OUT_DIR = path.join(ROOT, "assets/img");

/* --- Las dos paletas ------------------------------------------
   Noche: azul profundo, luna, estrellas. Es la que se vio y gusto.
   Dia:   cielo alto y frio, sol, nubes. El terreno sube de valor
          para que el texto oscuro encima siga teniendo contraste.
   ------------------------------------------------------------- */
const NIGHT = {
  skyTop: [8, 12, 24],
  skyMid: [14, 22, 46],
  skyLow: [22, 40, 78],
  skyGlow: [40, 74, 132],
  star: [180, 205, 245],
  body: [226, 236, 252],   // luna
  bodyShade: [196, 212, 240],
  sunGlow: [40, 74, 132],
  cloud: [40, 62, 104],
  cloudLight: [58, 84, 132],
  farA: [28, 44, 74],
  farB: [34, 54, 90],
  midA: [22, 34, 58],
  midB: [28, 44, 74],
  nearA: [14, 21, 36],
  nearB: [19, 29, 48],
  edge: [58, 96, 156],
  glow: [86, 140, 220],
  stars: true,
  clouds: false,
};

const DAY = {
  // Cielo alto y frio, casi de media mañana. El sol va alto y a la
  // derecha, donde estaba la luna, para que la composicion sea la
  // misma y solo cambie la luz.
  skyTop: [96, 142, 208],
  skyMid: [150, 188, 232],
  skyLow: [208, 226, 244],
  skyGlow: [255, 246, 222],  // calor alrededor del sol
  star: [255, 255, 255],
  body: [255, 252, 236],     // sol
  bodyShade: [252, 238, 194],
  sunGlow: [255, 238, 196],
  cloud: [255, 255, 255],
  cloudLight: [255, 255, 255],
  // Terreno en la familia de la marca: azules desaturados, no verdes.
  // Un verde aqui es Minecraft deManual, y rompe la paleta del sitio.
  farA: [156, 176, 205],
  farB: [172, 191, 216],
  midA: [126, 149, 183],
  midB: [142, 165, 196],
  nearA: [92, 114, 148],
  nearB: [108, 130, 162],
  edge: [200, 214, 234],
  glow: [186, 204, 228],
  stars: false,
  clouds: true,
};

function mix(a, b, t) {
  return [
    Math.round(a[0] + (b[0] - a[0]) * t),
    Math.round(a[1] + (b[1] - a[1]) * t),
    Math.round(a[2] + (b[2] - a[2]) * t),
  ];
}

/** Dibuja una escena completa en un buffer. */
function draw(P) {
  const buf = Buffer.alloc(W * H * 3);
  const set = (x, y, [r, g, b]) => {
    if (x < 0 || y < 0 || x >= W || y >= H) return;
    const i = (y * W + x) * 3;
    buf[i] = r; buf[i + 1] = g; buf[i + 2] = b;
  };

  // La misma semilla en las dos: la silueta del terreno es identica
  // y lo que cambia es la luz. Asi el cambio de tema no salta.
  let seed = 20260930;
  const rnd = () => {
    seed = (seed * 1664525 + 1013904223) % 4294967296;
    return seed / 4294967296;
  };

  // --- Cielo ---
  const CX = Math.round(W * 0.74);
  const CY = Math.round(H * 0.26);
  const R = 46;

  for (let y = 0; y < H; y++) {
    const t = y / H;
    const base =
      t < 0.55 ? mix(P.skyTop, P.skyMid, t / 0.55)
               : mix(P.skyMid, P.skyLow, (t - 0.55) / 0.45);
    for (let x = 0; x < W; x++) {
      const d = Math.hypot((x - CX) * 0.6, y - CY);
      let c = base;
      if (d < R * 11) {
        c = mix(base, P.sunGlow, Math.pow(1 - d / (R * 11), 4.0) * 0.5);
      }
      set(x, y, c);
    }
  }

  // --- Estrellas (solo de noche) ---
  if (P.stars) {
    for (let gy = 0; gy < Math.floor(H * 0.62 / BLOCK); gy++) {
      for (let gx = 0; gx < Math.floor(W / BLOCK); gx++) {
        if (rnd() > 0.10) continue;
        const x = gx * BLOCK + 3 + Math.floor(rnd() * 9);
        const y = gy * BLOCK + 3 + Math.floor(rnd() * 9);
        if (y > H * 0.5) continue;
        const c = mix(P.skyTop, P.star, 0.45 + rnd() * 0.55);
        set(x, y, c);
        if (rnd() > 0.82) {
          set(x + 1, y, c); set(x, y + 1, c); set(x + 1, y + 1, c);
        }
      }
    }
  }

  // --- Luna o sol ---
  for (let y = CY - R - 1; y <= CY + R + 1; y++) {
    for (let x = CX - R - 1; x <= CX + R + 1; x++) {
      const d = Math.hypot(x - CX, y - CY);
      if (d > R + 1) continue;
      if (d > R - 1) { set(x, y, mix(P.skyGlow, P.body, 0.35)); continue; }
      // Un par de crateros solo de noche; de dia el sol es liso.
      if (P.stars) {
        const c1 = Math.hypot(x - (CX - 14), y - (CY - 8)) < 9;
        const c2 = Math.hypot(x - (CX + 12), y - (CY + 10)) < 7;
        set(x, y, c1 || c2 ? P.bodyShade : P.body);
      } else {
        set(x, y, P.body);
      }
    }
  }

  // --- Nubes (solo de dia), en bloques y con cara iluminada ---
  if (P.clouds) {
    const puff = (x0, y0, w, h) => {
      for (let dy = 0; dy < h; dy++) {
        for (let dx = 0; dx < w; dx++) {
          // La cara de arriba recibe el sol; la de abajo, sombra.
          const c = dy < 2 ? P.cloudLight : mix(P.cloud, P.skyMid, 0.30);
          set(x0 + dx, y0 + dy, c);
        }
      }
    };
    // Posiciones fijas en la rejilla, para que los bordes caigan
    // enteros y se lean como bloques.
    const spots = [
      [0.08, 0.13, 5, 2], [0.14, 0.17, 3, 2], [0.08, 0.21, 6, 2],
      [0.46, 0.10, 6, 2], [0.53, 0.14, 4, 2], [0.46, 0.18, 7, 2],
      [0.86, 0.28, 4, 2], [0.28, 0.33, 4, 2],
    ];
    for (const [fx, fy, w, h] of spots) {
      puff(
        Math.round(W * fx) - (w * BLOCK) / 2,
        Math.round(H * fy),
        w * BLOCK,
        h * BLOCK
      );
    }
  }

  // --- Terreno: la misma silueta en los dos temas ---
  function ridge(baseY, amp, step, a, b, edgeChance) {
    const tops = [];
    let prevTop = baseY;
    for (let x = 0; x < W; x += BLOCK) {
      if (x % step === 0) {
        prevTop = baseY - Math.floor(rnd() * (amp / BLOCK)) * BLOCK;
      }
      tops.push(Math.max(0, Math.min(H - 1, prevTop)));
    }
    for (let bx = 0; bx < tops.length; bx++) {
      const x0 = bx * BLOCK;
      const top = tops[bx];
      for (let dx = 0; dx < BLOCK; dx++) {
        const x = x0 + dx;
        if (x >= W) break;
        for (let y = top; y < H; y++) {
          const t = (y - top) / Math.max(1, H - top);
          set(x, y, mix(a, b, Math.min(1, t * 1.3)));
        }
      }
      if (rnd() < edgeChance) {
        const ey = Math.max(0, top - 1);
        const c = mix(a, P.edge, 0.5);
        for (let dx = 0; dx < BLOCK; dx++) {
          const x = x0 + dx;
          if (x < W) set(x, ey, c);
        }
      }
    }
  }

  ridge(Math.round(H * 0.60), 200, 72, P.farA, P.farB, 0.8);
  ridge(Math.round(H * 0.74), 130, 48, P.midA, P.midB, 0.65);

  const groundTop = Math.round(H * 0.88);
  for (let bx = 0; bx * BLOCK < W; bx++) {
    const x0 = bx * BLOCK;
    const top = groundTop + (rnd() > 0.8 ? -BLOCK : 0);
    for (let dx = 0; dx < BLOCK; dx++) {
      const x = x0 + dx;
      if (x >= W) break;
      for (let y = top; y < H; y++) {
        const t = (y - top) / Math.max(1, H - top);
        set(x, y, mix(P.nearA, P.nearB, t * 0.9));
      }
    }
    const c = mix(P.nearA, P.glow, 0.3);
    for (let dx = 0; dx < BLOCK; dx++) {
      const x = x0 + dx;
      if (x < W) set(x, Math.max(0, top - 1), c);
    }
  }

  // --- Bloques sueltos flotando ---
  function floatBlock(x0, y0, s) {
    for (let dy = 0; dy < s; dy++) {
      for (let dx = 0; dx < s; dx++) {
        set(x0 + dx, y0 + dy, mix(P.midB, P.glow, 0.18));
      }
    }
    for (let dx = 0; dx < s; dx++) set(x0 + dx, y0 - 1, mix(P.midB, P.glow, 0.5));
  }
  floatBlock(Math.round(W * 0.20), Math.round(H * 0.50), 10);
  floatBlock(Math.round(W * 0.30), Math.round(H * 0.58), 6);
  floatBlock(Math.round(W * 0.60), Math.round(H * 0.42), 7);

  return buf;
}

async function write(name, buf) {
  const img = sharp(buf, { raw: { width: W, height: H, channels: 3 } });
  // Solo webp: lo soportan todos los navegadores desde 2020 (Safari 14,
  // Chrome 32, Firefox 65, Edge 79) y ocupa la mitad que un png. Un
  // png de respaldo serian 24 KB que nadie descarga.
  await img.clone().webp({ quality: 72, effort: 6 })
    .toFile(path.join(OUT_DIR, `${name}.webp`));
  await img.clone().resize(720).webp({ quality: 68, effort: 6 })
    .toFile(path.join(OUT_DIR, `${name}-sm.webp`));

  for (const f of [`${name}.webp`, `${name}-sm.webp`]) {
    console.log(`  ${f.padEnd(24)} ${(fs.statSync(path.join(OUT_DIR, f)).size / 1024).toFixed(1)} KB`);
  }
}

(async () => {
  // Dos semillas distintas por escena: comparten la silueta porque
  // el consumo se hace en el mismo orden, no por el mismo numero.
  await write("hero-bg", draw(NIGHT));
  await write("hero-bg-light", draw(DAY));
})();
