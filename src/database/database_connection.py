from datetime import date as dtdate, datetime
from typing import List

import pandas as pd
from config.config import StatementType
from database import CONFIG_INI_LOCATION, constants
from database.table_definition import tags_table, transactions_table
from sqlalchemy import create_engine, desc, select
from sqlalchemy.engine import Engine


def connect_to_db(section: str = 'postgresql') -> Engine:
    """" Create sqlalchemy engine to connect to postgres db"""

    params = constants['postgresql']
    url = f'{section}://{params["user"]}:' \
          f'{params["password"]}@{params["host"]}:' \
          f'{params["port"]}/{params["database"]}'
    db_eng = create_engine(url)

    return db_eng


def write_to_db(db: Engine, transactions: List[StatementType]) -> None:
    """ Writes the verified transactions to the database"""

    with db.connect() as conn:
        for transaction in transactions:

            ins = transactions_table.insert().returning(transactions_table.c.t_id).values(
                amount=transaction.amount,
                date=transaction.date,
                notes=transaction.description,
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


def get_latest_transaction_date(db: Engine) -> datetime.date:
    """ Fetches the last transaction date from transactions table"""

    with db.connect() as conn:
        query = select([transactions_table.c.date]).order_by(desc(transactions_table.c.date)).limit(1)
        transactions = conn.execute(query)

    date = transactions.fetchone()
    if date is None:
        # return date from before online banking was a thing
        return dtdate(int(1900), int(1), int(1))

    return date[0]
