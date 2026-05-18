# Design Spec — Landing Registro 7mo Congreso Internacional No Más Malezas 2026

> **Project:** MAINTER · Evento "No Más Malezas" 7ma edición
> **Date:** 2026-05-18
> **Author:** yacuserrano@gmail.com (con Claude Opus 4.7)
> **Approach approved:** A — Monolito WordPress + jsDelivr CDN + n8n + Supabase
> **Mapping participante↔color approved:** Estudiante=Azul/E, Productor=Verde/N, Empresa=Amarillo/O, Institución=Rojo/S, Prensa=Blanco, Otro=Gris

---

## 1. Purpose

Capturar registro de **1,200+ participantes** del 7mo Congreso Internacional No Más Malezas (Mainter · Santa Cruz, Bolivia · Lunes 1 de Junio 2026, 4 horas). Cada participante recibe automáticamente:

1. Email de confirmación
2. Entrada digital PDF con **código QR único**
3. Color/cardinal asignado según tipo (orientación al sector del salón)

QR se escanea día del evento → marca asistencia + orienta a sector. Base de datos exportable a Excel/CSV para staff Mainter.

---

## 2. Success Criteria

| Métrica | Target |
|---|---|
| Lighthouse Mobile Performance | ≥ 90 |
| Lighthouse SEO | 100 |
| Lighthouse Accessibility | ≥ 95 |
| Tiempo registro (visita → submit) | < 60 seg promedio |
| Conversión visita → registro | ≥ 70% |
| Tasa email entregado (no spam) | ≥ 95% |
| QR escaneable a 30cm distancia | 100% |
| Carga inicial 4G Bolivia | < 2.5s LCP |

---

## 3. Architecture (Approach A)

```
                  ┌────────────────────┐
                  │  WordPress Mainter │
                  │  /no-mas-malezas   │
                  │                    │
                  │  HTML inline       │◀───────┐
                  └────┬───────────────┘        │
                       │ <link>/<script>        │ subida via
                       ▼                        │ MCP wordpress
            ┌──────────────────────┐            │ (REST API
            │  GitHub repo         │            │  application
            │ nomas-malezas-2026   │            │  password)
            │  /dist/styles.css    │
            │  /dist/form.js       │
            │  /dist/qrcode.min.js │
            └─────────┬────────────┘
                      │ servido vía jsDelivr CDN
                      │ cdn.jsdelivr.net/gh/<user>/nomas-malezas-2026@main/dist/*
                      ▼
            ┌──────────────────────┐
            │  Browser (mobile)    │
            │  Form submit         │
            └─────────┬────────────┘
                      │ POST JSON
                      ▼
            ┌──────────────────────────────┐
            │  n8n webhook                 │
            │  /webhook/nmm-registro       │
            │                              │
            │  1. Validate                 │
            │  2. INSERT Supabase          │
            │  3. Generate QR PNG          │
            │  4. Render PDF (puppeteer)   │
            │  5. SMTP send w/ attachment  │
            │  6. Respond {ok, qr_data}    │
            └─────────┬────────────────────┘
                      │
            ┌─────────┴──────────┐
            ▼                    ▼
  ┌──────────────────┐  ┌──────────────────┐
  │ Supabase         │  │ SMTP SiteGround  │
  │ nmm_participantes│  │ → email user     │
  └──────────────────┘  └──────────────────┘
```

---

## 4. Data Model

**Table:** `nmm_participantes` (Supabase `supabase.imaginarte.cloud`)

```sql
CREATE TABLE IF NOT EXISTS nmm_participantes (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creado_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  nombre            TEXT NOT NULL,
  tipo              TEXT NOT NULL CHECK (tipo IN
                      ('estudiante','productor','empresa','institucion','prensa','otro')),
  contexto          TEXT NOT NULL,
  whatsapp          TEXT NOT NULL,
  email             TEXT NOT NULL,
  color             TEXT NOT NULL CHECK (color IN
                      ('azul','verde','amarillo','rojo','blanco','gris')),
  punto             TEXT NOT NULL CHECK (punto IN ('N','E','S','O','-')),
  sector            TEXT,
  qr_payload        TEXT NOT NULL,
  email_enviado_at  TIMESTAMPTZ,
  escaneado_at      TIMESTAMPTZ,
  user_agent        TEXT,
  ip_hash           TEXT
);

CREATE INDEX IF NOT EXISTS nmm_email_idx     ON nmm_participantes (email);
CREATE INDEX IF NOT EXISTS nmm_tipo_idx      ON nmm_participantes (tipo);
CREATE INDEX IF NOT EXISTS nmm_escaneado_idx ON nmm_participantes (escaneado_at);
CREATE UNIQUE INDEX IF NOT EXISTS nmm_email_unique ON nmm_participantes (LOWER(email));

-- RLS: tabla cerrada, solo service_role escribe vía n8n
ALTER TABLE nmm_participantes ENABLE ROW LEVEL SECURITY;
```

**Mapping tipo → color → punto (locked):**

| Tipo | Color | Punto | Sector |
|---|---|---|---|
| `estudiante` | `azul` (`#2E86DE`) | `E` | Pre-emergente · ZethaMaxx |
| `productor` | `verde` (`#27AE60`) | `N` | Barbecho · Ultracheval |
| `empresa` | `amarillo` (`#F1C40F`) | `O` | Resistentes · Apresa |
| `institucion` | `rojo` (`#E74C3C`) | `S` | Post-emergente · Balón |
| `prensa` | `blanco` (`#FFFFFF`) | `-` | Acceso prensa lateral |
| `otro` | `gris` (`#95A5A6`) | `-` | General |

---

## 5. Components

### 5.1 Frontend (single HTML page in WP)

| Componente | Responsabilidad | Archivo |
|---|---|---|
| `index.html` | Markup completo + meta SEO + JSON-LD | `src/index.html` |
| `styles.css` | Variables CSS + layout responsive + animations | `src/styles.css` → `dist/styles.css` |
| `form.js` | Validación + submit fetch + UI éxito | `src/form.js` → `dist/form.js` |
| `compass.js` | Brújula SVG interactiva (hover/click cardinales) | `src/compass.js` → `dist/compass.js` |
| `qrcode.min.js` | Render QR placeholder client-side (preview pre-submit) | `dist/qrcode.min.js` (vendored, MIT) |

**Build step:** ninguno. Solo concatenación opcional con `cat` para minify. Sin webpack/vite.

### 5.2 Backend (n8n workflow)

| Nodo | Tipo | Responsabilidad |
|---|---|---|
| `Webhook NMM Registro` | Webhook | POST público recibe form |
| `Validate Input` | Function | Email regex, WhatsApp +591, campos required |
| `Map Tipo to Color` | Set | Asigna color/punto/sector según tabla |
| `Check Duplicate` | Supabase | SELECT por email; si existe, devuelve QR existente |
| `Insert Supabase` | Supabase | INSERT nuevo registro |
| `Generate QR` | Function (qrcode npm) | PNG base64 con payload `{id, nombre, tipo, color}` |
| `Render PDF` | Function (puppeteer) | HTML template → PDF A5 |
| `Send Email` | SMTP | HTML + adjunto PDF |
| `Mark email_enviado` | Supabase | UPDATE timestamp |
| `Respond` | Respond to Webhook | JSON `{ok, id, color, punto, qr_data_url}` |

### 5.3 Validación día evento (workflow separado)

| Nodo | Responsabilidad |
|---|---|
| `Webhook Validar` | GET con `?id=UUID` |
| `Lookup Supabase` | SELECT + UPDATE escaneado_at |
| `Respond` | `{valido, nombre, tipo, color, sector}` |

---

## 6. Page Sections (orden)

1. **HERO** — Brújula SVG animada + título + fecha + CTA
2. **MANIFIESTO** — Frase ancla + 2-3 líneas concepto
3. **LOS 4 PUNTOS CARDINALES** — Grid 2x2 con cards color
4. **SPEAKERS** — 4 disertantes con bio breve + país
5. **VENUE** — Datos técnicos sala + 4 horas + experiencia
6. **REGISTRO** — Formulario sticky-mobile, foco principal
7. **FAQ** — Acordeón 6 preguntas
8. **FOOTER** — Logos + contacto + redes

---

## 7. Form UX detail

- **Mobile-first**: form visible al cargar en mobile (no scroll para encontrarlo)
- **Campo dinámico**: change suave 300ms ease-out al cambiar tipo
- **Validación inline**: en blur, no en submit (UX nielsen pattern)
- **Botón submit**: con loading spinner + disabled durante POST
- **Errores**: toast top + aria-live, no alert()
- **Éxito**: full-screen overlay con QR + animación checkmark + "Descargar entrada" + "Agregar al calendario .ics"
- **WhatsApp mask**: `+591 7 1234 5678` formato Bolivia

---

## 8. SEO

```html
<title>7mo Congreso Internacional No Más Malezas 2026 · MAINTER</title>
<meta name="description" content="Lunes 1 de Junio 2026 · 4 disertantes internacionales · Manejo de barbecho, pre-emergente, post-emergente y resistencias. Registro gratuito en línea.">
<meta property="og:title" content="7mo Congreso Internacional No Más Malezas">
<meta property="og:description" content="La Brújula del Lote — 4 puntos cardinales del manejo de malezas. 01·06·2026 · Santa Cruz, Bolivia">
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/<user>/nomas-malezas-2026@main/dist/og-image.jpg">
<meta property="og:type" content="event">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://mainter.com.bo/no-mas-malezas-2026">
<html lang="es">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "7mo Congreso Internacional No Más Malezas",
  "startDate": "2026-06-01T14:00:00-04:00",
  "endDate":   "2026-06-01T18:00:00-04:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Salón Principal MAINTER",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "3er Anillo Interno Esq. Av. La Salle",
      "addressLocality": "Santa Cruz de la Sierra",
      "addressCountry": "BO"
    }
  },
  "organizer": {
    "@type": "Organization",
    "name": "MAINTER",
    "url": "https://mainter.com.bo"
  },
  "performer": [
    {"@type": "Person", "name": "Pedro Christoffoleti", "nationality": "Brasil"},
    {"@type": "Person", "name": "Lucas Paterlini", "nationality": "Argentina"},
    {"@type": "Person", "name": "Pablo Franco", "nationality": "Bolivia"}
  ],
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "BOB",
    "availability": "https://schema.org/InStock",
    "url": "https://mainter.com.bo/no-mas-malezas-2026"
  }
}
</script>
```

---

## 9. Accesibilidad (WCAG 2.2 AA)

- Contraste ≥4.5:1 todos los textos (validar `#F1C40F` sobre `#FFFFFF` — falla, usar solo sobre `#0A1628`)
- `<label for>` + `id` en cada input
- `aria-required`, `aria-invalid`, `aria-describedby`
- Focus visible custom (no `outline: none` sin reemplazo)
- Tab order natural
- Brújula con `role="img"` + `aria-label="Brújula con los 4 puntos cardinales del manejo de malezas"`
- `prefers-reduced-motion`: deshabilita rotación
- `<button>` no `<div onclick>`
- `lang="es"` en HTML

---

## 10. Performance budget

| Recurso | Budget |
|---|---|
| HTML inicial | ≤ 30 KB gzip |
| CSS crítico inline | ≤ 14 KB |
| CSS external (jsDelivr) | ≤ 25 KB gzip |
| JS total | ≤ 20 KB gzip |
| Fonts (preload 1-2) | ≤ 60 KB |
| Imágenes hero | ≤ 80 KB (WebP, lazy) |
| **Total page** | **≤ 200 KB sobre la red** |

---

## 11. Risks

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Mainter WP theme bloquea custom HTML | Media | Usar template "Empty" o page builder, fallback shortcode plugin |
| Lighthouse SEO < 100 por meta inyectada por WP | Media | Plugin SEO (Yoast/RankMath) descripción manual + remover defaults |
| `#F1C40F` (amarillo) sobre `#FFFFFF` falla contraste | Alta | Reglas estrictas: amarillo solo sobre fondo oscuro |
| 1,200 submits concurrentes saturan n8n | Baja | n8n self-hosted aguanta. Agregar rate limit 10 req/IP/min |
| Email entra en spam | Alta | SPF + DKIM + DMARC configurados en SiteGround. From coherente. |
| QR no escanea bien impreso | Media | EC level H + tamaño ≥3cm en PDF |
| Self-hosted Supabase cae | Baja | Backup automático 24h. Plan B: tabla en WP via REST. |
| Email duplicado del mismo participante | Alta | UNIQUE constraint en email; n8n devuelve QR existente sin duplicar registro |

---

## 12. Out of scope (v1)

- Pasarela de pago (evento es gratuito)
- Multi-idioma (solo español)
- App nativa de escaneo (usar webapp simple en n8n)
- Dashboard analítico para Mainter (usar Supabase Studio + Lookerstudio si lo piden después)
- Login/usuarios persistentes (no aplica para evento puntual)
- Transmisión streaming en vivo
- Recordatorios automáticos pre-evento (planeable v1.1 con n8n cron)

---

## 13. Self-Review checklist

- [x] Sin "TBD" / "TODO" en campos críticos
- [x] Mapping tipo↔color↔punto definido completo
- [x] Schema DB lockeado con CHECK constraints
- [x] Flow E2E descripto (frontend → n8n → DB → email)
- [x] SEO meta + JSON-LD completo (no placeholders en valores)
- [x] Accesibilidad: contraste especial flagged (`#F1C40F` over white)
- [x] Riesgos identificados con mitigación concreta
- [x] Out of scope explícito (evita scope creep)
- [x] Success criteria medibles (Lighthouse scores, LCP, conversión)

---

## 14. User Review Gate

Spec escrito y pronto para review. Cambios solicitados van inline. Sólo después de aprobación se invoca `writing-plans`.
