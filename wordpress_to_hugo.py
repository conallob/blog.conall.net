#!/usr/bin/env python3
"""
WordPress to Hugo Migration Script

This script converts WordPress blog posts from a MySQL database to Hugo markdown files.
It extracts posts, categories, tags, and metadata from the WordPress database.

Usage:
    python3 wordpress_to_hugo.py --host localhost --user root --password pass --database wordpress_db

Or load from a SQL dump file:
    python3 wordpress_to_hugo.py --sql-file wordpress_dump.sql
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import html


def parse_sql_dump(sql_file):
    """
    Parse WordPress SQL dump file and extract posts, categories, and tags.

    Returns:
        dict: Contains 'posts', 'categories', 'tags', and 'post_meta' data
    """
    print(f"Reading SQL dump from {sql_file}...")

    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        sql_content = f.read()

    data = {
        'posts': [],
        'categories': {},
        'tags': {},
        'post_meta': {}
    }

    # Extract posts from wp_posts table
    posts_pattern = r"INSERT INTO `wp_posts` VALUES \((.*?)\);"
    posts_matches = re.findall(posts_pattern, sql_content, re.DOTALL)

    for match in posts_matches:
        # Split by commas but respect quotes
        values = parse_sql_values(match)
        if len(values) >= 24:
            post_id = values[0]
            post_date = values[2].strip("'")
            post_content = values[4].strip("'")
            post_title = values[5].strip("'")
            post_excerpt = values[6].strip("'")
            post_status = values[7].strip("'")
            post_name = values[12].strip("'")
            post_type = values[20].strip("'")

            # Only process published posts
            if post_status == 'publish' and post_type == 'post':
                data['posts'].append({
                    'id': post_id,
                    'date': post_date,
                    'title': html.unescape(post_title),
                    'content': html.unescape(post_content),
                    'excerpt': html.unescape(post_excerpt),
                    'slug': post_name,
                    'categories': [],
                    'tags': []
                })

    # Extract terms (categories and tags) from wp_terms
    terms_pattern = r"INSERT INTO `wp_terms` VALUES \((.*?)\);"
    terms_matches = re.findall(terms_pattern, sql_content, re.DOTALL)

    terms = {}
    for match in terms_matches:
        values = parse_sql_values(match)
        if len(values) >= 3:
            term_id = values[0]
            term_name = values[1].strip("'")
            term_slug = values[2].strip("'")
            terms[term_id] = {'name': term_name, 'slug': term_slug}

    # Extract term taxonomy to identify categories vs tags
    taxonomy_pattern = r"INSERT INTO `wp_term_taxonomy` VALUES \((.*?)\);"
    taxonomy_matches = re.findall(taxonomy_pattern, sql_content, re.DOTALL)

    term_taxonomy = {}
    for match in taxonomy_matches:
        values = parse_sql_values(match)
        if len(values) >= 3:
            term_taxonomy_id = values[0]
            term_id = values[1]
            taxonomy = values[2].strip("'")

            if term_id in terms:
                term_taxonomy[term_taxonomy_id] = {
                    'term': terms[term_id],
                    'type': taxonomy
                }

                if taxonomy == 'category':
                    data['categories'][term_taxonomy_id] = terms[term_id]
                elif taxonomy == 'post_tag':
                    data['tags'][term_taxonomy_id] = terms[term_id]

    # Extract term relationships to link posts with categories/tags
    relationships_pattern = r"INSERT INTO `wp_term_relationships` VALUES \((.*?)\);"
    relationships_matches = re.findall(relationships_pattern, sql_content, re.DOTALL)

    post_terms = {}
    for match in relationships_matches:
        values = parse_sql_values(match)
        if len(values) >= 2:
            object_id = values[0]
            term_taxonomy_id = values[1]

            if object_id not in post_terms:
                post_terms[object_id] = []
            post_terms[object_id].append(term_taxonomy_id)

    # Link categories and tags to posts
    for post in data['posts']:
        post_id = post['id']
        if post_id in post_terms:
            for term_taxonomy_id in post_terms[post_id]:
                if term_taxonomy_id in data['categories']:
                    post['categories'].append(data['categories'][term_taxonomy_id]['name'])
                elif term_taxonomy_id in data['tags']:
                    post['tags'].append(data['tags'][term_taxonomy_id]['name'])

    print(f"Found {len(data['posts'])} published posts")
    return data


def parse_sql_values(values_string):
    """
    Parse SQL INSERT values, handling quoted strings and NULL values.
    This is a simplified parser - may need enhancement for complex cases.
    """
    values = []
    current = ""
    in_quote = False
    quote_char = None
    escaped = False

    for char in values_string:
        if escaped:
            current += char
            escaped = False
            continue

        if char == '\\':
            escaped = True
            current += char
            continue

        if char in ("'", '"') and not in_quote:
            in_quote = True
            quote_char = char
            current += char
        elif char == quote_char and in_quote:
            in_quote = False
            quote_char = None
            current += char
        elif char == ',' and not in_quote:
            values.append(current.strip())
            current = ""
        else:
            current += char

    if current:
        values.append(current.strip())

    return values


def convert_wordpress_content_to_markdown(content):
    """
    Convert WordPress HTML content to Markdown.
    This is a basic conversion - you may want to use a library like html2text for better results.
    """
    # Remove WordPress shortcodes
    content = re.sub(r'\[.*?\]', '', content)

    # Convert common HTML tags to markdown
    # Headings
    content = re.sub(r'<h1>(.*?)</h1>', r'# \1', content)
    content = re.sub(r'<h2>(.*?)</h2>', r'## \1', content)
    content = re.sub(r'<h3>(.*?)</h3>', r'### \1', content)
    content = re.sub(r'<h4>(.*?)</h4>', r'#### \1', content)

    # Bold and italic
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)

    # Links
    content = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', content)

    # Images
    content = re.sub(r'<img src="(.*?)".*?alt="(.*?)".*?/?>', r'![\2](\1)', content)
    content = re.sub(r'<img src="(.*?)".*?/?>', r'![](\1)', content)

    # Code blocks
    content = re.sub(r'<pre><code>(.*?)</code></pre>', r'```\n\1\n```', content, flags=re.DOTALL)
    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content)

    # Paragraphs and line breaks
    content = re.sub(r'<p>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<br\s*/?>', '\n', content)

    # Lists
    content = re.sub(r'<ul>(.*?)</ul>', lambda m: convert_list(m.group(1), '-'), content, flags=re.DOTALL)
    content = re.sub(r'<ol>(.*?)</ol>', lambda m: convert_list(m.group(1), '1.'), content, flags=re.DOTALL)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Unescape HTML entities
    content = html.unescape(content)

    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def convert_list(list_content, marker):
    """Convert HTML list items to markdown."""
    items = re.findall(r'<li>(.*?)</li>', list_content, re.DOTALL)
    return '\n'.join([f'{marker} {item.strip()}' for item in items]) + '\n'


def create_hugo_post(post, output_dir):
    """
    Create a Hugo markdown post file from WordPress post data.
    """
    # Parse date
    try:
        post_date = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')
        date_str = post_date.strftime('%Y-%m-%dT%H:%M:%S')
        year = post_date.strftime('%Y')
    except:
        date_str = post['date']
        year = datetime.now().strftime('%Y')

    # Create directory structure: content/posts/YYYY/
    post_dir = Path(output_dir) / 'content' / 'posts' / year
    post_dir.mkdir(parents=True, exist_ok=True)

    # Create filename from slug or title
    slug = post['slug'] if post['slug'] else sanitize_filename(post['title'])
    filename = f"{slug}.md"
    filepath = post_dir / filename

    # Convert content to markdown
    content = convert_wordpress_content_to_markdown(post['content'])

    # Build front matter
    front_matter = f"""---
title: "{post['title'].replace('"', '\\"')}"
date: {date_str}
draft: false
"""

    if post['categories']:
        front_matter += f"categories: [{', '.join([f'"{cat}"' for cat in post['categories']])}]\n"

    if post['tags']:
        front_matter += f"tags: [{', '.join([f'"{tag}"' for tag in post['tags']])}]\n"

    if post['excerpt']:
        excerpt = post['excerpt'].replace('"', '\\"').replace('\n', ' ')
        front_matter += f'description: "{excerpt}"\n'

    front_matter += "---\n\n"

    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)

    print(f"Created: {filepath}")


def sanitize_filename(title):
    """Convert title to a safe filename."""
    # Convert to lowercase and replace spaces with hyphens
    filename = title.lower()
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename[:100]  # Limit length


def main():
    parser = argparse.ArgumentParser(
        description='Convert WordPress blog posts to Hugo markdown files'
    )
    parser.add_argument(
        '--sql-file',
        help='Path to WordPress SQL dump file'
    )
    parser.add_argument(
        '--host',
        help='MySQL host (alternative to SQL file)'
    )
    parser.add_argument(
        '--user',
        help='MySQL user'
    )
    parser.add_argument(
        '--password',
        help='MySQL password'
    )
    parser.add_argument(
        '--database',
        help='MySQL database name'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (Hugo site root, default: current directory)'
    )

    args = parser.parse_args()

    if args.sql_file:
        # Parse from SQL dump file
        data = parse_sql_dump(args.sql_file)
    elif args.host and args.user and args.database:
        # Connect to MySQL database (requires mysql-connector-python)
        try:
            import mysql.connector

            print(f"Connecting to MySQL database {args.database}...")
            conn = mysql.connector.connect(
                host=args.host,
                user=args.user,
                password=args.password or '',
                database=args.database
            )

            # This would require implementing direct database queries
            # For now, recommend using SQL dump
            print("Direct database connection not yet implemented.")
            print("Please export your WordPress database to a SQL file and use --sql-file option.")
            sys.exit(1)

        except ImportError:
            print("Error: mysql-connector-python not installed.")
            print("Install it with: pip install mysql-connector-python")
            sys.exit(1)
    else:
        print("Error: Please provide either --sql-file or database connection details.")
        parser.print_help()
        sys.exit(1)

    # Create Hugo posts
    print(f"\nCreating Hugo markdown files in {args.output_dir}...")
    for post in data['posts']:
        create_hugo_post(post, args.output_dir)

    print(f"\nMigration complete! Created {len(data['posts'])} posts.")
    print("\nNext steps:")
    print("1. Review the generated markdown files in content/posts/")
    print("2. Check for any formatting issues in the converted content")
    print("3. Download WordPress media files and place them in static/images/")
    print("4. Update image paths in posts if needed")
    print("5. Run 'hugo server' to preview your site")


if __name__ == '__main__':
    main()
