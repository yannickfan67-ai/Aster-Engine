#ifndef ASTER_GRAPHICS_COMPAT_H
#define ASTER_GRAPHICS_COMPAT_H
#include <stdint.h>
uint32_t gfx_text(uint32_t x,uint32_t y,const char *s,uint32_t rgb,uint32_t scale);
uint32_t gfx_display_text(uint32_t x,uint32_t y,const char *s,uint32_t rgb);
void gfx_line_h(uint32_t x,uint32_t y,uint32_t w,uint32_t rgb);
int gfx_image_uri(uint32_t x,uint32_t y,uint32_t w,uint32_t h,const char *uri);
#endif
