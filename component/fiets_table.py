from rich.console import Console
from rich.table import Table
from model.fiets import Fiets

# 0 usages TODO: remove this obsolete table
class FietsTable:
    COLUMNS = [
        'id',
        'merk',
        'aankoop datum',
    ]

    def __init__(self, fietsen_list = list[Fiets]):
        self.fietsen_list = fietsen_list

        if len(self.fietsen_list) == 0:
            raise Exception('Fietsen list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Fietsen')

        for column in self.COLUMNS:
            table.add_column(column)

        for fiets in self.fietsen_list.__iter__():
            table.add_row(
                str(fiets.fiets_id),
                fiets.merk,
                str(fiets.aankoop_datum)
            )

        console.print(table)