"""
get_mitre_attck_data
@authors: JavDomGom
"""

import argparse
import os

from src import app_logger
from src.get_mitre_attck_data import GetMitreAttckData

log = app_logger.get_logger(__name__)

def get_args() -> tuple:
    """ Function to parse program arguments """

    parser = argparse.ArgumentParser(
        description='This tool has been developed to download tactics and techniques '
                    'from MITRE ATT&CK and generate reports in different formats.'
    )

    parser.add_argument(
        '-u',
        '--updated',
        help="If you want to download updated data from internet every time. Accepted values are 'yes' or 'no'.",
        type=str,
        choices=['yes', 'no']
    )

    arguments = parser.parse_args()

    if not arguments.updated:
        parser.error("-u or --updated flag it's mandatory")

    return arguments, parser

if __name__ == '__main__':
    log.info('Starting program')

    args, _ = get_args()
    gmad = GetMitreAttckData(log=log)

    # Tactics section
    json_tactics = 'out/mitre_tactics.json'

    if args.updated == 'no' and os.path.exists(json_tactics):
        gmad.set_mitre_attck_tactics(input_file=json_tactics)
    else:
        gmad.set_mitre_attck_tactics()
        gmad.write_to_json_file(data=gmad.tactics, output_file=json_tactics)

    # Techniques section
    json_techniques = 'out/mitre_techniques.json'

    if args.updated == 'no' and os.path.exists(json_techniques):
        gmad.set_mitre_attck_techniques(input_file=json_techniques)
    else:
        gmad.set_mitre_attck_techniques()
        gmad.write_to_json_file(data=gmad.techniques, output_file=json_techniques)

    gmad.write_to_excel_file()

    log.info('Finish program')