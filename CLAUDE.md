# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## This directory

This is the home directory (`~`), not a single repository. Active projects live in subdirectories. Swedish is used in filenames, comments, and documentation throughout.

## Main projects

### swingbt — swing trading backtester

The primary coding project. Two versions exist in `~/Downloads/`:

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

**Expansion module** (`~/Desktop/files/swingbt_expansion.py`): Adds Setup D (accumulation breakout) and Setup E (momentum continuation). Intended to be placed next to the `swingbt/` directory and imported into `__init__.py`.

**Architecture of `swingbt_fixed_v2_core.py`:**
- `UNIVERSE` table — all tickers tagged with market (US/SE), sector, and size cap; drives watchlist filtering and sector/regime breakdown in reports
- Backtesting engine — models intraday stop/target hits, gap fills at open, and 1%-risk position sizing
- Five commands: `list`, `test` (per-ticker edge), `portfolio` (shared capital, max 5 positions), `scan` (today's signals), `report` (all strategies vs watchlist → markdown + CSV in `output/`)
- `Streamlit` UI (`swingbt_app.py`) is a pure presentation layer over `swingbt_fixed_v2_core`; trading logic lives only in core

**The 7 built-in strategies:**
`connors_rsi2`, `ema_pullback`, `bollinger_mr`, `donchian`, `accumulation_bo`, `momentum_cont`, `post_event_mr`

**Key known limitations**: yfinance data has survivorship bias and is not point-in-time; `same_close` entry is a proxy; intraday order of stop vs target is assumed (stop first).

**Dependencies**: `yfinance`, `pandas`, `numpy`, `tabulate`, `streamlit`, `matplotlib`, `pyarrow`

### personal-finance-tracker

`~/Desktop/personal-finance-tracker/` — vanilla HTML/CSS/JS, no build step. Open `index.html` in a browser. Expenses stored in `localStorage`.

### Pine Script strategies

`~/Desktop/files/*.pine` — TradingView indicators/strategies (Pine Script v6). Load via Pine Editor in TradingView. Mirror the same logic as the Python strategies.

## Language

The user writes and reads Swedish fluently. Code comments, variable names, and documentation in existing files are often in Swedish — match the language style of the file being edited.
