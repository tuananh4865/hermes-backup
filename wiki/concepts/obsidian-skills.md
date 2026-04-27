---
title: "Obsidian Skills — kepano/obsidian-skills"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [obsidian, skills, markdown, wiki, knowledge-management]
related:
  - [[obsidian]]
  - [[agent-skills]]
  - [[knowledge-quality-system]]
---

# Obsidian Skills (kepano)

**Source**: [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
**Spec**: [Agent Skills Specification](https://agentskills.io/specification)

Repo chứa các skill definitions theo chuẩn Agent Skills spec — có thể dùng cho Claude Code, Codex CLI, OpenCode, và bất kỳ skills-compatible agent nào.

## Skills có sẵn

| Skill | Mô tả |
|-------|-------|
| [obsidian-markdown](skills/obsidian-markdown) | Obsidian Flavored Markdown — wikilinks, embeds, callouts, properties, tags |
| [obsidian-bases](skills/obsidian-bases) | `.base` files — database-like views với filters, formulas, table/cards/map views |
| [json-canvas](skills/json-canvas) | `.canvas` files — visual canvases, mind maps, flowcharts |
| [obsidian-cli](skills/obsidian-cli) | Obsidian CLI — vault operations, plugin dev, screenshot, DOM inspection |
| [defuddle](skills/defuddle) | Extract clean markdown từ web pages, loại bỏ ads/clutter |

## Cài đặt cho Hermes

```bash
# Clone vào ~/.hermes/skills/
git clone https://github.com/kepano/obsidian-skills.git \
  ~/.hermes/skills/obsidian-skills

# Hoặc copy từng skill riêng
cp -r obsidian-skills/skills/obsidian-markdown \
  ~/.hermes/skills/
```

**Lưu ý**: Skills từ obsidian-skills dùng chuẩn Agent Skills spec (có frontmatter `name` + `description`). Hermes skills format tương thích nhưng có thêm `version`, `tags`, `allowed_tools`.

## obsidian-markdown — Chi tiết

### Cú pháp quan trọng

**Wikilinks** (internal links):
```
                    Link to note
[[Note Name|Display Text]]       Custom display text
[[Note Name#Heading]]             Link to heading
[[Note Name#^block-id]]          Link to block
```

**Embeds**:
```
!                    Embed full note
![[image.png|300]]               Embed with width
![[document.pdf#page=3]]         PDF page
```

**Callouts**:
```
> [!note]
> Basic callout

> [!warning] Custom Title
> Callout với custom title

> [!faq]- Collapsed
> Foldable (- collapsed, + expanded)
```

Types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`

**Properties (frontmatter)**:
```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

## obsidian-bases — Database Views

`.base` files là YAML-based database với:

- **Filters**: chọn notes theo tag, folder, property, date
- **Formulas**: computed properties (if/else, date arithmetic, string formatting)
- **Views**: table, cards, list, map

### Formula patterns hay

```yaml
formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'
```

**Duration pitfall**: Date subtraction trả về Duration type, KHÔNG phải number. Luôn access `.days`, `.hours` trước:
```yaml
# ĐÚNG
"(date(due_date) - today()).days"

# SAI - Duration không support .round() trực tiếp
"(date(due) - today()).round(0)"
```

## json-canvas

Canvas format cho visual content:

```json
{
  "nodes": [
    {
      "id": "6f0ad84f44ce9c17",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 200,
      "text": "# Hello\n\n**Markdown** content"
    }
  ],
  "edges": [
    {
      "id": "0123456789abcdef",
      "fromNode": "6f0ad84f44ce9c17",
      "toNode": "a1b2c3d4e5f67890",
      "label": "leads to"
    }
  ]
}
```

Node types: `text`, `file`, `link`, `group`
Color presets: `"1"` (red) through `"6"` (purple)

## obsidian-cli

Vault operations từ command line:

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" silent
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
```

**Plugin dev workflow**:
```bash
obsidian plugin:reload id=my-plugin    # Reload after code change
obsidian dev:errors                     # Check for errors
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".workspace-leaf" text
obsidian dev:console level=error
obsidian eval code="app.vault.getFiles().length"
```

## defuddle

Extract clean markdown từ web pages — loại bỏ ads, navigation, clutter.

```bash
npm install -g defuddle

# Markdown output (recommended)
defuddle parse <url> --md

# Save to file
defuddle parse <url> --md -o content.md

# Get specific metadata
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

**So với web_extract**: defuddle tốt hơn cho articles/documentation. web_extract tốt hơn cho structured data/API pages.

## So sánh với Hermes Skills Format

| Aspect | kepano/obsidian-skills | Hermes Skills |
|--------|------------------------|---------------|
| Frontmatter | `name`, `description` | `name`, `description`, `version`, `tags`, `allowed_tools` |
| Structure | SKILL.md + references/ | SKILL.md + references/, scripts/, templates/ |
| Validation | Spec-based | Custom validator in hermes-agent |
| Evolution | Manual | GEPA self-evolution |

## Integration với Hermes

Có thể copy các skill này vào `~/.hermes/skills/` và dùng cho:
- Writing notes trong Obsidian vault
- Managing knowledge base
- Better web content extraction (defuddle)
- Canvas visualization

Tuy nhiên cần adapt: Hermes skills có thêm `allowed_tools`, `version`, `tags` fields. Có thể thêm khi integrate.

---

_Last updated: 2026-04-12_
