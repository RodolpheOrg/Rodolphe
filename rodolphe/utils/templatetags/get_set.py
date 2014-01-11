from django import template

register = template.Library()

set_values = {}

class SetNode(template.Node):
    def __init__(self, key, nodes):
        set_values[key] = nodes
    def render(self, context):
        return ''

class GetNode(template.Node):
    def __init__(self, key):
       self.key = key
    def render(self, context):
        return ''.join(v.render(context) for v in set_values[self.key])

@register.tag('set')
def do_set(parser, token):
    _, key = token.split_contents()
    nodelist = parser.parse(('endset',))
    parser.delete_first_token() # Delete 'endset' tag
    return SetNode(key, nodelist)

@register.tag('get')
def do_get(parser, token):
    tag_name, key = token.split_contents()
    return GetNode(key)
