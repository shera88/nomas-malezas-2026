# PROMPT PARA CLAUDE DESIGN (claude.ai con Artifacts o Sonnet/Opus 4.7)

> **Versión:** 2.0 (aplicado `ui-ux-pro-max` + `canvas-design` + `interface-design` + `impeccable`)
> **Cómo usar**: abrí claude.ai, modelo Sonnet 4.6 o Opus 4.7. Adjuntá los 3 PDFs (`LogoNoMásMAlezas2026-Elementos.pdf`, `PROYETO MAINTER 2026 - BRUJULA.pdf`, `AmbientaciónoNoMalezas2.pdf`) **y este prompt completo**. Pedile un Artifact con HTML+CSS+JS embebidos.

---

## ⚙️ Instrucción base al modelo

Actuá como un **Senior Frontend Designer & Art Director** con 10+ años en interfaces premium para eventos corporativos, expertise en SEO técnico, accesibilidad WCAG 2.2 AA, Core Web Vitals y motion design sutil. Tu output debe verse "meticulously crafted, labored over with care, the product of countless hours by someone at the top of the field". Cada pixel deliberado. Cada espaciado intencional.

Vas a diseñar **una landing page de registro** para el **7mo Congreso Internacional No Más Malezas 2026** — organizado por **MAINTER** (empresa boliviana fundada 1983, Grupo LANDICORP, Santa Cruz, líder distribución agro-insumos).

---

## 🖼️ Assets gráficos YA DISPONIBLES (usá estos, no inventes)

El cliente entregó PNGs transparentes ya recortados. Vienen con la conversación adjunta. **Usalos directamente** en lugar de generar tus propios elementos:

```
Ilustrator/elementos/
├── logos/
│   ├── logo-NO-MAS-MALEZAS.png       ← logo principal del evento (con brújula+aguja+gradiente azul/amarillo)
│   ├── logo-mainter.png              ← logo corporativo MAINTER + cruz amarilla
│   ├── logo-letra-N.png              ← letra "N" con anillo elíptico verde + dots halftone
│   ├── logo-letra-E.png              ← letra "E" con anillo amarillo
│   ├── logo-letra-S.png              ← letra "S" con anillo rojo
│   └── logo-letra-O.png              ← letra "O" con anillo cian/turquesa
├── brujula/
│   ├── brujula-rosa-vientos.png      ← rosa de los vientos completa con aguja N negra/verde
│   ├── brujula-completa.png          ← brújula sobre mapa de país
│   └── mapa-pais.png                 ← solo contorno Bolivia
├── banderas/                          ← pines circulares con bandera
│   ├── bandera-bolivia.png (N)
│   ├── bandera-brasil.png (E)
│   ├── bandera-argentina.png (S)
│   └── bandera-paraguay.png (O)
├── fondos/
│   ├── fondo-limpio.png              ← topografía + cruces "+" sobre azul oscuro #1B0E48
│   └── fondo-tile-200x200.png        ← tile repetible para CSS background
├── decorativos/
│   ├── elipse-halftone-decorativa.png
│   └── boton-decorativo.png
└── mainter-en-N.png / E / S / O      ← variante "MAINTER" sobre cada color cardinal
```

**Color de fondo del evento (extraído del PNG real)**: `#1B0E48` — azul profundo violáceo (NO `#0A1628`). Ajustá el design system para alinearse con el branding entregado.

**Color paleta REAL del evento**:
- **NORTE = Verde lima** (`#A7C44A` aprox) — extraído de `logo-letra-N.png`
- **ESTE = Amarillo** (`#F1C40F` aprox) — extraído de `logo-letra-E.png`
- **SUR = Rojo coral** (`#E74C3C` aprox) — extraído de `logo-letra-S.png`
- **OESTE = Cian turquesa** (`#3DBCB0` aprox) — extraído de `logo-letra-O.png`

⚠️ **Cambio importante**: la paleta del PDF "Brújula" decía Verde-N / Azul-E / Rojo-S / Amarillo-O, pero la gráfica real entregada (PNGs) dice **Verde-N / Amarillo-E / Rojo-S / Cian-O**. **Confirmar con cliente** cuál es la final. Hasta confirmación, **usar la paleta de los PNGs entregados** (es lo que va impreso/ambientación).

---

## 📸 Fotos de oradores disponibles

Hay 3 JPEGs en `oradores/` (de WhatsApp, requieren post-procesado: recorte cuadrado, fondo limpio). El cliente debe identificar quién es quién entre Pedro Christoffoleti (Brasil), Lucas Paterlini (Argentina), Pablo Franco (Bolivia), y el disertante de Paraguay (pendiente). Mientras tanto, usá **placeholders circulares 96px con la letra cardinal** sobre fondo del color del cardinal.

---

## 📋 Pre-Delivery Checklist (debe cumplir el output final)

```
[ ] No emojis como íconos (usar SVG inline: Lucide / Heroicons / Phosphor)
[ ] cursor-pointer en todo elemento clickable
[ ] Hover states con transición suave (150-300ms ease-out)
[ ] Focus visible para nav teclado (no `outline: none` sin reemplazo)
[ ] Contraste texto ≥ 4.5:1 (validar amarillo #F1C40F NO sobre fondos claros)
[ ] prefers-reduced-motion respetado (sin rotación brújula, sin parallax)
[ ] Responsive: 375px, 768px, 1024px, 1440px, 1920px
[ ] Sin animaciones largas que demoren render inicial
[ ] Sin gradientes purple/pink "AI estilo 2023" — esto es una marca seria boliviana
[ ] Sin emojis decorativos en headlines — solo si tienen propósito específico
[ ] H1 único, jerarquía H2→H6 lógica
[ ] Imágenes con width/height declarados (sin CLS)
[ ] Loading="lazy" + decoding="async" en imágenes bajo fold
[ ] font-display: swap en custom fonts
[ ] Form con labels asociados (no placeholders como labels)
[ ] aria-live="polite" en feedback éxito/error
[ ] Botones <button>, no <div onclick>
[ ] lang="es" en <html>
```

---

## 🎨 Design System pre-definido (no inventar, usar exactamente esto)

### Pattern de landing: "Hero-Centric + Concept Anchor + Speakers + Trust Form"

```
1. Hero (brújula animada, fecha, CTA above-fold)
2. Manifiesto (concept anchor — frase grande)
3. 4 Puntos Cardinales (grid 2x2 con colores)
4. Speakers (4 disertantes internacionales)
5. Venue/Experiencia (datos sala + propuesta inmersiva)
6. Formulario (sticky CTA mobile, foco principal)
7. FAQ (acordeón)
8. Footer (logos + contacto)
```

### Style: "Editorial Brutalism Agrario"

- Mezcla de **Editorial Premium** (tipografía dominante, espacios respiradores) con **Brutalismo Sutil** (bordes definidos, geometría clara, sin sombras blandas decorativas).
- Inspiración: Linear.app (refinamiento dark) × Webby Awards Editorial (jerarquía) × Origin Coffee (craft) × campañas Bayer Crop Science (legitimidad agro).
- **No** Soft UI, **no** gradientes etéreos, **no** neumorphism, **no** glassmorphism saturado. Una pizca de glassmorphism solo en navbar/CTA flotante.
- Tono visual: serio, técnico-aspiracional, no infantil, no genérico tech-startup.

### Colors (LOCKED — source of truth: PDF "PROYECTO MAINTER 2026 - BRUJULA")

```css
:root {
  /* Fondos */
  --bg-deep:        #1B0E48;  /* azul violáceo profundo (extraído del fondo entregado) */
  --bg-elevated:    #2A1B65;  /* cards y secciones elevadas */
  --bg-surface:     #3A2680;  /* surfaces interactivas */

  /* Textos */
  --text-primary:   #FFFFFF;
  --text-secondary: #B8B3D6;
  --text-tertiary:  #8A86A6;

  /* Brand MAINTER */
  --gold:           #F5B82E;  /* cruz amarilla del logo */
  --gold-soft:      #FCD566;
  --gold-deep:      #C99421;

  /* 4 Cardinales (PDF brújula, lockeado) */
  --norte-verde:    #27AE60;  /* NORTE · Barbecho · Ultracheval · Pedro Christoffoleti · 🇧🇷 Brasil */
  --este-azul:      #2E86DE;  /* ESTE · Pre-emergente · ZethaMaxx · Lucas Paterlini · 🇦🇷 Argentina */
  --sur-rojo:       #E74C3C;  /* SUR · Post-emergente · Balón · (Paraguay, disertante pendiente) · 🇵🇾 */
  --oeste-amarillo: #F1C40F;  /* OESTE · Resistentes · Apresa · Pablo Franco · 🇧🇴 Bolivia */

  /* Auxiliares */
  --border-subtle:  rgba(255,255,255,0.10);
  --border-glow:    rgba(245,184,46,0.30);
  --success:        #2ECC71;
  --error:          #FF6B6B;
}
```

| Cardinal | Color | Tema | Producto | Disertante | País |
|---|---|---|---|---|---|
| **N** | Verde `#27AE60` | Manejo de Barbecho | Ultracheval | Pedro Christoffoleti | 🇧🇷 Brasil |
| **E** | Azul `#2E86DE` | Pre-emergente | ZethaMaxx | Lucas Paterlini | 🇦🇷 Argentina |
| **S** | Rojo `#E74C3C` | Post-emergente | Balón | (pendiente) | 🇵🇾 Paraguay |
| **O** | Amarillo `#F1C40F` | Malezas Resistentes | Apresa | Pablo Franco | 🇧🇴 Bolivia |

**Reglas de uso color**:
- Cada cardinal SOLO en su sección/card propia + entrada digital del participante de ese tipo
- Amarillo `#F1C40F` NUNCA sobre blanco/claro (fail contraste WCAG)
- Gold MAINTER `#F5B82E` es el único acento de marca — usar con criterio, no spammear
- 90% del UI es paleta dark violácea + blanco. Color cardinal es el "diamante" del momento

### Typography

```css
/* Display — títulos grandes */
font-family: 'Bricolage Grotesque', 'Space Grotesk', -apple-system, system-ui, sans-serif;
font-weight: 700-800; /* heavy en displays */
letter-spacing: -0.02em; /* tight tracking */
line-height: 0.95-1.1;

/* Body — párrafos */
font-family: 'Inter', 'Manrope', -apple-system, sans-serif;
font-weight: 400-500;
letter-spacing: -0.005em;
line-height: 1.55;

/* Mono — datos técnicos (fechas, IDs) */
font-family: 'JetBrains Mono', 'SF Mono', monospace;
font-weight: 500;
```

Cargar via Google Fonts con `&display=swap`, **preload** 2 weights críticos (Display 800, Body 400). Subset Latin Extended (acentos español).

### Spacing system (8-point grid)

```
--space-1:  4px
--space-2:  8px
--space-3:  12px
--space-4:  16px
--space-5:  24px
--space-6:  32px
--space-7:  48px
--space-8:  64px
--space-9:  96px
--space-10: 128px
```

### Border radius

```
--radius-sm: 8px   (chips, badges)
--radius-md: 16px  (cards, inputs)
--radius-lg: 24px  (sections, modals)
--radius-full: 9999px (pills)
```

### Motion

```
--ease-out-fast:  cubic-bezier(0.16, 1, 0.3, 1);  /* 200ms */
--ease-out-soft:  cubic-bezier(0.22, 1, 0.36, 1); /* 400ms */
--ease-in-out:    cubic-bezier(0.65, 0, 0.35, 1); /* 300ms */
```

Duraciones:
- Hover/focus: 150-200ms
- Section transitions: 300-400ms
- Brújula rotación: 20s linear infinite
- Page mount: stagger fade-in 60ms entre items

---

## 🧭 Visual Philosophy (canvas-design layer)

**Movement name:** "Cardinal Precision"

Es un congreso sobre **orientación, dirección, decisión correcta**. La página debe sentirse como una **brújula de bolsillo de cuero envejecido pero con tecnología precisa** — algo entre instrumento náutico clásico y dashboard analítico moderno.

**Principles** (expresar en cada decisión visual):

- **Eje y simetría axial**: la brújula impone un centro. Composiciones que respetan ejes (mitad-mitad, regla de tercios). Asymmetry solo cuando hace sentido conceptual.
- **Densidad selectiva**: zonas de mucha información (datos, formulario) contrastan con zonas de mucho aire (manifiesto, hero). Los pulmones de la página.
- **Líneas que orientan**: usar líneas finas (1px `var(--border-subtle)`) como guías visuales sutiles — meridianos, paralelos, hairlines que sugieren cartografía sin caricaturizar.
- **Tipografía como brújula**: grandes números, fechas, letras N/E/S/O como elementos casi escultóricos. Display gigante donde importa, body pequeño y disciplinado.
- **Color como territorio**: cada cardinal ocupa un "territorio" visual. Cuando el usuario está en zona NORTE, el verde solo aparece ahí. No salpicar.

**Frase ancla del manifiesto**: tiene que sentir como **golpe en la mesa** — no decoración. Tipo enorme, line-height compacto, breakeable solo en puntuación significativa.

---

## 📝 Contenido (literal, copy-paste)

### Hero

- **Eyebrow**: `MAINTER · 7° EDICIÓN`
- **Headline H1**: `Congreso Internacional No Más Malezas`
- **Subtitle**: `La Brújula del Lote`
- **Fecha**: `01 · 06 · 2026 · Santa Cruz, Bolivia`
- **CTA primario**: `Registrarme gratis →`
- **Stat-strip**: `1,200 asistentes · 4 disertantes · 4 países · 4 horas`

### Manifiesto

> **Frase grande**: *"Hoy el productor no está fallando por falta de productos. Está fallando por falta de **dirección clara**."*

> **Apoyo**: Demasiadas opciones. Clima cambiante. Presión de malezas. El resultado: decisiones desordenadas y lotes perdidos. Este año, MAINTER no trae un congreso. Trae una **brújula**.

### Los 4 Puntos Cardinales

Una tarjeta por punto:

| N | E | S | O |
|---|---|---|---|
| **NORTE** | **ESTE** | **SUR** | **OESTE** |
| Manejo de Barbecho | Pre-emergente | Post-emergente | Malezas Resistentes |
| Producto: **Ultracheval** | Producto: **ZethaMaxx** | Producto: **Balón** | Producto: **Apresa** |
| Pedro Christoffoleti · BR | Lucas Paterlini · AR | (por confirmar) · PY | Pablo Franco · BO |
| Color `--norte-verde` | Color `--este-azul` | Color `--sur-rojo` | Color `--oeste-amarillo` |

Cada card: borde 2px del color cardinal con `border-glow` al hover (subtle, no épico).

### Speakers (puede ir fusionado o separado de cardinales)

Bios cortas, máximo 2 líneas por persona. Avatares circulares 96px (placeholder ahora — yo reemplazo después).

### Venue & Experiencia

- Salón principal **38m × 65m** · capacidad **1,200 pax**
- Pantalla central **18m × 4m** LED 4K
- Anillo LED suspendido 15m + techo rosa de los vientos
- Sonido 7.1 inmersivo con voz en off "El Navegante"
- Performances temáticos por cardinal
- Frase cierre: **"4 momentos. 4 direcciones. Un solo rumbo."**

### Formulario de registro

Card centrada `max-width: 560px`. Título: **"Reservá tu lugar"**. Subtítulo: *"Recibirás tu entrada digital con código QR por email"*.

Campos en orden:

1. **Nombre completo** — `<input type="text" required minlength="3">`
2. **Tipo de participante** — `<select required>`:
   - Estudiante · Productor / Agricultor · Empresa · Institución · Prensa · Otro
3. **Campo dinámico (cambia con animación 300ms ease-out al cambiar tipo):**
   - Estudiante → "Nombre de la universidad"
   - Productor → "Zona productiva"
   - Empresa → "Nombre de la empresa"
   - Institución → "Nombre de la institución"
   - Prensa → "Medio de comunicación"
   - Otro → "Especificá" (libre)
4. **WhatsApp** — `<input type="tel" required pattern="...">` con máscara visual `+591 7 1234 5678`
5. **Email** — `<input type="email" required>`
6. Checkbox: **"Acepto recibir información del evento por email/WhatsApp"** (no pre-checked)

Aviso importante destacado:
> ⚠️ **Importante:** verificá que tu email y WhatsApp sean correctos. Ahí te enviaremos tu entrada con QR.

Botón submit grande full-width: `Confirmar registro →`.

**Estado loading**: spinner inline + texto "Procesando…", botón disabled.

**Pantalla éxito** (reemplaza form con transición):
- Checkmark animado (SVG dibujado con stroke-dashoffset)
- `¡Listo, {nombre}!`
- QR grande con borde del color cardinal asignado
- `Tu sector: {COLOR} · {Punto cardinal}` destacado
- `Te enviamos un email a {email}`
- Botones: **"Descargar entrada PDF"** + **"Agregar al calendario"** (.ics)

### FAQ (acordeón, máximo 6)

1. **¿Tiene costo?** → Gratuito, con registro previo obligatorio
2. **¿Qué debo llevar?** → Tu entrada digital. Mostrar el QR desde el celular alcanza
3. **¿Cómo llego?** → Av. La Salle, 3er anillo, Santa Cruz · [Ver en Google Maps]
4. **¿Puedo registrar un acompañante?** → Sí, cada uno debe registrarse individual
5. **¿Habrá transmisión online?** → (por confirmar)
6. **¿Hay estacionamiento?** → Sí, gratuito en el predio

### Footer

- Logos: MAINTER + LANDICORP + sponsors (Rodaria, ZNA, Tramontina, Gran Alimento) — placeholders ahora
- Redes: Facebook `Mainter.Srl`
- Contacto: `mainter@mainter.com.bo` · `+591 3 178000`
- Legal: © 2026 MAINTER S.R.L. · Términos · Privacidad

---

## 🧭 Brújula Hero — especificación detallada

- **SVG inline** preferido (no `<img>` para poder animar partes)
- Diámetro adaptativo: `clamp(280px, 50vw, 520px)`
- 32 marcas (cada 11.25°) + 4 cardinales gigantes N/E/S/O
- Rosa de los vientos clásica pero limpia (no ornamento victoriano)
- Aguja: forma de diamante alargada, mitad blanca mitad roja apuntando norte
- Animación default: rota lento 20s linear infinite
- Hover sobre punto cardinal: ese sector pulsa con su color + tooltip aparece con tema
- Click cardinal: scrollea suave a su tarjeta en la página
- **prefers-reduced-motion**: NO rota; queda estática, mantiene interactividad
- Mobile: touch-friendly, área tap ≥44×44px
- Stroke: 1.5px en bordes, 2.5px aguja
- Glow al hover: `filter: drop-shadow(0 0 20px var(--color-cardinal))`

---

## ⚙️ Especificaciones técnicas no negociables

1. **Un solo archivo HTML** con `<style>` y `<script>` inline. Yo después separo a archivos.
2. **CSS variables** para todo el design system (paleta + spacing + radius + motion).
3. **Mobile-first**. Breakpoints: 480 / 768 / 1024 / 1440px (max-width). Container fluido con `clamp()`.
4. **Sin frameworks**. Vanilla CSS + vanilla JS. Único permitido: SVG icons inline (Lucide-style).
5. **Animaciones CSS** primero; JS solo cuando CSS no alcanza.
6. **JSON-LD `Event` schema completo** en `<head>`.
7. **OG image** placeholder con `1200x630`.
8. **Form submit**: `<form id="reg-form">` con `preventDefault()` y `console.log(data)`. Stub para que yo cablee webhook después.
9. **Campo dinámico**: animar opacity+translateY al cambiar (300ms ease-out).
10. **Critical CSS inline** (no `<link>` externo en MVP). Yo separo después.
11. **Comentarios estructurales**: `<!-- ===== SECTION: HERO ===== -->` para facilitar edits.

---

## 🚫 Anti-patterns a evitar

```
✗ Gradientes purple/pink saturados (estética "AI 2023")
✗ Sombras blandas exageradas (no es app de wellness)
✗ Emojis como íconos de UI
✗ "Trust badges" genéricos con logos falsos
✗ Carousels innecesarios para 4 ítems (usar grid)
✗ Hero con video de stock genérico (sin propósito)
✗ Sticky CTA que tapa contenido sin razón
✗ Modal de cookies tipo GDPR molesto si no aplica
✗ Auto-playing audio o video con sonido
✗ Animaciones agresivas o de larga duración (>800ms)
✗ Texto rotando, fade-in masivo, parallax pesado
✗ Toda la página en una sola tipografía sin jerarquía
✗ Botones flat sin estado hover claro
✗ Forms con placeholders como única label
✗ Iconografía cute/cartoon (no es app infantil)
✗ "Get started for free" o copy genérico SaaS — esto es agro Bolivia
✗ Dark mode toggle (la página ya es dark, sin necesidad de toggle)
```

---

## 📦 Entregable esperado

**Un archivo HTML completo** listo para previsualizar, que cumpla TODO lo de arriba.

Si excede tamaño de un Artifact, dividilo en 2 (`part-1.html` head + hero + manifiesto + cardinales; `part-2.html` speakers + venue + form + faq + footer) y dame instrucciones de ensamblado.

---

## 🤝 Antes de empezar, respondé estas 3 preguntas:

1. **Brújula**: ¿geométrica minimal (estilo Linear/Stripe) o más ornamental clásica (rosa de vientos detallada, líneas finas náuticas)?

   Recomendación mía: **híbrida** — base geométrica minimal con detalles de cartografía sutiles (meridianos hairline, marcas grados).

2. **Tono de copy**: ¿técnico-profesional (Bayer, John Deere) o más motivacional-épico (al estilo del manifiesto "no trae congreso, trae brújula")?

   Recomendación mía: **70% épico-aspiracional, 30% técnico-data**. El epic vende, el técnico legitima.

3. **Detalle a destacar**: ¿hay alguna frase del PDF que querés sentir como **inscripción en piedra** (XL tipo)?

   Opciones del PDF:
   - "Del caos a la coordinación: una brújula para cada lote"
   - "4 destinos. 4 productos. 4 experiencias."
   - "Este año, MAINTER no trae un congreso. Trae una brújula."

   Recomendación mía: la tercera, al cierre del manifiesto.

---

# 🔁 RONDAS DE ITERACIÓN (después de v1)

## Ronda 2 — Craft check ("impeccable" methodology)

> Revisá tu v1 con ojos críticos de Senior Art Director:
> - **Jerarquía visual**: ¿el ojo viaja en orden de importancia? Identificá 3 lugares donde se rompe.
> - **Spacing rhythm**: ¿hay consistencia en el sistema 8pt o aparecen valores random? Auditá secciones más débiles.
> - **Contrast & legibilidad**: ¿algún texto cae bajo 4.5:1? ¿algún CTA pierde claridad?
> - **Line-height & tracking**: ¿algún display se ve apretado o suelto?
> - **Microcopy**: ¿alguna frase suena genérica? Reemplazala con copy específico al concepto brújula/orientación.
>
> Listame 5 cosas que pulirías y aplicalas. Mostrá el diff.

## Ronda 3 — Performance + SEO + A11y audit

> Auditá tu HTML como si corrieras Lighthouse en mobile slow 4G:
> - LCP: ¿el hero pinta rápido? ¿hero image preloaded? ¿font preload?
> - CLS: ¿hay layout shift al cargar? ¿width/height en todas las img?
> - INP: ¿el form responde inmediato al input? ¿animaciones bloquean main thread?
> - SEO: ¿title ≤60ch? ¿description con keywords + fecha + ciudad? ¿canonical? ¿OG/Twitter?
> - JSON-LD: ¿Event schema completo y válido?
> - A11y: ¿labels/aria/focus visibles? ¿landmarks `<main>`, `<nav>`, `<footer>`?
>
> Mostrame las fixes en diff. Apuntá a Lighthouse Mobile ≥ 90/100/95/95.

## Ronda 4 — Mobile real (iPhone 13 / Samsung A series)

> Imagináte el HTML renderizado en 390x844 (iPhone 13) y 360x780 (Samsung A series).
>
> Por cada sección decime:
> - ¿se ve bien o se rompe?
> - ¿la jerarquía aguanta en mobile o se diluye?
> - ¿el form es cómodo con thumb?
> - ¿la brújula sigue siendo el hero o estorba?
> - ¿algún hover-only state queda oculto sin equivalente touch?
>
> Reforzá las secciones débiles. Mostrá el diff mobile-specific.

## Ronda 5 — Final polish

> Última pasada: ¿hay 3 detalles micro que harían a esta página memorable?
> Ejemplos posibles (NO obligatorios):
> - Cursor custom sobre la brújula
> - Skeleton del form con preview de tu sector según tipo seleccionado (antes de submit)
> - Easter egg: tipear "NORTE" enfoca esa tarjeta
> - Scroll progress hairline en el borde superior
> - Animación de la brújula que apunta al cardinal seleccionado en hover
>
> Eligí 2-3 y aplicá con criterio. Nada gratuito.

---

# 📤 Entrega final al equipo de implementación

Cuando estés conforme con v5, devolvé:

1. **HTML completo** (un solo bloque, listo copy-paste)
2. **Lista de assets externos** necesarios (fonts URLs, imágenes placeholder a reemplazar)
3. **Notas para integración**:
   - Dónde va el webhook URL del form
   - Dónde se debe enchufar el QR generado server-side
   - Qué `data-*` attributes podemos usar para tracking
4. **Resumen de decisiones de diseño** (3-5 líneas: por qué esa tipo, por qué ese hero, etc.)

---

**Final reminder**: este es un evento real de una empresa real de Bolivia con disertantes internacionales. No es un mock de portfolio. La página tiene que **funcionar para un productor de soya en Pailón que abre el link desde WhatsApp en un celular gama media**. Diseñá para él, no para juries de Awwwards.
