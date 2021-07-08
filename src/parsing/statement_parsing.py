import re
from datetime import date as dtdate
from typing import List, Union

import pdftotext

from config.config import categories, StatementType
from transactions.transactions import Transaction


def parse_bank_statements(path: str, statement_type: StatementType) -> List[Transaction]:
    """ parse defined bank statements and extract line items """

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
                        entry_type = statement_type.entry_type[matched_amount.group(2).strip(' ')]
                        notes = re.sub(r'\s+', ' ', line).split(' ')[2:-1]

                        idx = line_idx + 1
                        while idx < len(lines) and not amount_pat.search(lines[idx]):
                            notes.extend(re.sub(r'\s+', ' ', lines[idx]).split(' '))
                            idx += 1

                        notes = ' '.join(notes)
                        date = dtdate(int(year), int(date.split('.')[1]), int(date.split('.')[0]))
                        replacements = [
                            ('\.', ''),
                            ('\,', '.')
                        ]
                        for old, new in replacements:
                            amount = re.sub(old, new, amount)

                        category = _assign_category(notes)
                        transactions.append(Transaction(
                            amount=float(amount),
                            entry_type=entry_type,
                            notes=notes,
                            date=date,
                            card=statement_type.name,
                            category=category)
                        )

        return transactions


def _assign_category(notes: str) -> Union[str, None]:
    """ Auto assign category based on pattern matching """

    for category, pattern in categories.items():
        pattern = re.compile(pattern, flags=re.IGNORECASE)
        if pattern.search(notes):
            return category
    return ''


def verify_categories(transactions: List[Transaction]) -> List[Transaction]:
    """ Prompt user input to identify category and tag"""

    cat_mapping = {str(idx): cat[0] for idx, cat in enumerate(categories.items())}
    category_choice = '\n'.join([f'{cat}: {str(idx)}' for idx, cat in cat_mapping.items()])

    for transaction in transactions:
        if not transaction.category:
            category_num = input(
                f'Enter category for the following transaction: \n'
                f'----------------------------------------------- \n'
                f'{transaction.entry_type}, {transaction.date}, {transaction.amount} {transaction.currency} \n'
                f'{transaction.notes}, \n'
                f'----------------------------------------------- \n'
                f'Choose one of the following:\n'
                f'{category_choice}\n'
                f'Type S if you want to skip to the end \n')

            if category_num.lower() == 's':
                break
            category = 'Other' if category_num not in cat_mapping else cat_mapping[category_num]
            transaction.category = category

        else:
            print(f'{transaction.entry_type}, {transaction.date}, {transaction.amount} {transaction.currency} \n'
                  f'{transaction.notes}, \n')

        # potentially add tags
        tag = input('Do you want to add tags? \n Type (space separated) tags \n')
        if tag != '':

            for t in tag.split(' '):
                transaction.add_tag(t)

    return transactions
