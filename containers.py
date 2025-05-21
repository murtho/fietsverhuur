from dependency_injector import containers, providers

from controller.contract_controller import ContractController
from controller.fiets_controller import FietsController
from controller.klant_controller import KlantController
from controller.overzicht_controller import OverzichtController
from config.database_config import DatabaseConfig
from database.connection import Database
from repository.contract_repository import ContractRepository
from repository.contract_fiets_repository import ContractFietsRepository
from repository.fiets_repository import FietsRepository
from repository.fiets_type_repository import FietsTypeRepository
from repository.hydrated.hydrated_contract_fiets_repository import HydratedContractFietsRepository
from repository.hydrated.hydrated_contract_repository import HydratedContractRepository
from repository.hydrated.hydrated_fiets_repository import HydratedFietsRepository
from repository.klant_repository import KlantRepository
from repository.vestiging_repository import VestigingRepository


class Container(containers.DeclarativeContainer):

    config = providers.Factory(DatabaseConfig)
    database = providers.Factory(Database, config=config)

    contract_repo = providers.Factory(ContractRepository, db=database)
    contract_fiets_repo = providers.Factory(ContractFietsRepository, db=database)
    fiets_repo = providers.Factory(FietsRepository, db=database)
    fiets_type_repo = providers.Factory(FietsTypeRepository, db=database)
    klant_repo = providers.Factory(KlantRepository, db=database)
    vestiging_repo = providers.Factory(VestigingRepository, db=database)

    hydrated_contract_repo = providers.Factory(HydratedContractRepository, db=database)
    hydrated_contract_fiets_repo = providers.Factory(HydratedContractFietsRepository, db=database)
    hydrated_fiets_repo = providers.Factory(HydratedFietsRepository, db=database)

    contract_controller = providers.Factory(ContractController,
                                            contract_repo=contract_repo,
                                            contract_fiets_repo=contract_fiets_repo,
                                            hydrated_contract_repo=hydrated_contract_repo,
                                            hydrated_contract_fiets_repo=hydrated_contract_fiets_repo,
                                            hydrated_fiets_repo=hydrated_fiets_repo,
                                            klant_repo=klant_repo,
                                            vestiging_repo=vestiging_repo)

    fiets_controller = providers.Factory(FietsController,
                                         fiets_repo=fiets_repo,
                                         fiets_type_repo=fiets_type_repo)

    klant_controller = providers.Factory(KlantController,
                                         klant_repo=klant_repo)

    overzicht_controller = providers.Factory(OverzichtController,
                                             hydrated_contract_repo=hydrated_contract_repo,
                                             hydrated_fiets_repo=hydrated_fiets_repo,
                                             klant_repo=klant_repo,
                                             vestiging_repo=vestiging_repo)