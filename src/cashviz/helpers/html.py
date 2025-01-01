from django.utils.html import format_html
from django.utils.safestring import SafeString


def float_colored_html(amount: float) -> SafeString:
    color = "gray"
    if amount > 0.0:
        color = "green"
    if amount < 0.0:
        color = "red"
    html = f"<span style='color:{color}'>{amount:.2f}</span>"
    return format_html(html)


def tax_formatter(tax: int) -> str:
    if tax == 0:
        return "-"
    return f"{tax}%"
