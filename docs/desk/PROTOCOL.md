# Desk protocol

Shared memory for Fry, Grok, Claude, Gemini.

## Inbox path

```
BGM/DESK/INBOX/
  for-claude/
  for-gemini/
  for-grok/
  for-fry/
```

Filename: `YYYY-MM-DD-<id>-<slug>.md`

```markdown
---
id: T001
verb: task
from: grok
to: claude
status: open
---

# Title

Body.
```

## Notes Log

Newest entries at the top. After every significant implementer pass, Grok appends.

- Desk → Notes
- `docs/desk/NOTES.md`
- Drive `BGM/DESK/NOTES`
- Archive: Drive doc `BGM_Notes_Log_Claude_Gemini` (2026-08-12)

## Reply

Write a new file in the target's folder. Do not edit the original task file except to mark `status: done` after you have posted the finding.

## Source

Do not require GitHub access. If you cannot clone:

- Public files: `https://raw.githubusercontent.com/Fryrocket/BGM/main/<path>`
- Firmware / models: ask Grok to drop a copy in `BGM/DESK/SOURCE/` (title-stable)

## Workers

Pi unit `bgm-desk-worker.timer` polls the inbox when `/etc/bgm-desk/keys.env` exists. Until then, open-chat + Drive is the path. Same files either way.
