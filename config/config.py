from dataclasses import dataclass

@dataclass
class StatementType:
    name: str
    year_pattern: str
    amount_pattern: str
    date_pattern: str
    entry_type: dict


statement_types = {
    'credit_card': StatementType(
        name='CREDIT_CARD',
        year_pattern=r'(Abrechnungsdatum:\s*\d{2}\.\d{2}\.)(202\d)',
        amount_pattern=r'(\d*\.?\d*\,\d{2})([-+]$)',
        date_pattern=r'^\d{2}\.\d{2}',
        entry_type={'-': 'expense', '+': 'income'}

    ),
    'ec_card': StatementType(
        name='EC_CARD',
        year_pattern=r'(erstellt am\s*\d{2}\.\d{2}\.)(202\d)',
        amount_pattern=r'(\d*\.?\d*\,\d{2})(\s[SH]$)',
        date_pattern=r'^\d{2}\.\d{2}',
        entry_type={'S': 'expense', 'H': 'income'}

    ),
}

# regexes for category auto assignment
categories = {
    'Transportation':  r'(Uber|Free Now|Share Now|Miles|NextBike|Lime|BVG|Swapfiets|DB Vertrieb GMBH)',
    'Rent': r'Miete',
    'Healthcare':  r'Generali',
    'FoodDrink': '$^',
    'BillsFees': r'(versicherung|Lidl Connect)',
    'Travel': '$^',
    'Entertainment': '$^',
    'SportHobbies': r'DownDog',
    'Education': r'(Factory|Medium|Audible)',
    'Shopping': '$^',
    'Groceries': r'(Aldi|Lidl|Denns|E Schnelle|Edeka|Rewe|Penny)',
    'Entertainment': '$^',
    'Travel': '$^',
    'Transfer': '$^',
    'Other': '$^'
}
