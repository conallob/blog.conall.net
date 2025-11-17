#!/usr/bin/env python3
"""Simple git commit script"""
import subprocess
import sys

try:
    # Change to repo directory
    import os
    os.chdir('/home/user/blog.conall.net')

    # Git add
    result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
    with open('/tmp/git_add_output.txt', 'w') as f:
        f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nReturn code: {result.returncode}\n")

    if result.returncode != 0:
        print(f"Git add failed: {result.stderr}")
        sys.exit(1)

    # Git commit
    commit_msg = """Set up Hugo static blog with WordPress migration support

- Initialize Hugo site structure
- Create custom Simple Blog theme with responsive design
- Add WordPress to Hugo migration script
- Include comprehensive migration documentation
- Configure site with menu, RSS, and syntax highlighting
- Add sample welcome post
- Include .gitignore for Hugo projects

The blog is ready to import WordPress content from MySQL database dumps."""

    result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
    with open('/tmp/git_commit_output.txt', 'w') as f:
        f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nReturn code: {result.returncode}\n")

    if result.returncode != 0:
        print(f"Git commit failed: {result.stderr}")
        sys.exit(1)

    print("SUCCESS")
    sys.exit(0)

except Exception as e:
    with open('/tmp/git_error.txt', 'w') as f:
        f.write(str(e))
    print(f"Error: {e}")
    sys.exit(1)
