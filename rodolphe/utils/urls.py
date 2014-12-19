from urllib.parse import urlencode


def build_url(base, *args, **kwargs):
    if not args and not kwargs:
        return base
    dic = {}
    for arg in args:
        dic.update(arg)
    dic.update(kwargs)
    return '{}?{}'.format(base, urlencode(dic))
