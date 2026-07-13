---
name: Presentation Maker
slug: presentation-maker
description: Generate professional PowerPoint presentations with slides, charts, and speaker notes
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create presentation"
  - "generate powerpoint"
  - "make slides"
  - "build pptx"
  - "create deck"
  - "pitch deck"
tags:
  - powerpoint
  - presentations
  - slides
  - pptx
  - keynote
---

# Presentation Maker

Generate professional PowerPoint (.pptx) presentations directly. This skill requires the `pptxgenjs` library since HTML cannot produce .pptx files. The same operational principle applies: **you generate the file, not a program that generates it.**

**Reference `document-design-foundation` for color palette and styling consistency.**

## How This Works

```
User: "create a presentation on our Q1 results"
                |
                v
  1. Determine slide structure (title, content, charts, closing)
  2. Write a temporary Node.js script using pptxgenjs
  3. Run it to generate the .pptx file
  4. Delete the script
  5. Tell the user where the file is
```

## Slide Structure Patterns

### Pitch Deck (8-12 slides)
```
1. Title Slide (company, tagline, date)
2. Problem (what pain exists)
3. Solution (how you solve it)
4. Product (screenshot or demo)
5. Market Size (TAM/SAM/SOM)
6. Business Model (how you make money)
7. Traction (metrics, growth)
8. Team (key people)
9. Ask (what you need)
10. Contact (how to reach you)
```

### Status Update (5-8 slides)
```
1. Title Slide (project, period)
2. Executive Summary (3 bullets + status badge)
3. KPI Dashboard (4-6 metrics)
4. Accomplishments (what got done)
5. Challenges (what's blocking)
6. Next Steps (priorities)
7. Appendix (optional, detailed data)
```

### Training / Workshop (10-20 slides)
```
1. Title Slide
2. Agenda / Outline
3-N. Content Slides (one idea per slide)
N+1. Key Takeaways (3-5 bullets)
N+2. Q&A / Discussion
N+3. Resources / Contact
```

## Generation Workflow

### Step 1: Write the Generator Script

Create at `/tmp/gen-presentation.mjs`:

```javascript
import PptxGenJS from 'pptxgenjs';

const pptx = new PptxGenJS();

// ============ THEME (Design Foundation Colors) ============
const NAVY = '1A1A2E';
const DARK_BLUE = '16213E';
const ACCENT = '0F3460';
const ACCENT_LIGHT = 'E8F0FE';
const BODY_TEXT = '525252';
const MUTED = 'A3A3A3';
const WHITE = 'FFFFFF';
const LIGHT_BG = 'F5F5F5';
const SUCCESS = '0D7C3D';
const DANGER = 'B91C1C';
const WARNING = 'B45309';

// ============ MASTER SLIDE ============
pptx.defineSlideMaster({
  title: 'MAIN',
  background: { color: WHITE },
  objects: [
    // Bottom accent bar
    { rect: { x: 0, y: 6.9, w: '100%', h: 0.1, fill: { color: NAVY } } },
    // Footer text
    { text: {
      text: 'id8Labs | Confidential',
      options: { x: 0.5, y: 7.0, w: 4, h: 0.3, fontSize: 8, color: MUTED, fontFace: 'Calibri' }
    }},
    // Slide number
    { text: {
      text: { type: 'slideNumber' },
      options: { x: 8.5, y: 7.0, w: 1, h: 0.3, fontSize: 8, color: MUTED, align: 'right', fontFace: 'Calibri' }
    }}
  ]
});

pptx.defineSlideMaster({
  title: 'TITLE',
  background: { color: NAVY },
  objects: []
});

// ============ SLIDE 1: TITLE ============
const slide1 = pptx.addSlide({ masterName: 'TITLE' });
slide1.addText('Presentation Title', {
  x: 0.8, y: 2.0, w: 8.4, h: 1.5,
  fontSize: 36, fontFace: 'Georgia', color: WHITE, bold: true
});
slide1.addText('Subtitle or context line', {
  x: 0.8, y: 3.5, w: 8.4, h: 0.6,
  fontSize: 18, fontFace: 'Calibri', color: MUTED
});
slide1.addText('April 16, 2026', {
  x: 0.8, y: 4.5, w: 8.4, h: 0.4,
  fontSize: 14, fontFace: 'Calibri', color: MUTED
});

// ============ SLIDE 2: CONTENT ============
const slide2 = pptx.addSlide({ masterName: 'MAIN' });
slide2.addText('Section Heading', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.8,
  fontSize: 28, fontFace: 'Georgia', color: NAVY, bold: true
});
slide2.addText([
  { text: 'First key point about the topic.\n', options: { fontSize: 16, color: BODY_TEXT, fontFace: 'Calibri', bullet: true } },
  { text: 'Second point with supporting detail.\n', options: { fontSize: 16, color: BODY_TEXT, fontFace: 'Calibri', bullet: true } },
  { text: 'Third point driving home the message.', options: { fontSize: 16, color: BODY_TEXT, fontFace: 'Calibri', bullet: true } },
], {
  x: 0.8, y: 1.5, w: 8.4, h: 4.5,
  lineSpacingMultiple: 1.5
});
// Speaker notes
slide2.addNotes('Talking points: expand on each bullet. Emphasize the second point as the most important.');

// ============ SLIDE 3: KPI DASHBOARD ============
const slide3 = pptx.addSlide({ masterName: 'MAIN' });
slide3.addText('Key Metrics', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.8,
  fontSize: 28, fontFace: 'Georgia', color: NAVY, bold: true
});

const kpis = [
  { label: 'MRR', value: '$2,400', change: '+34%', color: SUCCESS },
  { label: 'Users', value: '12', change: '+8', color: SUCCESS },
  { label: 'Runway', value: '5 mo', change: 'At risk', color: DANGER },
  { label: 'NPS', value: '72', change: 'Stable', color: MUTED },
];

kpis.forEach((kpi, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.8 + col * 4.5;
  const y = 1.6 + row * 2.2;

  // Card background
  slide3.addShape(pptx.ShapeType.roundRect, {
    x, y, w: 4.0, h: 1.8,
    fill: { color: LIGHT_BG },
    rectRadius: 0.1,
    line: { color: 'E5E5E5', width: 1 }
  });
  // Label
  slide3.addText(kpi.label.toUpperCase(), {
    x: x + 0.3, y: y + 0.2, w: 3.4, h: 0.3,
    fontSize: 10, fontFace: 'Calibri', color: MUTED, bold: true
  });
  // Value
  slide3.addText(kpi.value, {
    x: x + 0.3, y: y + 0.5, w: 3.4, h: 0.7,
    fontSize: 32, fontFace: 'Georgia', color: NAVY, bold: true
  });
  // Change
  slide3.addText(kpi.change, {
    x: x + 0.3, y: y + 1.2, w: 3.4, h: 0.3,
    fontSize: 12, fontFace: 'Calibri', color: kpi.color
  });
});

// ============ SLIDE 4: TABLE ============
const slide4 = pptx.addSlide({ masterName: 'MAIN' });
slide4.addText('Data Breakdown', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.8,
  fontSize: 28, fontFace: 'Georgia', color: NAVY, bold: true
});

slide4.addTable(
  [
    // Header row
    [
      { text: 'Product', options: { bold: true, color: WHITE, fill: { color: NAVY } } },
      { text: 'Revenue', options: { bold: true, color: WHITE, fill: { color: NAVY } } },
      { text: 'Status', options: { bold: true, color: WHITE, fill: { color: NAVY } } },
    ],
    // Data rows
    ['Homer Pro', '$1,800', 'Active'],
    ['Parallax', '$0', 'Maintenance'],
    ['Consulting', '$600', 'Active'],
  ],
  {
    x: 0.8, y: 1.5, w: 8.4,
    fontSize: 14, fontFace: 'Calibri', color: BODY_TEXT,
    border: { type: 'solid', pt: 0.5, color: 'E5E5E5' },
    rowH: [0.5, 0.45, 0.45, 0.45],
    colW: [3.5, 2.5, 2.4],
    autoPage: true
  }
);

// ============ SLIDE 5: CHART ============
const slide5 = pptx.addSlide({ masterName: 'MAIN' });
slide5.addText('Revenue Trend', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.8,
  fontSize: 28, fontFace: 'Georgia', color: NAVY, bold: true
});

slide5.addChart(pptx.ChartType.bar, [
  {
    name: 'Revenue',
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    values: [1200, 1500, 1800, 2400]
  }
], {
  x: 0.8, y: 1.5, w: 8.4, h: 5.0,
  showValue: true,
  valueFontSize: 10,
  catAxisLabelFontSize: 12,
  valAxisLabelFontSize: 10,
  chartColors: [ACCENT],
  catAxisOrientation: 'minMax'
});

// ============ CLOSING SLIDE ============
const closing = pptx.addSlide({ masterName: 'TITLE' });
closing.addText('Thank You', {
  x: 0.8, y: 2.5, w: 8.4, h: 1.0,
  fontSize: 36, fontFace: 'Georgia', color: WHITE, bold: true, align: 'center'
});
closing.addText('eddie@id8labs.com', {
  x: 0.8, y: 3.8, w: 8.4, h: 0.5,
  fontSize: 16, fontFace: 'Calibri', color: MUTED, align: 'center'
});

// ============ SAVE ============
await pptx.writeFile({ fileName: 'OUTPUT_PATH' });
console.log('Presentation saved.');
```

### Step 2: Run and Clean Up

```bash
# Ensure pptxgenjs is available
node -e "require('pptxgenjs')" 2>/dev/null || npm install -g pptxgenjs

# Generate
node /tmp/gen-presentation.mjs

# Clean up
rm /tmp/gen-presentation.mjs
```

## Slide Design Rules

### Typography
- **Titles:** Georgia, 28-36pt, navy (`1A1A2E`)
- **Body text:** Calibri, 14-18pt, gray (`525252`)
- **Captions/labels:** Calibri, 10-12pt, muted (`A3A3A3`)
- **Max 6 bullet points per slide**
- **Max 8 words per bullet**

### Layout
- **One idea per slide.** If you need two ideas, make two slides.
- **Left margin at 0.8"** for all content (consistent alignment)
- **Title at y: 0.4"** on every content slide
- **Content starts at y: 1.5"** (below title)
- **Footer bar at y: 6.9"** (master slide handles this)

### Color Usage
- **Title slides:** Navy background, white text
- **Content slides:** White background, navy headings, gray body
- **Positive metrics:** Success green (`0D7C3D`)
- **Negative metrics:** Danger red (`B91C1C`)
- **Warnings:** Amber (`B45309`)
- **Neutral:** Muted gray (`A3A3A3`)

### Charts
- Use `ACCENT` (`0F3460`) as primary chart color
- Add value labels on bars/columns (`showValue: true`)
- Keep axis labels readable (12pt minimum)
- One chart per slide maximum

## Content Quality Rules

- **Every slide needs a clear heading.** No untitled slides.
- **Speaker notes on every content slide.** Brief talking points.
- **Data slides need context.** Don't just show numbers. Add "Key Takeaway:" text.
- **No wall-of-text slides.** If it takes more than 6 bullets, split it.
- **End with a clear ask or next step.** Don't just stop.

## File Location

```
Project context:  ./docs/{subject}-{date}.pptx
No project:       ~/Development/artifacts/{topic}/{subject}-{date}.pptx
```

## What NOT to Do

- Do NOT scaffold a project with package.json
- Do NOT create a PresentationBuilder class
- Do NOT leave the temp script behind
- Do NOT put paragraphs on slides (bullets only)
- Do NOT skip speaker notes
- Do NOT use more than 3 colors per slide
- Do NOT use clip art or decorative shapes
