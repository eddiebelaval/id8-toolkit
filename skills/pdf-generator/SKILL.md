---
name: PDF Generator
slug: pdf-generator
description: Create professional PDF documents by generating polished HTML and converting to PDF
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create pdf"
  - "generate pdf document"
  - "convert to pdf"
  - "pdf from markdown"
  - "make a pdf"
tags:
  - pdf
  - documents
  - conversion
  - formatting
---

# PDF Generator

Create professional PDF documents. The workflow is HTML-first: generate a beautifully styled, self-contained HTML file, then convert to PDF when the user specifically needs .pdf format.

**Reference the `document-design-foundation` skill for the base template, CSS system, and component library.**

## How This Works

```
User: "create a PDF of our Q1 results"
                |
                v
  1. Write a styled HTML file using the design foundation template
  2. Fill in real content (not placeholder text)
  3. Save as .html to the appropriate location
  4. Convert to .pdf via puppeteer one-liner
  5. Tell the user where both files are
```

**You generate the document directly. You do NOT write a program that generates it.**

## When to Use This Skill

| User Says | What to Do |
|---|---|
| "create a PDF" | Generate HTML + convert to PDF |
| "make a PDF from this data" | Generate HTML with data formatted as tables/cards + convert |
| "convert this markdown to PDF" | Read the .md, wrap in design foundation template, convert |
| "generate a report as PDF" | Use the Report Builder skill (it references this for PDF conversion) |
| "create a document" | Generate HTML only (PDF conversion optional) |

## Step-by-Step Workflow

### Step 1: Determine Content

Ask yourself:
- What is the document about? (title, subject matter)
- Who is the audience? (executive, technical, client, internal)
- What sections does it need?
- Is there data to display? (tables, metrics, charts)

If the user provided content, use it directly. If they described what they want, write the content yourself.

### Step 2: Generate the HTML File

Use the design foundation template from `document-design-foundation`. The document should be:

- **Self-contained.** All CSS inline in `<style>`. No external dependencies.
- **Print-ready.** The `@media print` styles from the foundation handle this.
- **Content-complete.** Real text, real numbers, real structure. No "Lorem ipsum."

#### Document Structure Patterns

**Simple Document (letter, memo, one-pager):**
```html
<div class="document">
  <div class="cover">
    <h1>Document Title</h1>
    <p class="subtitle">Context or recipient</p>
    <div class="meta-row">
      <span>Author</span>
      <span>Date</span>
    </div>
  </div>
  <div class="document-body">
    <!-- Content sections -->
  </div>
  <div class="document-footer">
    <span>Organization</span>
    <span>Page info</span>
  </div>
</div>
```

**Data-Heavy Document (report, analysis):**
```html
<div class="document">
  <div class="cover">...</div>
  <div class="document-body">
    <p class="lead">Executive summary in 2-3 sentences.</p>

    <div class="kpi-grid">
      <!-- KPI cards from foundation -->
    </div>

    <h2>Section Title</h2>
    <p>Analysis text...</p>
    <table>
      <!-- Data table from foundation -->
    </table>

    <div class="callout info">
      <div class="callout-title">Key Finding</div>
      <p>Important insight highlighted here.</p>
    </div>
  </div>
</div>
```

**Multi-Section Document (proposal, plan, case study):**
```html
<div class="document">
  <div class="cover">...</div>
  <div class="document-body">
    <p class="lead">Summary paragraph.</p>

    <h2>1. Background</h2>
    <p>Context and problem statement...</p>

    <h2>2. Approach</h2>
    <p>What we propose...</p>

    <h2>3. Timeline</h2>
    <table><!-- milestones --></table>

    <h2>4. Investment</h2>
    <div class="kpi-grid"><!-- cost cards --></div>

    <h2>5. Next Steps</h2>
    <ol><!-- action items --></ol>
  </div>
</div>
```

### Step 3: Save the HTML

```
Project context:  ./{type}-{subject}.html  or  ./docs/{type}-{subject}.html
No project:       ~/Development/artifacts/{topic}/{type}-{subject}-{date}.html
```

### Step 4: Convert to PDF

Run this as a one-shot node command. Do NOT create a project or install dependencies globally.

```bash
# Check if puppeteer is available
node -e "require('puppeteer')" 2>/dev/null || npm install -g puppeteer

# Convert
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('file://ABSOLUTE_HTML_PATH', { waitUntil: 'networkidle0' });
  await page.pdf({
    path: 'ABSOLUTE_PDF_PATH',
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
  await browser.close();
  console.log('PDF saved to ABSOLUTE_PDF_PATH');
})();
"
```

**Important:** Use absolute paths. Replace `ABSOLUTE_HTML_PATH` and `ABSOLUTE_PDF_PATH` with real paths.

### Step 5: Report to User

Tell the user:
- Where the HTML file is (they can open it in a browser to preview)
- Where the PDF file is (if they requested PDF)
- Offer to make adjustments

## Markdown to PDF Conversion

When converting existing markdown files:

1. Read the markdown file content
2. Wrap it in the design foundation HTML template
3. Convert markdown formatting to HTML:
   - `# Heading` -> `<h1>`
   - `**bold**` -> `<strong>`
   - `- item` -> `<ul><li>`
   - Tables -> `<table>` with foundation styling
   - Code blocks -> `<pre><code>` with monospace font
4. Save as HTML
5. Convert to PDF

**Do NOT use a markdown-to-HTML library.** You can parse markdown yourself for the common patterns. This keeps the output clean and styled consistently with the design foundation.

## Content Quality Checklist

Before saving the document, verify:

- [ ] Title is specific and descriptive (not "Report" or "Document")
- [ ] Date is included and accurate
- [ ] All sections have real content (no placeholders)
- [ ] Numbers are formatted (currency, percentages, dates)
- [ ] Tables have proper headers
- [ ] Document has a clear conclusion or next steps section
- [ ] Spelling and grammar are correct
- [ ] The document reads well from top to bottom (logical flow)

## Advanced Patterns

### Adding Charts

For simple charts, use inline SVG:

```html
<!-- Bar chart as SVG -->
<svg viewBox="0 0 400 200" style="width:100%;max-width:500px;margin:1rem 0">
  <rect x="20" y="40" width="60" height="140" fill="#0f3460" rx="4"/>
  <rect x="100" y="80" width="60" height="100" fill="#0f3460" rx="4"/>
  <rect x="180" y="20" width="60" height="160" fill="#0f3460" rx="4"/>
  <rect x="260" y="60" width="60" height="120" fill="#0f3460" rx="4"/>
  <!-- Labels -->
  <text x="50" y="195" text-anchor="middle" font-size="12" fill="#525252">Q1</text>
  <text x="130" y="195" text-anchor="middle" font-size="12" fill="#525252">Q2</text>
  <text x="210" y="195" text-anchor="middle" font-size="12" fill="#525252">Q3</text>
  <text x="290" y="195" text-anchor="middle" font-size="12" fill="#525252">Q4</text>
</svg>
```

For interactive charts (HTML-only, not PDF), include Chart.js via CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### Multi-Page Documents

For documents that span multiple printed pages, add page break hints:

```html
<div style="page-break-before: always;"></div>
```

Place these before major `<h2>` sections in long documents.

### Cover Page as Full Page

For formal documents that need a standalone cover page:

```css
.cover {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

@media print {
  .cover {
    min-height: auto;
    page-break-after: always;
  }
}
```

### Watermark

```css
.document-body::before {
  content: "DRAFT";
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-45deg);
  font-size: 8rem;
  color: rgba(0, 0, 0, 0.04);
  pointer-events: none;
  z-index: 0;
}
```

## What NOT to Do

- Do NOT scaffold a Node.js project with package.json
- Do NOT write a "document generator" class or module
- Do NOT use placeholder text or sample data (unless explicitly asked for a template)
- Do NOT install pdfkit, jsPDF, or other PDF libraries (puppeteer converts HTML to PDF perfectly)
- Do NOT create multiple files for one document (one HTML file = one document)
- Do NOT ask the user to run a script (you run it yourself via Bash tool)
