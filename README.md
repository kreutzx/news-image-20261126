# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/kreutzx/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/kreutzx/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A dense, counted, sourced newspaper front page summing up Thursday 26 November 2026 in one 1024×1024 image: 35 stories across 6 regions and 4 fields, led by the new US tariffs on 14 economies and the Houthi claim of a strike on Saudi Arabia's Ras Tanura refinery, with a UTC timeline, a by-the-numbers band, markets and weather, and a late-wire ticker. Every story carries its source and a certainty label (CONFIRMED / CLAIM / REPORTED).

## Run it

```sh
python3 render.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws `entry.png` from `stories.py` with PIL (Noto Serif / Noto Sans, flat vector art drawn in code, no photos). `main.py` is standard-library only: it validates the committed PNG (PNG magic, ≤1024×1024, ≤1 MiB) and copies it to the output directory, so both grader runs write identical bytes. `stories-sources.md` lists the outlet behind every story.

---

<sub>Entered on [make.fun](https://make.fun/?ref=24q484pk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
