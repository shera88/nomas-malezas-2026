# GUÍA OPERATIVA — Landing No Más Malezas 2026

> Paso a paso humano. Qué hace **vos** (yacuserrano), qué hago **yo** (Claude Code).

---

## 🗺️ Mapa general del proyecto

```
1. Diseñás vos con Claude Design (claude.ai)      ← tu trabajo principal
                ↓
2. Me pasás el HTML final acá                     ← copy-paste a este chat
                ↓
3. Yo separo a archivos + cableo backend          ← mi trabajo
                ↓
4. Yo subo a GitHub + jsDelivr                    ← mi trabajo
                ↓
5. Yo creo página en WordPress vía MCP            ← mi trabajo
                ↓
6. Testeamos juntos                               ← ambos
                ↓
7. Mainter difunde URL                            ← tu cliente
```

---

## 📁 Estructura del proyecto

```
D:\Claude\No más malezas\
├── all-credentials.json          🔒 (gitignored, NO commitear)
├── .gitignore
├── .git/                          ← repo local inicializado
├── pdf/                           ← PDFs de Mainter (input)
│   ├── LogoNoMásMAlezas2026-Elementos.pdf
│   ├── PROYETO MAINTER 2026 - BRUJULA.pdf
│   ├── AmbientaciónoNoMalezas2.pdf
│   └── 7 mo Congreso Internacional NMM.docx
├── docs/
│   ├── PLAN.md                    ← plan v1 (deprecated, ver superpowers/plans/)
│   ├── PROMPT-DISENO.md           ← 📋 PROMPT para Claude Design
│   ├── GUIA.md                    ← este archivo
│   ├── CREDENCIALES-PENDIENTES.md ← lo que tenés que pasarme
│   └── superpowers/
│       ├── specs/2026-05-18-landing-nmm-2026-design.md  ← spec final
│       └── plans/2026-05-18-landing-nmm-2026.md         ← plan ejecutable
├── .claude/
│   └── skills/                    ← skills clonadas localmente
│       ├── auto-verify-loop/
│       ├── canvas-design/
│       ├── claude-mem/            ← MCP, activar con: npx claude-mem install
│       ├── csv-data-summarizer/
│       ├── docx/
│       ├── file-organizer/
│       ├── pdf/
│       ├── prompt-engineering/
│       ├── skill-creator/
│       ├── super-powers/
│       └── ui-ux-pro-max/
└── (los siguientes los creo yo cuando tengamos diseño)
    ├── src/
    ├── dist/
    ├── n8n/
    ├── supabase/
    ├── email/
    └── pdf/
```

---

## ✅ Tu checklist paso-a-paso

### PASO 1 — Tu trabajo de diseño con Claude Design

**Donde:** `claude.ai` (con tu cuenta logueada) — usá modelo **Opus 4.7** o **Sonnet 4.6**.

**Qué hacés:**

1. Abrí una conversación nueva en claude.ai
2. **Adjuntá los 3 PDFs** del directorio `pdf/`:
   - `LogoNoMásMAlezas2026-Elementos.pdf`
   - `PROYETO MAINTER 2026 - BRUJULA.pdf`
   - `AmbientaciónoNoMalezas2.pdf`
3. Abrí el archivo `docs/PROMPT-DISENO.md` con cualquier editor (Notepad alcanza)
4. **Copiá TODO el contenido del prompt** (desde "Actuá como un Senior Frontend Designer..." hasta "no para juries de Awwwards.")
5. Pegalo como tu primer mensaje a Claude
6. Esperá la **v1**. Va a ser un Artifact con HTML+CSS+JS.

**Respondé las 3 preguntas iniciales** que te haga Claude:
- ¿Brújula minimal o ornamental? → recomendado **híbrida**
- ¿Tono técnico o épico? → recomendado **70/30 épico/técnico**
- ¿Qué frase destacar XL? → recomendado **"Este año, MAINTER no trae un congreso. Trae una brújula."**

**Después iterá las rondas** (están al final del prompt):
- **Ronda 2** (craft): pegá el texto de "Ronda 2 — Craft check" del prompt
- **Ronda 3** (perf + SEO + a11y): pegá "Ronda 3 — Performance + SEO + A11y audit"
- **Ronda 4** (mobile real): pegá "Ronda 4 — Mobile real"
- **Ronda 5** (polish): pegá "Ronda 5 — Final polish"

**Cuándo parar**: cuando el diseño te haga sentir orgullo. No antes. Si dudás, una ronda más.

### PASO 2 — Pasarme el HTML final

**Donde:** este chat con Claude Code (yo).

**Qué hacés:**

1. Volvés acá
2. Decís: *"Acá va el HTML final"* y pegás el bloque HTML completo del Artifact
   - Si es muy grande, dividilo en 2-3 mensajes y avisás
3. Esperás. Yo:
   - Lo guardo en `src/index.html`
   - Separo CSS a `src/styles.css`
   - Separo JS a `src/form.js` y `src/compass.js`
   - Hago commit
   - Te muestro screenshot/preview

### PASO 3 — Antes de que yo suba a WordPress, necesito de vos:

Leé `docs/CREDENCIALES-PENDIENTES.md` y pasame todo. Sin esto no puedo deployar.

### PASO 4 — Yo subo todo

Yo me encargo de:
1. Crear repo GitHub `nomas-malezas-2026` con tu PAT
2. Push de los archivos
3. Verificar jsDelivr propaga el CSS/JS
4. Crear tabla `nmm_participantes` en Supabase
5. Importar workflow n8n
6. Instalar MCP wordpress en `settings.json`
7. Crear la página en el WordPress de Mainter
8. Verificar URL pública funciona

### PASO 5 — Testing juntos

Vos hacés 3-5 registros con datos reales (tu email, tu WhatsApp). Verificamos:
- Email llega
- PDF se abre
- QR escanea bien
- Color correcto según tipo
- Mobile fluido

### PASO 6 — Launch

Le pasás la URL a Mainter. Monitoreás primeras 24h en Supabase Studio.

---

## 🛠️ Comandos útiles para vos

### Ver qué tengo en el repo local

```powershell
cd "D:\Claude\No más malezas"
git status
git log --oneline
```

### Si Claude Design entregó archivos separados (no un solo HTML)

Decime explícito qué archivos tenés. Te ayudo a fusionarlos antes de subir.

### Para activar claude-mem (memoria persistente entre sesiones)

```powershell
npx claude-mem install
```

⚠️ Esto modifica tu `~/.claude/` global. Hacelo solo si querés activar el sistema de memoria automático del repo `thedotmack/claude-mem`. **No es obligatorio para este proyecto** — yo ya uso el sistema de memoria local de Claude Code default.

### Para limpiar PDFs temp generados (después)

```powershell
Remove-Item -Recurse -Force C:\Temp\nmm
```

---

## ❓ Preguntas frecuentes

**¿Puedo iterar diseño solo con vos sin Claude Design?**

Sí, pero perdés contexto visual. Claude Design en claude.ai con Artifacts ve los PDFs como imágenes — yo acá los leí como texto solamente. Para el output más fino, conviene Claude Design.

**¿Por qué tantas skills clonadas si no las uso todas?**

Las pediste vos. Las usables hoy son:
- `super-powers/writing-plans` ✅ (usada en docs/superpowers/plans/)
- `super-powers/brainstorming` ✅ (usada antes de spec)
- `ui-ux-pro-max` ✅ (aplicada al PROMPT-DISENO)
- `canvas-design` ✅ (visual philosophy en PROMPT-DISENO)
- `auto-verify-loop` (lista para Fase 3 testing visual)
- `prompt-engineering` (para futuros prompts a APIs)

Las demás son referencias por si las necesitamos después.

**¿El plan de superpowers tiene 14 tasks. Vamos a hacerlas todas?**

Sí, pero algunas son tuyas (Task 0 = pasarme creds, Task 3 = diseñar con Claude Design). Las técnicas (1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14) las hago yo cuando me destrabes lo que necesito.

**¿Y si Mainter no me da WordPress credentials?**

Plan B: hosteamos en Vercel con subdominio `nmm.mainter.com.bo` (necesitamos DNS) o en GitHub Pages. La página HTML es la misma — solo cambia el step de deploy.

**¿Cuánto cuesta esto?**

- jsDelivr: gratis
- GitHub público: gratis
- Supabase self-hosted: ya tenés
- n8n self-hosted: ya tenés
- SMTP SiteGround: ya tenés
- WordPress: ya tiene Mainter
- **Costo extra: $0**

---

## 🚨 Cosas que NO hacer

- ❌ Commitear `all-credentials.json` (ya está en .gitignore, dejarlo)
- ❌ Subir las credenciales de Mainter al repo público
- ❌ Hardcodear el webhook URL en el HTML sin que sea una constante editable
- ❌ Pushear sin hacer pull primero (después de Task 1)
- ❌ Modificar la tabla `nmm_participantes` después de tener registros sin migration script
- ❌ Mandar mass email desde el SMTP sin testear primero (riesgo spam)

---

## 📞 Cuando te trabes

Volvé acá y decime el síntoma exacto. Errores ⇒ pegá el stacktrace tal cual. Algo se ve raro ⇒ screenshot.
