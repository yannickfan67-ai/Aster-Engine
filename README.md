# Aster Engine

Aster is the from-scratch browser engine used by UN_Vela on UN_Orion.

Current version: **0.3.2**. Public ABI: **1.3**.

Aster is not a Chromium, WebKit or Gecko port. The implementation remains intentionally small, fixed-capacity and freestanding-friendly.

## Current engine pipeline

`HTML -> tokenizer/parser -> fixed DOM -> CSS cascade -> layout -> paint list -> platform renderer`

Implemented today:
- fixed-capacity HTML tokenizer/parser and DOM tree
- semantic document elements, headings, paragraphs, links, lists and emphasis
- entity decoding plus script/style source suppression
- href/src metadata and image paint items
- block/inline layout and line wrapping
- scroll-aware link hit testing and document height
- lightweight CSS cascade with inline styles
- native text/link/image painting hooks used by the UN_Orion port

## Layout

- `include/aster.h` — public engine ABI
- `src/aster.c` — current engine implementation
- `tests/parser_smoke.c` — parser/layout/CSS regression smoke

The current `src/aster.c` mirrors the tested UN_Orion integration and uses the Orion graphics API as its first platform backend. Parser/layout portability is continuously checked for x86_64, AArch64 and RISC-V64.

## CSS selectors (0.3.2)

Aster supports:
- `*` and tag selectors
- `.class` and `#id`
- `tag.class` and `tag#id`
- compound class selectors such as `.card.active` and `button.primary.large`
- comma-separated simple selector lists
- multiple class-token matching on elements
- compact ID/class/tag specificity for color and font-size cascade
- inline styles and additive style flags such as bold, underline and `display:none`

Descendant, child, sibling, attribute and pseudo selectors remain intentionally unsupported. The 0.3.2 compound-class work does not change the public document structure, so the engine remains on API 1.3.
