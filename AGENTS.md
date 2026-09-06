# Fotoclub Beeldspraak Website - Development Guidelines

## Overview

This document defines all governing guidelines for page layouts, tool usage, and complexity management for the Fotoclub Beeldspraak website. The site is built using Jekyll static site generator and deployed on GitHub Pages.

---

## 1. Technology Stack & Tool Usage

### 1.1 Core Technologies
- **Static Site Generator**: Jekyll 4.x (GitHub Pages compatible)
- **Markdown Processor**: kramdown (configured in `_config.yml`)
- **Template Language**: Liquid templating
- **CSS**: Vanilla CSS with CSS custom properties (variables)
- **JavaScript**: Vanilla ES5 for maximum compatibility
- **Hosting**: GitHub Pages

### 1.2 Required Tools
- Git for version control
- Jekyll for local development and testing
- Text editor with Liquid syntax support recommended

### 1.3 Build Configuration
```yaml
# _config.yml settings that must be maintained:
- markdown: kramdown
- theme: null (custom theme)
- baseurl: "" (root deployment)
- url: "https://beeldspraak.github.io"
- collections: pages (output: true, permalink: /:path/)
```

### 1.4 Plugin Compatibility
- Only use plugins supported by GitHub Pages
- Currently approved: `jekyll-feed`
- Avoid plugins that require external dependencies not available on GitHub Pages

---

## 2. File Structure & Organization

### 2.1 Directory Structure
```
.
├── _config.yml              # Site configuration
├── _data/                  # Data files (YAML)
│   └── nav_photos.yml      # Navigation photo gallery data
├── _includes/              # Reusable components
│   ├── head.html           # HEAD section
│   ├── header.html         # Site header/banner
│   ├── footer.html         # Site footer
│   ├── nav.html            # Main navigation
│   └── nav_photos.html     # Navigation photos component
├── _layouts/               # Page templates
│   ├── default.html        # Base layout
│   └── page.html           # Page-specific layout
├── assets/                 # Static assets
│   ├── images/             # Production images (web-optimized)
│   └── files/              # Downloadable files
├── assets/images - original/ # Original high-res images (EXCLUDED from git)
├── css/                    # Stylesheets
│   └── style.css           # Main stylesheet
├── js/                     # JavaScript
│   └── main.js             # Main functionality
├── pages/                  # Content pages (collection)
│   └── *.md                # Page content in Markdown
├── index.md                # Homepage
└── AGENTS.md               # This file
```

### 2.2 File Naming Conventions
- **Pages**: Use lowercase with hyphens (`contact.md`, `foto-van-de-maand.md`)
- **Images**: Use descriptive names with hyphens, include photographer credit
- **CSS/JS**: Use lowercase with hyphens
- **Data files**: Use snake_case for YAML files (`nav_photos.yml`)

### 2.3 Git Ignore Rules
- `/assets/images - original/` - Original high-resolution images excluded from repository
- Build artifacts and cache directories (handled by Jekyll defaults)

---

## 3. Page Layouts & Templates

### 3.1 Layout Hierarchy

#### 3.1.1 Default Layout (`_layouts/default.html`)
- **Purpose**: Base template for all pages
- **Structure**:
  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>          <!-- head.html include -->
  <body>
    <header>     <!-- header.html include -->
    <div class="layout">
      <div class="layout-nav">
        <nav>    <!-- nav.html include -->
        <nav>    <!-- nav_photos.html include -->
      </div>
      <main>     <!-- content -->
    </div>
    <footer>     <!-- footer.html include -->
    <modal>      <!-- Image lightbox -->
    <script>     <!-- main.js -->
  ```

#### 3.1.2 Page Layout (`_layouts/page.html`)
- **Purpose**: Standard page template
- **Inherits**: default.html
- **Adds**: Page title as `<h2>` heading
- **Content**: Page content with `<h2>{{ page.title }}</h2>` followed by `{{ content }}`

### 3.2 Layout Assignment Rules
- **Homepage** (`index.md`): Uses `layout: default`
- **Content pages** (`pages/*.md`): Use `layout: page`
- **Front matter required**: title, layout
- **Optional front matter**: description, categories, tags

### 3.3 Layout Constraints
- **Do not create new layouts** without documented justification
- **All new pages** must use existing layouts
- **Custom layouts** require approval and must follow the same pattern

---

## 4. Navigation System

### 4.1 Navigation Structure
- **Primary navigation**: Vertical sidebar (left column)
- **Secondary navigation**: Nested sub-menus (hidden by default, shown on parent active)
- **Mobile**: Hamburger menu with off-canvas navigation

### 4.2 Navigation Implementation
- **Location**: `_includes/nav.html`
- **Pattern**: Manual HTML with Liquid conditionals for active states
- **Active state logic**: Uses `page.url contains 'substring'` for matching
- **Nested menus**: CSS-controlled visibility (adjacent sibling selector)

### 4.3 Navigation Photo Gallery
- **Data source**: `_data/nav_photos.yml`
- **Component**: `_includes/nav_photos.html`
- **Image location**: `/assets/images/content/navigation/`
- **Display**: 1-3 recommended photos, responsive grid
- **Format**: YAML array with filename, title, credit

### 4.4 Navigation Rules
- **Add new pages**: Update `_includes/nav.html` manually
- **Sub-pages**: Nest under parent `<li>` with `<ul>` for dropdown
- **Active states**: Use consistent pattern: `{%- if page.url contains 'pagename' %}active{%- endif %}`
- **Mobile behavior**: Auto-close on link click, close on viewport resize to desktop

---

## 5. Component Architecture

### 5.1 Includes (Reusable Components)

#### 5.1.1 head.html
- **Purpose**: HEAD section with meta tags and stylesheet
- **Required elements**: charset, title, viewport, CSS link
- **Template**: `{{ page.title | default: site.title }}`

#### 5.1.2 header.html
- **Purpose**: Site header with banner
- **Content**: Permanent banner image
- **Image**: `/assets/images/permanent/beeldspraak_banner.png`
- **Behavior**: Responsive width (100% of layout, max-width: 1200px)

#### 5.1.3 footer.html
- **Purpose**: Site footer with copyright and links
- **Links required**: Privacyverklaring, Cookiebeleid
- **File paths**: Must use relative_url filter

#### 5.1.4 nav.html
- **Purpose**: Main navigation structure
- **Elements**: Mobile toggle button, navigation tree, overlay
- **IDs required**: navToggle, nav, navOverlay

#### 5.1.5 nav_photos.html
- **Purpose**: Navigation photo gallery
- **Data binding**: Uses site.data.nav_photos.photos
- **Fallback**: Graceful degradation if data missing

### 5.2 Component Rules
- **Do not duplicate** component logic
- **All includes** must be self-contained
- **Data dependencies** must be clearly documented
- **IDs and classes** must be consistent across components

---

## 6. Styling Guidelines

### 6.1 CSS Architecture
- **File**: `/css/style.css` (single file approach)
- **Methodology**: CSS custom properties with logical grouping
- **Organization**: Section comments with clear separators

### 6.2 CSS Variables (Design Tokens)
```css
:root {
  --bg: #f5f5f5;           /* Background color */
  --fg: #222;             /* Text color */
  --panel: #fff;           /* Panel background */
  --accent: #b22222;      /* Accent color (maroon) */
  --link: #0055aa;        /* Link color */
  --nav-bg: #8a8a8a;      /* Navigation background */
  --nav-fg: #eee;         /* Navigation text */
  --nav-active: #b22222;  /* Active navigation indicator */
  --border: #ddd;         /* Border color */
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.08); /* Box shadow */
}
```

### 6.3 Color Usage
- **Primary brand color**: `#b22222` (maroon) - used for headings and accents
- **Headers**: All heading levels (h1-h6) use accent color
- **Links**: `#0055aa` (blue) for content links
- **Background**: `#f5f5f5` (light gray) for body
- **Content panels**: `#fff` (white) with shadow

### 6.4 Layout System

#### 6.4.1 Two-Column Layout
- **Container**: `.layout` (max-width: 1200px)
- **Grid**: `grid-template-columns: 220px minmax(0, 1fr)`
- **Navigation column**: `.layout-nav` (220px fixed)
- **Content column**: `.content` (flexible)
- **Gap**: 2rem between columns

#### 6.4.2 Content Area
- **Background**: var(--panel) with shadow
- **Padding**: 1.5rem (desktop), 1.1rem (mobile)
- **Minimum height**: 60vh (desktop), 50vh (mobile)
- **Border radius**: 4px

#### 6.4.3 Navigation Styling
- **Background**: var(--nav-bg)
- **Text**: var(--nav-fg)
- **Hover**: Darker background (#333)
- **Active**: Darker background (#2c2c2c) with accent border
- **Nested**: Different background (#7a7a7a), shown only when parent active

### 6.5 Responsive Breakpoints
- **Tablet**: 801-1024px - narrower navigation column (180px)
- **Mobile**: <=800px - single column, hamburger menu
- **Extra small**: <=380px - tighter padding, smaller fonts

### 6.6 Mobile-Specific Styles
- **Navigation**: Off-canvas, transforms from left (-100%)
- **Overlay**: Semi-transparent backdrop (rgba(0,0,0,0.45))
- **Toggle button**: Hamburger icon with CSS transitions
- **Touch targets**: Minimum 44px height for navigation links
- **Content**: Full width, reduced padding
- **Navigation photos**: Hidden on mobile

### 6.7 Image Handling
- **Content images**: max-width: 100%, height: auto, border-radius: 4px
- **Banner images**: width: 100%, height: auto
- **Modal images**: max-width: 90vw, max-height: 80vh
- **All images**: cursor: pointer (for lightbox)

### 6.8 Typographic Scale
- **Body**: system-ui font stack, line-height: 1.6
- **Headings**: Color: var(--accent) (#b22222)
- **h2 in content**: Margin-top: 0, border-bottom: 1px solid var(--border)
- **h3 in content**: Margin-top: 1.2rem, border-bottom: 1px solid var(--border)
- **Mobile h2**: 1.3rem, mobile h3: 1.05rem

### 6.9 CSS Rules
- **Use CSS variables** for all colors and recurring values
- **Avoid !important** - use specific selectors instead
- **Box-sizing**: border-box on all elements
- **Flexbox/Grid**: Preferred over floats for layout
- **Transitions**: Use for interactive elements (0.15s-0.25s duration)

---

## 7. JavaScript Guidelines

### 7.1 Architecture
- **File**: `/js/main.js` (single file, self-contained)
- **Pattern**: IIFE (Immediately Invoked Function Expression) for scope isolation
- **Compatibility**: ES5 for maximum browser support

### 7.2 Core Functionality

#### 7.2.1 Mobile Navigation
- **Elements**: navToggle, nav, navOverlay
- **Functions**: openNav(), closeNav(), toggleNav()
- **Behavior**:
  - Toggle on button click
  - Close on overlay click
  - Close on link click (mobile only)
  - Close on viewport resize to desktop
- **ARIA**: Update aria-expanded attribute
- **Body scroll**: Prevent when navigation open

#### 7.2.2 Image Lightbox/Modal
- **Elements**: imageModal, modalOverlay, modalImage, modalCaption, modalClose, modalPrev, modalNext
- **Functions**:
  - openModal(index) - Open with specific image
  - closeModal() - Close the modal
  - updateModalContent() - Update image and caption
  - updateNavButtons() - Enable/disable navigation
  - navPrev() - Navigate to previous image
  - navNext() - Navigate to next image
  - handleKeyDown(e) - Keyboard navigation
  - collectPageImages() - Collect all images from content
  - getCaptionForImage(img) - Extract caption from DOM
  - initImageLightbox() - Initialize on page load
- **Keyboard support**:
  - Escape: Close modal
  - ArrowLeft: Previous image
  - ArrowRight: Next image
- **Content collection**: All `<img>` elements in #content
- **Caption detection**: Next sibling with .photo-caption, .caption, or non-empty div

### 7.3 JavaScript Rules
- **Vanilla JS only** - no frameworks or libraries
- **Progressive enhancement** - works without JavaScript
- **Event listeners**: Clean up when no longer needed
- **Error handling**: Graceful degradation on missing elements
- **Browser compatibility**: Works on file:// protocol
- **Performance**: Efficient DOM queries, cache references

### 7.4 DOM IDs (Required for JavaScript)
```javascript
// Navigation
navToggle     // Mobile toggle button
nav           // Navigation element
navOverlay    // Navigation overlay

// Modal
imageModal    // Modal container
modalOverlay  // Modal overlay
modalImage    // Modal image element
modalCaption  // Modal caption element
modalClose    // Close button
modalPrev     // Previous button
modalNext     // Next button

// Content
content       // Main content area (for image collection)
```

---

## 8. Content & Markdown Guidelines

### 8.1 Markdown Processing
- **Engine**: kramdown (configured in _config.yml)
- **Extensions**: Standard GitHub Pages kramdown configuration
- **HTML in Markdown**: Allowed and encouraged for complex layouts

### 8.2 Content Structure
- **Headings**: Use h2 for page titles (auto-generated by page.html), h3+ for content
- **Images**: Use Liquid for paths: `{{ '/assets/images/path/to/image.jpg' | relative_url }}`
- **Links**: Use relative_url filter for internal links

### 8.3 Common Content Patterns

#### 8.3.1 Photo Highlights
```html
<div class="photo-highlight">
  <img src="{{ '/assets/images/content/image.jpg' | relative_url }}" alt="Description">
  <div class="photo-caption">Caption text</div>
</div>
```

#### 8.3.2 News Lists
```html
<h3>Laatste nieuws</h3>
<div class="news-list">
  - News item 1
  - News item 2
</div>
```

#### 8.3.3 Image with Caption (Lightbox-enabled)
```html
<img src="{{ '/assets/images/content/image.jpg' | relative_url }}" alt="Description">
<div class="photo-caption">Caption &copy; Photographer</div>
```

### 8.4 Front Matter Requirements

#### 8.4.1 Required Front Matter
```yaml
---
layout: page       # or 'default' for homepage
title: Page Title  # Required for all pages
---
```

#### 8.4.2 Optional Front Matter
```yaml
---
layout: page
title: Page Title
description: SEO description
categories:
  - category1
  - category2
tags:
  - tag1
  - tag2
---
```

---

## 9. Complexity Management

### 9.1 Component Complexity Limits
- **Single Responsibility**: Each include file should have one clear purpose
- **Max lines per include**: 200 lines (nav.html is exception at ~100 lines due to manual structure)
- **CSS file size**: style.css should remain under 500 lines
- **JS file size**: main.js should remain under 200 lines

### 9.2 Nesting Limits
- **Navigation depth**: Maximum 2 levels (parent + children)
- **Component includes**: Maximum 1 level deep (layout includes components directly)
- **CSS specificity**: Avoid deeply nested selectors (>3 levels)

### 9.3 Performance Constraints
- **Image optimization**: All production images must be web-optimized
- **Image formats**: Use JPEG for photos, PNG for graphics with transparency
- **Image sizes**: Navigation photos max 400px width, content images max 1200px width
- **File sizes**: Individual images under 500KB, total page weight under 2MB

### 9.4 Asset Management
- **Originals**: Store in `/assets/images - original/` (git ignored)
- **Production**: Web-optimized versions in `/assets/images/`
- **Naming**: Consistent naming between original and production versions
- **Compression**: Use tools like ImageOptim, TinyPNG, or equivalent

---

## 10. Responsive Design Principles

### 10.1 Breakpoint Strategy
- **Mobile-first**: Styles cascade from mobile to desktop
- **Breakpoints**:
  - <=380px: Extra small phones
  - <=800px: Mobile (hamburger menu)
  - <=1024px: Tablet (narrower navigation)
  - >1024px: Desktop

### 10.2 Responsive Patterns
- **Layout**: Grid changes from single column to two-column
- **Navigation**: Off-canvas to vertical sidebar
- **Images**: Flexible sizing with max-width constraints
- **Typography**: Font sizes scale with viewport
- **Spacing**: Padding and gaps reduce on smaller screens

---

## 11. Accessibility Guidelines

### 11.1 ARIA Requirements
- **Navigation toggle**: aria-expanded, aria-controls
- **Modal**: aria-hidden (implicit via display: none/block)
- **Images**: Always include alt text
- **Forms**: Proper label associations

### 11.2 Keyboard Navigation
- **All interactive elements** must be keyboard accessible
- **Modal**: Escape to close, arrow keys for navigation
- **Focus management**: Logical tab order
- **Skip links**: Not currently implemented (consider for future)

### 11.3 Color Contrast
- **Text on background**: Minimum 4.5:1 ratio
- **Text on accent**: Ensure readability
- **Links**: Clear visual distinction from body text

### 11.4 Semantic HTML
- **Use proper elements**: nav, main, footer, header
- **Headings**: Hierarchical structure (h1 > h2 > h3)
- **Lists**: Use ul/ol for navigation and lists
- **Buttons**: Use button element for interactive actions

---

## 12. Performance Guidelines

### 12.1 GitHub Pages Constraints
- **Repository size**: Under 1GB (recommended under 100MB)
- **Build time**: Under 10 minutes
- **Page weight**: Individual pages under 2MB
- **Bandwidth**: Consider users on slow connections

### 12.2 Optimization Strategies
- **Image compression**: Essential for photo-heavy site
- **CSS/JS minification**: Not required (GitHub Pages handles)
- **Lazy loading**: Consider for below-the-fold images
- **Caching**: Leverage browser caching for static assets

---

## 13. Data Management

### 13.1 Data Files
- **Location**: `_data/` directory
- **Format**: YAML (.yml extension)
- **Naming**: snake_case for filenames

### 13.2 Current Data Files
- **nav_photos.yml**: Navigation photo gallery configuration

### 13.3 Data File Rules
- **Validation**: Always validate YAML syntax
- **Backups**: Critical data should be version controlled
- **Documentation**: Include comments explaining data structure

---

## 14. Deployment Guidelines

### 14.1 GitHub Pages Deployment
- **Branch**: gh-pages or main (configured in settings)
- **Domain**: beeldspraak.github.io
- **Build**: Automatic on push to configured branch
- **Custom domain**: Not currently configured

### 14.2 Local Development
- **Serve**: `bundle exec jekyll serve`
- **Watch**: Auto-regeneration enabled
- **Port**: Default 4000
- **Base URL**: Empty string for root deployment

### 14.3 Testing Checklist
- [ ] All internal links work
- [ ] All images display correctly
- [ ] Navigation works on desktop and mobile
- [ ] Lightbox works for all images
- [ ] Keyboard navigation works
- [ ] Responsive breakpoints function
- [ ] Build completes without errors

---

## 15. Maintenance & Evolution

### 15.1 Backlog Management
- **File**: BACKLOG.md contains prioritized improvements
- **Review**: Regular review of backlog items
- **Prioritization**: Based on user impact and implementation effort

### 15.2 Current Technical Debt
- Automatic image resizing/thumbnails
- Automated data-driven navigation
- Agenda as data with .ics generation
- Working contact form integration
- Site search functionality
- Sitemap and SEO improvements
- Paginated archives
- Tagged/categorized photo pages
- Custom 404 page
- CI checks for build and link validation

### 15.3 Change Management
- **Document all changes** in commit messages
- **Test locally** before pushing
- **Update guidelines** when patterns change
- **Maintain backward compatibility**

---

## 16. File Templates

### 16.1 New Page Template
```markdown
---
layout: page
title: Page Title
---

<content in markdown or HTML>
```

### 16.2 New Navigation Entry
```html
<li>
  <a href="{{ '/pages/pagename' | relative_url }}" class="{%- if page.url contains 'pagename' %}active{%- endif %}">Page Name</a>
</li>
```

### 16.3 New Navigation Entry with Subpages
```html
<li>
  <a href="{{ '/pages/parent' | relative_url }}" class="{%- if page.url contains 'parent' %}active{%- endif %}">Parent Page</a>
  <ul>
    <li><a href="{{ '/pages/parent/child' | relative_url }}" class="{%- if page.url contains 'child' %}active{%- endif %}">Child Page</a></li>
  </ul>
</li>
```

---

## 17. Troubleshooting Guide

### 17.1 Common Issues

#### 17.1.1 Broken Links
- **Cause**: Incorrect file paths or missing files
- **Solution**: Use relative_url filter, verify file exists
- **Check**: `site.pages` in Liquid for debugging

#### 17.1.2 Missing Images
- **Cause**: File not in correct location or wrong path
- **Solution**: Verify image exists in `/assets/images/`, use correct path

#### 17.1.3 Navigation Not Showing Active State
- **Cause**: URL matching logic incorrect
- **Solution**: Check `page.url contains 'substring'` pattern

#### 17.1.4 Lightbox Not Working
- **Cause**: Missing IDs or JavaScript errors
- **Solution**: Verify all required IDs exist, check browser console

#### 17.1.5 Mobile Navigation Not Opening
- **Cause**: JavaScript not loading or DOM elements missing
- **Solution**: Check IDs match JavaScript, verify script tag in layout

### 17.2 Debugging Tools
- Browser Developer Tools (Chrome/Firefox)
- Jekyll serve with --livereload
- YAML validator for data files
- HTML validator for markup

---

## 18. Version History

This guidelines document is maintained as the project evolves. Significant changes should be documented here.

- **v1.0** (2026-09-06): Initial comprehensive guidelines based on existing codebase analysis

---

*This AGENTS.md file serves as the authoritative source for all development guidelines governing the Fotoclub Beeldspraak website. All contributors must adhere to these guidelines to maintain consistency and quality across the codebase.*