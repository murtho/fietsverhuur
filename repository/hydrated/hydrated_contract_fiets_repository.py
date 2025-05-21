from model.hydrated.hydrated_contract_fiets import HydratedContractFiets
from model.hydrated.hydrated_fiets import HydratedFiets
from model.fiets_type import FietsType
from repository.contract_fiets_repository import ContractFietsRepository
from repository.fiets_repository import FietsRepository
from repository.fiets_type_repository import FietsTypeRepository
from repository.hydrated.abstract_hydrated_repository import AbstractHydratedRepository
import re # regex


class HydratedContractFietsRepository(AbstractHydratedRepository):

    __CONTRACT_FIETS_ALIAS = 'contract_fiets'
    __FIETS_ALIAS = 'fiets'
    __FIETS_TYPE_ALIAS = 'fiets_type'

    def __contract_fiets_fields(self) -> list[str]:
        fields = [
            'contract_fiets_id',
            'contract_id',
            'fiets_id',
        ]

        for i in range(len(fields)):
            fields[i] = self.__CONTRACT_FIETS_ALIAS + '.' + fields[i] + ' AS ' + self.__CONTRACT_FIETS_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __fiets_fields(self) -> list[str]:
        fields = [
            'fiets_id',
            'merk',
            'aankoop_datum',
            'fiets_type_id',
        ]

        for i in range(len(fields)):
            fields[i] = self.__FIETS_ALIAS + '.' + fields[i] + ' AS ' + self.__FIETS_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __fiets_type_fields(self) -> list[str]:
        fields = [
            'fiets_type_id',
            'beschrijving',
            'model',
            'dagprijs',
        ]

        for i in range(len(fields)):
            fields[i] = self.__FIETS_TYPE_ALIAS + '.' + fields[i] + ' AS ' + self.__FIETS_TYPE_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __hydrate(self, query_result: dict) -> HydratedContractFiets:
        contract_fiets_data = {}
        fiets_data = {}
        fiets_type_data = {}

        for key, value in query_result.items():

            if key.startswith(self.__CONTRACT_FIETS_ALIAS + self._DIVIDER):
                contract_fiets_data[re.sub(r'^' + self.__CONTRACT_FIETS_ALIAS + self._DIVIDER, '', key)] = value

            if key.startswith(self.__FIETS_ALIAS + self._DIVIDER):
                fiets_data[re.sub(r'^' + self.__FIETS_ALIAS + self._DIVIDER, '', key)] = value

            if key.startswith(self.__FIETS_TYPE_ALIAS + self._DIVIDER):
                fiets_type_data[re.sub(r'^' + self.__FIETS_TYPE_ALIAS + self._DIVIDER, '', key)] = value

        contract_fiets = HydratedContractFiets(contract_fiets_data)
        contract_fiets.set_fiets(HydratedFiets(fiets_data))
        contract_fiets.fiets.set_fiets_type(FietsType(fiets_type_data))

        return contract_fiets

    def get_all(self) -> list[HydratedContractFiets]:
        contract_fietsen_list = []

        fields = self.__contract_fiets_fields() + self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + ' AS ' + self.__CONTRACT_FIETS_ALIAS +
                 (' LEFT JOIN ' + FietsRepository.FIETS_TABLE + ' AS ' + self.__FIETS_ALIAS +
                  ' ON ' + self.__CONTRACT_FIETS_ALIAS + '.fiets_id = ' + self.__FIETS_ALIAS + '.fiets_id') +
                 (' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                  ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'))

        for query_result in self._fetch_all(query):
            contract_fietsen_list.append(self.__hydrate(query_result))

        return contract_fietsen_list

    def get_by_id(self, id: int) -> HydratedContractFiets | None:
        fields = self.__contract_fiets_fields() + self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + ' AS ' + self.__CONTRACT_FIETS_ALIAS +
                 (' LEFT JOIN ' + FietsRepository.FIETS_TABLE + ' AS ' + self.__FIETS_ALIAS +
                  ' ON ' + self.__CONTRACT_FIETS_ALIAS + '.fiets_id = ' + self.__FIETS_ALIAS + '.fiets_id') +
                 (' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                  ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'))

        params = {'contract_fiets_id': id}

        query_result = self._fetch_one(query, params)
        if len(query_result) == 0:
            return None

        return self.__hydrate(query_result)


    def get_by_contract_id(self, contract_id: int) -> list[HydratedContractFiets]:
        contract_fietsen_list = []

        fields = self.__contract_fiets_fields() + self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(
            fields) + ' FROM ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + ' AS ' + self.__CONTRACT_FIETS_ALIAS +
                 (' LEFT JOIN ' + FietsRepository.FIETS_TABLE + ' AS ' + self.__FIETS_ALIAS +
                  ' ON ' + self.__CONTRACT_FIETS_ALIAS + '.fiets_id = ' + self.__FIETS_ALIAS + '.fiets_id') +
                 (' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                  ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id') +
                 ' WHERE contract_id = %s')

        for query_result in self._fetch_all(query, (contract_id,)):
            contract_fietsen_list.append(self.__hydrate(query_result))

        if len(contract_fietsen_list) == 0:
            return []

        return contract_fietsen_list
