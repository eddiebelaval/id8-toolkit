---
name: Form Builder
slug: form-builder
description: Create professional forms, surveys, and questionnaires as styled HTML with validation
category: document-creation
complexity: complex
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create form"
  - "build survey"
  - "generate form"
  - "make questionnaire"
  - "fillable form"
  - "intake form"
  - "application form"
tags:
  - forms
  - surveys
  - questionnaires
  - data-collection
  - interactive
---

# Form Builder

Generate professional, functional forms as styled HTML files. Forms include client-side validation, conditional logic, and clean styling from the design foundation. Default to HTML forms that work in any browser.

**Reference `document-design-foundation` for the base template, CSS system, and component library.**

## How This Works

```
User: "create an intake form for new clients"
                |
                v
  1. Determine form type and fields needed
  2. Write a self-contained HTML file with form elements + validation
  3. Save to appropriate location
  4. Tell the user where the file is
```

**You generate the form directly. You do NOT write a form-generation framework.**

## Form Types

| User Says | Form Type | Key Elements |
|---|---|---|
| "intake form" | Client Intake | Contact info, business details, needs assessment |
| "survey" | Feedback Survey | Rating scales, open text, multiple choice |
| "application" | Application Form | Personal info, qualifications, uploads |
| "registration" | Registration | Account details, preferences, terms |
| "feedback form" | Feedback | Ratings, comments, NPS |
| "questionnaire" | Assessment | Scored questions, conditional sections |
| "contact form" | Contact | Name, email, message |

## HTML Form Template

Every form uses this structure with the design foundation styling plus form-specific CSS:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{FORM_TITLE}}</title>
  <style>
    /* === Design Foundation base styles (reset, typography, colors) === */

    /* === Form-Specific Styles === */
    .form-group {
      margin-bottom: 1.5rem;
    }

    label {
      display: block;
      font-weight: 600;
      color: #262626;
      margin-bottom: 0.4rem;
      font-size: 0.9rem;
    }

    label .required {
      color: #b91c1c;
      margin-left: 0.15rem;
    }

    .help-text {
      font-size: 0.8rem;
      color: #a3a3a3;
      margin-top: 0.25rem;
    }

    input[type="text"],
    input[type="email"],
    input[type="tel"],
    input[type="url"],
    input[type="number"],
    input[type="date"],
    input[type="password"],
    select,
    textarea {
      width: 100%;
      padding: 0.65rem 0.85rem;
      border: 1px solid #e5e5e5;
      border-radius: 6px;
      font-size: 0.95rem;
      font-family: inherit;
      color: #262626;
      background: #ffffff;
      transition: border-color 0.15s, box-shadow 0.15s;
    }

    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: #0f3460;
      box-shadow: 0 0 0 3px rgba(15, 52, 96, 0.1);
    }

    input.error, select.error, textarea.error {
      border-color: #b91c1c;
      box-shadow: 0 0 0 3px rgba(185, 28, 28, 0.1);
    }

    .error-message {
      color: #b91c1c;
      font-size: 0.8rem;
      margin-top: 0.25rem;
      display: none;
    }

    textarea { min-height: 100px; resize: vertical; }

    /* Radio & Checkbox Groups */
    .option-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-top: 0.35rem;
    }

    .option-group label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 400;
      cursor: pointer;
    }

    .option-group input[type="radio"],
    .option-group input[type="checkbox"] {
      width: 18px;
      height: 18px;
      accent-color: #0f3460;
    }

    /* Rating Scale */
    .rating-scale {
      display: flex;
      gap: 0.5rem;
      margin-top: 0.35rem;
    }

    .rating-scale label {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.25rem;
      cursor: pointer;
      padding: 0.5rem 0.75rem;
      border: 1px solid #e5e5e5;
      border-radius: 6px;
      font-weight: 400;
      font-size: 0.85rem;
      transition: all 0.15s;
    }

    .rating-scale input:checked + span,
    .rating-scale label:has(input:checked) {
      background: #e8f0fe;
      border-color: #0f3460;
      color: #0f3460;
    }

    .rating-scale input { display: none; }

    /* Form Sections */
    .form-section {
      margin-bottom: 2.5rem;
    }

    .form-section h2 {
      font-size: 1.25rem;
      margin-bottom: 1.25rem;
    }

    /* Two Column Layout */
    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    /* Submit Button */
    .btn-submit {
      display: inline-block;
      padding: 0.75rem 2rem;
      background: #1a1a2e;
      color: #ffffff;
      border: none;
      border-radius: 6px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s;
    }

    .btn-submit:hover { background: #16213e; }
    .btn-submit:disabled { background: #a3a3a3; cursor: not-allowed; }

    /* Progress Bar (multi-step) */
    .form-progress {
      display: flex;
      justify-content: space-between;
      margin-bottom: 2rem;
      position: relative;
    }

    .form-progress::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 2px;
      background: #e5e5e5;
      z-index: 0;
    }

    .form-progress .step {
      position: relative;
      z-index: 1;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #e5e5e5;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
      font-weight: 600;
      color: #525252;
    }

    .form-progress .step.active { background: #0f3460; color: white; }
    .form-progress .step.completed { background: #0d7c3d; color: white; }

    /* Conditional sections */
    .conditional { display: none; }
    .conditional.visible { display: block; }

    @media (max-width: 600px) {
      .form-row { grid-template-columns: 1fr; }
      .rating-scale { flex-wrap: wrap; }
    }

    @media print {
      input, select, textarea { border: 1px solid #999; }
      .btn-submit { display: none; }
    }
  </style>
</head>
<body>
  <div class="document">
    <div class="cover">
      <h1>{{FORM_TITLE}}</h1>
      <p class="subtitle">{{FORM_DESCRIPTION}}</p>
    </div>

    <div class="document-body">
      <form id="mainForm" novalidate>

        <!-- Section 1 -->
        <div class="form-section">
          <h2>Contact Information</h2>
          <div class="form-row">
            <div class="form-group">
              <label>First Name <span class="required">*</span></label>
              <input type="text" name="firstName" required>
              <div class="error-message">First name is required</div>
            </div>
            <div class="form-group">
              <label>Last Name <span class="required">*</span></label>
              <input type="text" name="lastName" required>
              <div class="error-message">Last name is required</div>
            </div>
          </div>
          <div class="form-group">
            <label>Email <span class="required">*</span></label>
            <input type="email" name="email" required>
            <div class="error-message">Please enter a valid email</div>
          </div>
        </div>

        <!-- Add more sections as needed -->

        <button type="submit" class="btn-submit">Submit</button>

      </form>
    </div>
  </div>

  <script>
    // Validation
    document.getElementById('mainForm').addEventListener('submit', function(e) {
      e.preventDefault();
      let valid = true;
      this.querySelectorAll('[required]').forEach(field => {
        const errorMsg = field.parentElement.querySelector('.error-message');
        if (!field.value.trim()) {
          field.classList.add('error');
          if (errorMsg) errorMsg.style.display = 'block';
          valid = false;
        } else {
          field.classList.remove('error');
          if (errorMsg) errorMsg.style.display = 'none';
        }
      });
      // Email validation
      const email = this.querySelector('[type="email"]');
      if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        email.classList.add('error');
        email.parentElement.querySelector('.error-message').style.display = 'block';
        valid = false;
      }
      if (valid) {
        const data = Object.fromEntries(new FormData(this));
        console.log('Form data:', data);
        alert('Form submitted successfully!');
      }
    });

    // Conditional logic helper
    function toggleConditional(triggerName, triggerValue, targetId) {
      document.querySelectorAll(`[name="${triggerName}"]`).forEach(el => {
        el.addEventListener('change', function() {
          const target = document.getElementById(targetId);
          target.classList.toggle('visible', this.value === triggerValue);
        });
      });
    }
  </script>
</body>
</html>
```

## Field Type Reference

Use these patterns inside form sections:

### Text Input
```html
<div class="form-group">
  <label>Field Label <span class="required">*</span></label>
  <input type="text" name="fieldName" required placeholder="Enter value...">
  <p class="help-text">Optional guidance text</p>
</div>
```

### Dropdown Select
```html
<div class="form-group">
  <label>Category</label>
  <select name="category">
    <option value="">Select one...</option>
    <option value="a">Option A</option>
    <option value="b">Option B</option>
  </select>
</div>
```

### Radio Group
```html
<div class="form-group">
  <label>Preference</label>
  <div class="option-group">
    <label><input type="radio" name="pref" value="a"> Option A</label>
    <label><input type="radio" name="pref" value="b"> Option B</label>
    <label><input type="radio" name="pref" value="c"> Option C</label>
  </div>
</div>
```

### Checkbox Group
```html
<div class="form-group">
  <label>Select all that apply</label>
  <div class="option-group">
    <label><input type="checkbox" name="features" value="x"> Feature X</label>
    <label><input type="checkbox" name="features" value="y"> Feature Y</label>
  </div>
</div>
```

### Rating Scale (1-5)
```html
<div class="form-group">
  <label>How satisfied are you?</label>
  <div class="rating-scale">
    <label><input type="radio" name="rating" value="1"><span>1</span></label>
    <label><input type="radio" name="rating" value="2"><span>2</span></label>
    <label><input type="radio" name="rating" value="3"><span>3</span></label>
    <label><input type="radio" name="rating" value="4"><span>4</span></label>
    <label><input type="radio" name="rating" value="5"><span>5</span></label>
  </div>
  <p class="help-text">1 = Not at all, 5 = Extremely</p>
</div>
```

### Conditional Section
```html
<div class="form-group">
  <label>Do you have a budget?</label>
  <div class="option-group">
    <label><input type="radio" name="hasBudget" value="yes"> Yes</label>
    <label><input type="radio" name="hasBudget" value="no"> No</label>
  </div>
</div>

<div id="budgetDetails" class="conditional">
  <div class="form-group">
    <label>Budget Range</label>
    <select name="budgetRange">
      <option value="">Select range...</option>
      <option value="under5k">Under $5,000</option>
      <option value="5k-25k">$5,000 - $25,000</option>
      <option value="over25k">Over $25,000</option>
    </select>
  </div>
</div>

<script>toggleConditional('hasBudget', 'yes', 'budgetDetails');</script>
```

## File Location

```
Project context:  ./forms/{type}-{subject}.html
No project:       ~/Development/artifacts/{topic}/form-{subject}.html
```

## What NOT to Do

- Do NOT scaffold a Node.js project with pdf-lib for fillable PDFs
- Do NOT create a FormBuilder class or framework
- Do NOT use external CSS/JS frameworks (keep it self-contained)
- Do NOT leave placeholder field names (use real labels)
- Do NOT skip validation for required fields
- Do NOT make forms wider than 820px (matches document foundation)
- Do NOT forget mobile responsiveness
