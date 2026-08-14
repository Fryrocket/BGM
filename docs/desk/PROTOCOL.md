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

## Reply

Write a new file in the target's folder. Do not edit the original task except to mark `status: done` after the finding exists.

## Source

If you cannot clone GitHub:

- Public files: `https://raw.githubusercontent.com/Fryrocket/BGM/main/<path>`
- Ask Grok to drop copies into `BGM/DESK/SOURCE/`

## Workers

Pi timer polls the inbox when `/etc/bgm-desk/keys.env` exists. Until then, chat + Drive is the path. Same files either way.
