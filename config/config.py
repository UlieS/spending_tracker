from dataclasses import dataclass
import re

@dataclass
class _StatementType:
    name: str
    year_pattern: str
    amount_pattern: str
    date_pattern: str
    entry_type: dict


StatementTypes = {
    'credit_card': _StatementType(
        name='CREDIT_CARD',
        year_pattern=r'(Abrechnungsdatum:\s*\d{2}\.\d{2}\.)(202\d)',
        amount_pattern=r'(\d*\.?\d*\,\d{2})([-+]$)',
        date_pattern=r'^\d{2}\.\d{2}',
        entry_type={'-': 'expense', '+': 'income'}

    ),
    'ec_card': _StatementType(
        name='EC_CARD',
        year_pattern=r'(erstellt am\s*\d{2}\.\d{2}\.)(202\d)',
        amount_pattern=r'(\d*\.?\d*\,\d{2})(\s[SH]$)',
        date_pattern=r'^\d{2}\.\d{2}',
        entry_type={'S': 'expense', 'H': 'income'}

    ),
}


Categories = {
    'Transportation': r'(Uber|FreeNow|ShareNow|Miles|NextBike|Lime)',
    'Rent': r'Miete',
    'Healthcare': r'Generali',
    'FoodDrink': '',
    'BillsFees': '',
    'Travel': '',
    'Entertainment': '',
    'SportHobbies': ''
}