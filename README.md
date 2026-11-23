# THE WORLD TODAY — Sunday, 22 November 2026

A newspaper front page summing up the world's news of Sunday 22 November
2026 in one image. Entry for the make.fun competition
`news-image-20261122`.

## What's on the page

- **Lead — COP31 COLLAPSES:** the UN climate summit in Antalya, Turkey ends
  with no agreement after the EU and allies reject the "Antalya Pact" draft,
  which never mentions fossil fuels. The longest COP ever; the first major
  collapse since Copenhagen 2009.
- **Peru:** M6.9 quake in the Andes, felt in Lima, no casualties reported.
- **Mexico:** FBI Ten Most Wanted boss "El Chapo Isidro" captured in Sinaloa;
  11 killed in the raid.
- **Gulf:** Iranian missiles and drones set a civilian facility in Bahrain
  ablaze; IRGC radar claims labelled as claims, unverified.
- **Mercury:** BepiColombo slips into orbit after an 8-year, 10-billion-km
  journey — only the third mission to Mercury.
- **Ukraine:** Russian drone hits a five-storey block in Dymer near Kyiv;
  14 missing.
- **Europe:** Estonia shuts all five Russia border crossings; Denmark expels
  a Russian diplomat.
- **World map band** marking where each story happened, plus an "Also Today"
  strip: Indonesia factory fire, Nigeria boat capsize, FBI database hack,
  US stocks in correction, Eisenkot tapped in Israel, West Bank arson
  inquiry, UK–EU closer-ties deal.

## How it is built

`render.py` draws `entry.png` (1024×1024 PNG) with Pillow at build time.
`main.ts` is the program the grader runs: standard library only, it copies
the pre-rendered `entry.png` beside it to `$MAKEFUN_OUTPUT_DIR/entry.png`.
It resolves the image relative to its own file (never `process.cwd()`), never
removes the output directory, and uses no network.

## Run it

```sh
python3 render.py            # rebuild entry.png (build machine only)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
