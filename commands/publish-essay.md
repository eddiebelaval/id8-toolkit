# /publish-essay - Publish Essay to your-domain.com

Create MDX file, commit to your-company-hub repo, and trigger Vercel deploy.

## Usage

```
/publish-essay "<title>" --content <mdx-content>
/publish-essay --from-file <path>  # Publish from existing MDX file
/publish-essay --slug custom-slug  # Override auto-generated slug
```

## Process

1. **Validate Content**
   - Ensure frontmatter is complete (title, date, category required)
   - Verify content is in proper MDX format
   - Check that category is one of: essay, research, release
   - Generate slug from title if not provided (kebab-case)

2. **Create MDX File**
   - Location: `/Users/the userbelaval/Development/your-company-hub/core/content/essays/`
   - Filename: `{slug}.mdx`
   - Add/verify all required frontmatter fields

3. **Git Operations**
   ```bash
   cd /Users/the userbelaval/Development/your-company-hub
   git checkout main
   git pull origin main
   git add core/content/essays/{slug}.mdx
   git commit -m "content: add essay - {title}"
   git push origin main
   ```

4. **Trigger Deploy**
   - Push to main triggers Vercel auto-deploy
   - Monitor deploy status with `vercel inspect`
   - Wait for production deploy completion

5. **Return Essay URL**
   - Format: `https://your-domain.com/essays/{slug}`
   - Verify URL is accessible (may take 1-2 minutes)

## MDX Frontmatter Reference

```yaml
---
title: "Required - Essay title"
subtitle: "Optional - Supporting tagline"
date: "YYYY-MM-DD"              # Required
author: "the author"          # Optional, defaults to the user
category: "essay|research|release"  # Required
tags: ["tag1", "tag2"]           # Optional
featured: true|false             # Optional
heroImage: "/path/to/image.webp" # Optional
---
```

## Content Guidelines

- Use standard Markdown syntax
- Code blocks with language identifiers
- No JSX components (pure Markdown)
- Images should be in /public/ or external URLs
- Estimated read time calculated automatically (~200 wpm)

## Example

```
/publish-essay "The 70% Problem" --content "---
title: \"The 70% Problem\"
subtitle: \"Why AI tools get us most of the way, then leave us stranded\"
date: \"2025-12-30\"
author: \"the author\"
category: \"research\"
tags: [\"research\", \"ai\", \"productivity\"]
---

I've been tracking something for the past six months...

[Full essay content]
"
```

## Output

```
Publishing essay to your-domain.com...

File created: core/content/essays/the-70-percent-problem.mdx
Commit: abc123 "content: add essay - The 70% Problem"
Deploy triggered on Vercel

Essay URL: https://your-domain.com/essays/the-70-percent-problem

Deploy status: Production (ready in ~60 seconds)
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing frontmatter | Prompt for required fields |
| Invalid category | Must be essay, research, or release |
| Slug conflict | Suggest alternative slug or overwrite |
| Git conflict | Pull latest and retry |
| Deploy failed | Check Vercel dashboard |

## Requirements

- Git access to your-company-hub repo
- Main branch must be clean (no uncommitted changes)
- Vercel project linked for deploy status
