---
name: Report Builder
slug: report-builder
description: Generate polished business reports, dashboards, and executive summaries as styled HTML documents
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create report"
  - "generate report"
  - "build report"
  - "make business report"
  - "executive summary"
  - "status report"
  - "dashboard"
tags:
  - reports
  - business
  - analytics
  - data-visualization
  - summaries
  - dashboard
---

# Report Builder

Generate professional business reports directly as styled HTML files. Reports look polished, print cleanly to PDF, and rival claude.ai Artifact quality.

**Reference the `document-design-foundation` skill for the base template, CSS system, and component library.**

## How This Works

```
User: "create a report on our Q1 performance"
                |
                v
  1. Determine report type (executive, status, financial, analysis)
  2. Structure content with BLUF (Bottom Line Up Front)
  3. Write a self-contained HTML file using the design foundation
  4. Save to appropriate location
  5. Convert to PDF if requested (see pdf-generator skill)
```

**You write the report directly. You do NOT write a program that generates reports.**

## Report Types

### 1. Executive Report
**When:** User wants a high-level overview with KPIs and recommendations
**Structure:**
```
Cover (title, date, author)
Executive Summary (2-3 sentences, the BLUF)
KPI Dashboard (4-6 metric cards)
Analysis Sections (2-4 sections with data)
Recommendations (numbered action items)
```

### 2. Status Report
**When:** Project update, weekly/monthly progress
**Structure:**
```
Cover (project name, reporting period)
Status Summary (one-line verdict + status badge)
KPI Cards (completion %, budget, timeline, team health)
Completed This Period (bullet list)
In Progress (table with owners and status)
Risks and Blockers (callout boxes)
Next Steps (numbered priorities)
```

### 3. Financial Report
**When:** Revenue, expenses, P&L, budget tracking
**Structure:**
```
Cover (period, fiscal year)
Financial Summary (KPI cards: revenue, expenses, net, margin)
Income Statement Table
Expense Breakdown (table + optional chart)
Cash Flow Summary
Variance Analysis (callout boxes for significant variances)
Forecast / Outlook
```

### 4. Analysis Report
**When:** Research findings, competitive analysis, market report
**Structure:**
```
Cover (topic, date)
Key Findings (3-5 bullet BLUF)
Methodology (brief)
Detailed Analysis (sections with tables and data)
Comparison Tables
Conclusions
Recommendations
```

### 5. One-Pager / Dashboard
**When:** Quick snapshot, single-page overview
**Structure:**
```
Title + date (no cover page)
KPI Grid (6-8 cards, compact)
Key highlights (3 bullets)
One data table
Status badges for key items
```

## Step-by-Step Workflow

### Step 1: Identify What the User Needs

Listen for these signals:

| User Says | Report Type | Key Focus |
|---|---|---|
| "how are we doing" | Executive | KPIs + trends |
| "project update" | Status | Progress + blockers |
| "revenue report" | Financial | Numbers + variance |
| "what did we find" | Analysis | Findings + evidence |
| "quick overview" | One-Pager | Density + at-a-glance |

### Step 2: Gather Content

Use data from:
- Information the user provided in the conversation
- Files in the current project (read them)
- Git history (if relevant to project status)
- Database queries (if Supabase/DB is connected)

If data is incomplete, use what you have and note assumptions. Do NOT ask the user to fill in a template.

### Step 3: Write the HTML

Use the design foundation template. Here is a complete executive report example showing how to compose the components:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Q1 2026 Performance Report</title>
  <style>
    /* === Paste the full CSS from document-design-foundation === */
    /* All reset, typography, KPI, table, callout, badge, print styles */
  </style>
</head>
<body>
  <div class="document">

    <!-- COVER -->
    <div class="cover">
      <h1>Q1 2026 Performance Report</h1>
      <p class="subtitle">id8Labs Portfolio Review</p>
      <div class="meta-row">
        <span>Prepared by Eddie Belaval</span>
        <span>April 15, 2026</span>
        <span><span class="badge green">On Track</span></span>
      </div>
    </div>

    <!-- BODY -->
    <div class="document-body">

      <!-- Executive Summary -->
      <p class="lead">
        Portfolio revenue grew 34% quarter-over-quarter driven by Homer's first
        paying brokerage client. Parallax remains in maintenance mode with 17 users
        and zero paying customers. The north star remains becoming cashflow positive
        by Q4 2026.
      </p>

      <!-- KPI Dashboard -->
      <h2>Key Metrics</h2>
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="label">MRR</div>
          <div class="value">$2,400</div>
          <div class="change up">+34% QoQ</div>
        </div>
        <div class="kpi-card">
          <div class="label">Active Projects</div>
          <div class="value">6</div>
          <div class="change neutral">Steady</div>
        </div>
        <div class="kpi-card">
          <div class="label">Users (Homer)</div>
          <div class="value">12</div>
          <div class="change up">+8 this quarter</div>
        </div>
        <div class="kpi-card">
          <div class="label">Runway</div>
          <div class="value">5 mo</div>
          <div class="change down">Needs attention</div>
        </div>
      </div>

      <!-- Analysis Section -->
      <h2>Revenue Breakdown</h2>
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Q1 Revenue</th>
            <th>Q4 Revenue</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Homer Pro</td>
            <td>$1,800</td>
            <td>$0</td>
            <td><span class="badge green">New</span></td>
          </tr>
          <tr>
            <td>Parallax</td>
            <td>$0</td>
            <td>$0</td>
            <td><span class="badge gray">No change</span></td>
          </tr>
          <tr>
            <td>Consulting</td>
            <td>$600</td>
            <td>$1,200</td>
            <td><span class="badge red">-50%</span></td>
          </tr>
        </tbody>
      </table>

      <!-- Key Finding -->
      <div class="callout info">
        <div class="callout-title">Key Finding</div>
        <p>Homer's first brokerage deal (Florida Realty of Miami) validates the
        agent-powered real estate thesis. The pipeline has two more agencies
        in conversation for Q2.</p>
      </div>

      <!-- Risks -->
      <h2>Risks and Blockers</h2>
      <div class="callout warning">
        <div class="callout-title">Runway Pressure</div>
        <p>At current burn rate, runway extends to September 2026. Revenue
        must reach $5,000 MRR by August to sustain operations without
        external funding.</p>
      </div>

      <div class="callout danger">
        <div class="callout-title">MARA Distribution Broken</div>
        <p>The automated posting daemon is exit-code-1 since last week.
        Social distribution is fully manual until fixed.</p>
      </div>

      <!-- Recommendations -->
      <h2>Recommendations</h2>
      <ol>
        <li><strong>Close the Shah partnership</strong> to unlock Homer's technical capacity for Q2 feature velocity.</li>
        <li><strong>Fix MARA daemon</strong> immediately. Portfolio distribution depends on it.</li>
        <li><strong>Convert Parallax to free-tier funnel</strong> since zero paying users after 6 months signals a pricing problem, not a product problem.</li>
        <li><strong>Pursue the Rose legal review</strong> for Homer's E&O and DBPR compliance before scaling to more agencies.</li>
      </ol>

    </div>

    <!-- FOOTER -->
    <div class="document-footer">
      <span>id8Labs LLC &middot; Confidential</span>
      <span>Q1 2026</span>
    </div>

  </div>
</body>
</html>
```

### Step 4: Save and Deliver

```
File location:
  - Project context:  ./reports/{type}-{date}.html
  - No project:       ~/Development/artifacts/{topic}/report-{subject}-{date}.html

Naming examples:
  - report-q1-performance-2026-04-15.html
  - status-homer-sprint-12-2026-04-15.html
  - analysis-competitor-landscape-2026-04-15.html
```

### Step 5: PDF Conversion (If Requested)

Reference the `pdf-generator` skill for the puppeteer one-liner conversion.

## Writing Quality Standards

### The BLUF Rule
Every report opens with the bottom line. The reader should understand the main message in the first 10 seconds.

**Good:** "Revenue grew 34% QoQ. Two risks need immediate attention: runway and distribution."
**Bad:** "This report provides an overview of Q1 2026 performance across the id8Labs portfolio of products..."

### Data Presentation Rules
- **Numbers always get context.** "$2,400 MRR" means nothing without "+34% QoQ" next to it.
- **Use relative change + absolute value.** Show both: "$2,400 (+34%)"
- **Color-code direction.** Green for positive trends, red for negative, gray for neutral.
- **Round appropriately.** Revenue to whole dollars. Percentages to one decimal.
- **Compare to something.** Previous period, target, industry benchmark.

### Section Writing Rules
- **One idea per section.** If a section covers two topics, split it.
- **Lead each section with its conclusion.** Then support with evidence.
- **2-4 paragraphs max per section.** Use tables and lists for density.
- **End with recommendations.** Every analysis section should answer "so what?"

### Recommendations Rules
- **Be specific.** "Close the Shah partnership by April 30" not "Consider partnerships."
- **Include the why.** "...to unlock technical capacity for Q2" explains the urgency.
- **Prioritize.** Number them. Most important first.
- **Make them actionable.** Each recommendation should be completable by one person.

## Adding Charts (Optional)

For reports that benefit from visual data, use inline SVG for print-safe charts:

### Simple Bar Chart
```html
<div style="margin: 1.5rem 0">
  <div style="display: flex; align-items: flex-end; gap: 1rem; height: 160px; padding: 0 1rem;">
    <div style="flex: 1; text-align: center;">
      <div style="background: #0f3460; height: 80%; border-radius: 4px 4px 0 0;"></div>
      <div class="small muted" style="margin-top: 0.5rem;">Jan</div>
    </div>
    <div style="flex: 1; text-align: center;">
      <div style="background: #0f3460; height: 60%; border-radius: 4px 4px 0 0;"></div>
      <div class="small muted" style="margin-top: 0.5rem;">Feb</div>
    </div>
    <div style="flex: 1; text-align: center;">
      <div style="background: #0f3460; height: 100%; border-radius: 4px 4px 0 0;"></div>
      <div class="small muted" style="margin-top: 0.5rem;">Mar</div>
    </div>
  </div>
</div>
```

### Horizontal Progress Bars (for comparison)
```html
<div style="margin: 1rem 0;">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
    <span class="small" style="width: 100px;">Homer</span>
    <div class="progress-bar" style="flex: 1;">
      <div class="fill" style="width: 72%; background: #0d7c3d;"></div>
    </div>
    <span class="small muted">72%</span>
  </div>
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
    <span class="small" style="width: 100px;">Parallax</span>
    <div class="progress-bar" style="flex: 1;">
      <div class="fill" style="width: 45%; background: #b45309;"></div>
    </div>
    <span class="small muted">45%</span>
  </div>
</div>
```

## What NOT to Do

- Do NOT write a Node.js program that generates reports
- Do NOT use pdfkit, chartjs-node-canvas, or other server-side libraries
- Do NOT create placeholder content ("Lorem ipsum", "[INSERT DATA]")
- Do NOT start with methodology. Start with the conclusion.
- Do NOT include more than 6 KPI cards (decision fatigue)
- Do NOT write paragraphs longer than 4 sentences
- Do NOT use passive voice in recommendations
- Do NOT ask the user to run any scripts (you run them yourself)
