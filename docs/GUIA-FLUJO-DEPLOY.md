# GUÍA DE FLUJO — Claude Design → GitHub → WordPress

Paso a paso humano. Lo que hace **vos** (Yacu) y lo que hago **yo** (Claude Code). Asumí que ya están listos: repo GitHub, App Password WP, sponsors, retratos oradores, paleta locked.

---

## 🗺️ Vista general — 3 fases, ~90 minutos totales

```
┌───────────────────────────────────────────────────────────────┐
│  FASE 1: DISEÑO (vos en claude.ai)                  ~45 min   │
│  Generás HTML+CSS+JS con Claude Design                        │
│  Iterás 4-5 rondas hasta estar conforme                       │
└────────────────────────┬──────────────────────────────────────┘
                         │ pegás HTML acá
                         ▼
┌───────────────────────────────────────────────────────────────┐
│  FASE 2: INTEGRACIÓN (yo en este chat)              ~20 min   │
│  Separo HTML/CSS/JS → push a GitHub → jsDelivr propaga        │
│  Cableo webhook n8n → Google Sheets                           │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
┌───────────────────────────────────────────────────────────────┐
│  FASE 3: DEPLOY (yo, via REST API)                  ~10 min   │
│  Subo HTML como página WP                                     │
│  Verificamos /no-mas-malezas-2026                             │
│  Testing 3-5 registros reales                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## 🎨 FASE 1 — Diseño con Claude Design (TU TRABAJO)

### Paso 1.1 — Preparar adjuntos (5 min)

Abrí Explorador de Windows en `D:\Claude\No más malezas\` y tené listos para arrastrar a claude.ai:

**PDFs (3 archivos):**
- `pdf/LogoNoMásMAlezas2026-Elementos.pdf`
- `pdf/PROYETO MAINTER 2026 - BRUJULA.pdf`
- `pdf/AmbientaciónoNoMalezas2.pdf`

**PNGs gráfica (recomendado mostrar, ayuda a Claude a entender visual):**
- `Ilustrator/elementos/logos/logo-NO-MAS-MALEZAS.png`
- `Ilustrator/elementos/logos/logo-letra-N.png`
- `Ilustrator/elementos/logos/logo-letra-E.png`
- `Ilustrator/elementos/logos/logo-letra-S.png`
- `Ilustrator/elementos/logos/logo-letra-O.png`
- `Ilustrator/elementos/brujula/brujula-rosa-vientos.png`

**Retratos oradores (3):**
- `oradores/perfiles/pedro-christoffoleti-600.webp`
- `oradores/perfiles/lucas-paterlini-600.webp`
- `oradores/perfiles/pablo-franco-600.webp`

### Paso 1.2 — Abrir Claude Design y pegar prompt (5 min)

1. Andá a https://claude.ai
2. Click **"New chat"**
3. Modelo (arriba): elegí **Claude Sonnet 4.6** (recomendado, balance velocidad/calidad)
   - Si querés máxima calidad: **Opus 4.7**
4. Arrastrá los archivos listados arriba a la caja de texto
5. Abrí en Notepad/VSCode el archivo `docs/PROMPT-DISENO.md`
6. **Copiá TODO el contenido** desde "Actuá como un Senior Frontend Designer..." hasta "no para juries de Awwwards." (final del archivo)
7. Pegalo como tu primer mensaje y enviá

### Paso 1.3 — Responder las 3 preguntas iniciales

Claude te va a hacer 3 preguntas al inicio. Respuestas recomendadas (podés cambiar):

1. **Brújula**: `Híbrida — geométrica minimal con detalles de cartografía sutiles`
2. **Tono de copy**: `70% épico-aspiracional, 30% técnico-data`
3. **Frase XL**: `Este año, MAINTER no trae un congreso. Trae una brújula.`

Esperá la v1. Va a tardar 1-3 min.

### Paso 1.4 — Iteraciones (4 rondas, ~30 min total)

Después de la v1, pegá una por una estas instrucciones de iteración del prompt (están al final de `PROMPT-DISENO.md`):

- **Ronda 2** — Craft check (jerarquía, spacing, contraste, microcopy)
- **Ronda 3** — Performance + SEO + A11y audit
- **Ronda 4** — Mobile real (iPhone 13 / Samsung A)
- **Ronda 5** — Final polish (2-3 detalles memorables)

**Criterio de stop**: cuando puedas mostrar la página a tu cliente sin avergonzarte. Si dudás, una ronda más.

### Paso 1.5 — Pedir entrega final

Cuando estés conforme, pedí a Claude Design:

> "Generá los 2 entregables finales que pide el prompt:
> 1. `index.html` completo (con head, body, CSS y JS embebidos, root `.nmm-2026`)
> 2. `embed-snippet.html` (solo bloque interno listo para WordPress)
>
> Pegámelos completos."

### Paso 1.6 — Pasarme el HTML

Volvé a este chat conmigo y mandá:

> "Acá va el HTML final"
>
> ```html
> (pegá el contenido de index.html)
> ```

Si es muy largo y se corta, dividilo en 2-3 mensajes y avisame "parte 2 de 3" en cada uno.

**Importante**: pegame también el `embed-snippet.html` si lo entregó. Acelera mucho la fase 2.

---

## 🔧 FASE 2 — Integración (MI TRABAJO, automático)

Cuando recibo el HTML, hago en este orden:

### 2.1 — Guardar y separar archivos

```
src/
├── index.html         ← lo que pegaste tal cual
├── styles.css         ← extraigo del <style> inline
├── form.js            ← extraigo lógica form del <script>
└── compass.js         ← extraigo lógica brújula (si está separable)
```

### 2.2 — Build minified a `dist/`

```
dist/
├── styles.min.css     ← whitespace collapsed
├── form.min.js
├── compass.min.js
└── qrcode.min.js      ← vendored para preview cliente-side
```

### 2.3 — Push a GitHub

```bash
git add src/ dist/
git commit -m "feat(ui): landing v1 from Claude Design"
git push origin main
```

### 2.4 — Verificar jsDelivr CDN (1-2 min de propagación)

```bash
curl -I https://cdn.jsdelivr.net/gh/shera88/nomas-malezas-2026@main/dist/styles.min.css
# expected: HTTP 200, content-type: text/css
```

### 2.5 — Crear workflow n8n NMM Registro

Yo lo hago en n8n UI. Estructura:

```
Webhook POST → Validate → Map tipo→color → Google Sheets Append
              → Generate QR → Render PDF → SMTP Send → Update Sheet → Respond
```

Te paso el URL del webhook generado, lo reemplazo en el HTML, push de nuevo.

### 2.6 — Reemplazar `PENDIENTE_N8N_URL` en form.js

```javascript
// Antes:
const WEBHOOK_URL = 'PENDIENTE_N8N_URL';
// Después:
const WEBHOOK_URL = 'https://danzarte-n8n.rgxmhp.easypanel.host/webhook/abc-123';
```

Push a GitHub. jsDelivr re-propaga en 1-2 min.

---

## 🚀 FASE 3 — Deploy a WordPress (MI TRABAJO, automático via REST API)

### 3.1 — Crear página WordPress

```bash
curl -X POST "https://www.mainter.com.bo/wp-json/wp/v2/pages" \
  -u "Nicole:tFxf 9mZ1 e4K6 3pfH EMOM vReh" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "7mo Congreso Internacional No Más Malezas",
    "slug": "no-mas-malezas-2026",
    "status": "publish",
    "content": "<HTML embed-snippet.html aquí>",
    "comment_status": "closed",
    "ping_status": "closed"
  }'
```

Yo lo ejecuto. Devuelve `id` de la página + `link` público.

### 3.2 — Configurar meta SEO (Yoast / AIOSEO)

Plugin AIOSEO ya está instalado. Yo seteo via REST:

```bash
PUT /wp-json/wp/v2/pages/{id}
{
  "yoast_head_json": { /* meta tags */ },
  "meta": { /* custom AIOSEO fields */ }
}
```

### 3.3 — Verificar URL pública

Abrir https://www.mainter.com.bo/no-mas-malezas-2026 en navegador.

Checklist:
- [ ] CSS de jsDelivr carga (sin styles del theme rompiendo)
- [ ] JS funciona (brújula anima, form valida)
- [ ] Imágenes cargan desde jsDelivr
- [ ] Form submit llega a n8n
- [ ] Email + PDF + QR llegan al testeo
- [ ] Mobile fluido en iPhone real / Android real
- [ ] Lighthouse Mobile ≥ 90 (lo corrés vos en PageSpeed Insights)

### 3.4 — Testing 5 registros (TU TRABAJO)

Probás cada tipo con tu email/WhatsApp:

```
1. Tipo: Estudiante       → debería asignar AZUL · ESTE
2. Tipo: Productor        → VERDE · NORTE
3. Tipo: Empresa          → AMARILLO · OESTE
4. Tipo: Institución      → ROJO · SUR
5. Tipo: Prensa           → BLANCO · sector prensa
```

Verificá que cada registro:
- Llega email con QR
- PDF se abre y muestra color correcto
- QR escanea con cualquier app
- Aparece en Google Sheet

### 3.5 — Limpiar pruebas

Yo borro las 5 filas de prueba del Sheet antes del launch público.

---

## 🎉 LAUNCH

1. Mainter aprueba página
2. Vos mandás URL `https://www.mainter.com.bo/no-mas-malezas-2026` a su equipo
3. Ellos difunden por WhatsApp, redes, email
4. Monitoreás Google Sheet en vivo

---

## 🔄 Si necesitás cambiar algo después del launch

### Cambio de texto/diseño

1. Hablás con Claude Design otra vez, mismo prompt + "v2: cambiá X, Y, Z"
2. Pegás HTML nuevo acá
3. Yo hago commit + push + actualizo página WP (1 comando)
4. jsDelivr propaga CSS/JS en 1-2 min

**Importante con jsDelivr cache**: si querés evitar cache de 12h, agregá `?v=2` al final del URL de jsDelivr:
```
https://cdn.jsdelivr.net/gh/shera88/nomas-malezas-2026@main/dist/styles.min.css?v=2
```

O mejor: usar **commit SHA** en vez de `main`:
```
https://cdn.jsdelivr.net/gh/shera88/nomas-malezas-2026@<sha-7chars>/dist/styles.min.css
```

Eso fuerza re-fetch siempre que cambias.

### Cambio en mapping color/tipo

1. Editás workflow n8n (mapping table)
2. Actualizo HTML form si cambian opciones
3. Push + deploy

### Más disertantes o cambios de speakers

1. Pasame fotos nuevas + datos
2. Genero retratos con Higgsfield
3. Actualizo HTML

---

## 🚨 Restauración al final del proyecto (NO OLVIDAR)

Cuando MAINTER termine el evento y ya no necesiten tracking en vivo:

```yaml
restauración_seguridad:
  - [ ] Wordfence: marcar de nuevo "Disable Application Passwords" en WAF options
  - [ ] AIOS: marcar de nuevo "Disable application password" en User Security → Additional
  - [ ] WordPress profile.php: revocar Application Password "Claude Code NMM 2026"
  - [ ] GitHub: revocar PAT "Claude Code NMM 2026" en https://github.com/settings/tokens
  - [ ] Eliminar `all-credentials.json` o moverlo a almacenamiento seguro fuera del proyecto
```

Yo te lo recuerdo al cerrar el proyecto.

---

## ❓ Si te trabás

Síntoma → solución rápida:

| Síntoma | Solución |
|---|---|
| Claude Design devuelve HTML feo | Pedí "Ronda 2: aplicá impeccable methodology", listame 5 cosas a pulir y aplicá |
| HTML pegado acá se corta | Pasalo en 2-3 mensajes, decime "parte 1 de 3" |
| WordPress muestra error al publicar página | Avisame, hay chance de que el theme tenga un page builder que conflictúa. Plan B: subir como Custom HTML widget |
| Form no envía a n8n | Probá con curl primero. Si curl funciona y browser no, es CORS — yo agrego header |
| Email cae en spam | Avisame, ajustamos DKIM/SPF/DMARC del SMTP |
| jsDelivr no propaga | Esperá 5 min y refrescá. Si no, uso `?v=timestamp` para forzar |
| QR no se ve bien impreso | Aumento error correction a H + tamaño mínimo 3cm |

---

## 📂 Archivos de referencia

- **Prompt para Claude Design**: [docs/PROMPT-DISENO.md](PROMPT-DISENO.md)
- **Spec técnico**: [docs/superpowers/specs/2026-05-18-landing-nmm-2026-design.md](superpowers/specs/2026-05-18-landing-nmm-2026-design.md)
- **Plan ejecutable**: [docs/superpowers/plans/2026-05-18-landing-nmm-2026.md](superpowers/plans/2026-05-18-landing-nmm-2026.md)
- **Estructura Google Sheets**: [google-sheets/README.md](../google-sheets/README.md)
- **Credenciales pendientes**: [docs/CREDENCIALES-PENDIENTES.md](CREDENCIALES-PENDIENTES.md)
