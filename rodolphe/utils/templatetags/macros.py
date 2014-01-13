from django import template

register = template.Library()


def get_macros(parser):
    if not hasattr(parser, '_macros'):
        parser._macros = {}
    return parser._macros


class DefineNode(template.Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def render(self, context):
        return ''


@register.tag('define')
def do_define_macro(parser, token):
    _, name = token.split_contents()
    nodelist = parser.parse(('enddefine',))
    parser.delete_first_token()  # Delete 'enddefine' tag
    macro = DefineNode(nodelist)
    get_macros(parser)[name] = macro
    return macro


class GetNode(template.Node):
    def __init__(self, macros, name):
        self.macros = macros
        self.name = name

    def render(self, context):
        try:
            return ''.join(v.render(context) for v in
                           self.macros[self.name].nodes)
        except KeyError:
            return ''


@register.tag('#')
def do_get_macro(parser, token):
    _, name = token.split_contents()
    return GetNode(get_macros(parser), name)
