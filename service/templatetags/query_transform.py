from django import template

register = template.Library()

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)
    return updated.urlencode()

@register.simple_tag
def update_query(request, **kwargs):
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    query.pop('page', None)
    return query.urlencode()


