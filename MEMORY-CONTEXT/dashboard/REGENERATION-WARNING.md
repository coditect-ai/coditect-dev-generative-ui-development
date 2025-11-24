# ⚠️ DASHBOARD REGENERATION WARNING

## Problem

The `generate-dashboard.py` script **overwrites** CSS and JavaScript files when regenerating dashboard data.

## What Happened (2025-11-24)

1. Enhanced CSS/JS files with:
   - AZ1.AI design system
   - Date/time fixes (noon UTC parsing)
   - File system timestamp display
   - Global word wrapping
   - Hover behavior fixes

2. Ran `generate-dashboard.py` to update JSON data

3. Script's `_copy_static_assets()` method **overwrote** all CSS/JS files with basic templates

4. Dashboard broke:
   - Theme gone (no AZ1.AI colors)
   - Links not working
   - All enhancements lost

## Solution

Restored CSS/JS files from previous commit (14cc3d8) before the regeneration.

## Solution (FINAL FIX - 2025-11-24)

**The script NOW ONLY generates data files. It NEVER touches HTML/CSS/JS:**

```bash
# Only way to run the script - generates JSON data only
python3 scripts/generate-dashboard.py
```

**Status:** ✅ **COMPLETELY FIXED** - HTML/CSS/JS are now treated as source code!

- Script renamed: "Dashboard Data Generator" (not "Dashboard Generator")
- Removed all flags and options
- Removed `copy_static_assets()` calls
- Removed `generate_html()` calls
- HTML/CSS/JS are version-controlled source files, edited directly

## What the Script Does Now

**ONLY generates JSON data files:**
- `dashboard/data/messages.json` - Message index
- `dashboard/data/messages-page-*.json` - Paginated messages
- `dashboard/data/topics.json` - Topic taxonomy
- `dashboard/data/files.json` - File references
- `dashboard/data/checkpoints.json` - Session data
- `dashboard/data/commands.json` - Command history
- `dashboard/data/git-commits.json` - Git commit history

**NEVER touches these source files:**
- `dashboard/index.html` - Application entry point
- `dashboard/css/*.css` - Styling
- `dashboard/js/*.js` - Application logic
- `dashboard/assets/*` - Images, fonts, etc.

## Current Status

**Fixed:** Commit 1e5553d restored all CSS/JS files ✅

All enhancements are back:
- ✅ AZ1.AI design system (theme)
- ✅ Date/time fixes (no more "7:00 PM" issues)
- ✅ File system timestamps
- ✅ Global word wrapping
- ✅ Hover behavior fixes
- ✅ All links working

## Recommendation

**✅ Script updated (2025-11-24):**
1. ✅ Default behavior now PRESERVES CSS/JS files (safe!)
2. ✅ Use `python3 scripts/generate-dashboard.py` to regenerate data only
3. ⚠️ Only use `--include-static` if intentionally updating base templates

---

**Last Updated:** 2025-11-24
**Incident:** Dashboard CSS/JS overwrite during regeneration
**Resolution:** Files restored from commit 14cc3d8
**Prevention:** Use `--skip-static` flag (to be implemented)
