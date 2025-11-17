# WordPress to Hugo Migration Guide

This guide explains how to migrate your WordPress blog to Hugo using the MySQL database snapshot.

## Overview

This Hugo site is configured to import content from a WordPress blog. The migration process involves:

1. Exporting your WordPress MySQL database
2. Running the migration script to convert posts to Hugo markdown
3. Downloading and migrating media files
4. Reviewing and adjusting the converted content

## Prerequisites

- Python 3.6 or higher
- Your WordPress MySQL database dump (SQL file)
- Access to your WordPress media files (wp-content/uploads/)

## Step 1: Export WordPress Database

### Option A: Using phpMyAdmin

1. Log in to phpMyAdmin
2. Select your WordPress database
3. Click the "Export" tab
4. Choose "Quick" export method and SQL format
5. Click "Go" to download the SQL file

### Option B: Using Command Line

```bash
mysqldump -u username -p database_name > wordpress_dump.sql
```

Replace `username` with your MySQL username and `database_name` with your WordPress database name.

### Option C: Using WordPress Hosting Control Panel

Most hosting providers (cPanel, Plesk, etc.) offer database export tools. Look for:
- "MySQL Databases" → "phpMyAdmin"
- "Database Tools" → "Backup/Export"

## Step 2: Run the Migration Script

Place your WordPress SQL dump file in this directory and run:

```bash
python3 wordpress_to_hugo.py --sql-file wordpress_dump.sql
```

The script will:
- Extract all published posts from the database
- Convert HTML content to Markdown
- Preserve categories and tags
- Create posts organized by year in `content/posts/YYYY/`
- Generate Hugo front matter with metadata

### Alternative: Direct Database Connection

If you have direct access to the MySQL database (not yet fully implemented):

```bash
python3 wordpress_to_hugo.py \
  --host localhost \
  --user wordpress_user \
  --password your_password \
  --database wordpress_db
```

## Step 3: Download WordPress Media Files

WordPress stores uploaded images and files in `wp-content/uploads/`. You need to download these files:

### Using FTP/SFTP

1. Connect to your WordPress site via FTP
2. Navigate to `wp-content/uploads/`
3. Download the entire `uploads` folder
4. Place the files in Hugo's `static/uploads/` directory:

```bash
# Create the directory if it doesn't exist
mkdir -p static/uploads

# Copy your WordPress uploads here
# The structure will be: static/uploads/YYYY/MM/filename.jpg
```

### Using SSH/SCP

If you have SSH access:

```bash
scp -r user@yoursite.com:/path/to/wp-content/uploads/* static/uploads/
```

### Using wget

```bash
wget -r -np -nH --cut-dirs=3 -R "index.html*" \
  https://yoursite.com/wp-content/uploads/ \
  -P static/
```

## Step 4: Update Image Paths (if needed)

The migration script attempts to preserve image URLs. If images don't display:

1. Check if WordPress used absolute URLs (https://yoursite.com/wp-content/uploads/...)
2. You may need to update these to relative paths (/uploads/...)

You can use a find-and-replace:

```bash
# In all markdown files, replace absolute URLs with relative paths
find content/posts -name "*.md" -type f -exec sed -i \
  's|https://oldsite.com/wp-content/uploads|/uploads|g' {} +
```

## Step 5: Review Converted Content

The HTML-to-Markdown conversion is basic. Review posts for:

### Common Issues

1. **Code blocks**: WordPress code shortcodes may not convert perfectly
2. **Embedded content**: YouTube embeds, tweets, etc. may need manual conversion
3. **Shortcodes**: WordPress shortcodes are stripped - add them back as Hugo shortcodes if needed
4. **Tables**: HTML tables may need manual markdown conversion
5. **Special formatting**: Custom HTML may need adjustment

### Testing Posts

Preview your site locally:

```bash
hugo server -D
```

Visit http://localhost:1313 to review your migrated content.

## Step 6: Advanced Content Fixes

### Better HTML to Markdown Conversion

For better conversion quality, you can use `html2text`:

```bash
pip install html2text
```

Then modify the `convert_wordpress_content_to_markdown()` function in `wordpress_to_hugo.py`:

```python
import html2text

def convert_wordpress_content_to_markdown(content):
    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    return h.handle(content)
```

### Importing Comments

WordPress comments are not included in this basic migration. To migrate comments:

1. Consider using a comment service like Disqus, utterances, or giscus
2. Export comments from WordPress and import to your chosen service
3. Add the comment system to your Hugo theme

### Preserving URLs

To maintain the same URL structure as WordPress:

1. Edit `hugo.toml` and add:

```toml
[permalinks]
  posts = "/:year/:month/:slug/"
```

2. Or use WordPress-style permalinks:

```toml
[permalinks]
  posts = "/:year/:month/:day/:slug/"
```

## Step 7: Custom WordPress Features

### Custom Post Types

If your WordPress site uses custom post types, modify the script's post type filter:

```python
# In wordpress_to_hugo.py, change this line:
if post_status == 'publish' and post_type == 'post':

# To include your custom post type:
if post_status == 'publish' and post_type in ('post', 'your_custom_type'):
```

### Featured Images

WordPress featured images can be added to front matter. The script currently doesn't extract these, but you can add this functionality by querying the `wp_postmeta` table for `_thumbnail_id`.

### Author Information

Multi-author blogs can preserve author data by extracting from `wp_users` and adding to front matter.

## Troubleshooting

### "No module named 'mysql'"

If you see this error and want direct database access:

```bash
pip install mysql-connector-python
```

### Encoding Issues

If you see garbled characters:

1. Ensure your SQL dump is UTF-8 encoded
2. Try re-exporting with:

```bash
mysqldump -u username -p --default-character-set=utf8mb4 database_name > wordpress_dump.sql
```

### Missing Posts

Check that:
- Posts have 'publish' status in WordPress
- Posts are of type 'post' (not 'page' or custom types)
- The SQL dump contains the `wp_posts` table

### Script Errors

If the script fails:
1. Check the SQL dump file is valid
2. Ensure you have write permissions in the content directory
3. Check the script output for specific error messages

## Next Steps After Migration

1. **Configure SEO**: Add meta descriptions, open graph tags
2. **Set up redirects**: Create redirect rules for changed URLs
3. **Test thoroughly**: Check all posts, images, and links
4. **Configure deployment**: Set up GitHub Pages, Netlify, or your hosting
5. **Add analytics**: Configure Google Analytics or similar
6. **Submit sitemap**: Generate and submit sitemap to search engines

## Additional Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Theme Docs](https://github.com/adityatelange/hugo-PaperMod/wiki)
- [Hugo Discourse Forum](https://discourse.gohugo.io/)

## Script Limitations

The `wordpress_to_hugo.py` script provides a basic migration. It:

**Handles:**
- ✅ Published posts with content
- ✅ Categories and tags
- ✅ Post dates and titles
- ✅ Basic HTML to Markdown conversion
- ✅ Post excerpts

**Doesn't Handle:**
- ❌ WordPress pages (can be added)
- ❌ Comments
- ❌ Featured images
- ❌ Custom fields
- ❌ Author information (multi-author sites)
- ❌ Media file downloads (manual step)
- ❌ Complex shortcodes
- ❌ WordPress blocks (Gutenberg)

For complex migrations, consider using existing tools like:
- [wordpress-export-to-markdown](https://github.com/lonekorean/wordpress-export-to-markdown)
- [blog2md](https://github.com/palaniraja/blog2md)
- [exitwp](https://github.com/thomasf/exitwp)

Or hire a professional for custom migration needs.
