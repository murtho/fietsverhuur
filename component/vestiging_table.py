from rich.console import Console
from rich.table import Table
from model.vestiging import Vestiging

class VestigingTable:
    COLUMNS = [
        'id',
        'naam',
        'adres',
        'postcode',
        'plaats'
    ]

    def __init__(self, vestigingen_list = list[Vestiging]):
        self.vestigingen_list = vestigingen_list

        if len(self.vestigingen_list) == 0:
            raise Exception('Vestigingen list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Vestigingen')

        for column in self.COLUMNS:
            table.add_column(column)

        for vestiging in self.vestigingen_list.__iter__():
            table.add_row(
                str(vestiging.vestiging_id),
                vestiging.naam,
                vestiging.adres(),
                vestiging.postcode,
                vestiging.plaats
            )

        console.print(table)