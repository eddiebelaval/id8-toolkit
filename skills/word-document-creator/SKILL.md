---
name: Word Document Creator
slug: word-document-creator
description: Generate professional documents as styled HTML or .docx files with formatting, tables, and images
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create word document"
  - "generate docx"
  - "make word file"
  - "create .docx"
  - "word document from template"
  - "create a document"
  - "write a document"
tags:
  - word
  - docx
  - microsoft-office
  - documents
  - templates
---

# Word Document Creator

Generate professional documents. Default to HTML format (opens in any browser, prints perfectly). Generate .docx only when the user specifically needs a Word file.

**Reference the `document-design-foundation` skill for the base template, CSS system, and component library.**

## Decision: HTML or .docx?

| User Says | Format | Why |
|---|---|---|
| "create a document" | HTML | Universal, looks best, printable |
| "write up a proposal" | HTML | Better styling control, instant preview |
| "make a Word doc" | .docx | User explicitly asked for Word format |
| "I need to send a .docx" | .docx | Recipient requires Word format |
| "create a document I can edit in Word" | .docx | Editing in Word is the goal |
| "template I can reuse" | .docx | Templates work better in Word |

**Default to HTML unless the user specifically says "Word", "docx", or ".docx".**

## HTML Document Workflow (Preferred)

This is the same workflow as the PDF Generator. Follow the `document-design-foundation` skill:

1. Choose the right template structure from the foundation
2. Write real content (not placeholders)
3. Save as a self-contained HTML file
4. Tell the user where it is

### Common Document Patterns

**Business Letter:**
```html
<div class="document">
  <div class="document-body" style="padding-top: 4rem;">
    <p><strong>id8Labs LLC</strong><br>
    Miami, FL<br>
    eddie@id8labs.com</p>

    <p style="margin-top: 2rem;">April 15, 2026</p>

    <p style="margin-top: 1.5rem;">
    Recipient Name<br>
    Company<br>
    Address
    </p>

    <p style="margin-top: 1.5rem;">Dear [Name],</p>

    <p>Body of the letter...</p>

    <p style="margin-top: 2rem;">Sincerely,</p>
    <p><strong>Eddie Belaval</strong><br>Founder, id8Labs</p>
  </div>
</div>
```

**Meeting Notes:**
```html
<div class="document">
  <div class="cover">
    <h1>Meeting Notes</h1>
    <p class="subtitle">Homer Strategy Session</p>
    <div class="meta-row">
      <span>April 15, 2026</span>
      <span>Attendees: Eddie, Shah, Gus</span>
    </div>
  </div>
  <div class="document-body">
    <h2>Decisions Made</h2>
    <ol>
      <li><strong>Shah joins as CTO</strong> under pod model partnership.</li>
      <li><strong>Focus on Miami market exclusively</strong> through Q3 2026.</li>
    </ol>

    <h2>Discussion Notes</h2>
    <p>Key points from the conversation...</p>

    <h2>Action Items</h2>
    <table>
      <thead>
        <tr><th>Action</th><th>Owner</th><th>Due</th></tr>
      </thead>
      <tbody>
        <tr><td>Draft partnership agreement</td><td>Eddie</td><td>Apr 22</td></tr>
        <tr><td>Technical audit of Homer codebase</td><td>Shah</td><td>Apr 25</td></tr>
      </tbody>
    </table>
  </div>
</div>
```

**Proposal / SOW:**
```html
<div class="document">
  <div class="cover">
    <h1>Service Proposal</h1>
    <p class="subtitle">Prepared for [Client Name]</p>
    <div class="meta-row">
      <span>id8Labs LLC</span>
      <span>April 15, 2026</span>
      <span><span class="badge blue">Draft</span></span>
    </div>
  </div>
  <div class="document-body">
    <p class="lead">Summary of what we're proposing and why it matters.</p>

    <h2>1. Scope of Work</h2>
    <p>Detailed description...</p>

    <h2>2. Deliverables</h2>
    <table>
      <thead><tr><th>Deliverable</th><th>Timeline</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Initial audit</td><td>Week 1</td><td><span class="badge gray">Pending</span></td></tr>
        <tr><td>Implementation</td><td>Weeks 2-4</td><td><span class="badge gray">Pending</span></td></tr>
      </tbody>
    </table>

    <h2>3. Investment</h2>
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="label">Project Total</div>
        <div class="value">$12,500</div>
        <div class="change neutral">Fixed price</div>
      </div>
      <div class="kpi-card">
        <div class="label">Timeline</div>
        <div class="value">4 weeks</div>
        <div class="change neutral">Start on signing</div>
      </div>
    </div>

    <h2>4. Terms</h2>
    <p>Payment schedule, cancellation policy, etc.</p>
  </div>
  <div class="document-footer">
    <span>id8Labs LLC &middot; Confidential</span>
    <span>Valid for 30 days</span>
  </div>
</div>
```

## .docx Workflow (When Word Format Required)

When the user specifically needs a .docx file, generate it using the `docx` npm library.

### Step 1: Write and Run a Generation Script

Create a temporary Node.js script that generates the .docx file. Run it, then delete the script.

```javascript
// /tmp/generate-doc.mjs
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
         Table, TableRow, TableCell, WidthType, Header, Footer,
         BorderStyle, ShadingType } from 'docx';
import { writeFileSync } from 'fs';

const doc = new Document({
  styles: {
    paragraphStyles: [
      {
        id: "Normal",
        name: "Normal",
        run: { size: 22, font: "Calibri", color: "525252" },
        paragraph: { spacing: { after: 200, line: 360 } }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: "id8Labs", size: 18, color: "A3A3A3" })],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    children: [
      // Title
      new Paragraph({
        children: [new TextRun({ text: "Document Title", size: 48, bold: true, color: "1A1A2E", font: "Georgia" })],
        spacing: { after: 100 }
      }),
      // Subtitle
      new Paragraph({
        children: [new TextRun({ text: "Subtitle or context", size: 24, color: "A3A3A3" })],
        spacing: { after: 400 }
      }),
      // Section heading
      new Paragraph({
        text: "Section Heading",
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 400, after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E5E5E5" } }
      }),
      // Body text
      new Paragraph({
        children: [new TextRun({ text: "Body content goes here..." })],
        alignment: AlignmentType.JUSTIFIED
      }),
    ]
  }]
});

const buffer = await Packer.toBuffer(doc);
writeFileSync("OUTPUT_PATH.docx", buffer);
console.log("Document saved.");
```

### Step 2: Run It

```bash
# Ensure docx is available
npm list -g docx 2>/dev/null || npm install -g docx

# Run the generator
node /tmp/generate-doc.mjs

# Clean up
rm /tmp/generate-doc.mjs
```

### .docx Style Guide

Match the design foundation's visual language in Word format:

| Design Foundation | .docx Equivalent |
|---|---|
| `#1a1a2e` headings | `color: "1A1A2E"`, `font: "Georgia"` |
| `#525252` body text | `color: "525252"`, `font: "Calibri"` |
| `#a3a3a3` muted text | `color: "A3A3A3"` |
| 16px body size | `size: 22` (in half-points) |
| 1.6 line height | `line: 360` (in 240ths of a line) |
| 1in margins | `1440` (in twips) |
| Bordered h2 | `border.bottom: SINGLE, 6, "E5E5E5"` |

### Table Styling in .docx

```javascript
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  rows: [
    // Header row
    new TableRow({
      children: ["Column A", "Column B", "Column C"].map(text =>
        new TableCell({
          children: [new Paragraph({
            children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 18, font: "Calibri" })]
          })],
          shading: { type: ShadingType.SOLID, color: "1A1A2E" },
          width: { size: 33, type: WidthType.PERCENTAGE }
        })
      )
    }),
    // Data rows
    new TableRow({
      children: ["Value 1", "Value 2", "Value 3"].map(text =>
        new TableCell({
          children: [new Paragraph({
            children: [new TextRun({ text, size: 20, color: "525252" })]
          })],
          borders: {
            bottom: { style: BorderStyle.SINGLE, size: 1, color: "E5E5E5" }
          }
        })
      )
    })
  ]
})
```

## Content Quality Checklist

Before saving any document:

- [ ] Title is specific (not "Document" or "Proposal")
- [ ] Date is accurate (check TEMPORAL CONTEXT)
- [ ] No placeholder text remains
- [ ] Numbers are formatted appropriately
- [ ] Logical flow: conclusion first, then evidence
- [ ] Spelling and grammar checked
- [ ] Author/organization correctly attributed

## What NOT to Do

- Do NOT default to .docx when the user just says "document" (use HTML)
- Do NOT scaffold a project with package.json for one document
- Do NOT leave placeholder text in delivered documents
- Do NOT use pdfkit for documents (that's for the PDF Generator skill)
- Do NOT create complex class hierarchies for document generation
- Do NOT ask the user to run scripts (you run them via Bash)
