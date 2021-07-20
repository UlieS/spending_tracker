import datetime
from typing import List

import pandas as pd


class Transaction:
    def __init__(self,
                 amount: float,
                 entry_type: str,
                 description: str,
                 date: datetime.date,
                 card: str,
                 currency: str = 'EURO',
                 tags: List[str] = None,
                 category: str = ''):

        self.amount = amount
        self.entry_type = entry_type
        self.description = description
        self.date = date
        self.currency = currency
        self.tags = tags or []
        self.category = category
        self.card = card

    def add_tag(self, tag):
        self.tags.append(tag)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            'amount': self.amount,
            'entry_type': self.entry_type,
            'date': self.date,
            'tags': self.tags,
            'category': self.category,
            'currency': self.currency,
            'card': self.card
        })


