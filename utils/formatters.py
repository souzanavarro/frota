import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

def moeda(v):
    try:
        return locale.currency(v, grouping=True)
    except Exception:
        return f'R$ {v:.2f}'

def format_date(dt: datetime):
    if not dt:
        return ''
    return dt.strftime('%d/%m/%Y')
