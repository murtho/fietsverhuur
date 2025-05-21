from rich.console import Console
from rich.table import Table
from model.hydrated.hydrated_contract_fiets import HydratedContractFiets


class HydratedContractFietsTable:
    COLUMNS = [
        'fietsnr',
        'type',
        'model',
        'electrisch',
        'prijs per dag',
    ]

    def __init__(self, contract_fietsen_list = list[HydratedContractFiets]):
        self.contract_fietsen_list = contract_fietsen_list

        if len(self.contract_fietsen_list) == 0:
            raise Exception('Contract fietsen list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Fietsen')

        for column in self.COLUMNS:
            table.add_column(column)

        for contract_fiets in self.contract_fietsen_list.__iter__():
            table.add_row(
                '{fiets_id} ({fiets_merk})'.format(fiets_id = contract_fiets.fiets.fiets_id, fiets_merk = contract_fiets.fiets.merk),
                '{fiets_type_id} ({beschrijving})'.format(fiets_type_id = contract_fiets.fiets.fiets_type.fiets_type_id, beschrijving = contract_fiets.fiets.fiets_type.beschrijving),
                contract_fiets.fiets.fiets_type.model,
                (contract_fiets.fiets.fiets_type.electrisch and 'ja') or 'nee',
                '€ ' + str(format(contract_fiets.fiets.fiets_type.dagprijs, '.2f'))
            )

        console.print(table)