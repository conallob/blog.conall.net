# Claude AI Workflows Documentation

This repository uses Claude AI to automate code review, quality checks, and security scanning through GitHub Actions.

## Available Workflows

### 1. Claude PR Review (`claude-pr-review.yml`)

**Trigger**: When pull requests are opened, synchronized, or reopened

**Purpose**: Automated code review using Claude AI

**What it checks**:
- Code quality and best practices
- Security vulnerabilities
- Performance issues
- Documentation completeness
- For markdown files: readability, grammar, and structure
- For Hugo templates: proper syntax and accessibility

**Files reviewed**: `.md`, `.py`, `.sh`, `.yml`, `.yaml`, `.toml`, `.html`, `.css`, `.js`

### 2. Claude Blog Quality Check (`claude-blog-check.yml`)

**Trigger**: When pull requests modify files in `content/posts/`

**Purpose**: Ensure blog posts meet quality standards

**What it checks**:
- Grammar and spelling
- Readability and clarity
- Structure and organization
- Front matter correctness (YAML)
- Markdown syntax issues
- SEO optimization (meta description, title)
- Content coherence and flow

**Output**: Detailed feedback in workflow logs and a comment on the PR

### 3. Claude Security Scan (`claude-security-scan.yml`)

**Trigger**:
- Pull requests to main
- Pushes to main
- Weekly schedule (Mondays at 9 AM UTC)
- Manual workflow dispatch

**Purpose**: Detect security vulnerabilities and issues

**What it scans for**:
- Hardcoded credentials or API keys
- SQL injection vulnerabilities
- Command injection risks
- Path traversal issues
- Insecure dependencies or configurations
- Exposed sensitive information
- YAML/configuration security issues

**Files scanned**: `.py`, `.sh`, `.yml`, `.yaml`, `.toml`

**Actions on detection**:
- Fails the workflow if issues are found
- Creates a GitHub issue for scheduled scans

## Setup Instructions

### Prerequisites

1. An Anthropic API key (get one at https://console.anthropic.com/)
2. Repository admin access to configure secrets

### Configuration Steps

1. **Add API Key to Secrets**:
   ```
   Repository → Settings → Secrets and variables → Actions → New repository secret

   Name: ANTHROPIC_API_KEY
   Value: <your-anthropic-api-key>
   ```

2. **Verify Permissions**:
   Ensure GitHub Actions has the necessary permissions:
   ```
   Repository → Settings → Actions → General → Workflow permissions

   ✅ Read and write permissions (for PR comments)
   ✅ Allow GitHub Actions to create and approve pull requests
   ```

3. **Enable Workflows**:
   The workflows are enabled by default. They will run automatically on the specified triggers.

## Customization

### Adjusting the Claude Model

All workflows use `claude-sonnet-4-5-20250929`. To change the model, edit the workflow files:

```yaml
model: claude-sonnet-4-5-20250929  # Change to different model
max_tokens: 2048                    # Adjust token limit
```

Available models:
- `claude-sonnet-4-5-20250929` (recommended, balanced performance)
- `claude-opus-4-20250514` (highest quality, slower)
- `claude-haiku-4-20250312` (fastest, lower cost)

### Modifying Review Criteria

Edit the prompt in each workflow file to customize what Claude reviews. Example:

```yaml
review-prompt: |
  Review the following code changes for:
  1. Custom criterion 1
  2. Custom criterion 2
  ...
```

### Changing Scan Schedule

The security scan runs weekly. To change the schedule, edit `claude-security-scan.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday at 9 AM UTC
  # Examples:
  # - cron: '0 0 * * *'  # Daily at midnight
  # - cron: '0 0 * * 0'  # Weekly on Sunday
```

### File Exclusions

To exclude specific files or directories from scanning, add to `.gitignore` or modify the workflow's file patterns:

```yaml
files: |
  **/*.md
  !vendor/**        # Exclude vendor directory
  !node_modules/**  # Exclude node_modules
```

## Cost Considerations

Claude API usage is metered. To manage costs:

1. **Limit file sizes**: Workflows skip files > 50KB
2. **Filter file types**: Only scan relevant file extensions
3. **Use appropriate models**: Haiku for simple checks, Sonnet for detailed review
4. **Adjust token limits**: Lower `max_tokens` for shorter responses
5. **Schedule wisely**: Run expensive scans less frequently

### Estimated Costs

Based on typical blog repository activity:
- PR Review: ~$0.01-0.05 per PR
- Blog Check: ~$0.02-0.10 per post
- Security Scan: ~$0.10-0.50 per full scan

**Note**: Costs vary based on file sizes and changes. Monitor usage in the Anthropic Console.

## Troubleshooting

### Workflow fails with "API key not found"

- Verify `ANTHROPIC_API_KEY` is set in repository secrets
- Check the secret name matches exactly (case-sensitive)

### No PR comments appearing

- Check workflow permissions in Settings → Actions → General
- Ensure "Read and write permissions" is enabled

### Claude responses seem off-topic

- Review and refine the prompt in the workflow file
- Ensure file content isn't too large (>50KB files are skipped)

### Rate limiting errors

- Space out workflow runs
- Use lower-frequency scanning schedules
- Consider caching results for unchanged files

## Best Practices

1. **Review Claude's feedback**: Treat it as suggestions, not requirements
2. **Iterative improvement**: Refine prompts based on feedback quality
3. **Combine with other tools**: Use Claude alongside traditional linters and tests
4. **Monitor costs**: Check Anthropic Console regularly
5. **Keep prompts specific**: Clear, focused prompts get better results

## Support

For issues with:
- **Workflows**: Check GitHub Actions logs and this documentation
- **Claude API**: Visit https://docs.anthropic.com/
- **Repository**: Open an issue in this repository

## Learn More

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Hugo Documentation](https://gohugo.io/documentation/)
