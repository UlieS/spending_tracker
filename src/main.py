import sys
from argparse import ArgumentParser
from pathlib import Path
from streamlit import cli as stcli

from config.config import statement_types
from banking.statement_parsing import parse_bank_statements, verify_categories
from database.database_connection import connect_to_db, write_to_db
from banking.verified_accounts import ACCOUNTS
from banking.online_banking import query_bank


def run_script(args):

    if args.pull_data:
        for account in ACCOUNTS.values():
            query_bank(account)

    if args.path:
        transactions = parse_bank_statements(args.path, statement_types[args.type])
        transactions = verify_categories(transactions)

        engine = connect_to_db()
        write_to_db(engine, transactions)

    if args.visualize:
        sys.argv = ["streamlit", "run", "visualization/visualizations.py"]
        sys.exit(stcli.main())


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--visualize',
                        action='store_true',
                        help='Start interactive Streamlit visualization')

    parser.add_argument('--type',
                        choices=['credit_card', 'ec_card'],
                        help='Bank statement type to be parsed')

    parser.add_argument('--path',
                        type=Path,
                        help='Path to the file')

    parser.add_argument('--pull_data',
                        action='store_true',
                        help='Indicate whether to update database from API')

    args = parser.parse_args()
    if bool(args.path) != bool(args.type):
        raise ValueError('Supply both `path` and `type` argument when banking bank statements.')

    run_script(args)
