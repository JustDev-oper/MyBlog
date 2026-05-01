import bleach
import re

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'hr',
    'img', 'span', 'div', 'sup', 'sub', 'mark'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'span': ['class', 'style'],
    'div': ['class', 'style'],
    'p': ['style'],
    'h1': ['class', 'style'], 'h2': ['class', 'style'], 'h3': ['class', 'style'],
    'h4': ['class', 'style'], 'h5': ['class', 'style'], 'h6': ['class', 'style'],
    'li': ['style'],
    'blockquote': ['style'],
    'code': ['style'],
    'iframe': ['style', 'frameborder', 'src', 'width', 'height', 'allow'],
}

ALLOWED_CSS_PROPERTIES = {
    'color',  # Цвет текста
    'background-color',  # Фон
    'font-size',  # Размер шрифта
    'font-weight',  # Толщина шрифта
    'text-align',  # Выравнивание
    'text-decoration',  # Подчеркивание, зачеркивание
    'margin',  # Отступ снаружи
    'padding',  # Отступ внутри
    'border',  # Граница
    'border-color',  # Цвет границы
    'border-radius',  # Скругленные углы
    'font-style',  # Наклон
    'line-height',  # Высота строки
    'text-indent',  # Отступ первой строки
    'letter-spacing',  # Расстояние между буквами
}

DANGEROUS_CSS_PATTERNS = [
    'expression',  # IE expression
    'javascript:',  # JavaScript URL
    'behavior:',  # IE behavior
    'import',  # @import
    '@',  # At-rules (кроме специальных)
    'vbscript:',  # VBScript URL
]


def sanitize_style(style_string):
    if not style_string:
        return ''

    safe_styles = []

    for declaration in style_string.split(';'):
        if ':' not in declaration:
            continue

        try:
            prop, value = declaration.split(':', 1)
            prop = prop.strip().lower()
            value = value.strip()

            if prop not in ALLOWED_CSS_PROPERTIES:
                continue

            if any(dangerous in value.lower() for dangerous in DANGEROUS_CSS_PATTERNS):
                continue

            if not re.match(r'^[a-zA-Z0-9\s\-#(),%\.]+$', value):
                continue

            safe_styles.append(f'{prop}: {value}')
        except (ValueError, AttributeError):
            continue

    return '; '.join(safe_styles)


def sanitize_html(html_string):
    if not html_string:
        return ''

    cleaned = bleach.clean(
        html_string,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

    def sanitize_style_attribute(match):
        tag_content = match.group(0)
        style_match = re.search(r'style=["\']([^"\']*)["\']', tag_content)

        if style_match:
            original_style = style_match.group(1)
            safe_style = sanitize_style(original_style)

            if safe_style:
                return tag_content.replace(
                    style_match.group(0),
                    f'style="{safe_style}"'
                )
            else:
                return re.sub(r'\s*style=["\'][^"\']*["\']', '', tag_content)

        return tag_content

    cleaned = re.sub(r'<[^>]+style=["\'][^"\']*["\'][^>]*>', sanitize_style_attribute, cleaned)

    return cleaned
