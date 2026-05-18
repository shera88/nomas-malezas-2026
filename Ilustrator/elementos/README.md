# Elementos extraídos — Logo No Más Malezas 2026

Estos PNGs están listos para usar en tu página web. Todos tienen fondo transparente (canal alfa).

## Estructura

**`fondos/`** — Fondos reutilizables
- `fondo-limpio.png` — Fondo topográfico con elementos centrales borrados (inpaint con OpenCV). Listo para usar como background de secciones.
- `fondo-tarjeta-completo.png` — Tarjeta N completa con todo (referencia)
- `fondo-principal-tarjeta.png` — Tarjeta "NO MAS MALEZAS" completa (referencia)
- `fondo-tile-200x200.png` — Muestra 200×200 px para usar con `background-repeat` en CSS

**`logos/`** — Logos y texto
- `logo-NO-MAS-MALEZAS.png` — Logo principal con la brújula y la N central + "7mo Congreso Internacional / Orientando el rumbo del Agro"
- `logo-letra-N.png`, `logo-letra-O.png`, `logo-letra-S.png`, `logo-letra-E.png` — Cada letra cardinal con su anillo elíptico decorativo
- `logo-mainter.png` — Texto MAINTER + ícono de cruz

**`banderas/`** — Pines con banderas
- `bandera-argentina.png` (S), `bandera-bolivia.png` (N), `bandera-brasil.png` (E), `bandera-paraguay.png` (O)

**`brujula/`** — Brújula y mapa
- `brujula-completa.png` — Rosa de los vientos + mapa de país juntos (original)
- `brujula-rosa-vientos.png` — Solo la rosa de los vientos con N/O/S/E
- `mapa-pais.png` — Solo el contorno del mapa

**`decorativos/`** — Elementos extra
- `elementos-decorativos.png` — Original con elipses + marco
- `elipse-halftone-decorativa.png` — Solo las elipses con dots
- `boton-decorativo.png` — Marco rectangular tipo botón

## Notas técnicas

- Todos los PNG tienen fondo transparente (canal alfa)
- Resolución original ~792×612 (alta calidad para web responsive)
- Los logos centrales pueden tener algunos puntos "+" decorativos del fondo en los bordes. Si necesitas eliminarlos, avísame y los recorto.
- Para fondo de página web: usa `fondo-limpio.png` (versión inpaint) o `fondo-tile-200x200.png` con `background-repeat: repeat` en CSS.

## Cómo usar en CSS

```css
/* Fondo de la página */
body {
  background: url('fondos/fondo-limpio.png') #1B0E48;
  background-size: cover;
}

/* O patrón repetido */
.bg-pattern {
  background: url('fondos/fondo-tile-200x200.png') repeat;
}

/* Hero con logo */
.hero-logo {
  background: url('logos/logo-NO-MAS-MALEZAS.png') no-repeat center;
}
```
