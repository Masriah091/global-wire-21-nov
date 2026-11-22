[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Masriah091/global-wire-21-nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Masriah091/global-wire-21-nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# THE GLOBAL WIRE — Challenger E4 (round 4), Saturday 21 November 2026

A wire-service monochrome front page rebuilt from scratch for round 4:
same paper name and identity as the round-3 entry, entirely new page
architecture. The date is demoted to the black kicker bar; the giant
Playfair masthead is the paper's NAME. Below it: a red hook band with
the day's top 3 stories, a 5-slot UTC timeline, and THE DAY IN NUMBERS
(3 · 42 · -5.28% · 372,000 · €1BN · 159/1 — every figure bound to a card
on the page). Thirteen pictured cards (3 wide leads over two compact
wire rows), each with a data-carrying strip, caption band, source tag
and a deck of at least two verified facts from the 21 Nov pool — the EU
item reads "EU adopts €1bn military aid" (joint buying via the Peace
Facility; Britain pledges 1,000+ drones in a £260m package). A real-
polygon world map carries Ø18px numbered pins for cards 1–13 and grey
dots for briefs 14–40, beside the ALSO ON THE WIRE brief column. A red
DATE CHECK box names six Friday 20 November stories deliberately left
out, plus three not-yet-happened items. Footer carries the verification
line and sources.

## Duel record (mandatory pre-submit duel)

- Layout duel A/B/C, judged on 300px readability + completeness:
  - **A (WINNER)** — 3 wide leads + 2 rows of 5 compact cards. Biggest
    lead headlines, every deck fits its card, strips legible at 300px.
  - B — 2 wide leads + rows of 5 and 6. The 6-across row crushes deck
    type and loses at 300px.
  - C — uniform 5/4/4 grid, numbers strip above timeline. No lead
    hierarchy; leads read the same weight as brief-grade cards.
- 3D-vs-2D duel: a drop-shadow ("3D") treatment of layout A was rendered
  and compared at 300px. Flat **2D wins** — shadows only smudge the
  crisp wire identity at judging size. The shadow render is the noted
  backup treatment.

## Build

`draw.py` is a deterministic Pillow program (Python stdlib + PIL only,
no network) that renders `entry.png` at 1024×1024 (256-colour palette).
`main.py` is the hand-in: it copies the committed `entry.png` into
`os.environ["MAKEFUN_OUTPUT_DIR"]` (default `/output`). Rendering twice
produces a byte-identical file, and `main.py` passes a read-only,
`env -i`, unprivileged (`nobody`) isolation run.
