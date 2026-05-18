# CREDENCIALES Y DECISIONES PENDIENTES

> **Acción para vos**: pasame esto en el chat (o pegá en `all-credentials.json` debajo de cada bloque).
> Mientras falten, no puedo ejecutar las Tasks 1, 2, 6, 11, 12 del plan.

---

## 🔴 Bloqueantes — necesito YA para empezar

### 1. WordPress de MAINTER

```yaml
# Pegame en chat así:
wordpress_mainter:
  admin_url:    https://___________________/wp-admin
  usuario:      ___________________
  password:     ___________________
  # Yo genero la Application Password después de loguearme con vos vía Playwright
```

**Cómo obtener si no tenés**:
1. Pediselo a tu contacto en MAINTER por WhatsApp
2. Diles: "necesito acceso de Administrador a `mainter.com.bo/wp-admin` para subir una página personalizada del evento No Más Malezas. Generaré una Application Password limitada que no requiere tu password normal después."

**Riesgo bajo**: voy a generar una Application Password (token limitado) y descartar el password normal. Si después quieren revocarme acceso, lo borran en 1 click.

---

### 2. GitHub Personal Access Token (PAT)

```yaml
github:
  username:     ___________________
  pat:          github_pat_11____________________________________________
```

**Cómo crear**:
1. Andá a https://github.com/settings/tokens/new
2. **Note**: `Claude Code — NMM 2026`
3. **Expiration**: 90 días
4. **Scopes** (marca estos):
   - `repo` (todos los sub-scopes)
   - `workflow`
5. Click **Generate token**
6. **COPIALO** (no se muestra de nuevo). Pegámelo acá.

**Riesgo**: el PAT tiene poder de lectura/escritura sobre tus repos. Solo va a este proyecto. Cuando terminemos, lo revocás.

---

### 3. Confirmación de uso de infra Danzarte

```yaml
infraestructura:
  reusar_n8n_danzarte:       [sí / no / preguntar a Mainter]
  reusar_supabase_imaginarte: [sí / no / preguntar a Mainter]
  reusar_smtp_siteground:    [sí / no / preguntar a Mainter]
  # Si "preguntar a Mainter": preguntales si tienen objeción a usar
  # tu infraestructura privada para hostear el backend del evento.
```

**Riesgo de reusar**: si Mainter migra a otra empresa el año que viene, te van a pedir backup. Si Mainter quiere todo en su propio cloud (más limpio comercialmente), creamos un Supabase Cloud nuevo (free tier — alcanza para 1,200 registros) y un n8n en su Coolify si tienen.

**Mi recomendación**: reusar para v1 (más rápido), migrar después si el cliente lo pide.

---

## 🟡 Decisiones de diseño/contenido — confirmá con MAINTER

### 4. Disertante de SUR (Paraguay)

El PDF dice "____________ - Paraguay" para el cardinal SUR (Post-emergente, producto Balón). **Necesito el nombre**.

```yaml
disertante_sur_paraguay:
  nombre:  ___________________
  bio:     ___________________  # 1-2 líneas para el sitio
  foto_url: ___________________  # opcional, podemos usar placeholder
```

### 5. ✅ Assets gráficos — YA TENGO

Encontré en `Ilustrator/elementos/`:
- ✅ logo NMM principal con brújula
- ✅ logo MAINTER + cruz amarilla
- ✅ 4 letras cardinales (N/E/S/O) con anillos color
- ✅ Brújula rosa de los vientos completa
- ✅ Banderas Bolivia/Brasil/Argentina/Paraguay
- ✅ Fondo topográfico tile

**Pendiente**: logos sponsors para footer.

```yaml
sponsors_footer:
  - nombre: Rodaria
    logo_url: ___________________  # PNG transparente, ideal
  - nombre: ZNA
    logo_url: ___________________
  - nombre: Tramontina
    logo_url: ___________________
  - nombre: Gran Alimento
    logo_url: ___________________
```

### 6. ⚠️ Confirmar mapping color↔cardinal↔país↔disertante

**Hay conflicto** entre PDF "Brújula" y PNGs entregados:

| Cardinal | Color en PNG | Bandera en PNG | País disertante (PDF) | Disertante (DOCX) |
|---|---|---|---|---|
| **N** | Verde lima | 🇧🇴 Bolivia | Brasil | Pedro Christoffoleti (BR) |
| **E** | Amarillo | 🇧🇷 Brasil | Argentina | Lucas Paterlini (AR) |
| **S** | Rojo coral | 🇦🇷 Argentina | Paraguay | (pendiente) |
| **O** | Cian turquesa | 🇵🇾 Paraguay | Bolivia | Pablo Franco (BO) |

**Confirmá con MAINTER**:

```yaml
mapping_final:
  norte:
    color:       [verde lima / verde mainter] # cuál usar
    bandera:     ___________________
    disertante:  ___________________
    tema:        Manejo de Barbecho
    producto:    Ultracheval

  este:
    color:       [amarillo / azul]
    bandera:     ___________________
    disertante:  ___________________
    tema:        Pre-emergente
    producto:    ZethaMaxx

  sur:
    color:       [rojo]
    bandera:     ___________________
    disertante:  ___________________  # ← falta nombre, era "______ Paraguay"
    tema:        Post-emergente
    producto:    Balón

  oeste:
    color:       [cian turquesa / amarillo]
    bandera:     ___________________
    disertante:  ___________________
    tema:        Malezas Resistentes
    producto:    Apresa
```

### 7. 📸 Identificar fotos de oradores

Hay 3 JPEGs en `oradores/`. Ayudame a asignar:

```yaml
oradores_identificacion:
  WhatsApp_Image_23.38.27.jpeg:  # Hombre mayor, lentes, sonriendo, fondo rojo "2"
    nombre:    ___________________
    pais:      ___________________
    cardinal:  ___________________

  WhatsApp_Image_23.38.28.jpeg:   # Hombre joven, calvo, barba, en campo de soya
    nombre:    ___________________
    pais:      ___________________
    cardinal:  ___________________

  WhatsApp_Image_23.38.28_1.jpeg: # Hombre, polo marrón, fondo verde BASF
    nombre:    ___________________
    pais:      ___________________
    cardinal:  ___________________

  cuarto_orador:                  # el de Paraguay, falta foto + nombre
    nombre:    ___________________
    pais:      Paraguay
    cardinal:  ___________________
    foto:      ___________________
```

### 7. URL final de la página

```yaml
url_final:
  opcion_a: https://mainter.com.bo/no-mas-malezas-2026
  opcion_b: https://mainter.com.bo/nmm2026
  opcion_c: https://mainter.com.bo/evento-2026
  # Confirmá con Mainter cuál slug prefieren
```

Mi recomendación: **opcion_a** (mejor SEO con keywords completos).

### 8. Email "From" del registro

```yaml
email_remitente:
  opcion_a:
    email: administracion@festivaldanzarte.com   # tu SMTP existente
    nombre: MAINTER · No Más Malezas
  opcion_b:
    email: eventos@mainter.com.bo                # nuevo email de Mainter (necesita setup SPF/DKIM)
    nombre: MAINTER
  opcion_c:
    email: nomasmalezas@mainter.com.bo
    nombre: 7° Congreso No Más Malezas
```

⚠️ **Cuidado**: si el `from` es de un dominio diferente al sitio web, los emails caen más en spam. Lo ideal es `*@mainter.com.bo` con SPF + DKIM + DMARC configurados.

**Recomendación**: **opcion_b o c**. Si Mainter no tiene email configurable, vamos con **a** como bridge (avisar a Mainter que cambiaremos cuando puedan).

---

## 🟢 Opcional / Nice-to-have

### 9. WhatsApp Business API para confirmación

Tenés YCloud configurado en `all-credentials.json`. ¿Querés que también mandemos confirmación por WhatsApp con el QR?

```yaml
notificacion_whatsapp:
  habilitar: [sí / no]
  # Si sí: necesito que Mainter apruebe usar el número +59162180085 como remitente
```

**Costo YCloud**: ~$0.005 por mensaje x 1,200 = ~$6 total. Trivial.

### 10. Google Calendar integration

```yaml
google_calendar:
  generar_ics: sí   # archivo .ics adjunto en email — gratis, recomendado
  link_directo:     # link "Agregar a Google Calendar" — gratis, recomendado
```

### 11. Google Maps embed en sección venue

```yaml
google_maps:
  embed: [sí / no]
  # Si sí: necesito coords exactas de "3er Anillo Interno Esq. Av. La Salle, Santa Cruz"
  # o link directo de Google Maps al lugar
```

### 12. Analytics

```yaml
analytics:
  herramienta: [GA4 / Plausible / Umami / ninguno]
  measurement_id: ___________________
```

**Recomendación**: GA4 si Mainter ya lo usa en `mainter.com.bo`. Plausible/Umami si querés algo más liviano y privacidad-first.

---

## 📋 Plantilla para responderme

Copiá esto, completá, pegámelo:

```yaml
# === BLOQUEANTES ===
wordpress_mainter:
  admin_url:
  usuario:
  password:

github:
  username:
  pat:

infraestructura:
  reusar_n8n_danzarte:
  reusar_supabase_imaginarte:
  reusar_smtp_siteground:

# === DECISIONES ===
disertante_sur_paraguay:
  nombre:
  bio:

sponsors_logos: # ok, pendiente, te paso después
url_final: # opcion_a / opcion_b / opcion_c
email_remitente: # opcion_a / opcion_b / opcion_c

# === OPCIONAL ===
whatsapp_confirmacion:
google_calendar:
google_maps_embed:
analytics:
```

---

## ⏰ Mientras tanto…

**Vos podés empezar Paso 1 (Claude Design)** sin estos datos. Solo bloqueás los Steps técnicos finales (deploy WordPress, push GitHub).

Diseñá en paralelo, pasame creds cuando las tengas. Cuando ambas cosas converjan, deployamos.
