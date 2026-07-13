---
name: Contract Drafter
slug: contract-drafter
description: Generate professional legal contracts and agreements as styled HTML documents
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create contract"
  - "draft agreement"
  - "generate contract"
  - "make NDA"
  - "service agreement"
  - "contractor agreement"
tags:
  - contracts
  - legal
  - agreements
  - templates
  - nda
---

# Contract Drafter

Generate professional legal contracts and agreements as styled HTML documents. Contracts use the design foundation styling with legal-specific formatting (numbered sections, signature blocks, defined terms).

**IMPORTANT DISCLAIMER:** This skill generates documents from patterns and does NOT provide legal advice. All generated contracts should be reviewed by a qualified attorney before use.

**Reference `document-design-foundation` for the base template, CSS system, and component library.**

## How This Works

```
User: "draft an NDA for a potential partner"
                |
                v
  1. Determine contract type
  2. Gather key terms (parties, dates, specifics)
  3. Generate styled HTML with proper legal formatting
  4. Save to appropriate location
  5. Remind user to have an attorney review before signing
```

**You generate the contract directly. You do NOT write a contract generation engine.**

## Contract Types

| User Says | Type | Key Sections |
|---|---|---|
| "NDA" / "confidentiality" | Non-Disclosure Agreement | Parties, definition of confidential info, obligations, term, remedies |
| "service agreement" / "SOW" | Service Agreement | Scope, deliverables, timeline, payment, IP, termination |
| "contractor agreement" | Independent Contractor | Services, compensation, IP assignment, relationship, termination |
| "partnership agreement" | Partnership/JV | Contributions, profit sharing, governance, dissolution |
| "consulting agreement" | Consulting Agreement | Engagement, fees, expenses, confidentiality, IP |
| "license agreement" | License Agreement | Grant, restrictions, fees, term, warranties |

## Legal Document Styling

Contracts need additional CSS beyond the design foundation:

```css
/* Legal-specific additions to design foundation CSS */

/* Numbered sections */
.contract-body {
  counter-reset: section;
}

.contract-body h2 {
  counter-increment: section;
  border-bottom: none;
  margin-top: 2rem;
}

.contract-body h2::before {
  content: counter(section) ". ";
}

/* Defined terms */
dfn {
  font-style: normal;
  font-weight: 600;
  color: #1a1a2e;
}

/* Section references */
.section-ref {
  font-weight: 600;
  color: #0f3460;
}

/* Subsections */
.contract-body ol {
  list-style-type: lower-alpha;
  margin: 0.75rem 0 0.75rem 1.5rem;
}

.contract-body ol ol {
  list-style-type: lower-roman;
}

/* Signature block */
.signature-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-top: 3rem;
  padding-top: 1rem;
}

.signature-party {
  padding-top: 1rem;
}

.signature-line {
  border-top: 1px solid #262626;
  margin-top: 3rem;
  padding-top: 0.5rem;
  font-size: 0.9rem;
}

.signature-field {
  margin-top: 1.5rem;
}

.signature-field .label {
  font-size: 0.8rem;
  color: #a3a3a3;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

/* Recitals */
.recitals {
  margin: 1.5rem 0;
  padding-left: 1.5rem;
}

.recitals p::before {
  content: "WHEREAS, ";
  font-weight: 600;
}

.recitals p:last-child::before {
  content: "NOW, THEREFORE, ";
  font-weight: 600;
}

/* Exhibit reference */
.exhibit-ref {
  font-weight: 600;
  font-style: italic;
}

/* Print */
@media print {
  .signature-block { page-break-inside: avoid; }
  h2 { page-break-after: avoid; }
}
```

## Contract Template Structure

```html
<div class="document">
  <!-- HEADER -->
  <div class="cover" style="text-align: center; border-bottom: 3px double #1a1a2e;">
    <h1 style="text-transform: uppercase; letter-spacing: 0.05em;">
      {{CONTRACT TYPE}}
    </h1>
    <p class="subtitle">Between {{PARTY A}} and {{PARTY B}}</p>
    <div class="meta-row" style="justify-content: center;">
      <span>Effective Date: {{DATE}}</span>
    </div>
  </div>

  <!-- BODY -->
  <div class="document-body contract-body">

    <!-- Preamble -->
    <p>
      This {{Contract Type}} (this <dfn>"Agreement"</dfn>) is entered into as of
      {{Date}} (the <dfn>"Effective Date"</dfn>) by and between:
    </p>

    <p>
      <strong>{{Party A Legal Name}}</strong>, a {{entity type}} organized under the
      laws of {{jurisdiction}}, with its principal place of business at {{address}}
      (<dfn>"{{Party A Short Name}}"</dfn>); and
    </p>

    <p>
      <strong>{{Party B Legal Name}}</strong>, {{entity description}}, located at
      {{address}} (<dfn>"{{Party B Short Name}}"</dfn>).
    </p>

    <p>Each a <dfn>"Party"</dfn> and collectively the <dfn>"Parties."</dfn></p>

    <!-- Recitals (if needed) -->
    <div class="recitals">
      <p>{{Party A}} is engaged in {{business description}};</p>
      <p>{{Party B}} desires to {{purpose of agreement}};</p>
      <p>in consideration of the mutual covenants set forth herein, the Parties agree as follows:</p>
    </div>

    <!-- Sections -->
    <h2>Definitions</h2>
    <p>...</p>

    <h2>Scope / Obligations</h2>
    <p>...</p>

    <h2>Term and Termination</h2>
    <p>...</p>

    <h2>Compensation</h2>
    <p>...</p>

    <h2>Confidentiality</h2>
    <p>...</p>

    <h2>Intellectual Property</h2>
    <p>...</p>

    <h2>Representations and Warranties</h2>
    <p>...</p>

    <h2>Limitation of Liability</h2>
    <p>...</p>

    <h2>Governing Law</h2>
    <p>
      This Agreement shall be governed by and construed in accordance with the laws
      of the State of {{State}}, without regard to its conflict of laws principles.
    </p>

    <h2>Entire Agreement</h2>
    <p>
      This Agreement constitutes the entire agreement between the Parties with
      respect to the subject matter hereof and supersedes all prior negotiations,
      representations, or agreements relating thereto.
    </p>

    <!-- Signature Block -->
    <p style="margin-top: 2rem;">
      <strong>IN WITNESS WHEREOF</strong>, the Parties have executed this Agreement
      as of the Effective Date.
    </p>

    <div class="signature-block">
      <div class="signature-party">
        <p><strong>{{Party A Name}}</strong></p>
        <div class="signature-field">
          <div class="signature-line">Signature</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Name</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Title</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Date</div>
        </div>
      </div>
      <div class="signature-party">
        <p><strong>{{Party B Name}}</strong></p>
        <div class="signature-field">
          <div class="signature-line">Signature</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Name</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Title</div>
        </div>
        <div class="signature-field">
          <div class="signature-line">Date</div>
        </div>
      </div>
    </div>

  </div>

  <!-- FOOTER -->
  <div class="document-footer">
    <span>{{Contract Type}} &middot; {{Party A}} / {{Party B}}</span>
    <span>Effective: {{Date}}</span>
  </div>
</div>
```

## Common Clause Patterns

### Confidentiality Clause
```
<dfn>"Confidential Information"</dfn> means any non-public information disclosed
by either Party to the other, whether orally, in writing, or by inspection, including
but not limited to business plans, financial data, technical specifications, customer
lists, and proprietary technology.
```

### IP Assignment (Work for Hire)
```
All work product, deliverables, and intellectual property created by {{Contractor}}
in connection with the Services shall be considered "work made for hire" as defined
under the Copyright Act. To the extent any work product does not qualify as work
made for hire, {{Contractor}} hereby irrevocably assigns to {{Client}} all right,
title, and interest in and to such work product.
```

### Termination for Convenience
```
Either Party may terminate this Agreement for any reason upon {{N}} days' prior
written notice to the other Party. Upon such termination, {{Client}} shall pay
{{Contractor}} for all Services performed and expenses incurred through the
effective date of termination.
```

### Non-Solicitation
```
During the term of this Agreement and for a period of {{N}} months following its
termination, neither Party shall directly or indirectly solicit, hire, or engage
any employee, contractor, or agent of the other Party without prior written consent.
```

### Indemnification
```
Each Party (the <dfn>"Indemnifying Party"</dfn>) shall indemnify, defend, and hold
harmless the other Party from and against any claims, damages, losses, or expenses
arising out of or resulting from the Indemnifying Party's breach of this Agreement
or negligent acts or omissions.
```

## Content Quality Rules

- **Define every capitalized term.** If a word is capitalized and bolded, it must have a definition.
- **Be specific about dates and amounts.** "30 days" not "a reasonable time." "$5,000" not "fair compensation."
- **Include governing law.** Always specify the state/jurisdiction.
- **Include an entire agreement clause.** Prevents side agreements from conflicting.
- **Signature blocks for all parties.** With spaces for name, title, and date.
- **Number all sections.** CSS handles auto-numbering.

## File Location

```
Project context:  ./legal/{type}-{parties}-{date}.html
No project:       ~/Development/artifacts/legal/{type}-{parties}-{date}.html
```

## After Generation

Always include this reminder to the user:

> This document is a draft generated from standard patterns. It should be reviewed
> by a qualified attorney before execution. Key areas to verify: jurisdiction-specific
> requirements, industry regulations, and any unique terms specific to your situation.

## What NOT to Do

- Do NOT scaffold a Node.js project with docxtemplater
- Do NOT create a ClauseLibrary class or database
- Do NOT generate contracts without specifying all parties and key terms
- Do NOT use placeholder brackets like [INSERT] in delivered documents
- Do NOT skip the legal disclaimer reminder
- Do NOT claim the output constitutes legal advice
- Do NOT forget the signature block
