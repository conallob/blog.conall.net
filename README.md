# blog.conall.net

A static weblog powered by [Hugo](https://gohugo.io/) with a custom Simple Blog theme.

## Quick Start

### Prerequisites

- Hugo Extended v0.120.0 or later
- Python 3.6+ (for WordPress migration)

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/conallob/blog.conall.net.git
cd blog.conall.net
```

2. Start the Hugo development server:

```bash
hugo server -D
```

3. Visit http://localhost:1313

### Building for Production

Generate the static site:

```bash
hugo
```

The output will be in the `public/` directory.

## Creating New Posts

Create a new post:

```bash
hugo new content/posts/2024/my-new-post.md
```

Or manually create a markdown file in `content/posts/YYYY/` with front matter:

```yaml
---
title: "My New Post"
date: 2024-01-01T12:00:00
draft: false
categories: ["Technology"]
tags: ["hugo", "blogging"]
description: "A brief description of the post"
---

Your content here...
```

## WordPress Migration

This blog supports migration from WordPress. See [WORDPRESS_MIGRATION.md](WORDPRESS_MIGRATION.md) for detailed instructions.

Quick steps:

1. Export your WordPress database to a SQL file
2. Run the migration script:

```bash
python3 wordpress_to_hugo.py --sql-file wordpress_dump.sql
```

3. Download WordPress media files to `static/uploads/`
4. Review and test the migrated content

## Site Configuration

Edit `hugo.toml` to customize:

- Site title and description
- Base URL
- Menu items
- Theme parameters

See the [Hugo documentation](https://gohugo.io/getting-started/configuration/) for all available options.

## Theme

This site uses a custom "Simple Blog" theme located in `themes/simple-blog`.

Features:
- Clean, minimal design
- Responsive layout
- Dark mode support (automatic based on system preference)
- Syntax highlighting for code blocks
- Categories and tags support
- RSS feed generation

The theme is lightweight and doesn't require any external dependencies.

## Deployment

This site can be deployed to:

- **GitHub Pages**: Push to `gh-pages` branch or use GitHub Actions
- **Netlify**: Connect your repository and set build command to `hugo`
- **Vercel**: Import project and deploy
- **Any static hosting**: Upload the `public/` directory

### GitHub Pages Example

See [.github/workflows/hugo.yml](.github/workflows/hugo.yml) for automatic deployment on push.

## GitHub Actions Workflows

This repository includes several automated workflows:

### Hugo Build & Deployment
- **hugo.yml**: Builds and deploys the site to GitHub Pages on push to main
- **pr-check.yml**: Validates that PRs build successfully before merging

### Claude AI Integration

The repository uses Claude AI for automated code review and quality checks:

- **claude-pr-review.yml**: Reviews all pull requests for code quality, best practices, and security
- **claude-blog-check.yml**: Analyzes blog post quality, grammar, SEO, and markdown syntax
- **claude-security-scan.yml**: Performs security scans on PRs, pushes, and weekly scheduled runs

#### Setting up Claude Workflows

To enable Claude-powered workflows, add your Anthropic API key to repository secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Anthropic API key from https://console.anthropic.com/
5. Click **Add secret**

The Claude workflows will automatically:
- Review code changes in pull requests
- Check blog posts for quality and readability
- Scan for security vulnerabilities
- Provide constructive feedback in workflow logs

## Project Structure

```
.
├── archetypes/          # Content templates
├── content/             # Markdown content
│   └── posts/          # Blog posts organized by year
├── data/               # Data files
├── layouts/            # Custom layout templates
├── static/             # Static files (images, css, js)
│   └── uploads/        # WordPress media files
├── themes/             # Hugo themes
│   └── simple-blog/    # Custom Simple Blog theme
├── hugo.toml           # Hugo configuration
├── wordpress_to_hugo.py # WordPress migration script
└── WORDPRESS_MIGRATION.md # Migration guide
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Content: © Conall O'Brien
Code: MIT License

## Support

For Hugo issues, see the [Hugo documentation](https://gohugo.io/documentation/).
