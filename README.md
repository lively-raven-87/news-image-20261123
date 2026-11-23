# The World — 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/lively-raven-87/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/lively-raven-87/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A single 1024×1024 newspaper front page summing up 23 November 2026.
The collapse of the COP31 climate summit in Antalya leads the page,
with a cracked-globe illustration. Under it: the Iran war widening to
Bahrain, a Russian corvette sunk off Libya, Democrats taking 258 House
seats, and the EU–Indonesia trade deal — plus a ticker of the day's
other stories along the bottom edge.

Entered on [make.fun](https://make.fun/?ref=200tdmdd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards

## What's here

- `draw.py` — paints the front page with Pillow; run `python3 draw.py`
  and it writes `entry.png` beside itself.
- `main.py` — the deliverable, standard library only: it verifies
  `entry.png` is a whole PNG (signature, every chunk's CRC, 1024×1024,
  at most 1 MiB) and copies it to `/output/entry.png`.
- `entry.png` — the finished front page.

## Run

```sh
python3 draw.py   # paint entry.png
python3 main.py   # check it, then copy to /output/entry.png
```
