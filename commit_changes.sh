#!/bin/bash
# Helper script to commit the Hugo blog setup
# Run this script from the repository root: bash commit_changes.sh

cd "$(dirname "$0")"

echo "Adding files to git..."
git add -A

echo "Creating commit..."
git commit -m "Set up Hugo static blog with WordPress migration support" \
           -m "- Initialize Hugo site structure" \
           -m "- Create custom Simple Blog theme with responsive design" \
           -m "- Add WordPress to Hugo migration script (wordpress_to_hugo.py)" \
           -m "- Include comprehensive migration documentation" \
           -m "- Configure site with menu, RSS, and syntax highlighting" \
           -m "- Add sample welcome post demonstrating the setup" \
           -m "- Include .gitignore for Hugo projects" \
           -m "" \
           -m "The blog is ready to import WordPress content from MySQL database dumps."

echo "Commit successful!"
echo ""
echo "To push to remote:"
echo "  git push -u origin claude/setup-hugo-weblog-01PCjT2bFJsoa1hXh5FB25Z3"
