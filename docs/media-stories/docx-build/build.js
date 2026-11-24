// Builds ../SG-Tech-Pulse-2026-Historias-para-medios.docx (the press Word doc).
//
// Nothing here is hardcoded to a dump:
//   - date and sample counts come from campaign/findings-site/data.json (meta),
//     which build_data.py recomputes from the current dump. Run it first.
//   - groups and story order come from the index in ../README.md.
//   - each story's text comes from its own ../NN-*.md file.
//
// Usage:  npm install && node build.js

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  PageBreak, BorderStyle, ImageRun, AlignmentType, Table, TableRow, TableCell, WidthType, VerticalAlign,
} = require("docx");

const REPO = path.resolve(__dirname, "..", "..", "..");
const SRC = path.join(REPO, "docs", "media-stories");
const OUT = path.join(SRC, "SG-Tech-Pulse-2026-Historias-para-medios.docx");
const LOGODIR = path.join(REPO, "campaign", "findings-site", "logos");
const DATA = path.join(REPO, "campaign", "findings-site", "data.json");

const meta = JSON.parse(fs.readFileSync(DATA, "utf8")).meta;
const DATE = meta.date_es;
const PCT_MX = Math.round((100 * meta.mx_n) / meta.total_n);
const fmt = n => n.toLocaleString("en-US");

const VIOLET = "6B3DFA", ROSE = "C81E4E", INK = "1A1A1A", MUTED = "6B6B6B", FONT = "Calibri";

// Groups and order, read from the "## Índice" section of README.md:
//   **Género**
//   - [01 · La desaparición](01-genero-desaparicion.md). blurb
function readGroups() {
  const lines = fs.readFileSync(path.join(SRC, "README.md"), "utf8").split("\n");
  const groups = [];
  let inIndex = false;
  for (const line of lines) {
    const t = line.trim();
    if (t.startsWith("## ")) { inIndex = t === "## Índice"; continue; }
    if (!inIndex || !t) continue;
    const g = t.match(/^\*\*(.+)\*\*$/);
    if (g) { groups.push({ name: g[1], files: [] }); continue; }
    const f = t.match(/^- \[[^\]]*\]\(([^)]+)\.md\)/);
    if (f && groups.length) groups[groups.length - 1].files.push(f[1]);
  }
  if (!groups.length) throw new Error("No groups found in the README index");
  return groups;
}
const GROUPS = readGroups();

function inline(text, base = {}) {
  const runs = [];
  text.split("**").forEach((p, i) => { if (p !== "") runs.push(new TextRun({ text: p, bold: i % 2 === 1, font: FONT, color: base.color || INK, size: base.size || 22 })); });
  return runs.length ? runs : [new TextRun({ text: "", font: FONT })];
}
function parseStory(slug) {
  const lines = fs.readFileSync(path.join(SRC, slug + ".md"), "utf8").split("\n");
  const s = { title: "", eyebrow: "", blocks: [], dato: "" };
  for (const line of lines) {
    const t = line.trim();
    if (!t) continue;
    if (t.startsWith("# ")) s.title = t.slice(2);
    else if (t.startsWith("> ")) s.eyebrow = t.slice(2).replace(/\*/g, "");
    else if (t.startsWith("## ")) s.blocks.push({ type: "h", text: t.slice(3) });
    else if (t === "---") continue;
    else if (t.startsWith("_") && t.endsWith("_")) s.dato = t.slice(1, -1);
    else if (t.startsWith("- ")) s.blocks.push({ type: "li", text: t.slice(2) });
    else s.blocks.push({ type: "p", text: t });
  }
  return s;
}

const NONE = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NONE, bottom: NONE, left: NONE, right: NONE };
function logoCell(file, w, h) {
  return new TableCell({
    width: { size: 33, type: WidthType.PERCENTAGE },
    borders: noBorders,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 80, bottom: 80, left: 80, right: 80 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new ImageRun({ type: "png", data: fs.readFileSync(path.join(LOGODIR, file)), transformation: { width: w, height: h } }),
    ] })],
  });
}

const children = [];

// Cover
children.push(
  new Paragraph({ spacing: { before: 2600 }, children: [new TextRun({ text: "SG Tech Pulse 2026", bold: true, font: FONT, size: 60, color: VIOLET })] }),
  new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "Historias para medios", font: FONT, size: 36, color: INK })] }),
  new Paragraph({ spacing: { before: 80 }, children: [new TextRun({ text: "Encuesta de Salarios · volcado del " + DATE, font: FONT, size: 22, color: MUTED })] }),
  new Paragraph({ spacing: { before: 40 }, children: [new TextRun({ text: "Corte de México · preliminar · uso para prensa", font: FONT, size: 22, color: MUTED })] }),
  new Paragraph({ spacing: { before: 900 }, border: { top: { style: BorderStyle.SINGLE, size: 6, color: VIOLET } }, children: [] }),
  new Paragraph({ spacing: { before: 200 }, children: [new TextRun({ text: "Una iniciativa de SG Software Guru", italics: true, font: FONT, size: 20, color: MUTED })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// Contents
children.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "Contenido", bold: true, font: FONT, size: 32, color: INK })] }));
GROUPS.forEach(group => {
  children.push(new Paragraph({ spacing: { before: 160, after: 60 }, children: [new TextRun({ text: group.name, bold: true, font: FONT, size: 24, color: VIOLET })] }));
  group.files.forEach(slug => children.push(new Paragraph({ indent: { left: 360 }, spacing: { after: 40 }, children: [new TextRun({ text: parseStory(slug).title, font: FONT, size: 22, color: INK })] })));
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// How to read + methods note
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Cómo leer estas piezas", font: FONT, bold: true, color: VIOLET })] }));
[
  "Son piezas cortas pensadas para prensa y redes, sacadas del volcado de respuestas del " + DATE + ". Están escritas en español de México, en tono cercano y con oraciones completas.",
  "Cada una sigue la misma estructura de tres partes. La afirmación es el gancho. El matiz explica o complica el dato. El lado bueno o la advertencia cierra, según la naturaleza del hallazgo.",
  `Se van a compartir con El Economista, El Financiero, Milenio y Expansión. Por eso todas usan solo a las personas que residen en México, que son ${fmt(meta.mx_n)} respuestas: ${fmt(meta.men)} hombres y ${fmt(meta.women)} mujeres.`,
].forEach(p => children.push(new Paragraph({ spacing: { after: 120 }, children: inline(p) })));
children.push(new Paragraph({ spacing: { before: 120, after: 80 }, children: [new TextRun({ text: "Nota metodológica", bold: true, font: FONT, size: 24, color: INK })] }));
[
  `La muestra son ${fmt(meta.total_n)} respuestas en total, de las cuales el ${PCT_MX}% reside en México. La encuesta sigue abierta y la muestra es autoseleccionada, no probabilística, así que describe a quienes quisieron responder y no al mercado entero. Trátese como preliminar.`,
  `El salario es el base bruto mensual. Los reportes en dólares se convierten a pesos con un tipo de cambio de ${meta.fx}, y las conclusiones se sostienen entre 17 y 20.`,
  "Los porcentajes se calculan sobre quienes respondieron cada pregunta. Algunas cifras cambian respecto a la versión de octubre, que contaba como \"no\" a quien no respondía.",
  "Salvo donde se menciona un modelo con controles, las cifras son asociaciones, no relaciones causales. Cada número se puede reproducir desde el volcado.",
].forEach(p => children.push(new Paragraph({ bullet: { level: 0 }, spacing: { after: 80 }, children: inline(p, { size: 21 }) })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// Stories, one per page, grouped as in the README index
GROUPS.forEach(group => {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { after: 120 }, children: [new TextRun({ text: group.name, font: FONT, bold: true, color: VIOLET })] }));
  group.files.forEach(slug => {
    const s = parseStory(slug);
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 120, after: 20 }, children: [new TextRun({ text: s.title, font: FONT, bold: true, color: INK })] }));
    if (s.eyebrow) children.push(new Paragraph({ spacing: { after: 140 }, children: [new TextRun({ text: s.eyebrow, italics: true, font: FONT, size: 18, color: ROSE })] }));
    s.blocks.forEach(b => {
      if (b.type === "h") children.push(new Paragraph({ spacing: { before: 140, after: 40 }, children: [new TextRun({ text: b.text, bold: true, font: FONT, size: 24, color: VIOLET })] }));
      else if (b.type === "li") children.push(new Paragraph({ bullet: { level: 0 }, spacing: { after: 60 }, children: inline(b.text) }));
      else children.push(new Paragraph({ spacing: { after: 120 }, children: inline(b.text) }));
    });
    if (s.dato) children.push(new Paragraph({ spacing: { before: 100 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD" } }, children: [new TextRun({ text: s.dato, italics: true, font: FONT, size: 17, color: MUTED })] }));
    children.push(new Paragraph({ children: [new PageBreak()] }));
  });
});

// Thank-you / sponsors
children.push(new Paragraph({ spacing: { before: 2400, after: 140 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Gracias", bold: true, font: FONT, size: 34, color: VIOLET })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: "Gracias a Improving, Mobiik y Svitla por difundir esta encuesta en la comunidad tech.", font: FONT, size: 22, color: INK })] }));
children.push(new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: { ...noBorders, insideHorizontal: NONE, insideVertical: NONE },
  rows: [new TableRow({ children: [
    logoCell("LogoImproving.png", 120, 60),
    logoCell("LogoMobiik.png", 60, 60),
    logoCell("LogoSvitla.png", 120, 60),
  ] })],
}));

const doc = new Document({
  creator: "SG Software Guru", title: "SG Tech Pulse 2026 · Historias para medios",
  styles: {
    default: { document: { run: { font: FONT, size: 22, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 30, bold: true, color: VIOLET }, paragraph: { spacing: { before: 240, after: 120 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, color: INK }, paragraph: { spacing: { before: 180, after: 60 } } },
    ],
  },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
const nStories = GROUPS.reduce((a, g) => a + g.files.length, 0);
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`wrote ${path.relative(REPO, OUT)} (${buf.length} bytes, ${GROUPS.length} groups, ${nStories} stories, ${DATE})`);
});
