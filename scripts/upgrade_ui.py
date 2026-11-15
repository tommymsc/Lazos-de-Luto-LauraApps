#!/usr/bin/env python3
"""Modernize the unpacked complete application; preserve assets and native sharing."""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
s=s.replace('showGallery();initAds();','showHome();initAds();',1)
s=s.replace('private static final int PAGE_SIZE=8;', 'private static final int PAGE_SIZE=10;')
start=s.index(' private void showGallery(){')
end=s.index(' private void showPrivacy(){',start)
new_home=r'''
 private int dp(int v){return (int)(v*getResources().getDisplayMetrics().density+0.5f);}
 private GradientDrawable rounded(int color,int rad){
  GradientDrawable g=new GradientDrawable();g.setColor(color);g.setCornerRadius(dp(rad));return g;
 }
 private TextView tile(String s,int size,int color,int background){
  TextView t=label(s,size);t.setTextColor(color);t.setTypeface(null,1);
  t.setGravity(Gravity.CENTER_VERTICAL);t.setPadding(dp(16),dp(12),dp(12),dp(12));
  t.setBackground(rounded(background,16));return t;
 }
 private void showHome(){
  ScrollView sc=new ScrollView(this);root=new LinearLayout(this);root.setOrientation(1);
  root.setPadding(dp(15),dp(16),dp(15),dp(16));root.setBackgroundColor(0xfffaf8f8);
  sc.addView(root);setContentView(sc);
  TextView title=label("Lazos de Luto",27);title.setTypeface(null,1);title.setTextColor(0xff493454);root.addView(title);
  root.addView(label("50 diseños para honrar y recordar",14));
  TextView messages=tile("💜  Mensajes de consuelo     ›",18,0xff58336d,0xffefe5f1);
  LinearLayout.LayoutParams mp=new LinearLayout.LayoutParams(-1,dp(70));mp.setMargins(0,dp(9),0,dp(14));root.addView(messages,mp);
  messages.setOnClickListener(v->showMessages());
  root.addView(label("Elige una categoría",20));
  String[] cats={"✦ Elegantes","◈ Sobrios","✿ Florales","✝ Religiosos","♡ Modernos"};
  String[] desc={"Distinción y cariño","Serenidad y respeto","Flores para recordar","Fe y esperanza","Diseños contemporáneos"};
  for(int row=0;row<3;row++){
   LinearLayout horizontal=new LinearLayout(this);root.addView(horizontal);
   for(int col=0;col<2;col++){
    int idx=row*2+col;if(idx>=5)continue;
    LinearLayout cell=new LinearLayout(this);cell.setOrientation(1);cell.setPadding(dp(13),dp(13),dp(8),dp(8));
    cell.setBackground(rounded(0xffffffff,17));
    LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(0,dp(98),1);
    cp.setMargins(0,dp(4),dp(col==0?8:0),dp(5));horizontal.addView(cell,cp);
    TextView main=label(cats[idx],17);main.setTypeface(null,1);main.setTextColor(0xff60466e);cell.addView(main);
    TextView sub=label("10 lazos · "+desc[idx],11);cell.addView(sub);
    cell.setOnClickListener(v->{style=idx+1;onlyFav=false;onlyPremium=false;page=0;showGallery();});
   }
   if(row==2){
    TextView top=tile("✦ Destacados premium  ›",14,0xff60466e,0xffeee7ee);
    LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(0,dp(98),1);
    cp.setMargins(0,dp(4),0,dp(5));horizontal.addView(top,cp);
    top.setOnClickListener(v->{style=0;onlyFav=false;onlyPremium=true;page=0;showGallery();});
   }
  }
  TextView all=tile("Ver todos los lazos  ›",17,Color.WHITE,0xff694f77);
  LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-1,dp(57));ap.setMargins(0,dp(7),0,dp(7));root.addView(all,ap);
  all.setOnClickListener(v->{style=0;onlyFav=false;onlyPremium=false;page=0;showGallery();});
  TextView fav=tile("♥  Mis favoritos  ›",16,0xff60466e,0xffefe6ee);
  root.addView(fav,new LinearLayout.LayoutParams(-1,dp(54)));
  fav.setOnClickListener(v->{style=0;onlyFav=true;onlyPremium=false;page=0;showGallery();});
  TextView privacy=label("Privacidad y preferencias de anuncios",13);privacy.setGravity(Gravity.CENTER);
  root.addView(privacy);privacy.setOnClickListener(v->showPrivacy());
  attachAd();
 }
 private void attachAd(){
  if(ad!=null){if(ad.getParent() instanceof ViewGroup)((ViewGroup)ad.getParent()).removeView(ad);root.addView(ad);}
 }
 private void showGallery(){
  ScrollView scroll=new ScrollView(this);root=new LinearLayout(this);root.setOrientation(1);
  root.setPadding(dp(13),dp(13),dp(13),dp(18));root.setBackgroundColor(0xfffaf8f8);scroll.addView(root);setContentView(scroll);
  TextView home=tile("‹  Volver a las categorías",15,0xff60466e,0xffefe6ee);root.addView(home);
  home.setOnClickListener(v->showHome());
  String title=onlyFav?"Mis favoritos":onlyPremium?"Destacados premium":style==0?"Todos los lazos":groups[style];
  TextView heading=label(title,22);heading.setTypeface(null,1);root.addView(heading);
  TextView help=label("Toca un diseño para guardarlo o compartirlo",13);root.addView(help);
  LinearLayout tabs=new LinearLayout(this);root.addView(tabs);
  Button all=new Button(this);all.setText("Todos");tabs.addView(all,new LinearLayout.LayoutParams(0,-2,1));
  all.setOnClickListener(v->{style=0;onlyFav=false;onlyPremium=false;page=0;showGallery();});
  Button fav=new Button(this);fav.setText("♥ Favoritos");tabs.addView(fav,new LinearLayout.LayoutParams(0,-2,1));
  fav.setOnClickListener(v->{style=0;onlyFav=true;onlyPremium=false;page=0;showGallery();});
  grid=new LinearLayout(this);grid.setOrientation(1);root.addView(grid);
  render();attachAd();
 }
 '''
s=s[:start]+new_home+s[end:]
start=s.index(' private void showMessages(){')
end=s.index(' private void render(){',start)
messages=r'''
 private void showMessages(){
  String[][] cats={
  {"Condolencias","Mi más sentido pésame. Te acompaño de corazón.","Recibe un abrazo sincero en este momento difícil.","Que el cariño de tu familia te brinde consuelo.","Comparto tu tristeza con respeto y afecto.","Te acompaño en el dolor y en el recuerdo.","Mis pensamientos están contigo y tu familia.","No hay palabras suficientes, pero sí todo mi cariño.","Que encuentres serenidad rodeado de quienes te aman.","Aquí estoy para acompañarte cuando lo necesites.","Con profundo respeto, recibe nuestras condolencias.","Que la paz llegue poco a poco a tu corazón.","Mi solidaridad y afecto en este tiempo de duelo."},
  {"Recuerdos","Su amor permanece vivo en cada recuerdo compartido.","Hay huellas que el tiempo jamás podrá borrar.","Su recuerdo nos acompañará cada día.","Quedan las sonrisas, las enseñanzas y el amor.","Una vida querida nunca se olvida.","El cariño verdadero permanece más allá de la despedida.","Recordar también es una manera de abrazar.","Siempre habrá un lugar para su memoria en nuestros corazones.","Los momentos compartidos seguirán dando luz.","La gratitud por haberle conocido perdura.","Su ejemplo seguirá inspirándonos.","El amor deja recuerdos que nos sostienen."},
  {"Fortaleza","Un día a la vez, con paciencia y amor.","Permítete sentir y sanar a tu propio ritmo.","No tienes que recorrer este camino en soledad.","Que cada día traiga un instante de calma.","Hay fuerza también en pedir apoyo.","Que la ternura de quienes te rodean te acompañe.","Tu dolor merece tiempo y comprensión.","Respira, descansa y cuídate con cariño.","Que los buenos recuerdos sean un refugio.","La esperanza puede volver en pequeños momentos.","Honrar su memoria también es seguir adelante.","Te deseo paz para atravesar esta ausencia."},
  {"Despedidas","Hasta siempre, con amor y gratitud.","Gracias por todo lo que compartimos.","Tu recuerdo seguirá iluminando nuestros días.","Descansa en paz; vivirás en nuestra memoria.","Nos despedimos con cariño y profundo respeto.","Lo vivido contigo permanece para siempre.","Tu historia seguirá en quienes te amamos.","Siempre presente, aunque ya no estés aquí.","Tu partida deja silencio y un amor inmenso.","Que tu descanso sea sereno.","Gracias por cada abrazo y cada enseñanza.","Nos queda tu luz, tu legado y tu recuerdo."}
  };
  ScrollView scroll=new ScrollView(this);root=new LinearLayout(this);root.setOrientation(1);root.setPadding(dp(14),dp(15),dp(14),dp(15));
  root.setBackgroundColor(0xfffaf8f8);scroll.addView(root);setContentView(scroll);
  TextView back=tile("‹  Inicio",15,0xff60466e,0xffefe6ee);root.addView(back);back.setOnClickListener(v->showHome());
  TextView heading=label("💜 Mensajes de consuelo",23);heading.setTypeface(null,1);root.addView(heading);
  root.addView(label("48 mensajes originales para copiar y compartir.",14));
  for(int c=0;c<cats.length;c++){
   int idx=c;TextView tile=tile(cats[c][0]+"   ·   12 mensajes  ›",17,0xff60466e,0xfff0e8f0);
   LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(66));lp.setMargins(0,dp(6),0,dp(6));root.addView(tile,lp);
   tile.setOnClickListener(v->showMessageCategory(cats[idx]));
  }
  attachAd();
 }
 private void showMessageCategory(String[] cat){
  ScrollView scroll=new ScrollView(this);root=new LinearLayout(this);root.setOrientation(1);root.setPadding(dp(14),dp(14),dp(14),dp(15));
  root.setBackgroundColor(0xfffaf8f8);scroll.addView(root);setContentView(scroll);
  TextView back=tile("‹  Mensajes de consuelo",15,0xff60466e,0xffeee6ef);root.addView(back);back.setOnClickListener(v->showMessages());
  TextView heading=label(cat[0],23);heading.setTypeface(null,1);root.addView(heading);
  for(int j=1;j<cat.length;j++){
   String quote=cat[j];LinearLayout card=new LinearLayout(this);card.setOrientation(1);card.setPadding(dp(12),dp(12),dp(12),dp(10));
   card.setBackground(rounded(0xffffffff,14));
   LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,-2);cp.setMargins(0,dp(6),0,dp(6));root.addView(card,cp);
   TextView message=label(quote,16);card.addView(message);
   LinearLayout actions=new LinearLayout(this);card.addView(actions);
   Button copy=new Button(this);copy.setText("Copiar");actions.addView(copy,new LinearLayout.LayoutParams(0,-2,1));
   copy.setOnClickListener(v->{((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(ClipData.newPlainText("Mensaje",quote));Toast.makeText(this,"Mensaje copiado",Toast.LENGTH_SHORT).show();});
   Button share=new Button(this);share.setText("Compartir");actions.addView(share,new LinearLayout.LayoutParams(0,-2,1));
   share.setOnClickListener(v->{Intent it=new Intent(Intent.ACTION_SEND);it.setType("text/plain");it.putExtra(Intent.EXTRA_TEXT,quote);startActivity(Intent.createChooser(it,"Compartir mensaje"));});
  }
  attachAd();
 }
 '''
s=s[:start]+messages+s[end:]
start=s.index(' private void render(){')
end=s.index(' private String path(int i)',start)
gallery=r'''
 private void render(){
  if(grid==null)return;grid.removeAllViews();
  ArrayList<Integer> filtered=new ArrayList<>();
  for(int id=1;id<=50;id++){
   if(style>0 && ((id-1)%10)/2 != style-1)continue;
   if(onlyPremium && !(id>=11 && id<=20 || id>=31 && id<=40))continue;
   if(onlyFav && !prefs.getBoolean("f"+id,false))continue;
   filtered.add(id);
  }
  if(filtered.isEmpty()){grid.addView(label("Todavía no tienes favoritos. Abre una categoría y guarda los que te gusten.",16));return;}
  int pages=(filtered.size()+PAGE_SIZE-1)/PAGE_SIZE;page=Math.min(Math.max(page,0),pages-1);
  grid.addView(label("Página "+(page+1)+" de "+pages+" · "+filtered.size()+" diseños",13));
  for(int base=page*PAGE_SIZE;base<Math.min(filtered.size(),(page+1)*PAGE_SIZE);base+=2){
   LinearLayout row=new LinearLayout(this);row.setBaselineAligned(false);grid.addView(row);
   for(int col=0;col<2;col++){
    int x=base+col;if(x>=filtered.size() || x>=(page+1)*PAGE_SIZE)break;int id=filtered.get(x);
    LinearLayout card=new LinearLayout(this);card.setOrientation(1);card.setPadding(dp(6),dp(7),dp(6),dp(10));
    card.setBackground(rounded(0xffffffff,15));
    LinearLayout.LayoutParams cardp=new LinearLayout.LayoutParams(0,dp(210),1);
    cardp.setMargins(0,dp(4),dp(col==0?8:0),dp(5));row.addView(card,cardp);
    ImageView img=new ImageView(this);img.setScaleType(ImageView.ScaleType.CENTER_CROP);
    try(InputStream in=getAssets().open(path(id))){BitmapFactory.Options op=new BitmapFactory.Options();op.inSampleSize=3;
     img.setImageBitmap(BitmapFactory.decodeStream(in,null,op));}catch(Exception ignored){}
    img.setContentDescription(names[id-1]);card.addView(img,new LinearLayout.LayoutParams(-1,0,1));
    TextView name=label(names[id-1],13);name.setTypeface(null,1);name.setSingleLine(true);name.setEllipsize(android.text.TextUtils.TruncateAt.END);card.addView(name);
    TextView more=label("Ver y compartir ›",12);more.setTextColor(0xff674876);card.addView(more);
    card.setOnClickListener(v->showDesign(id));
   }
  }
  if(pages>1){
   LinearLayout nav=new LinearLayout(this);grid.addView(nav);
   Button prev=new Button(this);prev.setText("‹ Anterior");prev.setEnabled(page>0);nav.addView(prev,new LinearLayout.LayoutParams(0,-2,1));
   prev.setOnClickListener(v->{page--;render();});
   Button next=new Button(this);next.setText("Siguiente ›");next.setEnabled(page<pages-1);nav.addView(next,new LinearLayout.LayoutParams(0,-2,1));
   next.setOnClickListener(v->{page++;render();});
  }
 }
 private void showDesign(int id){
  LinearLayout holder=new LinearLayout(this);holder.setOrientation(1);holder.setPadding(dp(10),dp(8),dp(10),dp(8));
  ImageView preview=new ImageView(this);preview.setScaleType(ImageView.ScaleType.FIT_CENTER);
  try(InputStream in=getAssets().open(path(id))){preview.setImageBitmap(BitmapFactory.decodeStream(in));}catch(Exception ignored){}
  holder.addView(preview,new LinearLayout.LayoutParams(-1,dp(300)));
  TextView title=label(names[id-1],18);title.setGravity(Gravity.CENTER);title.setTypeface(null,1);holder.addView(title);
  AlertDialog dialog=new AlertDialog.Builder(this).setView(holder).setNegativeButton("Cerrar",(d,w)->{}).create();
  Button save=new Button(this);save.setText("↓ Guardar imagen");holder.addView(save);save.setOnClickListener(v->save(id));
  Button whats=new Button(this);whats.setText("Compartir por WhatsApp");holder.addView(whats);whats.setOnClickListener(v->share(id,true));
  Button share=new Button(this);share.setText("Compartir en otra aplicación");holder.addView(share);share.setOnClickListener(v->share(id,false));
  Button fav=new Button(this);fav.setText(prefs.getBoolean("f"+id,false)?"♥ Quitar de favoritos":"♡ Añadir a favoritos");holder.addView(fav);
  fav.setOnClickListener(v->{boolean val=!prefs.getBoolean("f"+id,false);prefs.edit().putBoolean("f"+id,val).apply();
   fav.setText(val?"♥ Quitar de favoritos":"♡ Añadir a favoritos");if(onlyFav)render();});
  dialog.show();
 }
 '''
s=s[:start]+gallery+s[end:]
s=s.replace('root.addView(ad);ad.loadAd','root.addView(ad);ad.loadAd')
p.write_text(s,encoding="utf-8")
assert 'showHome();initAds();' in s and '48 mensajes originales' in s and 'private void showDesign' in s
print("Patched UI",len(s),"chars")

# A new version code distinguishes the redesigned application from the prior test.
gradle=Path('app/build.gradle')
gradle.write_text(gradle.read_text().replace('versionCode 9','versionCode 10').replace("versionName '2.0.0'","versionName '2.1.0'"),encoding='utf-8')
