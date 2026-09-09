#include <stdio.h>
#include <string.h>
#include "aster.h"

static int paint_has_text(const AsterDocument*d,const char*needle){
    for(unsigned i=0;i<d->paint_count;i++){
        const AsterPaintItem*p=&d->paint[i];
        if(!p->text_len)continue;
        char b[96];unsigned n=p->text_len<sizeof(b)-1?p->text_len:(unsigned)sizeof(b)-1;
        for(unsigned j=0;j<n;j++)b[j]=d->text[p->text_off+j];b[n]=0;
        if(strstr(b,needle))return 1;
    }
    return 0;
}

int main(void){
    AsterDocument d;
    const char *html="<html><head><title>Aster selectors</title><style>p{color:#123456}.notice{font-weight:bold}#hero{color:#654321}p.notice{font-size:24px}.accent,#other{text-decoration:underline}#gone{display:none}</style></head><body><p id='hero' class='notice accent'>Hello CSS</p><p id='other'>Other</p><p id='gone'>hidden id</p><img src='test.bmp' alt='demo' width='64' height='32'></body></html>";
    if(!aster_parse_html(&d,html))return 1;
    aster_layout(&d,320);
    if(d.css_count<7)return 2;
    int saw_hero=0,saw_other=0,saw_image=0;
    for(unsigned i=0;i<d.paint_count;i++){
        const AsterPaintItem*p=&d.paint[i];
        if((p->flags&ASTER_PAINT_BOLD)&&(p->flags&ASTER_PAINT_UNDERLINE)&&p->color==0x654321&&p->scale==2)saw_hero=1;
        if((p->flags&ASTER_PAINT_UNDERLINE)&&p->color==0x123456)saw_other=1;
        if(p->flags&ASTER_PAINT_IMAGE)saw_image=1;
    }
    if(!saw_hero||!saw_other||!saw_image)return 3;
    if(paint_has_text(&d,"hidden"))return 4;
    if(d.document_height<=32)return 5;
    puts("Aster CSS selector/image smoke passed");
    return 0;
}
