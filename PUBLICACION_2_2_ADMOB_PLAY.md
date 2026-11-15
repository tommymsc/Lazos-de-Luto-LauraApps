# Estado de publicación Lazos de Luto 2.2.0 (código 11)
Fecha: 15 noviembre 2026

## Publicación del código
- Compilación fuente: GitHub Actions extrae `LazosDeLuto50_GitHub.zip` y ejecuta `scripts/upgrade_ui.py` y `scripts/monetization_v22.py`.
- 50 JPG locales, cinco categorías, nueva navegación inicial, 48 mensajes de consuelo.
- Paquete de Play: `lazosdeluto.gratis`, API 36.
- Debug: banners/intersticiales/App Open utilizan IDs de prueba de Google.
- Release: banner e intersticial usan unidades existentes originales. **App Open se desactiva si no se ha proporcionado el ID de su unidad real**; nunca reutilizar el ID intersticial para apertura.
- Límite intersticial: solo si se visita una categoría diferente a otra previamente visitada, desde el segundo cambio, en transición natural y con enfriamiento mínimo 120 segundos; nunca después de descargar.
- App Open: solo desde pantalla de carga, después de dos aperturas previas, no se muestra si ya cargó la interfaz ni encima de un banner.
- UMP: solicitar actualizaciones de consentimiento antes de cargar anuncios; proporcionar opciones en interfaz.

## URLs del mismo alojamiento LauraApps
- Política específica: `https://tommymsc.github.io/lazos-de-luto-privacy.html`
- app-ads.txt: `https://tommymsc.github.io/app-ads.txt`
- El sitio fue actualizado en repositorio `tommymsc/tommymsc.github.io`. **Verificar HTTP 200 y contenido desde navegador, y después confirmar verificación en AdMob y dominio "Sitio web del desarrollador" de Google Play.**

## Impedimentos externos para AAB publicable
1. **Crear en AdMob una unidad de tipo App Open para Lazos de Luto** (no reutilizar banner/intersticial). Configurar el ID como GitHub Actions secret `LAZOS_ADMOB_OPEN_ID` (o propiedad Gradle `LAZOS_ADMOB_OPEN_ID`). Mientras esté ausente, release compila sin App Open.
2. **Clave de subida:** la app histórica fue generada por AppCreator24. Google administra clave de firma de distribución, pero puede existir una clave de subida antigua. Confirmar si es recuperable y, si no, solicitar restablecerla desde Play Console. No se puede asegurar que el nuevo AAB pase la comprobación de firma sin ese paso.
3. **AAB firmado:** configurar cuatro secretos GitHub:
   - `LAZOS_UPLOAD_KEYSTORE_BASE64` (keystore privado codificado base64)
   - `LAZOS_UPLOAD_KEYSTORE_PASSWORD`
   - `LAZOS_UPLOAD_KEY_ALIAS`
   - `LAZOS_UPLOAD_KEY_PASSWORD`
   El workflow puede crear un AAB firmado si están completos; en ausencia de ellos produce un AAB SIN FIRMA (no subir).
4. **Contenido engañoso:** la aplicación original fue retirada el 6 sep 2024. Eliminar la antigua frase "Tenemos las mejores 70 imágenes originales y de alta calidad de lazos de luto" y sustituir capturas y gráfico promocional para reflejar la app realmente probada. Revisar en todos los idiomas/localizaciones, incluir recurso gráfico correcto, y enviar todo para revisión.
5. **Play Console:** comprobar tamaño de página de memoria 16 KB en App Bundle Explorer; respuestas de seguridad de datos en línea con AdMob/UMP y demás SDKs; declarar anuncios; audiencia y calificación; política HTTPS, acceso sin cuenta, información de contacto y estado de comerciante (aviso plazo feb 2027).
6. **Pruebas reales:** versión nueva con consentimiento/región, abrir app tercera vez (App Open de prueba), saltar rápidamente entre categorías sin bloqueo, intersticial después del cooldown, probar después de cerrar app, sin conexión, guardar y compartir WhatsApp, favoritos, privacidad, Android 15 y 16.

## Títulos y textos honestos para Play
**Nombre:** Lazos de Luto

**Descripción breve:** 50 lazos de luto para recordar, guardar y compartir por WhatsApp.

**Descripción larga:** Lazos de Luto incluye 50 diseños conmemorativos en cinco categorías: elegantes, sobrios, florales, religiosos y modernos. Explora los diseños sin conexión, guarda tus favoritos y comparte imágenes con quienes quieras. Encontrarás también 48 mensajes de consuelo para copiar o compartir. No requiere crear una cuenta. Contiene publicidad.

**Novedades:** Nuevo inicio con acceso directo a categorías, galería mejorada, 48 mensajes de consuelo y ajustes de publicidad respetuosos.

## No confundir compilación con publicación
Que Actions genere correctamente el AAB no garantiza su aceptación en Play ni la restauración de la app retirada. Debe pasar revisión y utilizar firma de subida aceptada.
