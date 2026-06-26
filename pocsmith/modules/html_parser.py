from .base import Module


MODULE = Module(
    name="html_parser",
    aliases=("html-parser",),
    imports=("from bs4 import BeautifulSoup",),
    functions=(
        'def parse_html(response):\n    return BeautifulSoup(response.text, "html.parser")\n\n\ndef find_input_value(soup, name):\n    element = soup.find("input", {"name": name})\n    return element.get("value") if element else None\n\n\ndef find_attr(soup, selector, attr):\n    element = soup.select_one(selector)\n    return element.get(attr) if element else None',
    ),
)
