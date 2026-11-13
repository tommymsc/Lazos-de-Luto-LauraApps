package gratis.lazosdeluto;

import android.app.*;
import android.os.*;
import android.content.*;
import android.graphics.*;
import android.net.Uri;
import android.provider.MediaStore;
import android.view.*;
import android.widget.*;
import androidx.core.content.FileProvider;
import com.google.android.gms.ads.*;
import com.google.android.gms.ads.interstitial.*;
import com.google.android.ump.*;
import java.io.*;
import java.util.*;

public class MainActivity extends Activity {
 private LinearLayout main,items; private boolean favorites=false; private int filter=0, saves=0; private SharedPreferences prefs; private AdView banner; private InterstitialAd interstitial;
 private final int INK=Color.rgb(31,34,43);
 private final String[] filters={"Todos","Elegantes","Sobrios","Florales","Religiosos","Modernos"};
 private final String[] names={"Rosa de plata","Lirio de luz","Lazo de paz","Jardín de recuerdos","Orquídea violeta","Lirio al atardecer","Luz de esperanza","Paloma de consuelo","Luz de amor","Hasta siempre"};
 @Override public void onCreate(Bundle state){super.onCreate(state);prefs=getSharedPreferences("lazos_favorites",MODE_PRIVATE);show();requestAds();}
 private TextView text(String s,int sp){TextView t=new TextView(this);t.setText(s);t.setTextSize(sp);t.setTextColor(INK);t.setPadding(12,12,12,12);return t;}
 private void show(){
  ScrollView scroll=new ScrollView(this);main=new LinearLayout(this);main.setOrientation(1);main.setPadding(12,14,12,22);main.setBackgroundColor(Color.rgb(249,247,243));scroll.addView(main);setContentView(scroll);
  TextView title=text("Lazos de Luto",27);title.setTypeface(null,1);main.addView(title);
  main.addView(text("10 diseños en 5 categorías · colección en crecimiento",14));
  LinearLayout tabs=new LinearLayout(this);main.addView(tabs);
  Button gallery=new Button(this);gallery.setText("Galería");tabs.addView(gallery,new LinearLayout.LayoutParams(0,-2,1));gallery.setOnClickListener(v->{favorites=false;render();});
  Button fav=new Button(this);fav.setText("♥ Favoritos");tabs.addView(fav,new LinearLayout.LayoutParams(0,-2,1));fav.setOnClickListener(v->{favorites=true;render();});
  Spinner categories=new Spinner(this);categories.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,filters));main.addView(categories);
  categories.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener(){public void onNothingSelected(android.widget.AdapterView<?> a){} public void onItemSelected(android.widget.AdapterView<?> a,View v,int p,long id){filter=p;render();}});
  items=new LinearLayout(this);items.setOrientation(1);main.addView(items);render();
  Button phrase=new Button(this);phrase.setText("Copiar frase de condolencias");main.addView(phrase);phrase.setOnClickListener(v->{String[] lines={"Siempre en nuestros corazones.","Que su recuerdo sea una bendición.","Nuestro cariño en estos momentos difíciles.","Con respeto y afecto, nuestras condolencias."};String s=lines[new Random().nextInt(lines.length)];((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(ClipData.newPlainText("Condolencia",s));Toast.makeText(this,"Frase copiada",Toast.LENGTH_SHORT).show();});
  Button privacy=new Button(this);privacy.setText("Privacidad y preferencias de anuncios");main.addView(privacy);privacy.setOnClickListener(v->UserMessagingPlatform.showPrivacyOptionsForm(this,error->{if(error!=null) new AlertDialog.Builder(this).setMessage("Consulta la política de privacidad en la ficha de Google Play.").setPositiveButton("Aceptar",null).show();}));
 }
 private void render(){if(items==null)return;items.removeAllViews();int shown=0;for(int i=1;i<=10;i++){
  if(filter!=0 && (i-1)/2!=filter-1)continue;
  if(favorites&&!prefs.getBoolean("f"+i,false))continue;
  shown++;final int id=i;
  LinearLayout card=new LinearLayout(this);card.setOrientation(1);card.setPadding(8,12,8,16);items.addView(card);
  ImageView image=new ImageView(this);image.setImageBitmap(design(id,420,420));image.setScaleType(ImageView.ScaleType.FIT_CENTER);card.addView(image,new LinearLayout.LayoutParams(-1,360));
  card.addView(text(names[id-1],16));
  LinearLayout row=new LinearLayout(this);card.addView(row);
  Button f=new Button(this);f.setText(prefs.getBoolean("f"+id,false)?"♥":"♡");row.addView(f,new LinearLayout.LayoutParams(0,-2,1));f.setOnClickListener(v->{boolean b=!prefs.getBoolean("f"+id,false);prefs.edit().putBoolean("f"+id,b).apply();if(favorites)render();else f.setText(b?"♥":"♡");});
  Button save=new Button(this);save.setText("Guardar");row.addView(save,new LinearLayout.LayoutParams(0,-2,1));save.setOnClickListener(v->save(id));
  Button share=new Button(this);share.setText("Compartir");row.addView(share,new LinearLayout.LayoutParams(0,-2,1));share.setOnClickListener(v->share(id,false));
  Button wa=new Button(this);wa.setText("WhatsApp");card.addView(wa);wa.setOnClickListener(v->share(id,true));
 }
 if(shown==0)items.addView(text("No hay favoritos en esta categoría.",16));
 }
 private Bitmap design(int id,int w,int h){
  Bitmap bmp=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888);Canvas c=new Canvas(bmp);Paint p=new Paint(3);
  int variant=(id-1)/10;int[] bg={0xfff4f0e9,0xfff6f2f3,0xffe9edf0,0xfff2f1ec,0xfff0e9e5};
  c.drawColor(bg[variant]);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(3);p.setColor(0xffb6a486);c.drawRoundRect(24,24,w-24,h-24,16,16,p);p.setStyle(Paint.Style.FILL);
  int[] ribbons={0xff24252b,0xff35313b,0xff57616a,0xff5b5651,0xff413a42};
  p.setColor(ribbons[variant]);float cx=w/2f,cy=h*.45f;float shift=(id%10-5)*2.0f;
  Path left=new Path();left.moveTo(cx-5,cy-65);left.cubicTo(cx-110+shift,cy-130,cx-115,cy-5,cx-20,cy+20);left.lineTo(cx-78,cy+126);left.lineTo(cx-16,cy+114);left.lineTo(cx+20,cy+24);left.close();c.drawPath(left,p);
  Path right=new Path();right.moveTo(cx+5,cy-65);right.cubicTo(cx+115-shift,cy-130,cx+115,cy-5,cx+20,cy+20);right.lineTo(cx+78,cy+126);right.lineTo(cx+16,cy+114);right.lineTo(cx-20,cy+24);right.close();c.drawPath(right,p);
  p.setColor(0xffbca987);p.setStrokeWidth(4);p.setStyle(Paint.Style.STROKE);c.drawCircle(cx,cy-34,27+(id%5),p);p.setStyle(Paint.Style.FILL);
  p.setColor(0xff47454a);p.setTextAlign(Paint.Align.CENTER);p.setTypeface(Typeface.create("serif",Typeface.NORMAL));p.setTextSize(22);c.drawText(id%3==0?"En memoria":id%3==1?"Siempre presentes":"Con cariño",cx,h-70,p);p.setTextSize(13);c.drawText("LAZOS DE LUTO",cx,h-43,p);
  return bmp;
 }
 private void save(int id){Uri uri=null;try{Bitmap b=design(id,1080,1080);ContentValues cv=new ContentValues();cv.put(MediaStore.Images.Media.DISPLAY_NAME,"lazo_luto_"+id+".png");cv.put(MediaStore.Images.Media.MIME_TYPE,"image/png");cv.put(MediaStore.Images.Media.RELATIVE_PATH,"Pictures/LazosDeLuto");uri=getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,cv);if(uri==null)throw new IOException("Sin destino");try(OutputStream out=getContentResolver().openOutputStream(uri)){if(out==null||!b.compress(Bitmap.CompressFormat.PNG,100,out))throw new IOException("Error al escribir");}Toast.makeText(this,"Imagen guardada",Toast.LENGTH_SHORT).show();saves++;if(saves%5==0&&interstitial!=null){InterstitialAd ready=interstitial;interstitial=null;ready.setFullScreenContentCallback(new FullScreenContentCallback(){@Override public void onAdDismissedFullScreenContent(){loadInterstitial();}@Override public void onAdFailedToShowFullScreenContent(com.google.android.gms.ads.AdError e){loadInterstitial();}});ready.show(this);}}catch(Exception e){if(uri!=null)getContentResolver().delete(uri,null,null);Toast.makeText(this,"No se pudo guardar",Toast.LENGTH_LONG).show();}}
 private void share(int id,boolean whatsapp){try{File dir=new File(getCacheDir(),"shared");dir.mkdirs();File file=new File(dir,"lazo_"+id+".png");try(OutputStream out=new FileOutputStream(file)){design(id,1080,1080).compress(Bitmap.CompressFormat.PNG,100,out);}Uri uri=FileProvider.getUriForFile(this,"lazosdeluto.gratis.fileprovider",file);Intent send=new Intent(Intent.ACTION_SEND);send.setType("image/png");send.putExtra(Intent.EXTRA_STREAM,uri);send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);if(whatsapp){send.setPackage("com.whatsapp");try{startActivity(send);return;}catch(android.content.ActivityNotFoundException e){send.setPackage(null);}}startActivity(Intent.createChooser(send,"Compartir lazo"));}catch(Exception e){Toast.makeText(this,"No se pudo compartir",Toast.LENGTH_LONG).show();}}
 private void requestAds(){ConsentRequestParameters params=new ConsentRequestParameters.Builder().build();UserMessagingPlatform.getConsentInformation(this).requestConsentInfoUpdate(this,params,()->UserMessagingPlatform.loadAndShowConsentFormIfRequired(this,error->{if(UserMessagingPlatform.getConsentInformation(this).canRequestAds())startAds();}),error->{if(UserMessagingPlatform.getConsentInformation(this).canRequestAds())startAds();});}
 private void startAds(){MobileAds.initialize(this,status->{});if(banner!=null)return;banner=new AdView(this);banner.setAdUnitId(BuildConfig.BANNER_ID);banner.setAdSize(AdSize.BANNER);main.addView(banner);banner.loadAd(new AdRequest.Builder().build());loadInterstitial();}
 private void loadInterstitial(){InterstitialAd.load(this,BuildConfig.INTERSTITIAL_ID,new AdRequest.Builder().build(),new InterstitialAdLoadCallback(){@Override public void onAdLoaded(InterstitialAd ad){interstitial=ad;}@Override public void onAdFailedToLoad(LoadAdError e){interstitial=null;}});}
 @Override public void onDestroy(){if(banner!=null)banner.destroy();super.onDestroy();}
}
