from typing import Any

from django import template

register = template.Library()


@register.filter
def remove_category_from_url(url: str, value: str) -> str:
    # hacky hack :-D
    url = url.replace(f"{value},", "")
    url = url.replace(f",{value}", "")
    url = url.replace(f"{value}", "")
    return url


@register.filter
def add_category_to_url(url: str, value: str) -> str:
    print(f"{url} {value}")
    return f"{url},{value}"


@register.filter
def amount_color(value: str) -> str:
    fvalue = float(value)
    if fvalue > 0.0:
        return "green"
    if fvalue < 0.0:
        return "red"
    return "gray"


@register.filter
def amount_color_reverse(value: str) -> str:
    fvalue = float(value)
    if fvalue < 0.0:
        return "green"
    if fvalue > 0.0:
        return "red"
    return "gray"


@register.filter
def index(indexable: list[Any], i: int) -> Any:
    return indexable[i]


@register.filter
def clean_string(value: str) -> str:
    return value.replace("_", " ")


@register.filter
def get_month(value: str) -> str:
    return value.split(".")[0]


@register.filter
def get_year(value: str) -> str:
    return value.split(".")[1]
