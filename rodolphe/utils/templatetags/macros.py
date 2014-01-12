from django import template

register = template.Library()

#set_values = {}

class SetNode(template.Node):
    def __init__(self, macros, key, nodes):
        macros[key] = nodes
    def render(self, context):
        return ''

class GetNode(template.Node):
    def __init__(self, macros, key):
        self.macros = macros
        self.key = key
    def render(self, context):
        try:
            return ''.join(v.render(context) for v in self.macros[self.key])
        except KeyError:
            return ''

@register.tag('def')
def do_set_macro(parser, token):
    _, key = token.split_contents()
    nodelist = parser.parse(('enddef',))
    parser.delete_first_token() # Delete 'endset' tag
    if not hasattr(parser, '_set_macros'):
        parser._set_macros = {}
    return SetNode(parser._set_macros, key, nodelist)

@register.tag('macro')
def do_get_macro(parser, token):
    _, key = token.split_contents()
    if not hasattr(parser, '_set_macros'):
        parser._set_macros = {}
    return GetNode(parser._set_macros, key)
