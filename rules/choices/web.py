from dragonfly import (
    Choice
)

#---------------------------------------------------------------------------
# CSS
#---------------------------------------------------------------------------

css_attachments = dict(scroll='scroll'
                      , fixed='fixed'
                      , local='local'
                      , initial='initial'
                      , inherit='inherit'
)
css_attachment = Choice("css_attachment", css_attachments)

css_colors = dict(transparent='transparent'
                 , aqua='aqua'
                 , black='black'
                 , blue='blue'
                 , fuchsia='fuchsia'
                 , gray='gray'
                 , green='green'
                 , lime='lime'
                 , maroon='maroon'
                 , navy='navy'
                 , olive='olive'
                 , orange='orange'
                 , purple='purple'
                 , red='red'
                 , silver='silver'
                 , teal='teal'
                 , white='white'
                 , yellow='yellow'
)
css_color = Choice("css_color", css_colors)

css_lengths = dict(percent='%'
                  , inch='in'
                  , centimeter='cm'
                  , millimeter='mm'
                  , EM='em'
                  , EX='ex'
                  , point='pt'
                  , pica='pc'
                  , pixel='px'
                  , auto='auto'
)
css_length = Choice("css_length", css_lengths)
css_length_a = Choice("css_length_a", css_lengths)
css_length_b = Choice("css_length_b", css_lengths)

css_borders = dict(none='none'
              , hidden='hidden'
              , dotted='dotted'
              , dashed='dashed'
              , solid='solid'
              , double='double'
              , groove='groove'
              , ridge='ridge'
              , inset='inset'
              , outset='outset'
              , initial='initial'
              , inherit='inherit'
)
css_border = Choice("css_border", css_borders)

css_images = dict(url="url('')"
                 , default="url('../img/')"
)
css_image = Choice("css_image", css_images)

css_repeats = dict(no='no-repeat'
                  , ex='repeat-x'
                  , why='repeat-y'
                  , both='both'
                  , initial='initial'
                  , inherit='inherit'
)
css_repeat = Choice("css_repeat", css_repeats)

css_clears = dict(none='none'
                 , left='left'
                 , right='right'
                 , both='both'
                 , initial='initial'
                 , inherit='inherit'
)
css_clear = Choice("css_clear", css_clears)

css_caption_positions = dict(top='top'
                    , bottom='bottom'
                    , initial='initial'
                    , inherit='inherit'
)
css_caption_position = Choice("css_caption_position", css_caption_positions)

css_directions = dict(left='left'
                     , right='right'
                     , top='top'
                     , bottom='bottom'
)
css_direction = Choice("css_direction", css_directions)

css_direction_suffixes = dict(left='-left'
                            , right='-right'
                            , top='-top'
                            , bottom='-bottom'
)
css_direction_suffix = Choice("css_direction_suffix", css_direction_suffixes)

css_text_directions = {
    "left-to-right": "ltr"
    , "right-to-left": "rtl"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_text_direction = Choice("css_text_direction", css_text_directions)

css_displays = {
    "none": "none"
    , "block": "block"
    , "in line": "inline"
    , "flex": "flex"
    , "in-line block": "inline-block"
    , "in line flex": "inline-flex"
    , "in-line table": "inline-table"
    , "list item": "list-item"
    , "run in": "run-in"
    , "table": "table"
    , "[table] caption": "table-caption"
    , "[table] column group": "table-column-group"
    , "[table] header group": "table-header-group"
    , "[table] footer group": "table-footer-group"
    , "[table] row group": "table-row-group"
    , "[table] cell": "table-cell"
    , "[table] column": "table-column"
    , "[table] row": "table-row"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_display = Choice("css_display", css_displays)

css_cell_visibilities = {
    "show": "show"
    , "hide": "hide"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_cell_visibility = Choice("css_cell_visibility", css_cell_visibilities)

css_floats = {
    "none": "none"
    , "left": "left"
    , "right": "right"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_float = Choice("css_float", css_floats)

css_font_families = {
    "Georgia": "Georgia, serif"
    , "Palatino": '"Palatino Linotype", "Book Antiqua", Palatino, serif'
    , "times": '"Times New Roman", Times, serif'
    , "Arial": 'Arial, Helvetica, sans-serif'
    , "Arial black": 'Arial, Helvetica, sans-serif'
    , "comic": '"Comic Sans MS", cursive, sans-serif'
    , "impact": 'Impact, Charcoal, sans-serif'
    , "Lucida": '"Lucida Sans Unicode", "Lucida Grande", sans-serif'
    , "Tahoma": 'Tahoma, Geneva, sans-serif'
    , "Helvetica": '"Trebuchet MS", Helvetica, sans-serif'
    , "Verdana": 'Verdana, Geneva, sans-serif'
    , "Courier": '"Courier New", Courier, monospace'
    , "console": '"Console", "Lucida Console", Monaco, monospace'
    , "serif": "serif"
    , "sans serif": "sans-serif"
    , "monospace": "monospace"
}
css_font_family = Choice("css_font_family", css_font_families)

css_font_styles = {
    "normal": "normal"
    , "italic": "italic"
    , "oblique": "oblique"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_font_style = Choice("css_font_style", css_font_styles)

css_font_weights = {
    "normal": "normal"
    , "bold": "bold"
    , "bolder": "bolder"
    , "lighter": "lighter"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_font_weight = Choice("css_font_weight", css_font_weights)

css_font_variants = {
    "normal": "normal"
    , "small caps": "small-caps"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_font_variant = Choice("css_font_variant", css_font_variants)

css_list_positions = {
    "inside": "inside"
    , "outside": "outside"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_list_position = Choice("css_list_position", css_list_positions)

css_list_types = {
    "none": "none"
    , "disk": "disc"
    , "circle": "circle"
    , "square": "square"
    , "decimal": "decimal"
    , "decimal leading zero": "decimal-leading-zero"
    , "lower alpha": "lower-alpha"
    , "lower Greek": "lower-greek"
    , "lower Latin": "lower-latin"
    , "upper alpha": "upper-alpha"
    , "upper Greek": "upper-greek"
    , "upper Latin": "upper-latin"
    , "initial": "initial"
    , "inherit": "inherit"
}
css_list_type = Choice("css_list_type", css_list_types)

css_media_types = {
    "all":"all"
    , "aural":"aural"
    , "braille":"braille"
    , "embossed":"embossed"
    , "handheld":"handheld"
    , "print":"print"
    , "projection":"projection"
    , "screen":"screen"
    , "TTY":"tty"
    , "TV":"tv"
}
css_media_type = Choice("css_media_type", css_media_types)

css_media_features = {
    "aspect ratio":"aspect-ratio"
    , "color":"color"
    , "color index":"color-index"
    , "device aspect ratio":"device-aspect-ratio"
    , "device height":"device-height"
    , "device with":"device-width"
    , "grid":"grid"
    , "height":"height"
    , "max aspect ratio":"max-aspect-ratio"
    , "max color":"max-color"
    , "max color index":"max-color-index"
    , "max device aspect ratio":"max-device-aspect-ratio"
    , "max device height":"max-device-height"
    , "max device width":"max-device-width"
    , "max height":"max-height"
    , "max monochrome":"max-monochrome"
    , "max resolution":"max-resolution"
    , "max width":"max-width"
    , "min aspect ratio":"min-aspect-ratio"
    , "min color":"min-color"
    , "min color index":"min-color-index"
    , "min device aspect ratio":"min-device-aspect-ratio"
    , "min device height":"min-device-height"
    , "min device width":"min-device-width"
    , "min height":"min-height"
    , "min monochrome":"min-monochrome"
    , "min resolution":"min-resolution"
    , "min width":"min-width"
    , "monochrome":"monochrome"
    , "orientation":"orientation"
    , "resolution":"resolution"
    , "scan":"scan"
    , "width":"width"
}
css_media_feature = Choice("css_media_feature", css_media_features)

css_page_break_positions = {
    "after":"after"
    , "before":"before"
    , "inside":"inside"
}
css_page_break_position = Choice("css_page_break_position", css_page_break_positions)

css_page_breaks = {
    "auto":"auto"
    , "always":"always"
    , "avoid":"award"
    , "left":"left"
    , "right":"right"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_page_break = Choice("css_page_break", css_page_breaks)

css_positions = {
    "static":"static"
    , "absolute":"absolute"
    , "fixed":"fixed"
    , "relative":"relative"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_position = Choice("css_position", css_positions)

css_quotes = {
    "double [quote]":'"\0022" "\0022"'
    , "single [quote]":'"\0027" "\0027"'
    , "single angle [quote]":'"\2039" "\203A"'
    , "double angle [quote]":'"\00AB" "\00BB"'
    , "single high [quote]":'"\2018" "\2019"'
    , "double high [quote]":'"\201C" "\201D"'
    , "double low high [quote]":'"\201E" "\201D"'
}
css_quote = Choice("css_quote", css_quotes)
css_quote_a = Choice("css_quote_a", css_quotes)
css_quote_b = Choice("css_quote_b", css_quotes)

css_table_layouts = {
    "auto":"auto"
    , "fixed":"fixed"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_table_layout = Choice("css_table_layout", css_table_layouts)

css_text_aligns = {
    "left":"left"
    , "right":"right"
    , "center":"center"
    , "justify":"justified"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_text_align = Choice("css_text_align", css_text_aligns)

css_text_decorations = {
    "none":"none"
    , "underline":"underline"
    , "overline":"overline"
    , "line-through":"line-through"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_text_decoration = Choice("css_text_decoration", css_text_decorations)

css_text_transforms = {
    "none":"none"
    , "capitalize":"capitalize"
    , "uppercase":"uppercase"
    , "lowercase":"lowercase"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_text_transform = Choice("css_text_transform", css_text_transforms)

css_vertical_aligns = {
    "baseline":"baseline"
    , "sub":"sub"
    , "super":"super"
    , "top":"top"
    , "text-top":"text-top"
    , "middle":"middle"
    , "bottom":"bottom"
    , "text-bottom":"text-bottom"
    , "initial":"initial"
    , "inherit":"inherit"    
}
css_vertical_align = Choice("css_vertical_align", css_vertical_aligns)

css_visibilities = {
    "visible":"visible"
    , "hidden":"hidden"
    , "collapse":"collapse"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_visibility = Choice("css_visibility", css_visibilities)

css_whitespaces = {
    "normal":"normal"
    , "nowrap":"nowrap"
    , "pre":"pre"
    , "pre-line":"pre-line"
    , "pre-wrap":"pre-wrap"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_whitespace = Choice("css_whitespace", css_whitespaces)

css_word_wraps = {
    "normal":"normal"
    , "break-word":"break-word"
    , "initial":"initial"
    , "inherit":"inherit"
}
css_word_wrap = Choice("css_word_wrap", css_word_wraps)

css_minuses = {
    "minus":"-"
}
css_minus = Choice("css_minus", css_minuses)

#---------------------------------------------------------------------------
# HTML
#---------------------------------------------------------------------------

html_elements = {
    "(anchor | link | hyperlink)": "a"
    , "abbreviation": "abbr"
    , "address": "address"
    , "area": "area"
    , "article": "article"
    , "aside": "aside"
    , "audio": "audio"
    , "bold": "b"
    , "base": "base"
    , "bi-directional isolation": "bdi"
    , "bi-directional override": "bdo"
    , "(blockquote|block quote)": "blockquote"
    , "body": "body"
    , "break": "br"
    , "button": "button"
    , "canvas": "canvas"
    , "caption": "caption"
    , "(cite|citation)": "cite"
    , "code": "code"
    , "(col|C O L|[table] column)": "col"
    , "(colgroup|C O L group|[table] column group)": "colgroup"
    , "content": "content"
    , "data": "data"
    , "(datalist|data list)": "datalist"
    , "(dd|D D|description)": "dd"
    , "decorator": "decorator"
    , "(del|D E L|deleted text)": "del"
    , "details": "details"
    , "(D F N|definition)": "dfn"
    , "(div|D I V|[document] division)": "div"
    , "(D L|description list)": "dl"
    , "(D T|definition term)": "dt"
    , "element": "element"
    , "(em|E M|emphasis)": "em"
    , "embed": "embed"
    , "fieldset": "fieldset"
    , "(figcaption|fig caption|figure caption)": "figcaption"
    , "figure": "figure"
    , "footer": "footer"
    , "form": "form"
    , "(H 1|heading 1)": "h1"
    , "(H 2|heading 2)": "h2"
    , "(H 3|heading 3)": "h3"
    , "(H 4|heading 4)": "h4"
    , "(H 5|heading 5)": "h5"
    , "(H 6|heading 6)": "h6"
    , "head": "head"
    , "header": "header"
    , "(H R|horizontal rule)": "hr"
    , "html": "html"
    , "(I|italic)": "i"
    , "(I|inline) frame": "iframe"
    , "(I M G|image)": "img"
    , "input": "input"
    , "(I N S|inserted [text])": "ins"
    , "(K B D|keyboard [input])": "kbd"
    , "(keygen|key gen|key generation)": "keygen"
    , "label": "label"
    , "legend": "legend"
    , "(li|L I|list [item])": "li"
    , "link": "link"
    , "main": "main"
    , "map": "map"
    , "mark": "mark"
    , "menu": "menu"
    , "(menuitem|menu item)": "menuitem"
    , "(meta|meta data)": "meta"
    , "meter": "meter"
    , "(nav|N A V|navigation)": "nav"
    , "(noscript|no script)": "noscript"
    , "object": "object"
    , "(O L|ordered list)": "ol"
    , "(optgroup|opt group|(option|options) group)": "optgroup"
    , "option": "option"
    , "output": "output"
    , "(P|paragraph)": "p"
    , "(param|parameter)": "param"
    , "(pre|P R E|pre-formatted [text])": "pre"
    , "progress": "progress"
    , "(Q|quote)": "q"
    , "R P": "rp"
    , "R T": "rt"
    , "ruby": "ruby"
    , "(S|strike through|strikethrough)": "s"
    , "(samp|sample)": "samp"
    , "script": "script"
    , "section": "section"
    , "select": "select"
    , "shadow": "shadow"
    , "small": "small"
    , "source": "source"
    , "span": "span"
    , "strong": "strong"
    , "style": "style"
    , "(sub|S U B|sub-script)": "sub"
    , "summary": "summary"
    , "(sup|S U P|super [script])": "sup"
    , "table": "table"
    , "(T|table) body": "tbody"
    , "(T D|table cell|table data)": "td"
    , "template": "template"
    , "(textarea|text area)": "textarea"
    , "(T|table) foot": "tfoot"
    , "(T H|table header) ": "th"
    , "(T|table) head": "thead"
    , "time": "time"
    , "title": "title"
    , "(T R|table row)": "tr"
    , "track": "track"
    , "(U|uderline)": "u"
    , "(U L|an ordered list)": "ul"
    , "(var|V A R|variable)": "var"
    , "video": "video"
    , "(W B R|word break [opportunity])": "wbr"
}
html_element = Choice("html_element", html_elements)

html_void_elements = [
    'area'
    , 'base'
    , 'br'
    , 'col'
    , 'command'
    , 'embed'
    , 'hr'
    , 'img'
    , 'input'
    , 'keygen'
    , 'link'
    , 'meta'
    , 'param'
    , 'source'
    , 'track'
    , 'wbr'
]

html_attributes = {
    "accept": "accept"
    , "accept-charset": "accept-charset"
    , "accesskey": "accesskey"
    , "action": "action"
    , "align": "align"
    , "(alt|A L T|alternative)": "alt"
    , "(async|asynchronous)": "async"
    , "autocomplete": "autocomplete"
    , "autofocus": "autofocus"
    , "autoplay": "autoplay"
    , "buffered": "buffered"
    , "challenge": "challenge"
    , "charset": "charset"
    , "checked": "checked"
    , "cite": "cite"
    , "class": "class"
    , "code": "code"
    , "codebase": "codebase"
    , "(cols|columns)": "cols"
    , "(colspan|column span)": "colspan"
    , "content": "content"
    , "contenteditable": "contenteditable"
    , "contextmenu": "contextmenu"
    , "controls": "controls"
    , "coords": "coords"
    , "data": "data"
    , "datetime": "datetime"
    , "default": "default"
    , "defer": "defer"
    , "(dir|direction)": "dir"
    , "dirname": "dirname"
    , "disabled": "disabled"
    , "download": "download"
    , "draggable": "draggable"
    , "dropzone": "dropzone"
    , "(enctype|encoding type)": "enctype"
    , "for": "for"
    , "form": "form"
    , "headers": "headers"
    , "height": "height"
    , "hidden": "hidden"
    , "high": "high"
    , "(href|H ref)": "href"
    , "(hreflang|H ref lang)": "hreflang"
    , "http-equiv": "http-equiv"
    , "icon": "icon"
    , "(id|I D)": "id"
    , "ismap": "ismap"
    , "itemprop": "itemprop"
    , "keytype": "keytype"
    , "kind": "kind"
    , "label": "label"
    , "lang": "lang"
    , "language": "language"
    , "list": "list"
    , "loop": "loop"
    , "low": "low"
    , "manifest": "manifest"
    , "max": "max"
    , "maxlength": "maxlength"
    , "media": "media"
    , "method": "method"
    , "min": "min"
    , "multiple": "multiple"
    , "name": "name"
    , "(novalidate|no validate)": "novalidate"
    , "open": "open"
    , "optimum": "optimum"
    , "pattern": "pattern"
    , "ping": "ping"
    , "placeholder": "placeholder"
    , "poster": "poster"
    , "preload": "preload"
    , "pubdate": "pubdate"
    , "radiogroup": "radiogroup"
    , "readonly": "readonly"
    , "(rel|R E L|relationship)": "rel"
    , "required": "required"
    , "reversed": "reversed"
    , "rows": "rows"
    , "rowspan": "rowspan"
    , "sandbox": "sandbox"
    , "spellcheck": "spellcheck"
    , "scope": "scope"
    , "scoped": "scoped"
    , "seamless": "seamless"
    , "selected": "selected"
    , "shape": "shape"
    , "size": "size"
    , "sizes": "sizes"
    , "span": "span"
    , "(src|S R C|source)": "src"
    , "(S R C |source) doc": "srcdoc"
    , "(S R C |source) lang": "srclang"
    , "start": "start"
    , "step": "step"
    , "style": "style"
    , "summary": "summary"
    , "tabindex": "tabindex"
    , "target": "target"
    , "title": "title"
    , "type": "type"
    , "usemap": "usemap"
    , "value": "value"
    , "width": "width"
    , "wrap": "wrap"
}
html_attribute = Choice("html_attribute", html_attributes)

html_language_codes = {
    "Chinese": "zh"
    , "Chinese Simplified": "zh-Hans"
    , "Chinese Traditional": "zh-Hant"
    , "Czech": "cs"
    , "Danish": "da"
    , "Dutch": "nl"
    , "English": "en"
    , "Esperanto": "eo"
    , "Estonian": "et"
    , "Finnish": "fi"
    , "French": "fr"
    , "German": "de"
    , "Greek": "el"
    , "Hindi": "hi"
    , "Hungarian": "hu"
    , "Interlingua": "ia"
    , "Interlingue": "ie"
    , "Irish": "ga"
    , "Italian": "it"
    , "Japanese": "ja"
    , "Laothian": "lo"
    , "Latin": "la"
    , "Macedonian": "mk"
    , "Norwegian": "no"
    , "Polish": "pl"
    , "Portuguese": "pt"
    , "Romanian": "ro"
    , "Russian": "ru"
    , "Serbian": "sr"
    , "Serbo Croatian": "sh"
    , "Slovak": "sk"
    , "Slovenian": "sl"
    , "Swedish": "sv"
    , "Thai": "th"
    , "Turkish": "tr"
    , "Ukrainian": "uk"
    , "Vietnamese": "vi"
    , "Zulu": "zu"
}
html_language_code = Choice("html_language_code", html_language_codes)

html_relationships = {
    "alternate": "alternate"
    , "author": "author"
    , "bookmark": "bookmark"
    , "help": "help"
    , "license": "license"
    , "next": "next"
    , "nofollow": "nofollow"
    , "noreferrer": "noreferrer"
    , "prefetch": "prefetch"
    , "prev": "prev"
    , "search": "search"
    , "tag": "tag"
}
html_relationship = Choice("html_relationship", html_relationships)

html_targets = {
    "blank": "_blank"
    , "parent": "_parent"
    , "self": "_self"
    , "top": "_top"
}
html_target = Choice("html_target", html_targets)
