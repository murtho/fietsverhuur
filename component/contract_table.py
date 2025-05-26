from rich.console import Console
from rich.table import Table
from model.contract import Contract

# 0 usages TODO: remove this obsolete table
class ContractTable:
    COLUMNS = [
        'id',
        'start_datum',
        'eind_datum'
    ]

    def __init__(self, contracten_list = list[Contract]):
        self.contracten_list = contracten_list

        if len(self.contracten_list) == 0:
            raise Exception('Contracten list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Contracten')

        for column in self.COLUMNS:
            table.add_column(column)

        for contract in self.contracten_list.__iter__():
            table.add_row(
                str(contract.contract_id),
                str(contract.start_datum),
                str(contract.eind_datum)
            )

        console.print(table)