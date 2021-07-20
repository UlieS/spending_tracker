from dataclasses import dataclass

from database import constants


@dataclass
class Account:
    name: str
    account_id: str
    card_type: str


ACCOUNTS = {
    'main': Account(account_id=constants['nordigen']['main'], name='main', card_type='ec_card'),
    'savings': Account(account_id=constants['nordigen']['savings'], name='savings', card_type='ec_card')
}
