import pandas as pd
from config.config import StatementTypes, _StatementType, Categories
from transactions.transactions import Transaction
import re
import pdftotext
from datetime import date as dtdate

from typing import List, Union

def parse_bank_statements(path: str, statement_type: str) -> str:
    """"
        path: path to input file
        statement_type: StatementType indicating what type of parsing should be
        done

        returns: TBD
    """
    msg = f'Statement type must be one of {StatementTypes.keys()})'
    assert statement_type in ['credit_card', 'ec_card'], msg

    transactions = _parse_bank_statements(path, StatementTypes[statement_type])
    return transactions



def _parse_bank_statements(path: str, statement_type: _StatementType) -> List[Transaction]:

    amount_pat = re.compile(statement_type.amount_pattern)
    year_pat = re.compile(statement_type.year_pattern)
    date_pat = re.compile(statement_type.date_pattern)

    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
        year = year_pat.search(pdf[0]).group(2)

        transactions = []
        for page in pdf:
            lines = page.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip(' ')
                if re.search('Ausgleich Kreditkartensaldo', line):
                    continue

                matched_date = date_pat.search(line)
                if matched_date:
                    date = matched_date.group(0)
                    matched_amount = amount_pat.search(line)
                    if matched_amount:
                        amount = matched_amount.group(1)
                        entry_type = statement_type.entry_type[matched_amount.group(2)]
                        notes = re.sub(r'\s{1,}', ' ', line).split(' ')[2:-1]

                        idx = line_idx +1
                        while idx < len(lines) and not amount_pat.search(lines[idx]):
                            notes.extend(re.sub(r'\s{1,}', ' ', lines[idx]).split(' '))
                            idx +=1

                        notes = ' '.join(notes)
                        date = dtdate(int(year), int(date.split('.')[1]), int(date.split('.')[0]))
                        replacements = [
                            ('\.', ''),
                            ('\,', '.')
                        ]
                        for old, new in replacements:
                            amount = re.sub(old, new, amount)

                        category = _assign_categories(notes)
                        transactions.append(Transaction(float(amount), entry_type, notes, date, category=category))

        return transactions


def _assign_categories(notes: str) -> Union[str, None]:
    for cat, pattern in Categories.items():
        if pattern == '':
            continue
        pattern = re.compile(pattern, flags=re.IGNORECASE)
        if pattern.search(notes):
            return cat
    return None
