from configparser import ConfigParser
from typing import List

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine

from config.config import StatementType
from database.table_definition import tags_table, transactions_table

DB_INI_LOCATION = '/Users/ulieschnaithmann/repos/budgeting/src/config/database.ini'


def connect_to_db(section: str = 'postgresql') -> Engine:
    """" Create sqlalchemy engine to connect to postgres db"""

    parser = ConfigParser()
    parser.read(DB_INI_LOCATION)
    if parser.has_section(section):
        params = parser.items(section)
        params = {key: val for key, val in params}
        url = f'{section}://{params["user"]}:' \
              f'{params["password"]}@{params["host"]}:' \
              f'{params["port"]}/{params["database"]}'
        db_eng = create_engine(url)

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, DB_INI_LOCATION))

    return db_eng


def write_to_db(db: Engine, transactions: List[StatementType]) -> None:
    """ Writes the verified transactions to the database"""

    with db.connect() as conn:
        for transaction in transactions:

            ins = transactions_table.insert().returning(transactions_table.c.t_id).values(
                    amount=transaction.amount,
                    date=transaction.date,
                    notes=transaction.notes,
                    category=transaction.category,
                    type=transaction.entry_type,
                    card=transaction.card
            )
            res = conn.execute(ins)
            t_id = res.fetchone()[0]
            for tag in transaction.tags:
                ins = tags_table.insert().values(
                        transaction_id=t_id,
                        tag=tag
                    )

                conn.execute(ins)


def read_from_db(db: Engine) -> pd.DataFrame:
    """ Execute query to read transactions and tags from db"""

    with db.connect() as conn:
        query = select([transactions_table])
        transactions = conn.execute(query)
        transactions = pd.DataFrame(transactions.fetchall(), columns=transactions.keys())

        query = select([tags_table])
        tags = conn.execute(query)
        tags = pd.DataFrame(tags.fetchall(), columns=tags.keys())

    return tags, transactions
