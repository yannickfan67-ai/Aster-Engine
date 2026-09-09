#ifndef ASTER_PLATFORM_H
#define ASTER_PLATFORM_H
#include <stdint.h>
#include <stddef.h>

#define ASTER_PLATFORM_ABI_MAJOR 1u
#define ASTER_PLATFORM_ABI_MINOR 1u
#define ASTER_PLATFORM_ABI_VERSION ((ASTER_PLATFORM_ABI_MAJOR << 16) | ASTER_PLATFORM_ABI_MINOR)
#define ASTER_PLATFORM_CAP_TEXT         (1ull << 0)
#define ASTER_PLATFORM_CAP_DISPLAY_TEXT (1ull << 1)
#define ASTER_PLATFORM_CAP_LINES        (1ull << 2)
#define ASTER_PLATFORM_CAP_IMAGE_URI    (1ull << 3)

typedef struct AsterPlatformOps {
    uint32_t abi_version;
    uint32_t struct_size;
    uint64_t capabilities;
    uint32_t (*draw_text)(void *context,uint32_t x,uint32_t y,const char *text,uint32_t rgb,uint32_t scale);
    uint32_t (*draw_display_text)(void *context,uint32_t x,uint32_t y,const char *text,uint32_t rgb);
    void (*draw_line_h)(void *context,uint32_t x,uint32_t y,uint32_t width,uint32_t rgb);
    int (*draw_image_uri)(void *context,uint32_t x,uint32_t y,uint32_t width,uint32_t height,const char *uri);
    void *reserved[7];
} AsterPlatformOps;

int aster_platform_install(const AsterPlatformOps *ops,void *context);
uint64_t aster_platform_capabilities(void);
#endif
