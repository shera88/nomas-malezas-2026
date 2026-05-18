# PLAN — Landing Registro 7mo Congreso Internacional No Más Malezas

> ⚠️ **Este archivo está DEPRECADO.**
>
> Reemplazado por:
> - Spec final: [docs/superpowers/specs/2026-05-18-landing-nmm-2026-design.md](superpowers/specs/2026-05-18-landing-nmm-2026-design.md)
> - Plan ejecutable task-por-task: [docs/superpowers/plans/2026-05-18-landing-nmm-2026.md](superpowers/plans/2026-05-18-landing-nmm-2026.md)
>
> Se mantiene solo como referencia histórica del análisis inicial.
>
> ---

> Cliente: **MAINTER** (Grupo LANDICORP, Santa Cruz Bolivia, fundada 1983)
> Evento: **Lunes 1 de Junio 2026** · 4 horas · Sala principal · 1,200 asistentes
> Concepto: **"La Brújula del Lote"** — 4 puntos cardinales = 4 estrategias control malezas

---

## 1. Objetivo medible

Capturar registro de **1,200+ participantes**, enviar automáticamente:
1. Email confirmación
2. Entrada digital PDF + QR único (escaneable día evento)
3. Asignación automática de **color/sector** según tipo de participante

KPI: tasa conversión visita → registro completado ≥ 70% en mobile (audiencia llega por WhatsApp/social).

---

## 2. Stack técnico

| Capa | Herramienta | Razón |
|---|---|---|
| **Frontend** | HTML5 + CSS3 + JS vanilla (sin framework) | Cabe en WordPress como página custom. Sin build step. SEO perfecto. |
| **Hosting estáticos** | GitHub repo `nomas-malezas-2026` + jsDelivr CDN | `cdn.jsdelivr.net/gh/<user>/nomas-malezas-2026@main/dist/styles.css` |
| **Backend** | n8n self-hosted (ya tenés en `danzarte-n8n.rgxmhp.easypanel.host`) | Webhook recibe form → guarda → genera QR → envía email |
| **DB** | Supabase self-hosted (`supabase.imaginarte.cloud`) | Tabla `nmm_participantes`. Export Excel/CSV via Studio. |
| **Email** | SMTP SiteGround existente (`administracion@festivaldanzarte.com`) o nuevo de Mainter | Templates HTML, attachment PDF |
| **QR** | Librería `qrcode` en n8n Code node | UUID v4 único por participante. Payload: `{id, nombre, tipo, color}` |
| **PDF entrada** | Plantilla HTML → `puppeteer` (n8n) o PDFKit | A5 vertical, brújula+color+QR |
| **CMS** | WordPress de Mainter (acceso vía MCP `docdyhr/mcp-wordpress`) | Página custom `/no-mas-malezas-2026` |

---

## 3. Arquitectura de flujo

```
[Usuario en mobile]
    │
    ▼ navega a mainter.com.bo/no-mas-malezas-2026
[WordPress página custom]
    │   <link href="cdn.jsdelivr.net/.../styles.css">
    │   <script src="cdn.jsdelivr.net/.../form.js"></script>
    ▼ submit formulario
[POST /webhook/nmm-registro a n8n]
    │
    ├─ valida campos (email, WhatsApp formato Bolivia +591)
    ├─ INSERT en Supabase tabla nmm_participantes
    ├─ genera UUID + QR PNG (base64)
    ├─ asigna color según tipo:
    │     Estudiante      → AZUL  (ESTE)
    │     Productor       → VERDE (NORTE)
    │     Empresa         → AMARILLO (OESTE)
    │     Institución     → ROJO (SUR)
    │     Prensa          → BLANCO (neutro/admin)
    │     Otro            → GRIS
    ├─ renderiza PDF entrada (HTML template + QR)
    ├─ envía email SMTP con PDF adjunto + QR inline
    └─ responde 200 al frontend → muestra pantalla "¡Listo!"
        │
        └─ frontend muestra QR + botón "Descargar entrada"

[Día evento]
[Staff con app móvil simple]
    │
    ▼ escanea QR
[GET /webhook/nmm-validar?id=UUID]
    │
    ├─ busca en Supabase
    ├─ marca `escaneado_at = NOW()`
    └─ responde {nombre, tipo, color, sector, valido: true/false}
```

---

## 4. Esquema de datos (Supabase)

```sql
CREATE TABLE nmm_participantes (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creado_at    TIMESTAMPTZ DEFAULT NOW(),
  nombre       TEXT NOT NULL,
  tipo         TEXT NOT NULL CHECK (tipo IN
                ('estudiante','productor','empresa','institucion','prensa','otro')),
  contexto     TEXT NOT NULL,      -- universidad / zona / empresa / institución / medio / otro
  whatsapp     TEXT NOT NULL,
  email        TEXT NOT NULL,
  color        TEXT NOT NULL,      -- verde | azul | rojo | amarillo | blanco | gris
  punto        TEXT NOT NULL,      -- N | E | S | O | -
  sector       TEXT,               -- ej: "Sector Norte - Fila A"
  qr_payload   TEXT NOT NULL,      -- JSON minified
  escaneado_at TIMESTAMPTZ,
  email_enviado_at TIMESTAMPTZ
);

CREATE INDEX nmm_email_idx     ON nmm_participantes (email);
CREATE INDEX nmm_tipo_idx      ON nmm_participantes (tipo);
CREATE INDEX nmm_escaneado_idx ON nmm_participantes (escaneado_at);
```

Export a Excel: Supabase Studio → tabla → Export CSV. O via Edge Function.

---

## 5. Mapeo Tipo → Color → Punto cardinal

Decisión propuesta (revisable con cliente):

| Tipo participante | Color | Punto cardinal | Sector |
|---|---|---|---|
| Estudiante | Azul `#2E86DE` | ESTE | Pre-emergente · ZethaMaxx |
| Productor / Agricultor | Verde `#27AE60` | NORTE | Barbecho · Ultracheval |
| Empresa | Amarillo `#F1C40F` | OESTE | Resistentes · Apresa |
| Institución | Rojo `#E74C3C` | SUR | Post-emergente · Balón |
| Prensa | Blanco `#FFFFFF` | — | Acceso prensa (lateral) |
| Otro | Gris `#95A5A6` | — | General |

⚠️ Confirmar mapping con MAINTER antes de implementar — su pdf no especifica qué tipo va a qué cardinal.

---

## 6. Estructura página (single-page landing)

```
HERO         · Brújula animada SVG/Canvas, título 7mo Congreso, fecha, CTA
ABOUT        · 2 párrafos manifiesto "La Brújula del Lote"
4 CARDINALES · 4 cards con color, producto, disertante, país
SPEAKERS     · Avatares 4 disertantes + bio breve
VENUE        · Datos: 1,200 pax · 4 hrs · Sala principal
REGISTRO     · Formulario sticky o sección principal (mobile-first)
FAQ          · 4-6 preguntas (¿qué llevar?, ¿costo?, ¿cómo llego?)
FOOTER       · Logos MAINTER + LANDICORP + sponsors (Rodaria, ZNA, etc)
```

---

## 7. SEO checklist (objetivo: alcance orgánico)

- [ ] `<title>` ≤60 char: `7mo Congreso Internacional No Más Malezas 2026 · MAINTER`
- [ ] `<meta description>` 150 char con disertantes + fecha
- [ ] `<meta property="og:image">` 1200x630 con brújula + logo
- [ ] JSON-LD `Event` schema.org completo (location, startDate, organizer, performers)
- [ ] `<link rel="canonical">` apuntando URL única
- [ ] hreflang `es` (público boliviano + sudamericano)
- [ ] Imágenes con `loading="lazy"` + `<img alt>` descriptivo
- [ ] Sitemap.xml + robots.txt (delegar a SEO plugin WP, ej Yoast/RankMath)
- [ ] Open Graph + Twitter Cards
- [ ] Core Web Vitals: LCP <2.5s, INP <200ms, CLS <0.1
- [ ] Preload font crítica + `font-display: swap`
- [ ] Critical CSS inline ≤14KB
- [ ] H1 único con keyword principal: "7mo Congreso Internacional No Más Malezas"
- [ ] H2 por sección con keywords secundarias ("control de malezas", "manejo de barbecho", etc)
- [ ] Slug WordPress: `/no-mas-malezas-2026` (sin acentos, kebab)
- [ ] WhatsApp/social share buttons (CTR amplifier)

---

## 8. Accesibilidad (WCAG 2.2 AA)

- Contraste texto ≥4.5:1 (cuidado con amarillo sobre azul oscuro — testear)
- Labels asociados a inputs (`<label for="">`)
- `aria-required="true"` en obligatorios
- `aria-live="polite"` para feedback de éxito/error
- Focus visible (outline, no `outline: none` sin reemplazo)
- Tab order lógico
- Brújula decorativa con `aria-hidden="true"` o `role="img"` + `aria-label`

---

## 9. Componentes UI clave

1. **Hero con brújula interactiva** — SVG con `rotate` al hover/scroll, 4 puntos clickables que llevan a su sección
2. **Tarjetas cardinal** — borde color cardinal, hover eleva, número grande, badge producto
3. **Formulario sticky-on-mobile** — al hacer scroll, CTA fijo abajo
4. **Selector "Tipo participante"** — chips visuales con color (preview del sector)
5. **Campo dinámico** — animación fade-in al cambiar tipo
6. **Pantalla éxito** — confetti sutil, QR grande, botón descargar PDF, "agregar al calendario"
7. **Toast errores** — con `aria-live`

---

## 10. Plan de implementación (fases)

### Fase 0 — Setup (1 día)
- [ ] Recibir creds WordPress + GitHub PAT
- [ ] Instalar MCP `docdyhr/mcp-wordpress`
- [ ] Crear repo GitHub `nomas-malezas-2026`
- [ ] Crear tabla `nmm_participantes` en Supabase
- [ ] Crear workflow base n8n

### Fase 1 — Diseño (vos con Claude Design)
- [ ] Generar v1 HTML con prompt en `PROMPT-DISENO.md`
- [ ] Iterar 2-3 rondas hasta estar conforme
- [ ] Validar responsive en mobile real
- [ ] Validar contraste accesibilidad

### Fase 2 — Backend (yo)
- [ ] Workflow n8n: webhook → Supabase → QR → PDF → email
- [ ] Plantilla email HTML
- [ ] Plantilla PDF entrada
- [ ] Endpoint validación QR

### Fase 3 — Integración (yo)
- [ ] Cablear form HTML al webhook n8n
- [ ] Subir CSS/JS a GitHub
- [ ] Crear página WordPress vía MCP
- [ ] Pegar HTML con refs a jsDelivr

### Fase 4 — Testing (ambos)
- [ ] 5 registros prueba con datos reales
- [ ] Verificar email + PDF + QR escaneable
- [ ] Lighthouse score ≥90 en mobile
- [ ] Validar SEO con Search Console preview
- [ ] Cross-browser (Chrome, Safari iOS, Samsung Internet)

### Fase 5 — Launch
- [ ] Anunciar URL a MAINTER
- [ ] Monitorear primeras 24h (logs n8n + Supabase)
- [ ] Backup automático Supabase

---

## 11. Riesgos & mitigaciones

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Mainter no autoriza Supabase externo | Media | Plan B: usar tabla en WP (Custom Post Type) |
| WP version vieja sin REST API | Baja | Verificar wp-json antes; si falta, plugin "WordPress REST API" |
| Theme bloquea custom HTML/JS | Media | Usar template "Empty" o page builder existente |
| 1,200 registros en 1 día saturan n8n | Baja | n8n self-hosted aguanta; agregar rate limit en webhook |
| Email termina en spam | Alta | DKIM/SPF/DMARC en SiteGround. Sender domain coherente. |
| QR no escanea bien impreso | Media | Error correction level H, tamaño mínimo 3cm |

---

## 12. Skills usadas en este proyecto

| Skill | Uso |
|---|---|
| `impeccable` / `interface-design` | Audit + critique del diseño final |
| `auto-verify-loop` (local) | Loop verificación visual tras cada cambio |
| `caveman` | Comunicación interna (este chat) |
| `feature-dev:feature-dev` | Si hay features nuevas grandes |
| `claude-api` | Si decidimos automatizar generación QR vía Claude API |

Skills faltantes pendientes de URL del usuario: `ui-ux-pro-max`, `super-powers`, `csv-data-summarizer`, `skill-creator`, `canvas-design`, `docx`, `file-organizer`, `pdf`, `prompt-engineering`.
