# Aster Engine

Aster is the from-scratch browser engine used by UN_Vela on UN_Orion.

Current version: **0.1.0**.

Aster is not a Chromium, WebKit or Gecko port. The first implementation is intentionally small and freestanding-friendly.

## Current engine pipeline

`HTML -> tokenizer/parser -> fixed DOM -> layout -> paint list -> platform renderer`

Implemented today:
- HTML tokenizer/parser
- fixed-capacity DOM tree
- title/head/body/h1/h2/p/div/br/a/list/emphasis/code recognition
- entity decoding
- href metadata
- block/inline layout
- line wrapping
- paint list generation
- native text/link painting in the UN_Orion port

## Layout

- `include/aster.h` — public engine ABI
- `src/aster.c` — current engine implementation

The current `src/aster.c` mirrors the tested UN_Orion integration and uses the Orion graphics API as its first platform backend. The next engine milestone is extracting that paint backend behind a small adapter so the parser/layout core can be tested on a host PC independently of the OS.

## CSS selectors (0.3.1)
Aster supports `*`, tag, `.class`, `#id`, `tag.class`, `tag#id`, and comma-separated simple selector lists. Descendant, child, attribute and pseudo selectors remain intentionally unsupported. ID/class/tag specificity is applied for color and size within this compact cascade.
