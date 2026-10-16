# Noticias de Minerva's owl

Sitio de resúmenes diarios de noticias, desplegado automáticamente en GitHub Pages.

## Estructura

- `noticias/` — Páginas HTML de noticias diarias (formato `YYYY-MM-DD.html`)
- `index.html` — Página principal con enlaces a todas las noticias
- `scripts/update_index.py` — Script para regenerar el índice

## Agregar nuevas noticias

1. Coloca el archivo HTML con el nombre `YYYY-MM-DD.html` en la carpeta `noticias/`
2. Ejecuta el script para actualizar el índice:

   ```bash
   python scripts/update_index.py
   ```

3. Haz commit y push a `main`. El sitio se desplegará automáticamente.

## Licencia

MIT

