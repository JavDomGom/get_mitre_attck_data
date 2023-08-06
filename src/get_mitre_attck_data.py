"""
get_mitre_attck_data
@authors: JavDomGom
"""

import json
import logging
import os

import git
import pandas as pd

from datetime import datetime
from typing import List, NoReturn, Optional

from pyattck import Attck


class GetMitreAttckData:
    """ Class GetMitreAttckData """

    def __init__(self, log: logging.Logger):
        """
        Class constructor
        :param log: The logger
        """

        self.log = log
        self.attack = Attck()
        self.tactics = None
        self.techniques = None
        self.df_tactics = None
        self.df_techniques = None
        self.dt = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_file = f'out/MITRE_ATTCK_DATA_{self.dt}.xlsx'

    @staticmethod
    def format_datetime(datetime_str: str) -> Optional[str]:
        """
        Format datetime %Y-%m-%dT%H:%M:%S.%f%z to date as %Y-%m-%d and return it
        :param datetime_str: Datetime as string to format or None
        """

        if datetime_str is None:
            return datetime_str
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def write_to_json_file(data: list, output_file: str) -> NoReturn:
        """
        Dump data to JSON file
        :param data: List of dictionaries to dump
        :param output_file: File to save data
        """

        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    def write_to_excel_file(self) -> NoReturn:
        """ Write all MITRE ATT&CK data to excel file """

        self.log.info('Write all MITRE ATT&CK data to excel file')

        with pd.ExcelWriter(self.output_file) as file:
            if self.tactics:
                self.df_tactics.to_excel(file, sheet_name='MITRE ATT&CK Tactics', index=False)

            if self.techniques:
                self.df_techniques.to_excel(file, sheet_name='MITRE ATT&CK Techniques', index=False)

    def get_mitre_attck_tactics(self) -> List[dict]:
        """ Get all MITRE ATT&CK tactics """

        self.log.info('Download MITRE ATT&CK tactics from internet')

        tactics = self.attack.enterprise.tactics
        tactics += self.attack.mobile.tactics
        tactics += self.attack.ics.tactics
        tactics_list = []

        if tactics:
            for tactic in tactics:
                tactics_list.append(
                    {
                        'id': tactic.id,
                        'external_id': ', '.join(er.external_id for er in tactic.external_references),
                        'name': tactic.name,
                        'url': ', '.join(er.url for er in tactic.external_references),
                        'type': tactic.type,
                        'created': self.format_datetime(tactic.created),
                        'modified': self.format_datetime(tactic.modified),
                        'description': tactic.description.strip() and tactic.description.splitlines()[0] or tactic.description,
                        'techniques': ', '.join(t.technique_id for t in tactic.techniques),
                        'revoked': tactic.revoked and 'Yes' or 'No',
                        'x_mitre_attack_spec_version': tactic.x_mitre_attack_spec_version,
                        'x_mitre_deprecated': tactic.x_mitre_deprecated and 'Yes' or 'No',
                        'x_mitre_domains': ', '.join(xmd for xmd in tactic.x_mitre_domains),
                        'x_mitre_shortname': tactic.x_mitre_shortname,
                        'x_mitre_version': tactic.x_mitre_version,
                    }
                )

        return tactics_list

    def get_mitre_attck_techniques(self) -> List[dict]:
        """ Get all MITRE ATT&CK techniques """

        self.log.info('Download MITRE ATT&CK techniques from internet')

        techniques = self.attack.enterprise.techniques
        techniques += self.attack.mobile.techniques
        techniques += self.attack.ics.techniques
        techniques_list = []

        if techniques:
            for technique in techniques:
                techniques_list.append(
                    {
                        'id': technique.id,
                        'technique_id': technique.technique_id,
                        'name': technique.name,
                        'url': ', '.join(er.url for er in technique.external_references),
                        'type': technique.type,
                        'created': self.format_datetime(technique.created),
                        'modified': self.format_datetime(technique.modified),
                        'description': technique.description.strip() and technique.description.splitlines()[0] or technique.description,
                        'kill_data_components': ', '.join(dc.name for dc in technique.data_components),
                        'kill_chain_phases': ', '.join(p.phase_name for p in technique.kill_chain_phases),
                        'malwares': ', '.join(mal.name for mal in technique.malwares),
                        'mitigations': ', '.join(mit.name for mit in technique.mitigations),
                        'revoked': technique.revoked and 'Yes' or 'No',
                        'stix': technique.stix,
                        'x_mitre_data_sources': ', '.join(xmds for xmds in technique.x_mitre_data_sources),
                        'x_mitre_defense_bypassed': ', '.join(xmdb for xmdb in technique.x_mitre_defense_bypassed),
                        'x_mitre_deprecated': technique.x_mitre_deprecated and 'Yes' or 'No',
                        'x_mitre_network_requirements': technique.x_mitre_network_requirements and 'Yes' or 'No',
                        'x_mitre_platforms': ', '.join(xmp for xmp in technique.x_mitre_platforms),
                        'x_mitre_version': technique.x_mitre_version,
                    }
                )

        return techniques_list

    def set_mitre_attck_tactics(self, input_file: str = None) -> NoReturn:
        """
        Set value for tactics class attribute
        :param input_file: JSON file with tactics data previously downloaded
        """

        if input_file and os.path.exists(input_file):
            self.log.info('Set MITRE ATT&CK tactics from JSON file')

            with open(input_file, 'r', encoding='utf-8') as json_file:
                self.tactics = json.load(json_file)
        else:
            self.tactics = self.get_mitre_attck_tactics()

        self.df_tactics = pd.DataFrame(self.tactics)

        self.log.debug(f'Tactics found: {len(self.tactics)}')

    def set_mitre_attck_techniques(self, input_file: str = None) -> NoReturn:
        """
        Set value for techniques class attribute
        :param input_file: JSON file with techniques data previously downloaded
        """

        if input_file and os.path.exists(input_file):
            self.log.info('Set MITRE ATT&CK techniques from JSON file')

            with open(input_file, 'r', encoding='utf-8') as json_file:
                self.techniques = json.load(json_file)
        else:
            self.techniques = self.get_mitre_attck_techniques()

        self.df_techniques = pd.DataFrame(self.techniques)

        self.log.debug(f'Techniques found: {len(self.techniques)}')
