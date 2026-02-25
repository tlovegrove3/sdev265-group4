from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def filter_query_string(context):
    """
    Build a query string containing only the current filter parameters,
    excluding sort/dir. Used by sort buttons so they can append their
    own sort params without losing active filters.

    Usage:
        {% filter_query_string as filter_qs %}
        <a href="?{{ filter_qs }}&sort=date&dir=asc">Date</a>
    """
    request = context["request"]
    params = request.GET.copy()

    # Remove sort params — we only want filters
    params.pop("sort", None)
    params.pop("dir", None)

    return params.urlencode()
