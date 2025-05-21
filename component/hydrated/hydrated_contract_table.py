from rich.console import Console
from rich.table import Table
from model.hydrated.hydrated_contract import HydratedContract

class HydratedContractTable:
    COLUMNS = [
        'id',
        'start_datum',
        'eind_datum',
        'aantal dagen',
        'klant naam',
        'vestiging',
    ]

    def __init__(self, contracten_list = list[HydratedContract]):
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
                str(contract.eind_datum),
                str(contract.aantal_dagen()),
                contract.klant.naam(),
                contract.vestiging.naam
            )

        console.print(table)