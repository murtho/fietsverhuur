from rich.console import Console
from rich.table import Table
from model.fiets_type import FietsType

class FietsTypeTable:
    COLUMNS = [
        'id',
        'beschrijving',
        'model',
        'electrisch',
        'dagprijs',
    ]

    def __init__(self, fiets_typen_list = list[FietsType]):
        self.fiets_typen_list = fiets_typen_list

        if len(self.fiets_typen_list) == 0:
            raise Exception('Fiets typen list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Fietstypen')

        for column in self.COLUMNS:
            table.add_column(column)

        for fiets_type in self.fiets_typen_list.__iter__():
            table.add_row(
                str(fiets_type.fiets_type_id),
                fiets_type.beschrijving,
                fiets_type.model,
                (fiets_type.electrisch and 'ja') or 'nee',
                '€' + str(format(fiets_type.dagprijs, '.2f'))
            )

        console.print(table)