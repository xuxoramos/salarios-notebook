"""Generate a self-contained HTML rehearsal form from the survey inventory CSV.

Reads salarios_question_inventory_2026.csv and writes survey-rehearsal.html:
a single file (no build step, no network) that renders the full survey with
skip logic, measures response times (total + per-section, CSV export), and
includes a rewards-plan tab. Re-run whenever the CSV changes.
"""
import csv, json, os, datetime

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "salarios_question_inventory_2026.csv")
OUT = os.path.join(HERE, "survey-rehearsal.html")

SEC, BLK, ORD, FID, QES, QEN, TYP, OPT, STA, SKP, GOA, RSC, NOT = range(13)

# primary_role option list is needed to expand secondary_role and gate tech questions
PRIMARY_ROLE_OPTS = None

def parse_options(row):
    fid, typ, opt = row[FID], row[TYP].strip(), row[OPT].strip()
    if fid == "secondary_role":
        return (PRIMARY_ROLE_OPTS or []) + ["No tengo rol secundario"]
    if fid == "work_arrangement":  # option contains an internal ' / '
        return ["Totalmente remoto", "Híbrido (1–3 días en oficina por semana)",
                "Totalmente presencial", "Nómada / independiente de ubicación"]
    if typ in ("Numeric", "Free text") or not opt or opt == "(local currency)":
        return []
    return [o.strip() for o in opt.split(" / ") if o.strip()]

def skip_descriptor(row):
    s = row[SKP].strip()
    if not s:
        return None
    if "primary_role is technical" in s:
        return {"type": "technical"}
    if "has_certs" in s:
        return {"type": "eq", "field": "has_certs", "value": "Sí"}
    if "ai_role_status" in s:
        return {"type": "ai_spec"}
    if "employer_hq" in s:
        return {"type": "cross_border"}
    if "gender = mujer" in s:
        return {"type": "eq", "field": "gender", "value": "mujer"}
    if "no binario" in s:
        return {"type": "eq", "field": "gender", "value": "nb"}
    return None

rows = list(csv.reader(open(SRC, newline="", encoding="utf-8")))[1:]
defined = [r for r in rows if r[ORD] != "\u2014"]
PRIMARY_ROLE_OPTS = parse_options(next(r for r in defined if r[FID] == "primary_role"))

questions = []
for r in defined:
    questions.append({
        "order": int(r[ORD]),
        "id": r[FID],
        "section": r[SEC],
        "block": r[BLK],
        "es": r[QES],
        "en": r[QEN],
        "type": r[TYP].strip(),
        "options": parse_options(r),
        "skip": skip_descriptor(r),
    })

DATA = json.dumps(questions, ensure_ascii=False)
COUNT = str(len(questions))
GENERATED = datetime.date.today().isoformat()

TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Encuesta de Salarios 2026 — Ensayo</title>
<style>
  :root { --bg:#0f172a; --card:#ffffff; --ink:#1e293b; --muted:#64748b;
          --accent:#2563eb; --accent2:#16a34a; --line:#e2e8f0; --warn:#b45309; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
         color:var(--ink); background:#f1f5f9; line-height:1.5; }
  header { background:var(--bg); color:#fff; padding:16px 20px; position:sticky; top:0; z-index:10;
           display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
  header h1 { font-size:18px; margin:0; font-weight:700; }
  header .sub { color:#94a3b8; font-size:13px; }
  .spacer { flex:1; }
  .tabs { display:flex; gap:6px; }
  .tab { background:#1e293b; color:#cbd5e1; border:0; padding:8px 14px; border-radius:8px;
         cursor:pointer; font-size:14px; }
  .tab.active { background:var(--accent); color:#fff; }
  .timer { font-variant-numeric:tabular-nums; background:#1e293b; padding:8px 12px; border-radius:8px;
           font-size:15px; font-weight:700; }
  .langtoggle { background:#1e293b; color:#cbd5e1; border:0; padding:8px 12px; border-radius:8px; cursor:pointer; }
  main { max-width:820px; margin:0 auto; padding:20px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px; margin-bottom:16px; }
  .progresswrap { position:sticky; top:64px; z-index:9; background:#f1f5f9; padding:8px 0; }
  .bar { height:8px; background:var(--line); border-radius:99px; overflow:hidden; }
  .bar > i { display:block; height:100%; width:0; background:var(--accent); transition:width .25s; }
  .progresstxt { font-size:12px; color:var(--muted); margin-top:4px; }
  fieldset { border:1px solid var(--line); border-radius:12px; margin:0 0 16px; padding:14px 18px; }
  legend { font-weight:700; color:var(--accent); padding:0 6px; font-size:15px; }
  .blocklabel { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin:14px 0 6px; }
  .q { padding:12px 0; border-top:1px dashed var(--line); }
  .q:first-of-type { border-top:0; }
  .q label.qlabel { display:block; font-weight:600; margin-bottom:8px; }
  .q .fid { color:var(--muted); font-weight:400; font-size:12px; }
  .opts { display:flex; flex-direction:column; gap:6px; }
  .opts.inline { flex-direction:row; flex-wrap:wrap; gap:10px; }
  .opt { display:flex; align-items:center; gap:8px; font-weight:400; }
  input[type=number], textarea, select { width:100%; max-width:420px; padding:8px 10px;
        border:1px solid #cbd5e1; border-radius:8px; font:inherit; }
  textarea { min-height:64px; }
  .badge { display:inline-block; font-size:11px; padding:2px 8px; border-radius:99px;
           background:#fef3c7; color:var(--warn); margin-left:6px; }
  button.primary { background:var(--accent); color:#fff; border:0; padding:12px 22px; border-radius:10px;
                   font-size:16px; font-weight:700; cursor:pointer; }
  button.ghost { background:#fff; color:var(--ink); border:1px solid #cbd5e1; padding:10px 16px;
                 border-radius:10px; cursor:pointer; }
  .row { display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
  .hidden { display:none !important; }
  table { border-collapse:collapse; width:100%; font-size:14px; }
  th, td { text-align:left; padding:6px 10px; border-bottom:1px solid var(--line); }
  th { color:var(--muted); font-weight:600; }
  .big { font-size:34px; font-weight:800; color:var(--accent); }
  .kpi { display:flex; gap:20px; flex-wrap:wrap; margin:8px 0 16px; }
  .kpi > div { background:#f8fafc; border:1px solid var(--line); border-radius:10px; padding:12px 16px; min-width:130px; }
  .kpi small { color:var(--muted); display:block; }
  .muted { color:var(--muted); }
  h2 { font-size:20px; margin:18px 0 8px; }
  h3 { font-size:16px; margin:16px 0 6px; }
  ul { margin:6px 0 6px 18px; } li { margin:4px 0; }
  code { background:#f1f5f9; padding:1px 5px; border-radius:5px; font-size:.92em; }
  .tierbox { border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin:8px 0; }
</style>
</head>
<body>
<header>
  <div><h1>Encuesta de Salarios 2026 <span class="sub">· ensayo interno</span></h1></div>
  <div class="spacer"></div>
  <div class="timer" id="timer">00:00</div>
  <button class="langtoggle" id="langBtn">EN</button>
  <div class="tabs">
    <button class="tab active" data-view="survey">Encuesta</button>
    <button class="tab" data-view="rewards">Plan de recompensas</button>
  </div>
</header>

<main>
  <!-- SURVEY VIEW -->
  <div id="view-survey">
    <div id="startScreen" class="card">
      <h2>Ensayo de la encuesta</h2>
      <p class="muted">Este formulario reproduce la encuesta completa (__COUNT__ ítems, con lógica de salto)
      para que el equipo de comunicación la conteste, cronometre el tiempo de respuesta y calibre el plan
      de recompensas. Los tiempos se miden en tu navegador; nada se envía a ningún servidor.</p>
      <div class="row" style="margin:14px 0;">
        <label for="pid" style="font-weight:600;">Identificador de participante (opcional)</label>
        <input type="text" id="pid" placeholder="p. ej. comms-ana" style="max-width:220px;">
      </div>
      <button class="primary" id="startBtn">Comenzar y arrancar cronómetro</button>
    </div>

    <div id="formScreen" class="hidden">
      <div class="progresswrap">
        <div class="bar"><i id="barfill"></i></div>
        <div class="progresstxt" id="progresstxt">0 de 0 preguntas visibles respondidas</div>
      </div>
      <form id="surveyForm"></form>
      <div class="card row">
        <button class="primary" id="submitBtn">Terminar y ver tiempos</button>
        <button class="ghost" id="resetBtn">Reiniciar</button>
        <span class="muted">Es un ensayo: puedes terminar aunque falten respuestas.</span>
      </div>
    </div>

    <div id="resultScreen" class="hidden">
      <div class="card">
        <h2>Resultados del ensayo</h2>
        <div class="kpi">
          <div><span class="big" id="rTotal">--</span><small>tiempo total</small></div>
          <div><span class="big" id="rAnswered">--</span><small>respondidas / visibles</small></div>
          <div><span class="big" id="rAvg">--</span><small>seg. promedio por respuesta</small></div>
        </div>
        <h3>Tiempo por sección</h3>
        <table id="sectionTable"><thead><tr><th>Sección</th><th>Respondidas</th><th>Tiempo (s)</th></tr></thead><tbody></tbody></table>
        <div class="row" style="margin-top:16px;">
          <button class="ghost" id="dlCsv">Descargar tiempos (CSV)</button>
          <button class="ghost" id="dlJson">Descargar respuestas (JSON)</button>
          <button class="primary" id="againBtn">Otro ensayo</button>
        </div>
        <p class="muted" style="margin-top:12px;">Sugerencia: corran varias personas y comparen la mediana.
        Usen el tiempo mediano para fijar la expectativa de duración y el umbral de "respuesta apresurada"
        (ver plan de recompensas).</p>
      </div>
    </div>
  </div>

  <!-- REWARDS VIEW -->
  <div id="view-rewards" class="hidden">
    <div class="card">
      <h2>Plan de recompensas para respondientes</h2>
      <p class="muted">Objetivo: subir tasa de respuesta y completitud, reducir abandono y mejorar la
      representación de grupos subrepresentados (mujeres, género alternativo, ciudades fuera de CDMX,
      países LatAm nuevos), <b>sin</b> premiar la rapidez ni sesgar la muestra.</p>

      <h3>Principios</h3>
      <ul>
        <li><b>Premiar completar, no responder rápido.</b> Incentivar velocidad genera respuestas basura.
        La recompensa se ata a completar el core con calidad mínima.</li>
        <li><b>Mezcla garantizado + sorteo.</b> Un beneficio pequeño garantizado para todos + rifas por lo
        de mayor valor mantiene el costo por respuesta bajo.</li>
        <li><b>Anonimato protegido.</b> El flujo de contacto (para el sorteo) va separado del flujo de datos,
        para no ligar identidad con respuestas.</li>
        <li><b>Impulsar a los segmentos prioritarios</b> con rifas dedicadas, no bajando el estándar.</li>
      </ul>

      <h3>Mecánica escalonada</h3>
      <div class="tierbox"><b>Nivel 0 — Garantizado (todos los que completan el core)</b>
        <ul><li>Reporte anticipado + acceso al tablero interactivo de resultados</li>
        <li>Insignia digital "Contribuí a la Radiografía Tech 2026" (para LinkedIn)</li></ul></div>
      <div class="tierbox"><b>Nivel 1 — Sorteo base (completó el core)</b>
        <ul><li>Giftcards (Amazon / Mercado Libre) de monto medio</li>
        <li>Meses de suscripción a formación (Platzi / Udemy / cursos)</li></ul></div>
      <div class="tierbox"><b>Nivel 2 — Sorteo ampliado (completó también bloques opcionales)</b>
        <ul><li>Hardware (teclado mecánico, monitor, audífonos)</li>
        <li>1–2 premios mayores (p. ej. laptop) al cierre</li></ul></div>
      <div class="tierbox"><b>Nivel 3 — Referidos y segmentos prioritarios</b>
        <ul><li>Entradas extra al sorteo por invitar (con tope), enfocado a mujeres, género alternativo,
        ciudades no-CDMX y países LatAm nuevos</li>
        <li>Rifas dedicadas por segmento para elevar su representación (atiende la nota de tamaño de muestra
        del bloque de género)</li></ul></div>

      <h3>Anti-gaming (usar los tiempos de este ensayo)</h3>
      <ul>
        <li>Definir un <b>umbral de tiempo mínimo</b> a partir de la mediana medida aquí (p. ej. descartar
        del sorteo envíos por debajo de ~40% del tiempo mediano).</li>
        <li>Exigir completitud mínima del core; deduplicar por hash de correo / una entrada por persona.</li>
        <li>Detectar patrones (misma respuesta en todo, straight-lining) antes de asignar premios.</li>
      </ul>

      <h3>Presupuesto y medición</h3>
      <ul>
        <li>Fijar un <b>costo objetivo por respuesta válida</b> y dimensionar el sorteo según la meta
        (5,000 MX / 3,000 por país si hay expansión LatAm).</li>
        <li>KPIs: tasa de completitud, tiempo mediano, % por segmento prioritario, costo por respuesta válida,
        tasa de abandono por sección.</li>
        <li>Este ensayo entrega el <b>tiempo mediano esperado</b> y el <b>tiempo por sección</b>: úsenlos para
        redactar la promesa ("te toma ~X min") y para ubicar dónde la gente se cansa.</li>
      </ul>

      <h3>Legal / privacidad</h3>
      <ul>
        <li>Publicar bases del sorteo; separar el registro de contacto del cuestionario.</li>
        <li>Cumplir LFPDPPP: aviso de privacidad, consentimiento y no vincular identidad con respuestas
        en reportes públicos.</li>
      </ul>
    </div>
  </div>
</main>

<script>
const QUESTIONS = __DATA__;
const TECH_ROLES = ["Software Engineer (Backend/Frontend/Fullstack)","Mobile Engineer","Data Engineer",
  "Data Scientist-ML","Data Analyst","AI-ML Engineer","DevOps-SRE-Infra","Security-InfoSec","Architecture","QA-Testing"];
const COUNTRY_REGION = {"México":"México","Estados Unidos":"Estados Unidos","Colombia":"América Latina (otro)",
  "Argentina":"América Latina (otro)","Brasil":"América Latina (otro)","Otro (especificar)":"Otro"};

let lang = "es";
let startTime = null, tick = null;
const answers = {};        // id -> value | array
const firstAnswerAt = {};  // id -> ms offset from start

function fmt(ms){ const s=Math.floor(ms/1000); const m=Math.floor(s/60);
  return String(m).padStart(2,"0")+":"+String(s%60).padStart(2,"0"); }

/* ---------- rendering ---------- */
function buildForm(){
  const form = document.getElementById("surveyForm");
  form.innerHTML = "";
  let curSection=null, curBlock=null, fs=null;
  for(const q of QUESTIONS){
    if(q.section !== curSection){
      curSection = q.section; curBlock=null;
      fs = document.createElement("fieldset");
      const lg = document.createElement("legend"); lg.textContent = q.section; fs.appendChild(lg);
      form.appendChild(fs);
    }
    if(q.block !== curBlock){
      curBlock = q.block;
      const bl = document.createElement("div"); bl.className="blocklabel"; bl.textContent=q.block; fs.appendChild(bl);
    }
    fs.appendChild(renderQ(q));
  }
  applySkips(); updateProgress();
}

function renderQ(q){
  const wrap = document.createElement("div");
  wrap.className="q"; wrap.dataset.qid=q.id;
  const lab = document.createElement("label"); lab.className="qlabel";
  lab.innerHTML = `<span class="qtext">${lang==="es"?q.es:(q.en||q.es)}</span>
                   <span class="fid">· ${q.id}${q.skip?' <span class="badge">salto</span>':''}</span>`;
  wrap.appendChild(lab);

  const t = q.type;
  if(t==="Numeric"){
    const i=document.createElement("input"); i.type="number"; i.dataset.qid=q.id;
    i.addEventListener("input",()=>onAnswer(q.id,i.value)); wrap.appendChild(i);
  } else if(t==="Free text"){
    const i=document.createElement("textarea"); i.dataset.qid=q.id;
    i.addEventListener("input",()=>onAnswer(q.id,i.value)); wrap.appendChild(i);
  } else if(t==="Multi-select"){
    const box=document.createElement("div"); box.className="opts";
    q.options.forEach(o=>{
      const d=document.createElement("label"); d.className="opt";
      const c=document.createElement("input"); c.type="checkbox"; c.value=o; c.dataset.qid=q.id;
      c.addEventListener("change",()=>{ const sel=[...box.querySelectorAll("input:checked")].map(x=>x.value);
        onAnswer(q.id, sel); });
      d.appendChild(c); d.appendChild(document.createTextNode(" "+o)); box.appendChild(d);
    });
    wrap.appendChild(box);
  } else if(t==="Single" && q.options.length>6){
    const sel=document.createElement("select"); sel.dataset.qid=q.id;
    sel.innerHTML='<option value="">— elige —</option>'+q.options.map(o=>`<option>${o}</option>`).join("");
    sel.addEventListener("change",()=>onAnswer(q.id,sel.value)); wrap.appendChild(sel);
  } else {
    // Single (<=6), Likert 1-5, NPS scale
    let opts = q.options;
    if(t==="NPS scale") opts = Array.from({length:10},(_,i)=>String(i+1));
    const box=document.createElement("div"); box.className="opts"+((t==="Likert 1–5"||t==="NPS scale")?" inline":"");
    opts.forEach(o=>{
      const d=document.createElement("label"); d.className="opt";
      const r=document.createElement("input"); r.type="radio"; r.name="q_"+q.id; r.value=o; r.dataset.qid=q.id;
      r.addEventListener("change",()=>onAnswer(q.id,o));
      d.appendChild(r); d.appendChild(document.createTextNode(" "+o)); box.appendChild(d);
    });
    wrap.appendChild(box);
  }
  return wrap;
}

/* ---------- answering + skip logic ---------- */
function onAnswer(id,val){
  if(Array.isArray(val) ? val.length : (val!==""&&val!=null)){
    if(firstAnswerAt[id]==null && startTime!=null) firstAnswerAt[id]=Date.now()-startTime;
    answers[id]=val;
  } else { delete answers[id]; }
  applySkips(); updateProgress();
}

function evalSkip(desc){
  if(!desc) return true;
  if(desc.type==="technical") return TECH_ROLES.includes(answers["primary_role"]);
  if(desc.type==="eq") return answers[desc.field]===desc.value;
  if(desc.type==="ai_spec") return (answers["ai_role_status"]&&answers["ai_role_status"]!=="No")
        || answers["primary_role"]==="AI-ML Engineer";
  if(desc.type==="cross_border"){ const reg=COUNTRY_REGION[answers["country"]]; const e=answers["employer_hq"];
        return !!(e && reg && e!==reg); }
  return true;
}

function applySkips(){
  for(const q of QUESTIONS){
    if(!q.skip) continue;
    const show = evalSkip(q.skip);
    const wrap = document.querySelector(`.q[data-qid="${q.id}"]`);
    if(!wrap) continue;
    wrap.classList.toggle("hidden", !show);
    if(!show && answers[q.id]!=null){       // cleared when it becomes irrelevant
      delete answers[q.id]; delete firstAnswerAt[q.id];
      wrap.querySelectorAll("input,select,textarea").forEach(el=>{
        if(el.type==="checkbox"||el.type==="radio") el.checked=false; else el.value="";
      });
    }
  }
}

function visibleQuestions(){ return QUESTIONS.filter(q=>{
  const w=document.querySelector(`.q[data-qid="${q.id}"]`); return w && !w.classList.contains("hidden"); }); }

function updateProgress(){
  const vis=visibleQuestions(); const ans=vis.filter(q=>answers[q.id]!=null).length;
  const pct = vis.length? Math.round(ans/vis.length*100):0;
  document.getElementById("barfill").style.width=pct+"%";
  document.getElementById("progresstxt").textContent=`${ans} de ${vis.length} preguntas visibles respondidas (${pct}%)`;
}

/* ---------- timer ---------- */
function startTimer(){ startTime=Date.now();
  tick=setInterval(()=>{document.getElementById("timer").textContent=fmt(Date.now()-startTime);},1000); }

/* ---------- results ---------- */
function computeResults(){
  const total = Date.now()-startTime;
  const vis = visibleQuestions();
  const answered = vis.filter(q=>answers[q.id]!=null);
  // order by first-answer offset for delta attribution
  const ev = answered.map(q=>({id:q.id,section:q.section,off:firstAnswerAt[q.id]??total}))
                     .sort((a,b)=>a.off-b.off);
  let prev=0; const perSection={};
  for(const e of ev){ const delta=Math.max(0,e.off-prev); prev=e.off;
    perSection[e.section]=perSection[e.section]||{n:0,t:0};
    perSection[e.section].n++; perSection[e.section].t+=delta; }
  return {total, visCount:vis.length, answered:answered.length, perSection, ev};
}

function showResults(){
  clearInterval(tick);
  const r=computeResults();
  document.getElementById("rTotal").textContent=fmt(r.total);
  document.getElementById("rAnswered").textContent=`${r.answered}/${r.visCount}`;
  document.getElementById("rAvg").textContent = r.answered? (r.total/1000/r.answered).toFixed(1) : "--";
  const tb=document.querySelector("#sectionTable tbody"); tb.innerHTML="";
  Object.entries(r.perSection).forEach(([s,v])=>{
    tb.insertAdjacentHTML("beforeend",`<tr><td>${s}</td><td>${v.n}</td><td>${(v.t/1000).toFixed(1)}</td></tr>`);
  });
  document.getElementById("formScreen").classList.add("hidden");
  document.getElementById("resultScreen").classList.remove("hidden");
  window._results=r;
}

function download(name,text,mime){
  const b=new Blob([text],{type:mime}); const a=document.createElement("a");
  a.href=URL.createObjectURL(b); a.download=name; a.click(); URL.revokeObjectURL(a.href);
}

/* ---------- wiring ---------- */
document.getElementById("startBtn").onclick=()=>{
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("formScreen").classList.remove("hidden");
  buildForm(); startTimer();
};
document.getElementById("submitBtn").onclick=showResults;
document.getElementById("resetBtn").onclick=()=>location.reload();
document.getElementById("againBtn").onclick=()=>location.reload();
document.getElementById("dlCsv").onclick=()=>{
  const pid=(document.getElementById("pid").value||"anon");
  const r=window._results;
  let csv="participant,field_id,section,offset_seconds\n";
  r.ev.forEach(e=>{csv+=`${pid},${e.id},"${e.section}",${(e.off/1000).toFixed(1)}\n`;});
  csv+=`${pid},__TOTAL__,,${(r.total/1000).toFixed(1)}\n`;
  download(`tiempos_${pid}.csv`,csv,"text/csv");
};
document.getElementById("dlJson").onclick=()=>{
  const pid=(document.getElementById("pid").value||"anon");
  download(`respuestas_${pid}.json`, JSON.stringify({participant:pid,answers,firstAnswerAt},null,2),"application/json");
};
document.getElementById("langBtn").onclick=()=>{
  lang = lang==="es"?"en":"es";
  document.getElementById("langBtn").textContent = lang==="es"?"EN":"ES";
  document.querySelectorAll(".q").forEach(w=>{
    const q=QUESTIONS.find(x=>x.id===w.dataset.qid);
    if(q) w.querySelector(".qtext").textContent = lang==="es"?q.es:(q.en||q.es);
  });
};
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active")); t.classList.add("active");
  const v=t.dataset.view;
  document.getElementById("view-survey").classList.toggle("hidden", v!=="survey");
  document.getElementById("view-rewards").classList.toggle("hidden", v!=="rewards");
});
</script>
<footer style="text-align:center;color:#94a3b8;font-size:12px;padding:20px;">
Generado desde salarios_question_inventory_2026.csv (__COUNT__ ítems) · __GENERATED__ · ensayo interno, sin backend
</footer>
</body>
</html>
"""

html = (TEMPLATE.replace("__DATA__", DATA)
                .replace("__COUNT__", COUNT)
                .replace("__GENERATED__", GENERATED))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"wrote {OUT} ({len(questions)} questions)")
