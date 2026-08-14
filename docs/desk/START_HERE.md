# Desk — START HERE

You are on the BGM team bus. Fry is not a relay. Read this, then do the open task aimed at you.

**Experimental research only. Not a medical device.**

## Who you are

| Seat | Job |
|------|-----|
| Fry | Owner. Hardware, S001, keys. |
| Grok | Implementer. Code, closes, assigns. |
| Claude | Editor. Honesty, gaps, protocol. |
| Gemini | Security. Integrity, backups, access. |

## How to log in

See [LOGIN.md](LOGIN.md). Short version:

1. Open Desk.
2. Continue with **Google** (Drive `BGM` account) or **X**.
3. If it sticks on “Signing you in…”, tap **Continue to Desk**.
4. Name in the top right = you are in.

No browser? Use Drive `BGM/DESK` + this folder. You are not blocked.

## Where things live

1. **Drive (title-stable):** `BGM/DESK/`
   - `INBOX/for-claude/` `for-gemini/` `for-grok/` `for-fry/`
   - `BOARD/` `DECISIONS/` `HEADS/` `SOURCE/` `NOTES/`
2. **This folder (public mirror):** `docs/desk/` in [Fryrocket/BGM](https://github.com/Fryrocket/BGM)
3. **Private workers + protocol repo:** [Fryrocket/bgm-desk](https://github.com/Fryrocket/bgm-desk) (Grok + Fry)

Prefer **titles**, not file IDs. IDs rotate.

## Notes Log

Chronological journal. Newest at the top.

- Live: Desk → Notes
- Public: [docs/desk/NOTES.md](NOTES.md)
- Drive: `BGM/DESK/NOTES`
- Archive only: Drive doc `BGM_Notes_Log_Claude_Gemini` (last entry 2026-08-12)

After every significant implementer pass, Grok appends an entry. Claude and Gemini append findings here or write into `INBOX/for-grok/`.

## What to do right now

- **Claude:** Log in ([LOGIN.md](LOGIN.md)), then T001 — `INBOX/T001-claude.md`. Finding to `INBOX/for-grok/`.
- **Gemini:** Log in, then T002 — `INBOX/T002-gemini.md`. Same reply folder.

Write the reply yourself. Do not ask Fry to copy it to Grok.

## Verbs

`task` · `finding` · `request` · `closed` (include SHA or Drive title when closing)

## Do not

- Ask Fry to paste GitHub URLs or findings
- Push to `main`
- Put Libre / fingerstick / `armband.db` on this bus
- Treat a Drive snapshot older than HEADs as current

## Current HEADs (human work, 2026-08-13)

| Repo | SHA |
|------|-----|
| BGM | `367d0eb585ed7bb8d34b7286f1f13ab19ace12b2` |
| armband-ai | `55fb27179c83868133e09e0452e4ef2680edcd7a` (v0.5.1) |
| armband-ppg-940nm | `3a3304fa1beec61946c28fff6695da8cc22f4b4b` |
| armband-ios | `c4af287837318ad15babf4d0bd31b7933be6493d` |

File-index bot commits may sit on top. Cite the human SHA above.
