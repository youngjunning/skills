# Fiction Site Builder

Claude Code skill for writing fiction content and building mobile-first fiction reading sites.

This README is intentionally limited to installation and usage. Operational rules, phase details, quality gates, and implementation references live in `SKILL.md` and `references/`.

## Install

### Global install

```bash
npx skills add youngjunning/skills --skill fiction-site-builder -g
```

### Project install

```bash
npx skills add youngjunning/skills --skill fiction-site-builder
```

## Enable

Claude Code discovers skills automatically from:

- `~/.claude/skills/{skill-name}/`
- `{project-root}/.claude/skills/{skill-name}/`

The skill metadata is defined in `SKILL.md`.

For project-specific defaults, add or update the project-level `AGENTS.md`. Project instructions override skill defaults when they conflict.

## Optional Environment

Image generation requires:

```bash
export APIYI_API_KEY=your_key_here
```

If the key is not configured, image-related steps may be skipped or require manual follow-up.

## Usage

Ask Claude Code in natural language. Examples:

```text
Build a new werewolf romance reading site.
Add one vampire romance book to this site.
Continue writing the next chapter.
Generate covers for all books.
Add illustrations.
Import this manuscript into the standard project structure.
Review and deslop these chapters.
Build only the site.
```

You can also refer to the skill by name when you want to force the context:

```text
Use fiction-site-builder to add a new book.
```

## Reference Entry Points

Use these files as the source of truth:

- `SKILL.md` — routing, pipeline, required gates, and operating rules.
- `references/story-long-write.md` — long-form chapter writing.
- `references/story-short-write.md` — short-form story writing.
- `references/story-import.md` — manuscript import.
- `references/story-review.md` and `references/story-deslop.md` — review and prose cleanup.
- `references/story-cover.md`, `references/cover-styles.md`, and `references/cover-allure-elements.md` — covers.
- `references/story-illustrations.md` — illustrations.
- `references/tech-stack.md`, `references/design-system.md`, `references/data-contract.md`, `references/ui-components.md`, and `references/reader-ux.md` — site build.
- `references/performance.md`, `references/qa-checklist.md`, and `references/lighthouse-qa.md` — verification.
- `references/vercel-operations.md` — deployment operations.

## Maintenance

When behavior changes, update `SKILL.md` or the relevant file in `references/` first. Keep this README focused on installation and usage so it does not drift from the executable instructions.

## License

MIT License
