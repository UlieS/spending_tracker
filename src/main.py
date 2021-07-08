import sys
from argparse import ArgumentParser
from pathlib import Path

from streamlit import cli as stcli

from config.config import statement_types
from database.database_connection import connect_to_db, write_to_db
from parsing.statement_parsing import parse_bank_statements, verify_categories


def run_script(args):

    if args.path:
        transactions = parse_bank_statements(args.path, statement_types[args.type])
        transactions = verify_categories(transactions)

        engine = connect_to_db()
        write_to_db(engine, transactions)

    if args.visualise:
        sys.argv = ["streamlit", "run", "visualisation/visualisations.py"]
        sys.exit(stcli.main())


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--path',
                        type=Path,
                        help='Path to the file')

    parser.add_argument('--visualise',
                        action='store_true',
                        help='Start interactive Streamlit visualisation')

    args = parser.parse_args()
    if args.path:
        parser.add_argument('--type',
                            choices=['credit_card', 'ec_card'],
                            required=True,
                            help='Bank statement type to be parsed')
        args = parser.parse_args()
    run_script(args)
