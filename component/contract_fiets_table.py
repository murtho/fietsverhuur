from rich.console import Console
from rich.table import Table
from model.contract_fiets import ContractFiets

# 0 usages TODO: remove this obsolete table
class ContractFietsTable:
    COLUMNS = [
        'contract_id',
        'fiets_id',
    ]

    def __init__(self, contract_fietsen_list = list[ContractFiets]):
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
                str(contract_fiets.contract_id),
                str(contract_fiets.fiets_id)
            )

        console.print(table)