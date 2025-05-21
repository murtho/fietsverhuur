from rich.console import Console
from rich.table import Table
from model.klant import Klant

class KlantTable:
    COLUMNS = [
        'id',
        'voornaam',
        'achternaam',
        'adres',
        'postcode',
        'plaats'
    ]

    def __init__(self, klanten_list = list[Klant]):
        self.klanten_list = klanten_list

        if len(self.klanten_list) == 0:
            raise Exception('Klanten list is leeg')

    def print(self) -> None:
        console = Console()

        table = Table(title='Klanten')

        for column in self.COLUMNS:
            table.add_column(column)

        for klant in self.klanten_list.__iter__():
            table.add_row(
                str(klant.klant_id),
                klant.voornaam,
                klant.achternaam,
                klant.adres(),
                klant.postcode,
                klant.plaats
            )

        console.print(table)
