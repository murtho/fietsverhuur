from component.contract_table import ContractTable
from component.hydrated.hydrated_contract_fiets_table import HydratedContractFietsTable
from component.hydrated.hydrated_fiets_table import HydratedFietsTable
from component.klant_table import KlantTable
from component.vestiging_table import VestigingTable
from model.contract import Contract
from model.contract_fiets import ContractFiets
from repository.contract_fiets_repository import ContractFietsRepository
from repository.contract_repository import ContractRepository
from repository.hydrated.hydrated_contract_fiets_repository import HydratedContractFietsRepository
from repository.hydrated.hydrated_contract_repository import HydratedContractRepository
from repository.hydrated.hydrated_fiets_repository import HydratedFietsRepository
from repository.klant_repository import KlantRepository
from repository.vestiging_repository import VestigingRepository
from rich.console import Console
from rich.table import Table
import datetime
import re # regex

# Interactie met de gebruiker voor het tonen en opstellen van contracten
class ContractController:

    __contract_repo : ContractRepository = None
    __contract_fiets_repo : ContractFietsRepository = None
    __hydrated_contract_repo : HydratedContractRepository = None
    __hydrated_fiets_repo : HydratedFietsRepository = None
    __hydrated_contract_fiets_repo : HydratedContractFietsRepository = None
    __klant_repo : KlantRepository = None
    __vestiging_repo : VestigingRepository = None

    def __init__(self, contract_repo : ContractRepository, contract_fiets_repo : ContractFietsRepository, hydrated_contract_repo : HydratedContractRepository, hydrated_contract_fiets_repo : HydratedContractFietsRepository, hydrated_fiets_repo : HydratedFietsRepository, klant_repo : KlantRepository, vestiging_repo : VestigingRepository):
        self.__contract_repo = contract_repo
        self.__contract_fiets_repo = contract_fiets_repo
        self.__hydrated_contract_repo = hydrated_contract_repo
        self.__hydrated_contract_fiets_repo = hydrated_contract_fiets_repo
        self.__hydrated_fiets_repo = hydrated_fiets_repo
        self.__klant_repo = klant_repo
        self.__vestiging_repo = vestiging_repo

    def toon_contract(self, contract_id : int = None) -> None:
        if contract_id is None:
            contracten_list = self.__contract_repo.get_all()
            contract_table = ContractTable(contracten_list)
            contract_table.print()

            print('om een contract te tonen, dient u deze te selecteren?')
            contract_id = self.__prompt_for_contract_id()

        contract = self.__contract_repo.get_by_id(contract_id)
        klant = self.__klant_repo.get_by_id(contract.klant_id)
        vestiging = self.__vestiging_repo.get_by_id(contract.vestiging_id)

        print('contractnummer: {contract_id}'.format(contract_id = contract.contract_id))
        print('datum: {start_datum}'.format(start_datum = contract.start_datum.strftime('%d-%m-%Y')))
        print('')
        print('klant: {achternaam}, {voornaam} (klantnr: {klantnummer})'.format(achternaam = klant.achternaam, voornaam = klant.voornaam, klantnummer = contract.klant_id))
        print('adres: {adres}'.format(adres = klant.adres()))
        print('       {postcode} {plaats}'.format(postcode = klant.postcode, plaats = klant.plaats))
        print('')
        print('vestiging: {naam}'.format(naam = vestiging.naam))
        print('adres: {adres}'.format(adres = vestiging.adres()))
        print('       {postcode} {plaats}'.format(postcode = vestiging.postcode, plaats = vestiging.plaats))
        print('')
        print('startdatum: {start_datum}'.format(start_datum = contract.start_datum.strftime('%d-%m-%Y')))
        print('einddatum:  {eind_datum} -> aantal dagen: {aantal_dagen}'.format(eind_datum = contract.eind_datum.strftime('%d-%m-%Y'), aantal_dagen = contract.aantal_dagen()))
        print('')

        contract_fietsen = self.__hydrated_contract_fiets_repo.get_by_contract_id(contract_id)
        contract_fiets_table = HydratedContractFietsTable(contract_fietsen)
        contract_fiets_table.print()

        totaal_prijs_per_dag : float = float(0)

        for contract_fiets in contract_fietsen:
            totaal_prijs_per_dag = contract_fiets.fiets.fiets_type.dagprijs + totaal_prijs_per_dag

        totaal_prijs = contract.aantal_dagen() * totaal_prijs_per_dag

        totaal_tabel = Table(title = 'Totaal')
        totaal_tabel.add_column('Aantal dagen')
        totaal_tabel.add_column('Prijs per dag')
        totaal_tabel.add_column('Totaalbedrag')

        totaal_tabel.add_row(str(contract.aantal_dagen()), '€ ' + str(format(totaal_prijs_per_dag, '.2f')), '€ ' + str(format(totaal_prijs, '.2f')))

        console = Console()
        console.print(totaal_tabel)

    def nieuw_contract(self) -> None:
        klanten_list = self.__klant_repo.get_all()
        klant_table = KlantTable(klanten_list)
        klant_table.print()

        print('om een nieuw contract te maken, dient u een klant te selecteren.')
        klant_id = self.__prompt_for_klant_id()

        vestigingen_list = self.__vestiging_repo.get_all()
        vestiging_table = VestigingTable(vestigingen_list)
        vestiging_table.print()

        print('om een nieuw contract te maken, dient u een vestiging te selecteren.')
        vestiging_id = self.__prompt_for_vestiging_id()

        print('om een nieuw contract te maken, dient u de startdatum en einddatum in te voeren.')
        start_datum = self.__prompt_for_start_datum()
        eind_datum = self.__prompt_for_eind_datum(start_datum)

        contract = Contract({
            'klant_id': klant_id,
            'vestiging_id': vestiging_id,
            'start_datum': start_datum,
            'eind_datum': eind_datum,
        })

        beschikbare_fietsen_list = self.__hydrated_fiets_repo.get_all_beschikbaar_binnen_datum_bereik(start_datum, eind_datum)

        # Controleer of er überhaupt fietsen beschikbaar zijn om het contract op te stellen
        if len(beschikbare_fietsen_list) == 0:
            print('Er zijn geen fietsen beschikbaar voor het geselecteerde datum bereik.')
            return

        fiets_table = HydratedFietsTable(beschikbare_fietsen_list)
        fiets_table.print()

        print('om een nieuw contract te maken, dient u een of meerdere fietsen te selecteren.')
        geselecteerde_fietsen_list = []

        # Er wordt ten minste 1 fiets geselecteerd tot het maximale aantal fietsen bereikt is.
        while len(geselecteerde_fietsen_list) <= len(beschikbare_fietsen_list):
            geselecteerde_fiets_id = self.__prompt_for_fiets_id(start_datum, eind_datum)
            geselecteerde_fiets = self.__hydrated_fiets_repo.get_beschikbaar_binnen_datum_bereik_by_id(start_datum, eind_datum, geselecteerde_fiets_id)
            geselecteerde_fietsen_list.append(geselecteerde_fiets)
            print('je hebt de {merk} (id: {id}) fiets toegevoegd'.format(merk = geselecteerde_fiets.merk, id = geselecteerde_fiets.fiets_id))

            if (len(geselecteerde_fietsen_list) == len(beschikbare_fietsen_list)):
                print('U hebt alle beschikbare fietsen aan het contract toegevoegd')
                break

            if 'j' == input('Wil je nog een fiets toevoegen? (j/n)'):
                continue
            else:
                break

        nieuw_contract_id = self.__contract_repo.insert(contract)

        for geselecteerde_fiets in geselecteerde_fietsen_list:
            contract_fiets = ContractFiets({
                'contract_id': nieuw_contract_id,
                'fiets_id': geselecteerde_fiets.fiets_id,
            })
            self.__contract_fiets_repo.insert(contract_fiets)

        print('Het nieuwe contract is toegevoegd. U huurt {aantal} fietsen'.format(aantal = len(geselecteerde_fietsen_list)))

        if 'j' == input('Wil je het contract bekijken? (j/n)'):
            self.toon_contract(nieuw_contract_id)


    def __prompt_for_contract_id(self) -> int:
        while True:
            contract_id = input('Welke contract wil je selecteren? (id)')
            if re.match(r'^\d+$', contract_id) is None:
                print('U dient een geldig heel getal in te voeren om het contract te selecteren.')
                return self.__prompt_for_contract_id()
            if self.__contract_repo.get_by_id(int(contract_id)) is None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van contracten.')
                return self.__prompt_for_contract_id()
            else:
                return int(contract_id)

    def __prompt_for_klant_id(self) -> int:
        while True:
            klant_id = input('Welke klant wil je selecteren? (id)')
            if re.match(r'^\d+$', klant_id) is None:
                print('U dient een geldig heel getal in te voeren om de klant te selecteren.')
                return self.__prompt_for_klant_id()
            elif self.__klant_repo.get_by_id(int(klant_id)) is None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van klanten.')
                return self.__prompt_for_klant_id()
            else:
                return int(klant_id)

    def __prompt_for_vestiging_id(self) -> int:
        while True:
            vestiging_id = input('Welke vestiging wil je selecteren? (id)')
            if re.match(r'^\d+$', vestiging_id) is None:
                print('U dient een geldig heel getal in te voeren om de vestiging te selecteren.')
                return self.__prompt_for_vestiging_id()
            elif self.__vestiging_repo.get_by_id(int(vestiging_id)) is None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van vestigingen.')
                return self.__prompt_for_vestiging_id()
            else:
                return int(vestiging_id)

    def __prompt_for_start_datum(self) -> str:
        while True:
            start_datum = input('Wat is de startdatum van het contract? (YYYY-MM-DD)')
            if start_datum == '':
                print('De startdatum mag niet leeg zijn.')
                return self.__prompt_for_start_datum()
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', start_datum) is None:
                print('De startdatum dient een geldige datum te zijn. (YYYY-MM-DD)')
                return self.__prompt_for_start_datum()
            elif start_datum < datetime.datetime.now().strftime('%Y-%m-%d'):
                print('De startdatum dient in de toekomst te liggen.')
            else:
                return start_datum

    def __prompt_for_eind_datum(self, start_datum : str) -> str:
        while True:
            eind_datum = input('Wat is de einddatum van het contract? (YYYY-MM-DD)')
            if eind_datum == '':
                print('De einddatum mag niet leeg zijn.')
                return self.__prompt_for_eind_datum(start_datum)
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', eind_datum) is None:
                print('De einddatum dient een geldige datum te zijn. (YYYY-MM-DD)')
                return self.__prompt_for_eind_datum(start_datum)
            elif eind_datum < start_datum:
                print('De einddatum mag niet voor de startdatum liggen.')
                return self.__prompt_for_eind_datum(start_datum)
            else:
                return eind_datum

    def __prompt_for_fiets_id(self, start_datum : str, eind_datum : str) -> int:
        while True:
            fiets_id = input('Welke fiets wil je selecteren? (id)')
            if re.match(r'^\d+$', fiets_id) is None:
                print('U dient een geldig heel getal in te voeren om de fiets te selecteren.')
                return self.__prompt_for_fiets_id(start_datum, eind_datum)
            elif self.__hydrated_fiets_repo.get_beschikbaar_binnen_datum_bereik_by_id(start_datum, eind_datum, int(fiets_id)) is None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van fietsen.')
                return self.__prompt_for_fiets_id(start_datum, eind_datum)
            else:
                return int(fiets_id)