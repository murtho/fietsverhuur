from rich.console import Console
from rich.table import Table
from model.hydrated.hydrated_fiets import HydratedFiets

class HydratedFietsTable:
    COLUMNS = [
        'id',
        'merk',
        'aankoop datum',
        'beschrijving',
        'model',
        'electrisch',
        'dagprijs',
    ]

    def __init__(self, fietsen_list = list[HydratedFiets]):
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
                str(fiets.aankoop_datum),
                fiets.fiets_type.beschrijving,
                fiets.fiets_type.model,
                (fiets.fiets_type.electrisch and 'ja') or 'nee',
                '€' + str(format(fiets.fiets_type.dagprijs, '.2f'))
            )

        console.print(table)