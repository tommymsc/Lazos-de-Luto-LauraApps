# GitHub Actions: firma segura del AAB de Lazos de Luto

Última revisión: 16 de noviembre de 2026.

**Estado:** Google Play Console indica que la solicitud para restablecer la clave de carga está **pendiente**. No marcar aprobada ni publicar el AAB hasta confirmación explícita de Google.

## Protecciones ya instaladas
- La compilación pública hace APK de prueba y AAB **sin firma**. Nunca utiliza la clave privada durante eventos de tipo push.
- Solo **Actions → Build Lazos de Luto - 50 diseños → Run workflow** con el indicador `google_upload_key_reset_approved = true` habilita la firma. Ejecutar únicamente tras aprobación del cambio.
- El workflow verifica que la clave privada corresponda al certificado PEM entregado a Google. Rechaza parejas distintas.
- La clave temporal vive en `/tmp/lazos-upload-key.jks` durante el trabajo; GitHub la elimina con la máquina temporal.
- El AAB se verifica: 50 JPG distintos, manifiesto y DEX. Si se firma, además se ejecuta `jarsigner -verify`.
- El ID de anuncio de apertura real confirmado es `ca-app-pub-2506564165861733/9553696934`; banner `ca-app-pub-2506564165861733/3900408409`, intersticial `ca-app-pub-2506564165861733/6482514721`.
- El paquete Android sigue siendo `lazosdeluto.gratis`, versión 2.2.0, código 11, objetivo API 36.

## Secretos que debe introducir únicamente el propietario en GitHub

Ruta: `https://github.com/tommymsc/Lazos-de-Luto-LauraApps/settings/secrets/actions` → New repository secret.

1. `LAZOS_UPLOAD_KEYSTORE_BASE64`: contenido del archivo JKS, **codificado en base64**.
2. `LAZOS_UPLOAD_CERT_PEM_BASE64`: contenido del certificado PEM entregado a Google, **codificado en base64**.
3. `LAZOS_UPLOAD_KEYSTORE_PASSWORD`: contraseña de almacén creada al usar keytool.
4. `LAZOS_UPLOAD_KEY_ALIAS`: `upload`.
5. `LAZOS_UPLOAD_KEY_PASSWORD`: contraseña de la clave. En PKCS12 de keytool suele ser la misma que la del almacén.

Archivo JKS **privado**, no subir al repositorio ni enviarlo por chat.

Para introducir base64 sin mostrarlo en la pantalla, usa PowerShell en Windows y pega cada resultado *directamente en el campo secreto de GitHub*, sin copiarlo aquí:

```powershell
$folder = "$env:USERPROFILE\Documents\LauraApps\LazosDeLuto\Firma"
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$folder\lazos-upload.jks")) | Set-Clipboard
# Pega desde el portapapeles en el secreto LAZOS_UPLOAD_KEYSTORE_BASE64, guarda y después:
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$folder\lazos-upload-cert.pem")) | Set-Clipboard
# Pega en LAZOS_UPLOAD_CERT_PEM_BASE64
```

No ejecutes ni registres secretos desde computadores compartidos. Después de introducirlos, limpia el portapapeles (por ejemplo, `Set-Clipboard -Value ""`). El PEM público es inocuo; el JKS no.

**IMPORTANTE:** nunca generes o subas el AAB firmado hasta que Google Play confirme que el nuevo certificado de subida ha sido aprobado y está en uso. El workflow únicamente revisa que el PEM y el JKS concuerden; Google Play es quien debe confirmar que acepta esa clave.

## Comprobaciones externas antes de enviar el AAB
- Google Play → Firma de apps: la solicitud ya NO debe figurar como pendiente; comparar huella SHA-256 del certificado de subida registrado con el PEM local.
- Actualizar ficha para retirar las antiguas afirmaciones de "las mejores 70 imágenes". Declarar contenido real (50 diseños, 48 mensajes).
- Probar consentimiento UMP y anuncios App Open/intersticial/banner en equipo físico; comprobar inicio con y sin Internet.
- Revisar datos de seguridad de AdMob, declaración de anuncios, público objetivo y clasificación en Play Console.
- Política: `https://tommymsc.github.io/lazos-de-luto-privacy.html`.
- Archivo `app-ads.txt`: `https://tommymsc.github.io/app-ads.txt`.
- Verificar HTTP 200 en ambos; el sitio del desarrollador en Play Console debe usar el dominio correspondiente.
- Confirmar estado de comerciante de la cuenta según aviso en Play.
- Comprobar compatibilidad de 16 KB mediante App Bundle Explorer / Play Console.
