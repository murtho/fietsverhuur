from component.fiets_type_table import FietsTypeTable
from repository.fiets_repository import FietsRepository
from repository.fiets_type_repository import FietsTypeRepository
from rich.table import Table
from rich.console import Console
from model.fiets import Fiets
import re # regex

# Interactie met de gebruiker voor het invoeren van nieuwe fietsen
class FietsController:

    __fiets_repo : FietsRepository = None
    __fiets_type_repo : FietsTypeRepository = None

    def __init__(self, fiets_repo : FietsRepository, fiets_type_repo : FietsTypeRepository) -> None:
        self.__fiets_repo = fiets_repo
        self.__fiets_type_repo = fiets_type_repo

    # Maak een nieuwe fiets aan
    def nieuwe_fiets(self) -> None:
        print('Voer de gevraagde gegevens in om een nieuwe fiets in te voeren.')

        merk = self.__prompt_for_merk()
        aankoop_datum = self.__prompt_for_aankoop_datum()
        fiets_type_id = self.__prompt_for_fiets_type_id()

        fiets = Fiets({
            'merk': merk,
            'aankoop_datum': aankoop_datum,
            'fiets_type_id': fiets_type_id,
        })

        print('Valideer of je deze fiets definitief wil toevoegen?')
        table = Table(title='Nieuwe fiets')
        table.add_column('Eigenschap')
        table.add_column('Waarde')

        table.add_row('merk', fiets.merk)
        table.add_row('aankoop datum', str(fiets.aankoop_datum))

        fiets_type = self.__fiets_type_repo.get_by_id(int(fiets.fiets_type_id))
        table.add_row('beschrijving', fiets_type.beschrijving)
        table.add_row('model', fiets_type.model)
        table.add_row('electrisch', (fiets_type.electrisch and 'ja') or 'nee')

        console = Console()
        console.print(table)

        proceed = input('Wil je deze fiets toevoegen? (j/n)')

        if proceed == 'j':
            # TODO: test of insert van fiets werkt
            self.__fiets_repo.insert(fiets)

            print('De fiets is toegevoegd.')
        else:
            print('De fiets is niet toegevoegd.')

    def __prompt_for_merk(self) -> str:
        while True:
            merk = input('Wat is het merk?')
            if merk == '':
                print('Merk mag niet leeg zijn')
                return self.__prompt_for_merk()
            elif merk.__len__() > Fiets.MERK_MAX_LENGTH:
                print('Merk mag maximaal {max} tekens bevatten'.format(max = Fiets.MERK_MAX_LENGTH))
                return self.__prompt_for_merk()
            else:
                return merk

    def __prompt_for_aankoop_datum(self) -> str:
        while True:
            aankoop_datum = input('Wat is de aankoop datum? (YYYY-MM-DD)')
            if aankoop_datum == '':
                print('Aankoop datum mag niet leeg zijn')
                return self.__prompt_for_aankoop_datum()
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', aankoop_datum) is None:
                print('Aankoop datum dient een geldige datum te zijn. (YYYY-MM-DD)')
                return self.__prompt_for_aankoop_datum()
            else:
                return aankoop_datum

    def __prompt_for_fiets_type_id(self) -> int:
        fiets_type_table = FietsTypeTable(self.__fiets_type_repo.get_all())
        fiets_type_table.print()

        while True:
            fiets_type_id = input('Welke fiets type wil je toevoegen?')
            if re.match(r'^\d+$', fiets_type_id) is None:
                print('U dient een geldig heel getal in te voeren om het fiets type ID te selecteren.')
                return self.__prompt_for_fiets_type_id()
            if self.__fiets_type_repo.get_by_id(fiets_type_id) == None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van fiets typen.')
                return self.__prompt_for_fiets_type_id()
            else:
                return int(fiets_type_id)