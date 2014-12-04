from dragonfly import MappingRule

from actions.action_shortcut import (
    K,
    T,
    P
)

import choices.base as chc_base
import choices.web as chc_web

#---------------------------------------------------------------------------
# Unused
#---------------------------------------------------------------------------

def start_tag(element):
    if element in voidElements:
        T("<%s />" % str(element)).execute()
    else:
        T("<%s>" % str(element)).execute()
        
def tags(element):
    elementString = str(element)
    if element in voidElements:
        T("<%s />" % str(element)).execute()
    else:
        T("<%s></%s>" % (elementString, elementString)).execute()
        K("left:%s" % (len(elementString) + 3)).execute()
        
def end_tag(element):
    T("</%s>" % str(element)).execute()
    
def attribute_with_content(attribute, text):
    T(' %(attribute)s=""').execute()
    K("left").execute()
    # SCText is undefined!
    # SCText(str(text)).execute()

#---------------------------------------------------------------------------
# Html Core Rule
#---------------------------------------------------------------------------

class HtmlCoreRule(MappingRule):
    mapping = {
        # doctype
        "doc type": T("<!DOCTYPE >") + K("left")
        , "doc type five": T("<!DOCTYPE html>")
        , "doc type four [strict]": T('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
        , "H doc type four loose": T('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">')
        , "doc type four frames": T('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">')
        , "doc type X one [strict]": T('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
        , "doc type X one loose": T('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        , "doc type X one frames": T('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">')
        , "doc type X one one": T('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')
        , "comment": T("<!--   -->") + K("left:5")
        , "comment <text>": T("<!-- %(text)s -->")
        , "open comment": T("<!-- ")
        , "close comment": T(" -->")
        # html_elements
        , "(open | start) <html_element>": T("<%(html_element)s>")
        , "(close | end | stop) <html_element>": T("</%(html_element)s>")
        , "<html_element>": T("<%(html_element)s></")
        , "<html_element> ID": T('<%(html_element)s id="">') + K("left:2")
        , "<html_element> ID <text>": T('<%(html_element)s id="%(text)s"></')
        , "<html_element> class": T('<%(html_element)s class="">') + K("left:2")
        , "<html_element> class <text>": T('<%(html_element)s class="%(text)s"></')
        # attributes
        , "<html_attribute>": T(' %(html_attribute)s=""') + K("left")
        , "<html_attribute> [equals] <text>": T(' %(html_attribute)s="%(text)s"')
        
        , "download": T(' download')
        , "download <text>": T(' download="%(text)s"')
        , "HREF": T(' href=""') + K("left")
        , "HREF <text>": T(' href="%(text)s"')
        , "HREF lang": T(' hreflang=""') + K("left")
        , "HREF lang <html_language_code>": T(' hreflang="%(html_language_code)s"')
        , "HREF lang <text>": T(' hreflang="%(text)s"')
        , "media": T(' media=""') + K("left")
        , "media <text>": T(' media="%(text)s"')
        , "(relation | relationship)": T(' rel=""') + K("left")
        , "(relation | reltionship) <html_relationship>": K(' rel="%(html_relationship)s"')
        , "target": T(' target=""') + K("left")
        , "target <html_target>": T(' target="%(html_target)s"')
        , "media type": T(' type=""') + K("left")
        # title
        , "title": T("<title></")
        # meta
        # page
        , "diff": T('<div></')
        , "diff ID [<text>]": T('<div id="%(text)s"></')
        , "diff class [<text>]": T('<div class="%(text)s"></')
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
        , chc_web.html_element
        , chc_web.html_attribute
        , chc_web.html_language_code
        , chc_web.html_relationship
        , chc_web.html_target
    ]



class HtmlTemplateRule(MappingRule):
    mapping = {
        "Lorem ipsum [short]": K("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,dot")
        , "Lorem ipsum medium": K("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot")
        , "Lorem ipsum long": K("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot,space,D,u,i,s,space,a,u,t,e,space,i,r,u,r,e,space,d,o,l,o,r,space,i,n,space,r,e,p,r,e,h,e,n,d,e,r,i,t,space,i,n,space,v,o,l,u,p,t,a,t,e,space,v,e,l,i,t,space,e,s,s,e,space,c,i,l,l,u,m,space,d,o,l,o,r,e,space,e,u,space,f,u,g,i,a,t,space,n,u,l,l,a,space,p,a,r,i,a,t,u,r,dot,space,E,x,c,e,p,t,e,u,r,space,s,i,n,t,space,o,c,c,a,e,c,a,t,space,c,u,p,i,d,a,t,a,t,space,n,o,n,space,p,r,o,i,d,e,n,t,comma,space,s,u,n,t,space,i,n,space,c,u,l,p,a,space,q,u,i,space,o,f,f,i,c,i,a,space,d,e,s,e,r,u,n,t,space,m,o,l,l,i,t,space,a,n,i,m,space,i,d,space,e,s,t,space,l,a,b,o,r,u,m,dot,L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot,space,D,u,i,s,space,a,u,t,e,space,i,r,u,r,e,space,d,o,l,o,r,space,i,n,space,r,e,p,r,e,h,e,n,d,e,r,i,t,space,i,n,space,v,o,l,u,p,t,a,t,e,space,v,e,l,i,t,space,e,s,s,e,space,c,i,l,l,u,m,space,d,o,l,o,r,e,space,e,u,space,f,u,g,i,a,t,space,n,u,l,l,a,space,p,a,r,i,a,t,u,r,dot,space,E,x,c,e,p,t,e,u,r,space,s,i,n,t,space,o,c,c,a,e,c,a,t,space,c,u,p,i,d,a,t,a,t,space,n,o,n,space,p,r,o,i,d,e,n,t,comma,space,s,u,n,t,space,i,n,space,c,u,l,p,a,space,q,u,i,space,o,f,f,i,c,i,a,space,d,e,s,e,r,u,n,t,space,m,o,l,l,i,t,space,a,n,i,m,space,i,d,space,e,s,t,space,l,a,b,o,r,u,m,dot")
    }
    
#---------------------------------------------------------------------------
# CSS Core Rule
#---------------------------------------------------------------------------

class CssCoreRule(MappingRule):
    mapping = {
        # general
        "[<n>] <css_length>": T("%(n)s%(css_length)s")
        # selectors
        , "idea [<text>]": T("#%(text)s ")
        , "class [<text>]": T(".%(text)s" )
        # attributes
        , "background": T("background: ;") + K("left")
        , "background <css_color>": T("background: %(color)s;")
        , "background <css_color> <css_image>": T("background: %(css_color)s %(css_image)s;") + K("left:3")
        , "background <css_color> <css_image> <css_repeat>": T("background: %(css_color)s %(css_image)s %(css_repeat)s;") + K("left:3")
        , "background <css_color> <css_image> <css_repeat> <css_attachment>": T("background: %(css_color)s %(css_image)s %(css_repeat)s %(css_attachment)s;") + K("left:3")
        , "background <css_color> <css_image> <css_repeat> <css_attachment> <css_position>": T("background: %(css_color)s %(css_image)s %(css_repeat)s %(css_attachment)s %(css_position)s;") + K("left:3")
        , "background color <css_color>": T("background-color: %(css_color)s;")
        , "background position <css_position>": T("background-position: %(css_position)s;")
        , "background repeat <css_repeat>": T("background-repeat: %(css_repeat)s;")
        , "background attachment <css_attachment>": T("background-attachment: %(css_attachment)s;")
        , "background image <css_image>": T("background-image: %(css_image)s;") + K("left:3")
        , "border [<css_direction_suffix>]": T("border%(css_direction_suffix)s: ;") + K("left")
        , "border [<css_direction_suffix>] <n> <css_length> <css_border> <css_color>": T("border%(css_direction_suffix)s: %(n)s%(css_length)s %(css_border)s %(css_color)s;")
        , "border [<css_direction_suffix>] with <n> <css_length>": T("border%(css_direction_suffix)s: %(n)s%(css_length)s;")
        , "border [<css_direction_suffix>] style <css_border>": T("border%(css_direction_suffix)s-style: %(css_border)s;")
        , "border [<css_direction_suffix>] color <css_color>": T("border%(css_direction_suffix)s-color: %(css_color)s;")
        , "<css_direction> [<n>] <css_length>": T("%(css_direction)s: %(n)s%(css_length)s;")
        , "caption-side <css_caption_position>": T("caption-side: %(css_caption_position)s;")
        , "clear <css_clear>": T("clear: %(css_clear)s;")
        , "clip": T("clip: rect();") + K("left:2")
        , "color": T("color: #;") + K("left")
        , "color <css_color>": T("color: %(css_color)s;")
        , "color RGB": T("color: rgb();") + K("left:2")
        , "color RGB <n> <m> <o>": T("color: rgb(%(n)s,%(m)s,%(o)s;") + K("left")
        , "column count <n>": T("column-count: %(n)s;")
        , "cursor": T("cursor: ;") + K("left")
        , "text direction <css_text_direction>": T("direction: %(css_text_direction)s;")
        , "display <css_display>": T("display: %(css_display)s;")
        , "empty cells <css_cell_visibility>": T("empty-cells: %(css_cell_visibility)s;")
        , "float <css_float>": T("float: %(css_float)s;")
        , "font-family <css_font_family>": "font-family: %(css_font_family)s;"
        , "font size": T("font-size: ;") + K("left")
        , "font size [<n>] <css_length>": T("font-size: %(n)s%(css_length)s;")
        , "font style <css_font_style>": T("font-style: %(css_font_style)s;")
        , "font weight <css_font_weight>": T("font-weight: %(css_font_weight)s;")
        , "font variant <css_font_variant>": T("font-variant: %(css_font_variant)s;")
        , "font": T("font: ;") + K("left")
        , "font <n> <css_length> <css_font_family>": T("font: %(n)s%(css_length)s %(css_font_family)s;")
        , "font <n> <css_length_a> <m> <css_length_b> <css_font_family>": T("font: %(n)s%(css_length_a)s/%(m)s%(css_length_b)s %(css_font_family)s;")
        , "<css_font_family>": T("%(css_font_family)s")
        , "height": T("height: ;") + K("left")
        , "height [<n>] <css_length>": T("height: %(n)s%(css_length)s;")
        , "letter spacing <n> <css_length>": T("letter-spacing: %(n)s%(css_length)s;")
        , "list style image none": T("list-style-image: none;")
        , "list style image <css_image>": T("list-style-image: %(css_image)s;") + K("left:3")
        , "list style position <css_list_position>": T("list-style-position: %(css_list_position)s;")
        , "list style type <css_list_type>": T("lists-style-type: %(css_list_type)s;")
        , "list style <css_list_type> <css_list_position> <css_image>": T("list-style: %(css_list_type)s %(css_list_position)s %(css_image)s;") + K("left:3")
        , "list style <css_list_position> <css_image>": T("list-style: %(css_list_position)s %(css_image)s;") + K("left:3")
        , "list style <css_list_type> <css_list_position>": T("list-style: %(css_list_type)s %(css_list_position)s;")
        , "margin [<css_direction_suffix>]": T("margin%(css_direction_suffix)s: ;") + K("left")
        , "margin [<css_direction_suffix>] [<n>] <css_length>": T("margin%(css_direction_suffix)s: %(n)s%(css_length)s;")
        , "max height": T("max-height: ;") + K("left")
        , "max height [<n>] <css_length>": T("max-height: %(n)s%(css_length)s;")
        , "max with": T("max-width: ;") + K("left")
        , "max with [<n>] <css_length>": T("max-width: %(n)s%(css_length)s;")
        , "min height": T("min-height: ;") + K("left")
        , "min height [<n>] <css_length>": T("min-height: %(n)s%(css_length)s;")
        , "min with": T("min-width: ;") + K("left")
        , "min with [<n>] <css_length>": T("min-width: %(n)s%(css_length)s;")
        # TODO: Integrate the CSS media queries.
        , "opacity <n>": T("opacity: %(n)s;")
        , "opacity <n> point <m>": T("opacity: %(n)s.%(m)s;")
        , "outline": T("outline: ;") + K("left")
        , "outline <css_color> <css_border> <n> <css_length>": T("outline: %(css_color)s %(css_border)s %(n)s%(css_length)s;")
        , "outline with <n> <css_length>": T("outline: %(n)s%(css_length)s;")
        , "outline style <css_border>": T("outline-style: %(css_border)s;")
        , "outline color <css_color>": T("outline-color: %(css_color)s;")
        , "padding [<css_direction_suffix>]": T("padding%(css_direction_suffix)s: ;") + K("left")
        , "padding [<css_direction_suffix>] [<n>] <css_length>": T("padding%(css_direction_suffix)s: %(n)s%(css_length)s;")
        , "page break <css_page_break_position>": T("page-break-%(css_page_break_position)s: ;") + K("left")
        , "page break <css_page_break_position> <css_page_break>": T("page-break-%(css_page_break_position)s: %(css_page_break)s;")
        , "position": T("position: ;") + K("left")
        , "position <css_position>": T("position: %(css_position)s;")
        , "quotes": T("quotes: ;") + K("left")
        , "quotes <css_quote>": T("quotes: %(css_quote)s;")
        , "quotes <css_quote_a> <css_quote_b>": T("quotes: %(css_quote_a)s %(css_quote_b)s;")
        , "table layout": T("table-layout: ;") + K("left")
        , "table layout <css_table_layout>": T("table-layout: %(css_table_layout)s;")
        , "text align": T("text-align: ;") + K("left")
        , "text align <css_text_align>": T("text-align: %(css_text_align)s;")
        , "text decoration": T("text-decoration: ;") + K("left")
        , "text decoration <css_text_decoration>": T("text-decoration: %(css_text_decoration)s;")
        , "text indent": T("text-indent: ;") + K("left")
        , "text indent <n> <css_length>": T("text-indent: %(n)s%(css_length)s;")
        , "text transform": T("text-transform: ;") + K("left")
        , "text transform <css_text_transform>": T("text-transform: %(css_text_transform)s;")
        , "vertical align": T("vertical-align: ;") + K("left")
        , "vertical align <n> <css_length>": T("vertical-align: %(n)s%(css_length)s;")
        , "vertical align <css_vertical_align>": T("vertical-align: %(css_vertical_align)s;")
        , "visibility": T("visibility: ;") + K("left")
        , "visibility <css_visibility>": T("visibility: %(css_visibility)s;")
        , "whitespace": T("white-space: ;") + K("left")
        , "whitespace <css_whitespace>": T("white-space: %(css_whitespace)s;")
        , "width": T("width: ;") + K("left")
        , "width [<n>] <css_length>": T("width: %(n)s%(css_length)s;") 
        , "word spacing": T("word-spacing: ;") + K("left")
        , "word spacing <n> <css_length>": T("word-spacing: %(n)s%(css_length)s;")
        , "word wrap": T("word-wrap: ;") + K("left")
        , "word wrap <css_word_wrap>": T("word-wrap: %(css_word_wrap);")
        , "Z index": T("z-index: ;") + K("left")
        , "Z index [<css_minus>] <n>": T("z-index: %(css_minus)s%(n)s;")
    }
    defaults = {
        "text":"",
        "n":"",
        "m":"",
        "o":"",
        "css_direction_suffix":"",
        "css_color":"transparent",
        "css_image":"default",
        "css_minus":""
    }
    extras = [
        chc_base.text
        , chc_base.any_number_n
        , chc_base.any_number_m
        , chc_base.any_number_o
        , chc_web.css_border
        , chc_web.css_length
        , chc_web.css_length_a
        , chc_web.css_length_b
        , chc_web.css_direction_suffix
        , chc_web.css_direction
        , chc_web.css_color
        , chc_web.css_image
        , chc_web.css_repeat
        , chc_web.css_attachment
        , chc_web.css_position
        , chc_web.css_caption_position
        , chc_web.css_clear
        , chc_web.css_display
        , chc_web.css_text_direction
        , chc_web.css_cell_visibility
        , chc_web.css_float
        , chc_web.css_font_family
        , chc_web.css_font_style
        , chc_web.css_font_weight
        , chc_web.css_font_variant
        , chc_web.css_list_position
        , chc_web.css_list_type
        , chc_web.css_page_break
        , chc_web.css_page_break_position
        , chc_web.css_quote
        , chc_web.css_quote_a
        , chc_web.css_quote_b
        , chc_web.css_table_layout
        , chc_web.css_text_align
        , chc_web.css_text_decoration
        , chc_web.css_text_transform
        , chc_web.css_vertical_align
        , chc_web.css_visibility
        , chc_web.css_whitespace
        , chc_web.css_word_wrap
        , chc_web.css_minus
    ]
