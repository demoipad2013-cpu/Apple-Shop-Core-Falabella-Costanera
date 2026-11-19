# Apple Shop Core V3.0 · Falabella Costanera

Dashboard de la Apple Shop de Falabella Costanera (FY27): Resumen, Metas, Share de tienda, Seasonality, Planograma (check de verificación), Inventario, Promociones y Equipo de ventas (Sales Pills y packs NPI).

## Publicar en GitHub Pages
1. Crea un repositorio nuevo en GitHub (por ejemplo `apple-shop-core`).
2. Sube **todo el contenido de esta carpeta** (index.html, README.md, .nojekyll y la carpeta `fuente`).
3. En el repositorio: **Settings → Pages → Build and deployment → Deploy from a branch**, rama `main`, carpeta `/ (root)` → **Save**.
4. En 1–2 minutos queda en `https://TU-USUARIO.github.io/apple-shop-core/`.

## Cómo funciona fuera de Claude
- Es un solo archivo `index.html`; no necesita servidor ni instalación.
- **Cargar Excel** (Apple Cascade) funciona igual: ventas ST Rptd / ST Rptd $ e inventario por PPN.
- **Guardar** guarda los cambios en el navegador que estás usando (localStorage). Para compartir datos entre equipos, usa **Cargar Excel → Descargar respaldo** y vuelve a subirlo.
- **PDF** se descarga directo desde el navegador.
- **Insights de ofertas (Promociones)**: dentro de Claude funciona directo. En GitHub / app en el inicio del iPhone toca *Configurar clave API* y pega una clave de console.anthropic.com (se guarda solo en ese dispositivo; el uso se cobra en esa cuenta).
- Las librerías (GSAP, SheetJS, html2canvas, jsPDF) se cargan desde cdnjs, por lo que necesita internet.

## Carpeta `fuente`
`template.html` (código) y `build.py` (datos iniciales) usados para generar `index.html`. No son necesarios para publicar.
