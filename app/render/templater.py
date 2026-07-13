from pathlib import Path
from jinja2 import Template


def render_template(template_name: str, **context) -> str:
    template_path = Path("templates") / template_name
    with template_path.open('r', encoding='utf-8') as f:
        jinja2_template_string = f.read()
    
    template = Template(jinja2_template_string)
    return template.render(context)
