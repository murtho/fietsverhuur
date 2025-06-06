from component.hydrated.hydrated_contract_table import HydratedContractTable
from component.hydrated.hydrated_fiets_table import HydratedFietsTable
from component.klant_table import KlantTable
from component.vestiging_table import VestigingTable
from repository.hydrated.hydrated_contract_repository import HydratedContractRepository
from repository.hydrated.hydrated_fiets_repository import HydratedFietsRepository
from repository.klant_repository import KlantRepository
from repository.vestiging_repository import VestigingRepository

# Toon overzicht van alle opgeslagen gegevens
class OverzichtController:

    __hydrated_contract_repo : HydratedContractRepository = None
    __hydrated_fiets_repo : HydratedFietsRepository = None
    __klant_repo : KlantRepository = None
    __vestiging_repo : VestigingRepository = None

    def __init__(self, hydrated_contract_repo : HydratedContractRepository, hydrated_fiets_repo : HydratedFietsRepository, klant_repo : KlantRepository, vestiging_repo : VestigingRepository) -> None:
        self.__hydrated_contract_repo = hydrated_contract_repo
        self.__hydrated_fiets_repo = hydrated_fiets_repo
        self.__klant_repo = klant_repo
        self.__vestiging_repo = vestiging_repo

    def totaal_overzicht(self):
        # Toon een lijst met fietsen (gecombineerd met fietstype)
        fietsen_list = self.__hydrated_fiets_repo.get_all()
        fietsen_table = HydratedFietsTable(fietsen_list)
        fietsen_table.print()

        # Toon een lijst met vestigingen
        vestigingen_list = self.__vestiging_repo.get_all()
        vestigingen_table = VestigingTable(vestigingen_list)
        vestigingen_table.print()

        # Toon een lijst met klanten
        klanten_list = self.__klant_repo.get_all()
        klanten_table = KlantTable(klanten_list)
        klanten_table.print()

        # Toon een lijst met contracten (gecombineerd met klant en vestigingsgegevens)
        contracten_list = self.__hydrated_contract_repo.get_all()
        contracten_table = HydratedContractTable(contracten_list)
        contracten_table.print()