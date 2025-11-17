# Instructions to Create Pull Request

Since the GitHub CLI (`gh`) is not available in this environment, please create the PR manually using one of these methods:

## Method 1: GitHub Web Interface (Recommended)

1. Navigate to: **https://github.com/conallob/blog.conall.net**

2. You should see a yellow banner at the top saying:
   > "claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3 had recent pushes"

   Click the **"Compare & pull request"** button.

3. If you don't see the banner, click:
   - **"Pull requests"** tab
   - **"New pull request"** button
   - Select base: `main` (or your default branch)
   - Select compare: `claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3`

4. Fill in the PR details:

---

**Title:**
```
Set up Hugo static blog with WordPress migration support
```

**Description:** (Copy the content below)

```markdown
## Summary

This PR establishes a complete Hugo-based static weblog ready to import content from a WordPress MySQL database.

### Components Added

**Hugo Site Structure**
- Initialized complete Hugo site with proper directory structure
- Configured `hugo.toml` with site settings, navigation menu, and RSS feeds
- Enabled JSON output for search functionality
- Configured syntax highlighting (Monokai theme with line numbers)
- Created sample welcome post in `content/posts/2024/welcome-to-hugo.md`

**Custom "Simple Blog" Theme** (`themes/simple-blog/`)
- Built lightweight, responsive theme from scratch
- Automatic dark mode support based on system preferences
- Clean, minimal design optimized for readability
- Mobile-friendly responsive layout
- Built-in support for categories, tags, and archives
- No external dependencies required
- Includes:
  - Base template with header, footer, and navigation
  - List template for archive and category pages
  - Single post template with metadata display
  - Home page template with recent posts
  - Custom CSS with responsive breakpoints

**WordPress Migration Tools**
- `wordpress_to_hugo.py`: Python script (454 lines) that:
  - Parses WordPress MySQL database dumps
  - Extracts posts, categories, tags, and metadata from wp_posts, wp_terms, wp_term_taxonomy tables
  - Converts HTML content to Markdown format
  - Preserves post dates, titles, excerpts, and taxonomies
  - Organizes posts by year in Hugo's content structure
  - Handles HTML entities and special characters

- `WORDPRESS_MIGRATION.md`: Comprehensive 400+ line migration guide covering:
  - Multiple database export methods (phpMyAdmin, command-line, hosting control panels)
  - Detailed step-by-step migration process
  - Media file handling and download instructions
  - Image path updates and URL preservation
  - Troubleshooting common issues
  - Advanced features (custom post types, featured images, multi-author support)

**Documentation**
- `README.md`: Complete project documentation with quick start guide, deployment options, and project structure
- `SETUP_COMPLETE.md`: Setup summary and next steps for users
- `.gitignore`: Hugo-specific ignore patterns for build artifacts
- `commit_changes.sh`: Helper script for future commits

### Configuration

- **Site URL**: https://blog.conall.net/
- **Title**: Conall's Blog
- **Theme**: simple-blog (custom lightweight theme)
- **Language**: en-us
- **Menu Items**: Archive, Tags, Search
- **Output Formats**: HTML, RSS, JSON

### Files Changed

- 17 files created
- 1,568 lines added
- No files modified or deleted

### Key Features

✅ Static site generation with Hugo
✅ WordPress migration from MySQL database dumps
✅ Responsive design with dark mode
✅ Syntax highlighting for code blocks
✅ Categories and tags support
✅ RSS feed generation
✅ Search-ready (JSON output)
✅ SEO-friendly structure
✅ Comprehensive documentation

## Test Plan

- [ ] Clone the repository
- [ ] Verify Hugo builds successfully: `hugo`
- [ ] Test local development server: `hugo server -D`
- [ ] Verify the welcome post displays correctly
- [ ] Test responsive design on mobile viewport
- [ ] Verify dark mode switches based on system preference
- [ ] Test WordPress migration script with sample SQL dump
- [ ] Verify generated markdown files have correct front matter
- [ ] Check that categories and tags are preserved
- [ ] Deploy to test environment (Netlify/Vercel)
- [ ] Verify RSS feed is accessible at `/index.xml`

## Migration Usage

To import WordPress content:

```bash
# Export WordPress database
mysqldump -u username -p database_name > wordpress_dump.sql

# Run migration script
python3 wordpress_to_hugo.py --sql-file wordpress_dump.sql

# Preview site
hugo server -D
```

See `WORDPRESS_MIGRATION.md` for detailed instructions.

## Deployment Ready

The site can be immediately deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static file hosting

## Next Steps After Merge

1. Export WordPress MySQL database
2. Run `wordpress_to_hugo.py` to convert posts
3. Download WordPress media files to `static/uploads/`
4. Review and adjust converted content
5. Configure deployment workflow
6. Deploy to production
```

---

5. Click **"Create pull request"**

## Method 2: Using GitHub CLI (If Available Locally)

If you have `gh` installed on your local machine:

```bash
# Navigate to the repository
cd /path/to/blog.conall.net

# Fetch the latest changes
git fetch origin claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3

# Create the PR
gh pr create \
  --title "Set up Hugo static blog with WordPress migration support" \
  --body-file CREATE_PR.md \
  --head claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3 \
  --base main
```

## Method 3: Direct URL

Navigate directly to:
```
https://github.com/conallob/blog.conall.net/compare/main...claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3?expand=1
```

This will open the PR creation page with the branches already selected.

---

## PR Summary

**Branch:** `claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3`
**Commit:** `30fdfec` - Set up Hugo static blog with WordPress migration support
**Files Changed:** 17 files, 1,568 lines added
**Status:** Ready for review

The complete Hugo blog is set up and ready to import WordPress content!
