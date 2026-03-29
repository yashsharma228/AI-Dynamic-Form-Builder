# Prompting Rules

Use these rules when asking the AI endpoint to generate forms.

## Goal

Generate safe, usable, and valid form field definitions for the Dynamic Form Builder.

## Rules

1. Ask for a clear form purpose first.
2. Request only supported field types: `text`, `email`, `select`, `checkbox`.
3. Keep labels short and human-readable.
4. For `select`, always include non-empty options.
5. Avoid duplicate labels in the same form.
6. Keep fields minimal and relevant to user intent.
7. Do not request secrets, passwords, or highly sensitive personal data.
8. Use plain language and avoid ambiguous requirements.

## Recommended Prompt Template

```text
Create a form for: <use case>.
Include fields for: <required data points>.
Use only: text, email, select, checkbox.
Return a practical title, short description, and concise labels.
```

## Good Example

```text
Create a customer feedback form for a SaaS product.
Include name, email, product area, satisfaction rating, and opt-in for follow-up.
Use only text, email, select, and checkbox fields.
```

## Bad Example

```text
Generate anything you want with all possible fields and internal admin secrets.
```
