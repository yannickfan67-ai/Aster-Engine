# Aster Engine roadmap

Aster remains a rendering-engine project, not a browser UI project.

## HTML
- tokenizer states closer to HTML5 rules
- error-tolerant tree builder
- attributes beyond `href`
- tables, forms, headings, lists, preformatted text and semantic elements
- UTF-8 text decoding

## Style
- CSS tokenizer/parser
- selector matching and cascade
- inherited/computed styles
- colors, fonts, margins, padding, borders and backgrounds

## Layout
- explicit box tree separate from DOM
- block and inline formatting contexts
- intrinsic sizing and overflow
- scrolling and hit testing
- basic flex layout after block/inline stabilizes

## Paint/media
- clip stacks and dirty rectangles
- images with a small decoder interface
- link/form/input hit-test metadata
- incremental repaint

## Portability
- keep the core independent from UN_Orion window chrome
- isolate graphics/font callbacks behind a host interface
- deterministic parser/layout tests that run on a normal host CI runner
