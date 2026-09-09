from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"missing expected snippet in {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new))

# Public ABI: selector metadata is stored in fixed-capacity node/rule records.
replace("include/aster.h", '#define ASTER_VERSION "0.3.0"', '#define ASTER_VERSION "0.3.1"')
replace("include/aster.h", '#define ASTER_API_MINOR 2u', '#define ASTER_API_MINOR 3u')
replace(
    "include/aster.h",
    '    uint16_t text_off,text_len,href_off,href_len,src_off,src_len;\n    uint16_t width_hint,height_hint;\n',
    '    uint16_t text_off,text_len,href_off,href_len,src_off,src_len;\n    uint16_t id_off,id_len,class_off,class_len;\n    uint16_t width_hint,height_hint;\n'
)
replace(
    "include/aster.h",
    'typedef struct { uint8_t tag,flags,scale,color_set; uint32_t color; } AsterCssRule;',
    'typedef struct {\n    uint8_t tag,selector_kind,flags,scale,color_set;\n    uint16_t selector_off,selector_len;\n    uint32_t color;\n} AsterCssRule;'
)

# Selector kinds stay private to the engine; the struct only carries the compact discriminator.
replace(
    "src/aster.c",
    '#define CSS_ANY_TAG 255u\ntypedef struct {uint8_t flags,scale,color_set;uint32_t color;} ParsedStyle;',
    '#define CSS_ANY_TAG 255u\n#define CSS_SELECTOR_ANY 0u\n#define CSS_SELECTOR_TAG 1u\n#define CSS_SELECTOR_CLASS 2u\n#define CSS_SELECTOR_ID 3u\n#define CSS_SELECTOR_TAG_CLASS 4u\n#define CSS_SELECTOR_TAG_ID 5u\ntypedef struct {uint8_t flags,scale,color_set;uint32_t color;} ParsedStyle;'
)
replace(
    "src/aster.c",
    'n->href_off=0;n->href_len=0;n->src_off=0;n->src_len=0;n->width_hint=0;n->height_hint=0;',
    'n->href_off=0;n->href_len=0;n->src_off=0;n->src_len=0;n->id_off=0;n->id_len=0;n->class_off=0;n->class_len=0;n->width_hint=0;n->height_hint=0;'
)

old_css = '''static void parse_css_rules(AsterDocument*d,const char*s,size_t len){size_t p=0;while(p<len&&d->css_count<ASTER_MAX_CSS_RULES){while(p<len&&is_space(s[p]))p++;size_t ss=p;while(p<len&&s[p]!='{')p++;if(p>=len)break;size_t sn=p-ss;p++;size_t ds=p;while(p<len&&s[p]!='}')p++;size_t dn=p-ds;if(p<len)p++;while(sn&&is_space(s[ss+sn-1]))sn--;while(sn&&is_space(s[ss])){ss++;sn--;}uint8_t tag=CSS_ANY_TAG;if(!(sn==1&&s[ss]=='*')){tag=tag_id(s+ss,sn);if(tag==ASTER_TAG_UNKNOWN)continue;}ParsedStyle st=parse_style_text(s+ds,dn);AsterCssRule*r=&d->css[d->css_count++];r->tag=tag;r->flags=st.flags;r->scale=st.scale;r->color_set=st.color_set;r->color=st.color;}}'''
new_css = '''static int simple_selector(AsterDocument*d,const char*s,size_t n,AsterCssRule*r){while(n&&is_space(*s)){s++;n--;}while(n&&is_space(s[n-1]))n--;if(!n)return 0;for(size_t i=0;i<n;i++)if(is_space(s[i])||s[i]=='>'||s[i]=='['||s[i]==':'||s[i]=='+')return 0;r->tag=CSS_ANY_TAG;r->selector_kind=CSS_SELECTOR_ANY;r->selector_off=0;r->selector_len=0;if(n==1&&s[0]=='*')return 1;size_t split=n;char marker=0;for(size_t i=0;i<n;i++)if(s[i]=='.'||s[i]=='#'){split=i;marker=s[i];break;}if(split==0){if(n<2)return 0;r->selector_kind=marker=='.'?CSS_SELECTOR_CLASS:CSS_SELECTOR_ID;r->selector_off=store_bytes(d,s+1,n-1);r->selector_len=(uint16_t)(n-1);return r->selector_len!=0;}uint8_t tag=tag_id(s,split);if(tag==ASTER_TAG_UNKNOWN)return 0;r->tag=tag;if(!marker){r->selector_kind=CSS_SELECTOR_TAG;return 1;}if(split+1>=n)return 0;r->selector_kind=marker=='.'?CSS_SELECTOR_TAG_CLASS:CSS_SELECTOR_TAG_ID;r->selector_off=store_bytes(d,s+split+1,n-split-1);r->selector_len=(uint16_t)(n-split-1);return r->selector_len!=0;}
static void add_css_selector(AsterDocument*d,const char*s,size_t n,ParsedStyle st){if(d->css_count>=ASTER_MAX_CSS_RULES)return;AsterCssRule r;r.flags=st.flags;r.scale=st.scale;r.color_set=st.color_set;r.color=st.color;if(!simple_selector(d,s,n,&r))return;d->css[d->css_count++]=r;}
static void parse_css_rules(AsterDocument*d,const char*s,size_t len){size_t p=0;while(p<len&&d->css_count<ASTER_MAX_CSS_RULES){while(p<len&&is_space(s[p]))p++;size_t ss=p;while(p<len&&s[p]!='{')p++;if(p>=len)break;size_t sn=p-ss;p++;size_t ds=p;while(p<len&&s[p]!='}')p++;size_t dn=p-ds;if(p<len)p++;ParsedStyle st=parse_style_text(s+ds,dn);size_t q=0;while(q<sn&&d->css_count<ASTER_MAX_CSS_RULES){size_t a=q;while(q<sn&&s[ss+q]!=',')q++;add_css_selector(d,s+ss+a,q-a,st);if(q<sn&&s[ss+q]==',')q++;}}}'''
replace("src/aster.c", old_css, new_css)

replace(
    "src/aster.c",
    'if(attr_value(s,len,"src",&v,&vn)&&vn){n->src_off=store_bytes(d,v,vn);n->src_len=(uint16_t)vn;}if(attr_value(s,len,"alt",&v,&vn)&&vn)',
    'if(attr_value(s,len,"src",&v,&vn)&&vn){n->src_off=store_bytes(d,v,vn);n->src_len=(uint16_t)vn;}if(attr_value(s,len,"id",&v,&vn)&&vn){n->id_off=store_bytes(d,v,vn);n->id_len=(uint16_t)vn;}if(attr_value(s,len,"class",&v,&vn)&&vn){n->class_off=store_bytes(d,v,vn);n->class_len=(uint16_t)vn;}if(attr_value(s,len,"alt",&v,&vn)&&vn)'
)

old_apply = '''static void apply_rule_for(const AsterDocument*d,uint8_t tag,ParsedStyle*st){for(uint8_t i=0;i<d->css_count;i++){const AsterCssRule*r=&d->css[i];if(r->tag!=CSS_ANY_TAG&&r->tag!=tag)continue;st->flags|=r->flags;if(r->scale)st->scale=r->scale;if(r->color_set){st->color_set=1;st->color=r->color;}}}'''
new_apply = '''static int text_eq_range(const AsterDocument*d,uint16_t off,uint16_t len,const char*s,uint16_t n){if(len!=n||(size_t)off+len>ASTER_TEXT_CAP)return 0;for(uint16_t i=0;i<len;i++)if(d->text[off+i]!=s[i])return 0;return 1;}
static int class_has(const AsterDocument*d,const AsterNode*n,uint16_t off,uint16_t len){if(!n->class_len||(size_t)n->class_off+n->class_len>ASTER_TEXT_CAP||(size_t)off+len>ASTER_TEXT_CAP)return 0;const char*w=d->text+off;uint16_t p=0;while(p<n->class_len){while(p<n->class_len&&is_space(d->text[n->class_off+p]))p++;uint16_t a=p;while(p<n->class_len&&!is_space(d->text[n->class_off+p]))p++;uint16_t count=(uint16_t)(p-a);if(count==len){int same=1;for(uint16_t i=0;i<len;i++)if(d->text[n->class_off+a+i]!=w[i]){same=0;break;}if(same)return 1;}}return 0;}
static int rule_matches(const AsterDocument*d,const AsterCssRule*r,const AsterNode*n){if(r->tag!=CSS_ANY_TAG&&r->tag!=n->tag)return 0;switch(r->selector_kind){case CSS_SELECTOR_ANY:case CSS_SELECTOR_TAG:return 1;case CSS_SELECTOR_CLASS:case CSS_SELECTOR_TAG_CLASS:return class_has(d,n,r->selector_off,r->selector_len);case CSS_SELECTOR_ID:case CSS_SELECTOR_TAG_ID:return n->id_len&&text_eq_range(d,n->id_off,n->id_len,d->text+r->selector_off,r->selector_len);default:return 0;}}
static uint8_t rule_specificity(const AsterCssRule*r){switch(r->selector_kind){case CSS_SELECTOR_ID:return 100;case CSS_SELECTOR_TAG_ID:return 101;case CSS_SELECTOR_CLASS:return 10;case CSS_SELECTOR_TAG_CLASS:return 11;case CSS_SELECTOR_TAG:return 1;default:return 0;}}
static void apply_rule_for(const AsterDocument*d,int node,ParsedStyle*st){const AsterNode*n=&d->nodes[node];uint8_t color_spec=0,scale_spec=0;int color_order=-1,scale_order=-1;for(uint8_t i=0;i<d->css_count;i++){const AsterCssRule*r=&d->css[i];if(!rule_matches(d,r,n))continue;uint8_t spec=rule_specificity(r);st->flags|=r->flags;if(r->scale&&(spec>scale_spec||(spec==scale_spec&&(int)i>=scale_order))){st->scale=r->scale;scale_spec=spec;scale_order=i;}if(r->color_set&&(spec>color_spec||(spec==color_spec&&(int)i>=color_order))){st->color_set=1;st->color=r->color;color_spec=spec;color_order=i;}}}'''
replace("src/aster.c", old_apply, new_apply)
replace("src/aster.c", 'apply_rule_for(d,d->nodes[n].tag,&st);', 'apply_rule_for(d,n,&st);')
replace("src/aster.c", 'apply_rule_for(d,n->tag,&st);', 'apply_rule_for(d,chain[i],&st);')

# Strengthen smoke coverage: tag + class + id + tag.class + comma lists + hidden id.
Path("tests/parser_smoke.c").write_text(r'''#include <stdio.h>
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
''')

# Keep docs explicit about the supported lightweight subset.
readme = Path("README.md").read_text()
if "`.class`" not in readme:
    readme += "\n## CSS selectors (0.3.1)\nAster supports `*`, tag, `.class`, `#id`, `tag.class`, `tag#id`, and comma-separated simple selector lists. Descendant, child, attribute and pseudo selectors remain intentionally unsupported. ID/class/tag specificity is applied for color and size within this compact cascade.\n"
Path("README.md").write_text(readme)
