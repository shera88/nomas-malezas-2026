# Google Sheets — NMM 2026

## Archivos

- **`nmm-2026-registros-headers.csv`** — Solo encabezados, 1 fila. Importar para crear el Sheet vacío con columnas listas.
- **`nmm-2026-registros-con-ejemplo.csv`** — Headers + 1 fila de ejemplo (Juan Pérez). Útil para ver cómo se ve un registro real. **Eliminar la fila de ejemplo antes de producción.**

## Importar a Google Sheets

### Opción 1 — Crear Sheet nuevo desde CSV (rápido)

1. Andá a https://sheets.new
2. Archivo → **Importar** → **Subir** → seleccioná `nmm-2026-registros-headers.csv`
3. Configuración:
   - **Ubicación**: "Reemplazar hoja de cálculo"
   - **Tipo de separador**: Coma
   - **Convertir texto en números, fechas y fórmulas**: No (para que `59171234567` no pierda el primer dígito)
4. Click **Importar**
5. Renombrar: archivo a **`NMM 2026 - Registros`** · pestaña a **`participantes`**

### Opción 2 — Sheet existente

Si ya creaste un Sheet vacío:

1. Archivo → Importar → Subir el CSV
2. Marcar **Reemplazar datos desde la celda seleccionada** posicionado en A1

## Después de importar

- [ ] **Congelar fila 1**: Vista → Inmovilizar → 1 fila
- [ ] **Negrita** en fila 1
- [ ] **Validación de datos**:
  - Columna D (tipo): lista → `estudiante, productor, empresa, institucion, prensa, otro`
  - Columna H (color): lista → `verde, azul, rojo, amarillo, blanco, gris`
  - Columna I (punto): lista → `N, E, S, O, -`
- [ ] **Formato fechas** columnas B, L, M: `Formato → Número → Fecha y hora`
- [ ] **Compartir**: botón "Compartir" → "Cualquier persona con el enlace" → Editor (necesario para n8n escribir vía OAuth)
- [ ] **Copiar URL del Sheet** y pegarla al chat para que Claude Code la guarde en `all-credentials.json`

## URL formato

`https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit#gid=0`

Donde `<SHEET_ID>` es la parte larga entre `/d/` y `/edit`.

## Exportar para Mainter (después del evento)

- Archivo → Descargar → **Microsoft Excel (.xlsx)** — abre directo en Excel
- O **CSV** — universal
- O **PDF** si quieren reporte impreso
