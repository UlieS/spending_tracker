import sys
from argparse import ArgumentParser
from pathlib import Path
from streamlit import cli as stcli

from config.config import statement_types
from parsing.statement_parsing import parse_bank_statements, verify_categories


def run_script(args):

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

    args = parser.parse_args()
    if bool(args.path) != bool(args.type):
        raise ValueError('Supply both `path` and `type` argument when parsing bank statements.')

    run_script(args)
