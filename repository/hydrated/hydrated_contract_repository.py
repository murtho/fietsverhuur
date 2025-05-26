from model.hydrated.hydrated_contract import HydratedContract
from model.contract import Contract
from model.klant import Klant
from model.vestiging import Vestiging
from repository.contract_repository import ContractRepository
from repository.klant_repository import KlantRepository
from repository.vestiging_repository import VestigingRepository
from repository.hydrated.abstract_hydrated_repository import AbstractHydratedRepository
import re # regex

# De repository haalt data op uit meerdere database tabellen
# De data voor Contract, Klant en Vestiging wordt aan elkaar gekoppeld tijdens het hydrateren
class HydratedContractRepository(AbstractHydratedRepository):

    __CONTRACT_ALIAS = 'c'
    __KLANT_ALIAS = 'k'
    __VESTIGING_ALIAS = 'v'

    def __contract_fields(self) -> list[str]:
        fields = Contract.fields()

        for i in range(len(fields)):
            fields[i] = self.__CONTRACT_ALIAS + '.' + fields[i] + ' AS ' + self.__CONTRACT_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __klant_fields(self) -> list[str]:
        fields = Klant.fields()

        for i in range(len(fields)):
            fields[i] = self.__KLANT_ALIAS + '.' + fields[i] + ' AS ' + self.__KLANT_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __vestiging_fields(self) -> list[str]:
        fields = Vestiging.fields()

        for i in range(len(fields)):
            fields[i] = self.__VESTIGING_ALIAS + '.' + fields[i] + ' AS ' + self.__VESTIGING_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __hydrate(self, query_result: dict) -> HydratedContract:
        contract_data = {}
        klant_data = {}
        vestiging_data = {}

        for key, value in query_result.items():

            if key.startswith(self.__CONTRACT_ALIAS + self._DIVIDER):
                contract_data[re.sub(r'^' + self.__CONTRACT_ALIAS + self._DIVIDER, '', key)] = value

            if key.startswith(self.__KLANT_ALIAS + self._DIVIDER):
                klant_data[re.sub(r'^' + self.__KLANT_ALIAS + self._DIVIDER, '', key)] = value

            if key.startswith(self.__VESTIGING_ALIAS + self._DIVIDER):
                vestiging_data[re.sub(r'^' + self.__VESTIGING_ALIAS + self._DIVIDER, '', key)] = value

        contract = HydratedContract(contract_data)
        contract.set_klant(Klant(klant_data))
        contract.set_vestiging(Vestiging(vestiging_data))

        return contract

    def get_all(self) -> list[HydratedContract]:
        contracts_list = []

        fields = self.__contract_fields() + self.__klant_fields() + self.__vestiging_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + ContractRepository.CONTRACT_TABLE + ' AS ' + self.__CONTRACT_ALIAS +
                 (' LEFT JOIN ' + KlantRepository.KLANT_TABLE + ' AS ' + self.__KLANT_ALIAS +
                  ' ON ' + self.__CONTRACT_ALIAS + '.klant_id = ' + self.__KLANT_ALIAS + '.klant_id') +
                 (' LEFT JOIN ' + VestigingRepository.VESTIGING_TABLE + ' AS ' + self.__VESTIGING_ALIAS +
                  ' ON ' + self.__CONTRACT_ALIAS + '.vestiging_id = ' + self.__VESTIGING_ALIAS + '.vestiging_id'))

        for query_result in self._fetch_all(query):
            contracts_list.append(self.__hydrate(query_result))

        return contracts_list

    def get_by_id(self, id: int) -> HydratedContract | None:
        fields = self.__contract_fields() + self.__klant_fields() + self.__vestiging_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + ContractRepository.CONTRACT_TABLE + ' AS ' + self.__CONTRACT_ALIAS +
                 (' LEFT JOIN ' + KlantRepository.KLANT_TABLE + ' AS ' + self.__KLANT_ALIAS +
                  ' ON ' + self.__CONTRACT_ALIAS + '.klant_id = ' + self.__KLANT_ALIAS + '.klant_id') +
                 (' LEFT JOIN ' + VestigingRepository.VESTIGING_TABLE + ' AS ' + self.__VESTIGING_ALIAS +
                  ' ON ' + self.__CONTRACT_ALIAS + '.vestiging_id = ' + self.__VESTIGING_ALIAS + '.vestiging_id'))

        params = {'contract_id': id}

        query_result = self._fetch_one(query, params)
        if query_result is None :
            return None

        return self.__hydrate(query_result)