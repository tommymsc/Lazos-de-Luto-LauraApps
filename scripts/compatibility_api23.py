#!/usr/bin/env python3
"""Add Android 7-9 gallery support; preserve Android 10+ saves."""
from pathlib import Path
build=Path("app/build.gradle")
s=build.read_text()
assert "minSdk 29" in s and "versionCode 11" in s
s=s.replace("minSdk 29","minSdk 24").replace("versionCode 11","versionCode 13").replace("versionName '2.2.0'","versionName '2.2.2'")
build.write_text(s)
manifest=Path("app/src/main/AndroidManifest.xml")
m=manifest.read_text()
assert "android.permission.WRITE_EXTERNAL_STORAGE" not in m
m=m.replace('<uses-permission android:name="android.permission.INTERNET"/>','<uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28"/>')
manifest.write_text(m)
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
j=p.read_text()
assert "private void save(int i){" in j
j=j.replace(" private void save(int i){",''' private static final int LEGACY_STORAGE_PERMISSION=6109;
 private int pendingLegacySave=0;
 @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] results){
  super.onRequestPermissionsResult(requestCode,permissions,results);
  if(requestCode==LEGACY_STORAGE_PERMISSION){
   int image=pendingLegacySave;pendingLegacySave=0;
   if(image>0 && results.length>0 && results[0]==android.content.pm.PackageManager.PERMISSION_GRANTED)save(image);
   else Toast.makeText(this,"Se requiere permiso para guardar en Fotos",Toast.LENGTH_LONG).show();
  }
 }
 private void saveLegacy(int id){
  File output=null;
  try{
   File directory=new File(android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_PICTURES),"LazosDeLuto");
   if(!directory.isDirectory() && !directory.mkdirs())throw new IOException("No se pudo crear carpeta");
   output=new File(directory,"lazo_luto_"+id+"_"+System.currentTimeMillis()+".jpg");
   try(InputStream in=getAssets().open(path(id));OutputStream out=new FileOutputStream(output)){
    byte[] buffer=new byte[8192];int n;
    while((n=in.read(buffer))!=-1)out.write(buffer,0,n);
   }
   android.media.MediaScannerConnection.scanFile(this,new String[]{output.getAbsolutePath()},new String[]{"image/jpeg"},null);
   Toast.makeText(this,"Imagen guardada en Fotos",Toast.LENGTH_SHORT).show();
  }catch(Exception error){
   if(output!=null && output.exists())output.delete();
   Toast.makeText(this,"No se pudo guardar la imagen",Toast.LENGTH_LONG).show();
  }
 }
 private void save(int i){
  if(Build.VERSION.SDK_INT<29){
   if(checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){
    pendingLegacySave=i;
    requestPermissions(new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE},LEGACY_STORAGE_PERMISSION);
    return;
   }
   saveLegacy(i);return;
  }''',1)
p.write_text(j)
print("Compat API24/versionCode13 applied; API24-28 save uses runtime permission and media scan")
