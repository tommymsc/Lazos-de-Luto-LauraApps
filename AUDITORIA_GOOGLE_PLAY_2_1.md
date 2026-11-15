# Auditoría de preparación para Google Play — Lazos de Luto 2.1.0
Fecha de revisión: 15 noviembre 2026

## Confirmado en código
- ID de paquete histórico: `lazosdeluto.gratis`
- Nueva versión de prueba: `2.1.0`, `versionCode 10` (mediante `scripts/upgrade_ui.py` aplicado después de extraer el ZIP)
- Objetivo Android 16: `targetSdk 36`, `compileSdk 36`
- Mínimo Android 10: `minSdk 29`
- 50 lazos JPG incluidos en ZIP fuente; cinco categorías de diez; no prometer más de 50
- Nueva pantalla inicial: categorías visibles, favoritos, mensajes arriba
- Mensajes de consuelo: 48 textos en cuatro categorías, copiable/compartible
- Compartir por WhatsApp, compartir por otras apps, guardar localmente con MediaStore
- Icono launcher del ZIP y arte 512x512 para ficha
- Google AdMob: ID aplicación `ca-app-pub-2506564165861733~5189200154`; banner `ca-app-pub-2506564165861733/3900408409`; intersticial `ca-app-pub-2506564165861733/6482514721`
- Compilación de debug usa IDs de anuncio de prueba y no sirve para Play

## Impedimentos y comprobaciones pendientes ANTES DE PUBLICAR
1. **Firma:** Google Play administra la clave de distribución, pero la de **subida** usada por AppCreator24 no ha sido recuperada. Generar firma de subida válida o solicitar restablecimiento en Play Console; guardar claves solo en GitHub Secrets, jamás en el repositorio.
2. **AAB release firmado:** configurar keystore + secretos, compilar AAB `release` firmado y comprobar que Play Console lo acepta. AAB sin firma NO sirve.
3. **Política eliminada por afirmaciones engañosas (septiembre 2024):** sustituir gráfico promocional, capturas antiguas y texto "Tenemos las mejores 70 imágenes originales y de alta calidad de lazos de luto", y cualquier afirmación no demostrable. Debe enviarse **toda** la corrección a revisión; revisar si Play exige apelación adicional.
4. **Privacidad HTTPS:** la política Markdown en GitHub es de consulta, no una página oficial en dominio de desarrollador. Activar GitHub Pages o un hosting autorizado y enlazar URL pública HTTPS estable en Play Console.
5. **AdMob app-ads.txt:** publicarlo en `https://DOMINIO-DEL-DESARROLLADOR/app-ads.txt` y registrar exactamente ese dominio en ficha de Play. La ruta raw.githubusercontent.com no sustituye la raíz de un dominio reconocido por AdMob.
6. **Declaraciones en Play:** "Contiene anuncios" = sí; seguridad de datos según SDK AdMob/UMP y configuraciones reales; clasificación de contenido, público objetivo, políticas de familias si procede, accesos especiales (sin cuenta), datos de contacto, comercio antes de febrero de 2027, actualizaciones pertinentes.
7. **Consentimiento publicitario:** configurar mensaje UMP en AdMob, comprobar opción de privacidad en regiones aplicables; no solicitar anuncios personalizados sin consentimiento donde corresponda.
8. **Compatibilidad 16 KB:** revisar AAB final en explorador de paquetes. Si hubiera binarios nativos (.so), validar alineación ELF y empaquetado. Java/Kotlin sin SDKs nativos es normalmente compatible, pero esta comprobación **no** ha sido ejecutada.
9. **Pruebas funcionales reales:** instalar APK 2.1.0, navegación entre las cinco categorías, 50 imágenes, mensajes, favoritos persistentes, descarga, compartir WhatsApp instalado y ausente, anuncio de prueba y gestión del consentimiento; verificar Android 10, 15 y 16, y teléfono con recortes de pantalla.
10. **Material de Play:** usar icono de 512x512, gráfico promocional de 1024x500, capturas reales tomadas de esta versión y ficha de descripción corregida en es-419. Reemplazar imágenes obsoletas y actualizar notas de versión.
11. **Disponibilidad y revisión:** al subir el AAB, comprobar API36, 16 KB, políticas y que la app removida se habilite tras aprobación. Firma no garantiza aprobación.

## Propuesta de ficha honesta
- **Nombre:** Lazos de Luto
- **Descripción breve:** 50 lazos de luto para recordar, guardar y compartir por WhatsApp.
- **Descripción completa:** Lazos de Luto es una colección de 50 imágenes conmemorativas organizadas en cinco categorías: elegantes, sobrios, florales, religiosos y modernos. Explora los diseños, guarda tus favoritos y comparte imágenes por WhatsApp u otras aplicaciones. También encontrarás 48 mensajes de consuelo, recuerdo, fortaleza y despedida que puedes copiar o compartir. No requiere registro. La galería funciona sin conexión; los anuncios pueden requerir Internet.
- **Notas 2.1.0:** Nueva pantalla de inicio, acceso rápido a categorías, galería de dos columnas y 48 mensajes de consuelo.

Fuentes oficiales consultadas:
- https://support.google.com/googleplay/android-developer/answer/11926878?hl=es-419
- https://developer.android.com/guide/practices/page-sizes
- https://support.google.com/googleplay/android-developer/answer/9898842
- https://support.google.com/admob/answer/9675354
