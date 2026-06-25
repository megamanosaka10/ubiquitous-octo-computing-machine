# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

**`megamanosaka10/ubiquitous-octo-computing-machine`** is a utility repository containing a Windows CMD bootstrap installer for Claude Code and a GitHub Actions security scanning workflow.

### Files

| File | Purpose |
|------|---------|
| `install.cmd` | Windows CMD bootstrap script that downloads and installs the Claude Code CLI |
| `.github/workflows/codeql.yml` | GitHub Actions CodeQL security analysis, runs on push/PR to `main` and weekly |
| `README.md` | Minimal — just the repo name |

## `install.cmd` — Claude Code Windows installer

A Windows CMD alternative to the PowerShell installer, for environments where PowerShell is unavailable.

### Usage

```cmd
install.cmd                  # installs latest stable
install.cmd stable           # explicit stable channel
install.cmd latest           # latest (including pre-release)
install.cmd 1.0.58           # pin a specific version
```

**Requirements**: 64-bit Windows (x64 or ARM64), `curl` on PATH, `certutil` (built-in on Windows).

### How it works

1. Detects architecture (`win32-x64` or `win32-arm64`)
2. Fetches version from `https://downloads.claude.ai/claude-code-releases/latest`
3. Downloads and parses `manifest.json` to extract the SHA-256 checksum for the platform
4. Downloads the versioned binary (`claude-<ver>-<platform>.exe`)
5. Verifies SHA-256 with `certutil -hashfile`
6. Runs `claude install <target>` to set up the launcher and shell integration
7. Cleans up the temporary binary

### Key subroutines

- `:download_file` — thin wrapper around `curl -fsSL`
- `:parse_manifest` — line-by-line JSON parser (no external JSON tool needed)
- `:check_length` — validates SHA-256 string is exactly 64 hex chars
- `:verify_checksum` — calls `certutil` and compares against expected hash

### Known limitations

- The manifest parser is a line-by-line CMD loop; malformed or minified JSON may confuse it.
- No retry logic — a network failure aborts immediately.
- Temporary binary is written to `%USERPROFILE%\.claude\downloads\`; the cleanup uses `timeout /t 1` to release file handles, which is a heuristic.

## GitHub Actions

### CodeQL (`.github/workflows/codeql.yml`)

- Triggers: push and PR to `main`; scheduled every Friday at 11:16 UTC
- Language matrix is auto-detected (currently empty — no compiled languages in repo)
- Uses `github/codeql-action/init@v4` and `github/codeql-action/analyze@v4`
- To add a language: extend the `matrix.include` array in the workflow

## Development conventions

- **Active branch**: `claude/claude-md-docs-kmhw4f` (feature work); `main` is the default branch
- **No build step**: everything is plain CMD script and YAML
- **Language**: Swedish may appear in commit messages and comments (user is Swedish-speaking)
- **Testing `install.cmd`**: requires a real Windows machine or CI with `windows-latest`; cannot be unit-tested in Linux/macOS

## Home directory context

The CLAUDE.md inherited context below applies when Claude Code is invoked from the user's home directory (`~`), not from this repository. Active local projects live in subdirectories of `~`:

### swingbt — swing trading backtester

Primary coding project. Two versions in `~/Downloads/`:

**Standalone CLI** (`~/Downloads/swingbt.py` or `swingbt_fixed_v2_core.py`):
```bash
cd ~/Downloads
pip3 install yfinance pandas numpy tabulate
python3 swingbt.py list
python3 swingbt.py test -s connors_rsi2 -w us_tech
python3 swingbt.py portfolio -s connors_rsi2 -w us_all
python3 swingbt.py scan -s connors_rsi2 -w us_all
python3 swingbt.py report -w us_all
```

**Streamlit app** (`~/Downloads/swingbt_app_package/`):
```bash
cd ~/Downloads/swingbt_app_package
pip install -r requirements_swingbt_app.txt
streamlit run swingbt_app.py
```

**Expansion module** (`~/Desktop/files/swingbt_expansion.py`): Adds Setup D (accumulation breakout) and Setup E (momentum continuation). Place next to the `swingbt/` directory and import into `__init__.py`.

**Architecture of `swingbt_fixed_v2_core.py`:**
- `UNIVERSE` table — tickers tagged with market (US/SE), sector, and size cap
- Backtesting engine — models intraday stop/target hits, gap fills at open, 1%-risk sizing
- Five commands: `list`, `test`, `portfolio`, `scan`, `report`
- Streamlit UI is a pure presentation layer; all trading logic lives in core

**7 built-in strategies**: `connors_rsi2`, `ema_pullback`, `bollinger_mr`, `donchian`, `accumulation_bo`, `momentum_cont`, `post_event_mr`

**Known limitations**: yfinance has survivorship bias; `same_close` entry is a proxy; intraday stop-before-target order is assumed.

**Dependencies**: `yfinance`, `pandas`, `numpy`, `tabulate`, `streamlit`, `matplotlib`, `pyarrow`

### personal-finance-tracker

`~/Desktop/personal-finance-tracker/` — vanilla HTML/CSS/JS, no build step. Open `index.html` in a browser. Data stored in `localStorage`.

### Pine Script strategies

`~/Desktop/files/*.pine` — TradingView indicators/strategies (Pine Script v6). Load via Pine Editor in TradingView. Mirror the Python strategy logic.

## Language

The user writes and reads Swedish fluently. Code comments, variable names, and documentation in existing files are often in Swedish — match the language style of the file being edited.
