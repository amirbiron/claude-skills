---
name: tech-guide-design
description: Comprehensive design system for creating technical guides and documentation with modern dark-themed aesthetic. Use when creating technical tutorials, documentation pages, API guides, system architecture documents, or any Hebrew RTL technical content requiring professional styling with code blocks, tables, alerts, badges, and interactive components.
---

# Technical Guide Design System

מערכת עיצוב מקיפה ליצירת מדריכים טכניים ותיעוד עם אסתטיקה מודרנית כהה.

## Color Palette

### Primary Colors
- **Primary**: `#0088cc` - כותרות H2, קישורים, כפתורים ראשיים
- **Secondary**: `#2ecc71` - כותרות H3, הודעות הצלחה
- **Warning**: `#f39c12` - כותרות H4, אזהרות
- **Danger**: `#e74c3c` - שגיאות קריטיות, התראות חמורות
- **Purple**: `#9b59b6` - אנומליות, סטטוס מיוחד

### Background Colors
- **Page Background**: `linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%)`
- **Card/Section Background**: `#16213e`
- **Code Background**: `#0f0f23` (כהה יותר)
- **Border Color**: `#3d5a80`

### Text Colors
- **Primary Text**: `#eee` (לבן-שבור)
- **Secondary Text**: opacity 0.8-0.9
- **Code Text**: `#7fdbca` (inline code)
- **Code Block Text**: `#c3cee3`

### Syntax Highlighting
```css
.comment { color: #6a9955; }     /* ירוק זית */
.keyword { color: #c586c0; }     /* סגול */
.string { color: #ce9178; }      /* כתום */
.function { color: #dcdcaa; }    /* צהוב */
.variable { color: #9cdcfe; }    /* כחול בהיר */
.number { color: #b5cea8; }      /* ירוק בהיר */
.operator { color: #d4d4d4; }    /* אפור בהיר */
```

## CSS Variables Template

Always start with CSS variables in `:root`:

```css
:root {
    --primary-color: #0088cc;
    --secondary-color: #2ecc71;
    --warning-color: #f39c12;
    --danger-color: #e74c3c;
    --dark-bg: #1a1a2e;
    --card-bg: #16213e;
    --text-color: #eee;
    --code-bg: #0f0f23;
    --border-color: #3d5a80;
}
```

## Layout Structure

### General Layout
- **Direction**: `dir="rtl"` (עברית)
- **Container Width**: `max-width: 1200px` ממורכז
- **Font Family**: 'Segoe UI', Tahoma, Arial, sans-serif
- **Line Height**: `1.8` (קריאות מיטבית)
- **Spacing**: `40px` בין sections, `20px` בין אלמנטים

### Body Styling
```css
body {
    font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
    background: linear-gradient(135deg, var(--dark-bg) 0%, #0f0f23 100%);
    color: var(--text-color);
    line-height: 1.8;
    min-height: 100vh;
}
```

## Header Component

### Styling
- **Padding**: `60px 20px`
- **Background**: `linear-gradient(135deg, #0088cc 0%, #005577 100%)`
- **Border Radius**: `0 0 30px 30px` (פינות עגולות רק בתחתית)
- **Box Shadow**: `0 10px 40px rgba(0, 136, 204, 0.3)`

### Typography
- **H1**: `2.8em` עם `text-shadow: 2px 2px 4px rgba(0,0,0,0.3)`
- **Subtitle**: `1.3em` עם `opacity: 0.9`

### Example
```css
header {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #005577 100%);
    margin-bottom: 40px;
    border-radius: 0 0 30px 30px;
    box-shadow: 0 10px 40px rgba(0, 136, 204, 0.3);
}
```

## Section/Card Components

### Standard Section
- **Background**: `#16213e`
- **Border**: `1px solid #3d5a80`
- **Border Radius**: `15px`
- **Padding**: `35px`
- **Margin Bottom**: `30px`
- **Box Shadow**: `0 5px 25px rgba(0,0,0,0.3)`

### Example
```css
section {
    background: var(--card-bg);
    border-radius: 15px;
    padding: 35px;
    margin-bottom: 30px;
    border: 1px solid var(--border-color);
    box-shadow: 0 5px 25px rgba(0,0,0,0.3);
}
```

## Typography Hierarchy

### H2 (Main Headings)
```css
h2 {
    color: var(--primary-color);
    font-size: 1.8em;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 3px solid var(--primary-color);
    display: flex;
    align-items: center;
    gap: 15px;
}
```
- Icon size: `1.2em`
- Border bottom: `3px solid`

### H3 (Secondary Headings)
```css
h3 {
    color: var(--secondary-color);
    font-size: 1.3em;
    margin: 25px 0 15px 0;
}
```

### H4 (Tertiary Headings)
```css
h4 {
    color: var(--warning-color);
    margin: 20px 0 10px 0;
}
```

## Code Components

### Inline Code
```css
code {
    background: var(--code-bg);
    padding: 3px 8px;
    border-radius: 5px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
    color: #7fdbca;
}
```

### Code Blocks
```css
pre {
    background: var(--code-bg);
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
    margin: 20px 0;
    border: 1px solid var(--border-color);
    direction: ltr;
    text-align: left;
}

pre code {
    padding: 0;
    background: none;
    color: #c3cee3;
    line-height: 1.6;
}
```

**Important**: Code blocks always have `direction: ltr` and `text-align: left`.

## Table Components

### Structure
```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: var(--code-bg);
    border-radius: 10px;
    overflow: hidden;
}

th, td {
    padding: 15px;
    text-align: right;
    border-bottom: 1px solid var(--border-color);
}

th {
    background: var(--primary-color);
    color: white;
    font-weight: 600;
}

tr:hover {
    background: rgba(0, 136, 204, 0.1);
}
```

## Alert Boxes

### Structure
- **Layout**: Flexbox עם gap `15px`
- **Padding**: `20px`
- **Border Radius**: `10px`
- **Border Right**: `4px solid` (צבע לפי סוג)
- **Icon**: Emoji בגודל `1.5em` - `2em`

### Alert Types

#### Info Alert
```css
.alert-info {
    background: rgba(0, 136, 204, 0.15);
    border-right: 4px solid var(--primary-color);
}
/* Icon: 💡 or ℹ️ */
```

#### Success Alert
```css
.alert-success {
    background: rgba(46, 204, 113, 0.15);
    border-right: 4px solid var(--secondary-color);
}
/* Icon: ✅ */
```

#### Warning Alert
```css
.alert-warning {
    background: rgba(243, 156, 18, 0.15);
    border-right: 4px solid var(--warning-color);
}
/* Icon: ⚠️ */
```

#### Danger Alert
```css
.alert-danger {
    background: rgba(231, 76, 60, 0.15);
    border-right: 4px solid var(--danger-color);
}
/* Icon: ❌ */
```

### Example HTML
```html
<div class="alert-box alert-info">
    <span style="font-size: 1.5em;">💡</span>
    <div>
        <strong>טיפ:</strong> תוכן ההתראה כאן
    </div>
</div>
```

## Badge Components

### Styling
```css
.badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: bold;
    color: white;
    margin: 5px 5px 5px 0;
}

.badge-primary { background: #0088cc; }
.badge-success { background: #2ecc71; }
.badge-warning { background: #f39c12; }
.badge-danger { background: #e74c3c; }
.badge-purple { background: #9b59b6; }
```

**Key Features**:
- צורת גלולה (pill shape)
- צבע רקע מלא (לא שקוף)
- טקסט לבן תמיד

## Grid System

### CSS Grid Layout
```css
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}
```

### Feature Cards (inside Grid)
```css
.feature-card {
    background: var(--code-bg);
    padding: 25px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
}
```

## Special Components

### Architecture Diagrams
```css
.architecture-diagram {
    background: var(--code-bg);
    padding: 30px;
    border-radius: 15px;
    margin: 25px 0;
    direction: ltr;
    text-align: center;
    font-family: monospace;
    font-size: 0.95em;
    line-height: 1.4;
    overflow-x: auto;
    white-space: pre;
}
```

### File Tree
```css
.file-tree {
    background: var(--code-bg);
    padding: 20px;
    border-radius: 10px;
    font-family: monospace;
    direction: ltr;
    text-align: left;
}

.file-tree .folder { color: #f39c12; }
.file-tree .file { color: #3498db; }
```

### Table of Contents
```css
.toc {
    background: var(--code-bg);
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 30px;
}

.toc ul {
    list-style: none;
    margin: 0;
}

.toc li {
    padding: 8px 0;
    border-bottom: 1px solid var(--border-color);
}

.toc a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.3s;
}

.toc a:hover {
    color: var(--secondary-color);
}
```

### API Endpoint Cards
```css
.endpoint-card {
    background: var(--code-bg);
    border-radius: 10px;
    margin: 15px 0;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.endpoint-header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    background: rgba(0, 136, 204, 0.1);
}

.method {
    padding: 5px 12px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 0.85em;
}

.method-get { background: #2ecc71; color: white; }
.method-post { background: #3498db; color: white; }

.endpoint-path {
    font-family: monospace;
    color: var(--text-color);
    direction: ltr;
}
```

## Responsive Design

### Mobile Breakpoint (max-width: 768px)
```css
@media (max-width: 768px) {
    header h1 {
        font-size: 2em;
    }

    section {
        padding: 20px;
    }

    .grid-2 {
        grid-template-columns: 1fr;
    }
}
```

## Lists

### Styling
```css
ul, ol {
    margin: 15px 30px;
    line-height: 1.8;
}

li {
    margin: 8px 0;
}
```

## Usage Instructions

### Document Structure Template
```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מדריך טכני</title>
    <style>
        /* Include all CSS variables and styles */
    </style>
</head>
<body>
    <header>
        <h1>כותרת המדריך</h1>
        <p>תיאור קצר</p>
        <div>
            <span class="badge badge-primary">טכנולוגיה 1</span>
            <span class="badge badge-success">טכנולוגיה 2</span>
        </div>
    </header>

    <div class="container">
        <nav class="toc">
            <h3>תוכן עניינים</h3>
            <ul>
                <li><a href="#section1">1. נושא ראשון</a></li>
            </ul>
        </nav>

        <section id="section1">
            <h2><span class="icon">📊</span> נושא ראשון</h2>
            <!-- Content here -->
        </section>
    </div>
</body>
</html>
```

### Key Principles

1. **Always use RTL**: `dir="rtl"` on `<html>` element
2. **CSS Variables First**: Define all colors as CSS variables
3. **Semantic HTML**: Use proper HTML5 semantic elements
4. **Code Direction**: All code blocks should be `ltr`
5. **Consistent Spacing**: Follow spacing guidelines strictly
6. **Icon Integration**: Use emojis in H2 headings (optional but recommended)
7. **Progressive Enhancement**: Mobile-first responsive design

### Common Patterns

#### Pattern 1: Section with Alert
```html
<section id="overview">
    <h2><span class="icon">📊</span> סקירה כללית</h2>
    <p>תוכן הסקירה...</p>

    <div class="alert-box alert-info">
        <span style="font-size: 1.5em;">💡</span>
        <div>
            <strong>טיפ:</strong> מידע שימושי
        </div>
    </div>
</section>
```

#### Pattern 2: Grid with Feature Cards
```html
<div class="grid-2">
    <div class="feature-card">
        <h4>תכונה 1</h4>
        <p>תיאור התכונה</p>
    </div>
    <div class="feature-card">
        <h4>תכונה 2</h4>
        <p>תיאור התכונה</p>
    </div>
</div>
```

#### Pattern 3: Code Block with Syntax Highlighting
```html
<pre><code><span class="comment"># Comment</span>
<span class="keyword">def</span> <span class="function">example</span>():
    <span class="variable">result</span> = <span class="string">"Hello"</span>
    <span class="keyword">return</span> result</code></pre>
```

## Best Practices

1. **Token Efficiency**: Keep inline styles minimal, use CSS classes
2. **Readability**: Maintain high contrast and generous spacing
3. **Consistency**: Use the same patterns throughout the document
4. **Accessibility**: Ensure proper color contrast and semantic HTML
5. **Performance**: Minimize inline styles, use CSS variables
6. **Maintainability**: Clear class naming, logical structure

## When NOT to Use This Skill

- Simple text documents without code or technical content
- Forms or interactive applications (use webapp skills instead)
- Print-optimized documents (this is screen-optimized)
- Light-themed documentation (this is dark-themed)