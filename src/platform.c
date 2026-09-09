#include "aster_platform.h"
#include "graphics.h"

static AsterPlatformOps g_ops;
static void *g_context;
static int g_ready;

static void mem_zero(void *p,size_t n){unsigned char*b=(unsigned char*)p;while(n--)*b++=0;}
static void mem_copy(void*d,const void*s,size_t n){unsigned char*dd=(unsigned char*)d;const unsigned char*ss=(const unsigned char*)s;while(n--)*dd++=*ss++;}

int aster_platform_install(const AsterPlatformOps *ops,void *context){
    mem_zero(&g_ops,sizeof(g_ops));g_context=context;g_ready=0;
    if(!ops)return 1;
    if((ops->abi_version>>16)!=ASTER_PLATFORM_ABI_MAJOR)return 0;
    if(ops->struct_size<offsetof(AsterPlatformOps,draw_text)+sizeof(ops->draw_text))return 0;
    size_t n=ops->struct_size<sizeof(g_ops)?ops->struct_size:sizeof(g_ops);
    mem_copy(&g_ops,ops,n);g_ready=1;return 1;
}
uint64_t aster_platform_capabilities(void){return g_ready?g_ops.capabilities:0;}
uint32_t gfx_text(uint32_t x,uint32_t y,const char*s,uint32_t rgb,uint32_t scale){if(g_ready&&(g_ops.capabilities&ASTER_PLATFORM_CAP_TEXT)&&g_ops.draw_text)return g_ops.draw_text(g_context,x,y,s,rgb,scale);uint32_t n=0;while(s&&s[n])n++;return n*11u*(scale?scale:1u);}
uint32_t gfx_display_text(uint32_t x,uint32_t y,const char*s,uint32_t rgb){if(g_ready&&(g_ops.capabilities&ASTER_PLATFORM_CAP_DISPLAY_TEXT)&&g_ops.draw_display_text)return g_ops.draw_display_text(g_context,x,y,s,rgb);return gfx_text(x,y,s,rgb,2);}
void gfx_line_h(uint32_t x,uint32_t y,uint32_t w,uint32_t rgb){if(g_ready&&(g_ops.capabilities&ASTER_PLATFORM_CAP_LINES)&&g_ops.draw_line_h)g_ops.draw_line_h(g_context,x,y,w,rgb);}
int gfx_image_uri(uint32_t x,uint32_t y,uint32_t w,uint32_t h,const char *uri){if(g_ready&&(g_ops.capabilities&ASTER_PLATFORM_CAP_IMAGE_URI)&&g_ops.draw_image_uri)return g_ops.draw_image_uri(g_context,x,y,w,h,uri);return 0;}
