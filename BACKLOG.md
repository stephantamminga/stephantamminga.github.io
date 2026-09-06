---
title: BACKLOG - Fotoclub Beeldspraak Website
description: Prioritized list of issues and enhancements with severity, impact, and implementation notes
---

## 🚨 CRITICAL - Must Fix Immediately

### 2. Missing Privacy/Cookie Policy Pages
- **Issue**: Footer links in `_includes/footer.html` lines 5-6 point to non-existent pages
  - `/pages/privacy` - Missing
  - `/pages/cookies` - Missing
- **Impact**: 404 errors, legal compliance risk (GDPR)
- **Solution**: Create `pages/privacy.md` and `pages/cookies.md` with appropriate content
- **Effort**: 2-3 hours (content creation)
- **Dependencies**: Legal review if needed
- **Validation**: Footer links resolve to valid pages

### 3. Lightbox Broken for Markdown Links
- **Issue**: Lightbox in `js/main.js` only attaches to `<img>` elements (lines 156, 161-166). Foto-van-de-maand page uses markdown links (`[text](/path/to/image.jpg)`) which render as `<a>` tags without `<img>`.
- **Impact**: Users cannot view Foto-van-de-maand images in lightbox; inconsistency across site
- **Solution**: Extend `initImageLightbox()` to handle `<a>` tags with image extensions (jpg, jpeg, png, gif) in href. Add logic to collect and display these as images.
- **Files**: `js/main.js`, `pages/foto-van-de-maand.md`
- **Effort**: 2-3 hours
- **Dependencies**: None
- **Validation**: All image links (inline `<img>` and markdown `[text](image.jpg)`) open in lightbox

---

## 🔧 HIGH PRIORITY - System Improvements

### 4. Automated Data-Driven Navigation
- **Issue**: `_includes/nav.html` (93 lines) manually maintained. Contains hardcoded URLs for 65+ pages. Error-prone as site grows.
- **Current State**: Mostly in sync but requires manual updates for every new page
- **Impact**: Maintenance burden, risk of broken links, inconsistent active states
- **Solution**: 
  - Add front matter metadata to pages (e.g., `nav_title:`, `nav_order:`, `nav_parent:`)
  - Create Jekyll plugin or Liquid template to auto-generate navigation from page collection
  - Maintain manual overrides for special cases
- **Effort**: 4-6 hours
- **Dependencies**: None (pure Liquid possible)
- **Validation**: Navigation renders correctly, all links work

### 5. Agenda as Data with Auto-Generated ICS
- **Issue**: Agenda data duplicated across:
  - `pages/agenda-2025-26.md` (markdown table)
  - `pages/agenda-2026-27.md` (markdown table)
  - `assets/files/calender-2025-26.ics` (manual ICS)
  - `assets/files/calender-2026-27.ics` (manual ICS)
- **Impact**: Risk of desync, manual maintenance burden
- **Solution**:
  - Create `_data/agenda.yml` with structured event data
  - Use Jekyll plugin (e.g., `jekyll-icalendar`) or custom Liquid to generate ICS files
  - Generate agenda pages from YAML data
- **Effort**: 4-8 hours
- **Dependencies**: May require `jekyll-icalendar` plugin (check GitHub Pages compatibility)
- **Validation**: ICS files match agenda pages, all dates consistent

### 6. Working Contact Form
- **Issue**: `pages/contact.md` has form with `action="#"` - doesn't work on GitHub Pages (no server-side processing)
- **Current State**: Form exists but non-functional; note warns users
- **Impact**: Users cannot submit contact requests through website
- **Solution**: Integrate with zero-server form service:
  - **Formspree**: Free tier, simple integration (change action to Formspree endpoint)
  - **Formspark**: Alternative, similar approach
  - **Netlify Forms**: Would require moving from GitHub Pages
- **Recommendation**: Formspree (minimal changes, GitHub Pages compatible)
- **Effort**: 1 hour
- **Dependencies**: Formspree account (free)
- **Validation**: Form submission works, confirmation received

### 7. Custom 404 Page
- **Issue**: No custom 404 page exists
- **Impact**: Users see GitHub Pages default 404, poor UX
- **Solution**: Create `404.md` or `404.html` with helpful navigation links
- **Effort**: 1 hour
- **Dependencies**: None
- **Validation**: Visit non-existent URL, see custom page

---

## 📈 MEDIUM PRIORITY - Quality of Life

### 8. Automatic Image Resizing/Thumbnails
- **Issue**: Large images slow page load; Foto-van-de-maand lacks thumbnail grid
- **Current State**: Images manually optimized
- **Impact**: Performance, user experience
- **Solution**:
  - Option A: Use `jekyll-responsive_image` plugin (GitHub Pages compatible?)
  - Option B: Pre-process images with build script (requires local build hooks)
  - Option C: Create thumbnail generation script for Foto-van-de-maand
- **Effort**: 3-5 hours (Option B/C), 1-2 hours (Option A if compatible)
- **Dependencies**: Plugin compatibility check, or script setup
- **Validation**: Images load quickly, thumbnail grid works

### 9. Site Search
- **Issue**: No search functionality for 65+ pages
- **Impact**: Users cannot find content easily
- **Solution**:
  - **Pagefind**: Modern, fast, GitHub Pages compatible
  - **Lunr.js**: Traditional, works but heavier
- **Recommendation**: Pagefind (better performance, easier setup)
- **Effort**: 2-3 hours
- **Dependencies**: Pagefind build step (can run locally before deploy)
- **Validation**: Search returns relevant results for all pages

### 10. Sitemap & SEO Improvements
- **Issue**: No automated sitemap, no Open Graph tags, basic SEO
- **Solution**:
  - Add `jekyll-sitemap` plugin (auto-generates sitemap.xml)
  - Add `jekyll-seo-tag` plugin (auto-generates meta tags, Open Graph)
  - Both are GitHub Pages compatible
- **Effort**: 1 hour
- **Dependencies**: None (both plugins supported by GitHub Pages)
- **Validation**: `/sitemap.xml` exists, pages have proper meta tags

### 11. Paginated Archive
- **Issue**: 21+ fotobespreking pages listed in navigation; growing list becomes unwieldy
- **Impact**: Navigation clutter, page load time
- **Solution**:
  - Implement `jekyll-paginate` for fotobespreking archives
  - Group by year/season with automatic pagination
- **Effort**: 3-4 hours
- **Dependencies**: `jekyll-paginate` plugin (GitHub Pages compatible)
- **Validation**: Archive pages load quickly, navigation clear

---

## 💡 ENHANCEMENTS - Future Considerations

### 12. Tagged/Categorized Photo Pages
- **Issue**: No tag-based browsing for photos
- **Impact**: Hard to find photos by theme/photographer/date
- **Solution**: Use front matter tags to auto-generate index pages
- **Effort**: 2-3 hours
- **Dependencies**: None (pure Jekyll collections)
- **Priority**: Low

### 13. Scheduled "Foto van de Maand"
- **Issue**: foto-van-de-maand.md manually updated; no automatic current/previous logic
- **Impact**: Manual monthly updates
- **Solution**:
  - Add `date` front matter to each foto-van-de-maand entry
  - Create template that auto-selects current month's photo
  - Generate archive of past photos automatically
- **Effort**: 3-4 hours
- **Dependencies**: None
- **Priority**: Low

### 14. Map Embed
- **Issue**: "Over Beeldspraak" page mentions location but no visual map
- **Impact**: Users cannot easily see location
- **Solution**: Add static OpenStreetMap iframe (no cookies, privacy-friendly)
- **Location**: Dorpshuis de Groenenberg, Markeweg 17, Glimmen
- **Effort**: 1 hour
- **Dependencies**: None
- **Priority**: Low
- **Implementation**: Add iframe to `pages/over-beeldspraak.md`

### 15. CI Checks
- **Issue**: No automated validation before deploy
- **Impact**: Broken builds/links may reach production
- **Solution**: GitHub Actions workflow to:
  - Validate Jekyll build
  - Check for broken links (using linkchecker)
  - Validate HTML (optional)
- **Effort**: 2 hours
- **Dependencies**: GitHub Actions setup
- **Priority**: Low

---

## 📊 Implementation Roadmap

### Phase 1: Critical Fixes (Week 1)
- [ ] #1 - Fix broken image references in index.md
- [ ] #2 - Create privacy/cookie policy pages
- [ ] #3 - Fix lightbox for markdown links

### Phase 2: System Improvements (Week 2-3)
- [ ] #4 - Fix contact form (Formspree)
- [ ] #5 - Create 404 page
- [ ] #6 - Automated navigation generation
- [ ] #7 - Agenda as data with ICS generation

### Phase 3: Quality of Life (Week 4+)
- [ ] #8 - Sitemap & SEO plugins
- [ ] #9 - Site search (Pagefind)
- [ ] #10 - Paginated archives

### Phase 4: Enhancements (Ongoing)
- [ ] #11 - Map embed
- [ ] #12 - Image resizing/thumbnails
- [ ] #13 - Tagged photo pages
- [ ] #14 - Scheduled foto van de maand
- [ ] #15 - CI checks

---

## 📋 Notes & Assumptions

### Verified Issues
1. **Broken image references**: Confirmed both `ingang-uitgang-guido-kamp.jpg` and `art-of-broken-glass-margreet-nagelsmit.jpg` do not exist in assets/
2. **Missing privacy/cookie pages**: Confirmed `pages/privacy.md` and `pages/cookies.md` do not exist
3. **Lightbox limitation**: Confirmed `js/main.js` lines 156, 161-166 only handle `<img>` elements
4. **Data inconsistency**: Confirmed `_data/nav_photos.yml` line 10 references `LeonEngels.jpg` but actual file is `LeonEngels.png`

### Current State
- **Total pages**: 65 pages in `pages/` directory
- **Fotobespreking pages**: 21 pages
- **Images**: Navigation PNGs are primary size concern; content images appear optimized
- **Agenda**: Manually maintained in markdown tables and separate ICS files
- **Contact form**: Placeholder form with `action="#"`

### Plugin Compatibility
- **Confirmed GitHub Pages compatible**: `jekyll-feed` (currently used), `jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-paginate`
- **To verify**: `jekyll-icalendar`, `jekyll-responsive_image`

### GitHub Pages Constraints
- Repository size limit: 1GB (recommended <100MB)
- Individual file size limit: 100MB
- Current navigation PNGs total ~13.7MB - significant portion of budget

### Priority Rationale
- **Critical**: Blocks deployment or causes runtime errors
- **High**: Reduces maintenance burden significantly
- **Medium**: Improves user experience and discoverability  
- **Enhancements**: Adds polish but not blocking current functionality