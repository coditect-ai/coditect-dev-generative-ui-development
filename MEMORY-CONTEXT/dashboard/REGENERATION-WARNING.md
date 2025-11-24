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

## How to Prevent This

### Option 1: Default Behavior (Recommended) ✅ IMPLEMENTED
**As of 2025-11-24, the script NOW preserves CSS/JS files by default:**

```bash
# Default: Only regenerate JSON data files, preserve CSS/JS
python3 scripts/generate-dashboard.py

# Explicit: Overwrite CSS/JS files (use with caution!)
python3 scripts/generate-dashboard.py --include-static
```

**Status:** ✅ Implemented - CSS/JS files are now preserved by default!

### Option 2: Manual Process
1. **BEFORE** running `generate-dashboard.py`:
   ```bash
   # Backup CSS/JS files
   cp -r MEMORY-CONTEXT/dashboard/css MEMORY-CONTEXT/dashboard/css.backup
   cp -r MEMORY-CONTEXT/dashboard/js MEMORY-CONTEXT/dashboard/js.backup
   ```

2. Run regeneration:
   ```bash
   python3 scripts/generate-dashboard.py
   ```

3. **AFTER** regeneration, restore CSS/JS:
   ```bash
   # Restore CSS/JS files
   cp -r MEMORY-CONTEXT/dashboard/css.backup/* MEMORY-CONTEXT/dashboard/css/
   cp -r MEMORY-CONTEXT/dashboard/js.backup/* MEMORY-CONTEXT/dashboard/js/
   ```

### Option 3: Modify generate-dashboard.py
Add a `--skip-static` flag to skip copying static assets:

```python
parser.add_argument(
    '--skip-static',
    action='store_true',
    help='Skip copying CSS/JS static assets (preserve existing files)'
)

# In main():
if not args.skip_static:
    generator._copy_static_assets()
```

Then use:
```bash
python3 scripts/generate-dashboard.py --skip-static
```

## Files That Get Overwritten (with --include-static)

When `--include-static` flag is used, these files are **replaced**:
- `dashboard/css/main.css`
- `dashboard/css/layout.css`
- `dashboard/css/components.css`
- `dashboard/css/print.css`
- `dashboard/js/navigation.js`
- `dashboard/js/data-loader.js`
- `dashboard/index.html` ⚠️ **ALSO OVERWRITTEN** (as of 2025-11-24)

## Files That Are Safe (default behavior)

These files are **NOT** overwritten by default:
- `dashboard/css/*.css` (preserved)
- `dashboard/js/*.js` (preserved)
- `dashboard/index.html` (preserved) ✅ **NEW: Now protected by default**
- `dashboard/data/*.json` (intentionally regenerated with new data)

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
