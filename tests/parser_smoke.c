#include <stdio.h>
#include "aster.h"

int main(void){
    AsterDocument d;
    const char *html="<html><head><title>Aster CSS</title><style>p{color:#123456;font-weight:bold} span{display:none}</style></head><body><p style='font-size:24px'>Hello CSS</p><span>hidden</span><img src='test.bmp' alt='demo' width='64' height='32'></body></html>";
    if(!aster_parse_html(&d,html))return 1;
    aster_layout(&d,320);
    if(d.css_count<2)return 2;
    if(d.paint_count<2)return 3;
    int saw_css=0,saw_image=0;
    for(unsigned i=0;i<d.paint_count;i++){
        if((d.paint[i].flags&ASTER_PAINT_BOLD)&&d.paint[i].color==0x123456&&d.paint[i].scale==2)saw_css=1;
        if(d.paint[i].flags&ASTER_PAINT_IMAGE)saw_image=1;
    }
    if(!saw_css||!saw_image)return 4;
    if(d.document_height<=32)return 5;
    puts("Aster parser/CSS/image smoke passed");
    return 0;
}
