# THE WORLD IN ONE DAY — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/top234/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/top234/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One 1024×1024 newspaper page summing up Wednesday 25 November 2026:
35 stories, 5 regions, every one dated that day.

- **3 top stories, each with a scene drawn in code:** Houthis hit Riyadh's
  PIF Tower (11 wounded), Zelenskiy confirms Ukraine hit a Russian cargo
  ship, Huawei convicted in a US trial.
- **10 numbered small cards (#4–#13)** with mini icons, a proportional
  region bar (Americas 10 · Middle East 8 · Europe 7 · Asia-Pacific 7 ·
  World 3), a dotted world map with numbered pins, and the remaining
  22 stories (#14–#35) in two columns.
- **DATE CHECK box** explaining the dating method (TUE = the news the
  world woke up to on Wednesday 25 November; WED = reported on Wednesday
  itself; sources Reuters / AP / BBC / Washington Post).

## Run

```sh
mkdir -p out && OUTPUT_DIR=out node main.ts   # draws with generate.py (Python + PIL)
```

If Python or PIL is missing, `main.ts` falls back to the bundled
`entry.png` and verifies it the same way: PNG signature, IHDR 1024×1024,
≤ 1 MiB, intact IEND trailer, sha256 printed. Both paths write identical
bytes. Fully deterministic: no clock, no network, no randomness — every
date and figure is hardcoded from the research notes.

## Files

- `generate.py` — draws `entry.png` from scratch with Pillow.
- `main.ts` — Node 22 entrypoint: runs `generate.py`, else copies the
  bundled image, then verifies the PNG.
- `entry.png` — the rendered image, bundled for the fallback path.
- `package.json` — `render` / `start` scripts.

Bounty: https://make.fun/bounty/news-image-20261125
