---
name: Spreadsheet Builder
slug: spreadsheet-builder
description: Generate professional Excel and CSV files with formatting, formulas, and data analysis
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create spreadsheet"
  - "generate excel"
  - "make csv file"
  - "build xlsx"
  - "create workbook"
tags:
  - excel
  - csv
  - spreadsheet
  - data
  - xlsx
  - analysis
---

# Spreadsheet Builder

Generate professional Excel (.xlsx) and CSV files directly. Unlike other document skills, spreadsheets require the `exceljs` library since HTML cannot produce .xlsx files. But the same operational principle applies: **you generate the file, not a program that generates it.**

**Reference `document-design-foundation` for color palette and styling consistency.**

## How This Works

```
User: "create a spreadsheet of our expenses"
                |
                v
  1. Determine structure (columns, data types, formulas)
  2. Write a temporary Node.js script using exceljs
  3. Run it to generate the .xlsx file
  4. Delete the script
  5. Tell the user where the file is
```

## Decision: Excel or CSV?

| User Says | Format | Why |
|---|---|---|
| "spreadsheet" | .xlsx | Full formatting, formulas, multiple sheets |
| "excel file" | .xlsx | Explicit request |
| "csv" or "csv file" | .csv | Simple, universal, no library needed |
| "export this data" | .csv | Simplest format for data transfer |
| "financial model" | .xlsx | Needs formulas, formatting, charts |
| "data dump" | .csv | Just raw data |

## CSV Generation (No Library Needed)

For simple data exports, write CSV directly with the Write tool:

```csv
Name,Revenue,Expenses,Profit,Margin
Homer Pro,$1800,$400,$1400,77.8%
Parallax,$0,$200,-$200,-
Consulting,$600,$100,$500,83.3%
```

Save as `{subject}-{date}.csv`. Done. No script needed.

## Excel Generation Workflow

### Step 1: Write the Generator Script

Create a temporary script at `/tmp/gen-spreadsheet.mjs`:

```javascript
import ExcelJS from 'exceljs';

const workbook = new ExcelJS.Workbook();
workbook.creator = 'id8Labs';
workbook.created = new Date();

// ============ SHEET 1 ============
const sheet = workbook.addWorksheet('Sheet Name', {
  properties: { defaultColWidth: 18 },
  views: [{ state: 'frozen', ySplit: 1 }]  // Freeze header row
});

// -- Design Foundation Colors --
const NAVY = '1A1A2E';
const BODY = '525252';
const LIGHT_BG = 'F5F5F5';
const BORDER = 'E5E5E5';
const SUCCESS = '0D7C3D';
const DANGER = 'B91C1C';
const WHITE = 'FFFFFF';

// -- Header Row --
sheet.columns = [
  { header: 'Column A', key: 'a', width: 20 },
  { header: 'Column B', key: 'b', width: 15 },
  { header: 'Column C', key: 'c', width: 15 },
];

// Style header row
sheet.getRow(1).eachCell(cell => {
  cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: NAVY } };
  cell.font = { bold: true, color: { argb: WHITE }, size: 11, name: 'Calibri' };
  cell.alignment = { vertical: 'middle', horizontal: 'left' };
  cell.border = {
    bottom: { style: 'thin', color: { argb: BORDER } }
  };
});
sheet.getRow(1).height = 28;

// -- Data Rows --
const data = [
  { a: 'Row 1', b: 1000, c: 500 },
  { a: 'Row 2', b: 2000, c: 800 },
];

data.forEach((row, i) => {
  const excelRow = sheet.addRow(row);
  excelRow.eachCell(cell => {
    cell.font = { size: 11, color: { argb: BODY }, name: 'Calibri' };
    cell.border = { bottom: { style: 'hair', color: { argb: BORDER } } };
  });
  // Alternate row shading
  if (i % 2 === 1) {
    excelRow.eachCell(cell => {
      cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: LIGHT_BG } };
    });
  }
});

// -- Totals Row --
const totalRow = sheet.addRow({
  a: 'Total',
  b: { formula: `SUM(B2:B${data.length + 1})` },
  c: { formula: `SUM(C2:C${data.length + 1})` },
});
totalRow.eachCell(cell => {
  cell.font = { bold: true, size: 11, color: { argb: NAVY }, name: 'Calibri' };
  cell.border = { top: { style: 'double', color: { argb: NAVY } } };
});

// -- Number Formatting --
sheet.getColumn('b').numFmt = '$#,##0.00';
sheet.getColumn('c').numFmt = '$#,##0.00';

// -- Save --
await workbook.xlsx.writeFile('OUTPUT_PATH');
console.log('Spreadsheet saved.');
```

### Step 2: Run and Clean Up

```bash
# Ensure exceljs is available
node -e "require('exceljs')" 2>/dev/null || npm install -g exceljs

# Generate
node /tmp/gen-spreadsheet.mjs

# Clean up
rm /tmp/gen-spreadsheet.mjs
```

## Style Guide (Design Foundation Mapping)

Keep spreadsheets visually consistent with other documents:

| Design Foundation | Excel Equivalent |
|---|---|
| `#1a1a2e` (navy headings) | Header row fill: `ARGB: 1A1A2E`, white text |
| `#525252` (body text) | Data cell font color: `525252` |
| `#f5f5f5` (alt row bg) | Alternate row fill: `F5F5F5` |
| `#e5e5e5` (borders) | Cell borders: `E5E5E5` |
| `#0d7c3d` (success) | Positive values conditional format |
| `#b91c1c` (danger) | Negative values conditional format |
| Calibri font | `name: 'Calibri'` throughout |
| 11pt body | `size: 11` for data cells |

## Common Patterns

### Financial Report Sheet

```javascript
// Currency columns
column.numFmt = '$#,##0.00';

// Percentage columns  
column.numFmt = '0.0%';

// Date columns
column.numFmt = 'mm/dd/yyyy';

// Conditional formatting for negative values
sheet.addConditionalFormatting({
  ref: 'C2:C100',
  rules: [{
    type: 'cellIs',
    operator: 'lessThan',
    formulae: [0],
    style: { font: { color: { argb: 'B91C1C' } } }
  }]
});
```

### Multi-Sheet Workbook

```javascript
const summary = workbook.addWorksheet('Summary');
const details = workbook.addWorksheet('Details');
const appendix = workbook.addWorksheet('Appendix');

// Cross-sheet formula
summary.getCell('B2').value = { formula: "Details!B10" };
```

### Data Validation (Dropdowns)

```javascript
sheet.getCell('D2').dataValidation = {
  type: 'list',
  allowBlank: true,
  formulae: ['"Active,Paused,Completed,Cancelled"']
};
```

### Auto-Filter

```javascript
sheet.autoFilter = {
  from: { row: 1, column: 1 },
  to: { row: data.length + 1, column: 3 }
};
```

## File Location

```
Project context:  ./data/{subject}-{date}.xlsx
No project:       ~/Development/artifacts/{topic}/{subject}-{date}.xlsx
CSV:              Same pattern with .csv extension
```

## What NOT to Do

- Do NOT scaffold a project with package.json
- Do NOT write a SpreadsheetGenerator class
- Do NOT leave the temp script behind after generation
- Do NOT use placeholder data unless building a template
- Do NOT forget number formatting (raw numbers without $ or % look amateur)
- Do NOT skip the header row styling (it's the first thing people see)
