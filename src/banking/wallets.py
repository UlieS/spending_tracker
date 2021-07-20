from dataclasses import dataclass
from typing import List


@dataclass
class Wallet:
    name: str
    iban: str
    current_amount: float
    transaction_history: List[int]
