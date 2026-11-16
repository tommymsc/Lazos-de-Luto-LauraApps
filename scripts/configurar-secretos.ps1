# Ejecutar localmente en PowerShell, no en GitHub Actions.
# Requiere GitHub CLI (gh) autenticado. Clave y contraseña nunca se escriben en el repositorio.
# Uso: powershell -ExecutionPolicy Bypass -File .\configurar-secretos.ps1
$ErrorActionPreference = "Stop"
$repo = "tommymsc/Lazos-de-Luto-LauraApps"
$folder = Join-Path $env:USERPROFILE "Documents\LauraApps\LazosDeLuto\Firma"
$keystore = Join-Path $folder "lazos-upload.jks"
$certificate = Join-Path $folder "lazos-upload-cert.pem"

if (!(Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "Falta GitHub CLI. Instálalo con 'winget install --id GitHub.cli -e' y abre PowerShell nuevamente."
}
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) { throw "Primero ejecuta 'gh auth login' e inicia sesión en GitHub." }
if (!(Test-Path $keystore) -or !(Test-Path $certificate)) {
  throw "Faltan lazos-upload.jks o lazos-upload-cert.pem en $folder"
}

Write-Host "Usando el par JKS + PEM que tienes localmente. Se guardarán SOLO en GitHub Actions Secrets." -ForegroundColor Cyan

$secure = Read-Host "Introduce la contraseña local de la clave (no se mostrará)" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
  $password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
  if ([string]::IsNullOrWhiteSpace($password)) { throw "Contraseña vacía" }
  $env:LAZOS_KEYSTORE_CHECK_PASSWORD = $password
  & keytool -list -keystore $keystore -alias upload -storepass:env LAZOS_KEYSTORE_CHECK_PASSWORD 1>$null
  if ($LASTEXITCODE -ne 0) { throw "No se pudo validar el almacén o alias 'upload'. Revisa la contraseña." }

  # Verificar que el PEM registrado en Play corresponde exactamente al par de claves local.
  $temp = Join-Path $env:TEMP ("lazos-cert-" + [guid]::NewGuid().ToString() + ".pem")
  try {
    # En PowerShell 5.1, el aviso normal de keytool en stderr puede activar ErrorActionPreference=Stop.
    # Lanzar keytool como proceso externo evita el falso error sin mostrar la contraseña.
    $arguments = @('-exportcert','-rfc','-keystore',('"' + $keystore + '"'),'-alias','upload','-storepass:env','LAZOS_KEYSTORE_CHECK_PASSWORD','-file',('"' + $temp + '"'))
    $process = Start-Process -FilePath 'keytool.exe' -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
    $exitCode = $process.ExitCode
    if ($exitCode -ne 0) { throw "No se pudo exportar el certificado de verificación." }
    # Comparar los bloques PEM certificados, ignorando saltos de línea.
    $aText = (Get-Content $temp -Raw) -replace '\s', ''
    $bText = (Get-Content $certificate -Raw) -replace '\s', ''
    if ($aText -ne $bText) { throw "El PEM y la clave JKS no corresponden. No se instalarán secretos." }
  } finally { Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue }

  function Set-SecretFromString([string]$name,[string]$value) {
    $value | gh secret set $name --repo $repo
    if ($LASTEXITCODE -ne 0) { throw "Error cargando secreto $name" }
    Write-Host "Secreto cargado: $name" -ForegroundColor Green
  }
  Set-SecretFromString "LAZOS_UPLOAD_KEYSTORE_BASE64" ([Convert]::ToBase64String([IO.File]::ReadAllBytes($keystore)))
  Set-SecretFromString "LAZOS_UPLOAD_CERT_PEM_BASE64" ([Convert]::ToBase64String([IO.File]::ReadAllBytes($certificate)))
  Set-SecretFromString "LAZOS_UPLOAD_KEYSTORE_PASSWORD" $password
  Set-SecretFromString "LAZOS_UPLOAD_KEY_ALIAS" "upload"
  Set-SecretFromString "LAZOS_UPLOAD_KEY_PASSWORD" $password
  Write-Host "Los cinco secretos están configurados. No ejecutes la firma hasta que Google Play apruebe el certificado." -ForegroundColor Green
} finally {
  Remove-Item Env:LAZOS_KEYSTORE_CHECK_PASSWORD -ErrorAction SilentlyContinue
  if ($ptr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  $password = $null
  $secure = $null
}
