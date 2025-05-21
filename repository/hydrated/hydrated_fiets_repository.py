from model.hydrated.hydrated_fiets import HydratedFiets
from model.fiets_type import FietsType
from repository.contract_fiets_repository import ContractFietsRepository
from repository.contract_repository import ContractRepository
from repository.fiets_repository import FietsRepository
from repository.fiets_type_repository import FietsTypeRepository
from repository.hydrated.abstract_hydrated_repository import AbstractHydratedRepository
import re # regex


class HydratedFietsRepository(AbstractHydratedRepository):

    __FIETS_ALIAS = 'fiets'
    __FIETS_TYPE_ALIAS = 'fiets_type'

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
            'electrisch',
            'dagprijs',
        ]

        for i in range(len(fields)):
            fields[i] = self.__FIETS_TYPE_ALIAS + '.' + fields[i] + ' AS ' + self.__FIETS_TYPE_ALIAS + self._DIVIDER + fields[i]

        return fields

    def __hydrate(self, query_result: dict) -> HydratedFiets:
        fiets_data = {}
        fiets_type_data = {}

        for key, value in query_result.items():

            if key.startswith(self.__FIETS_ALIAS + self._DIVIDER):
                fiets_data[re.sub(r'^' + self.__FIETS_ALIAS + self._DIVIDER, '', key)] = value

            if key.startswith(self.__FIETS_TYPE_ALIAS + self._DIVIDER):
                fiets_type_data[re.sub(r'^' + self.__FIETS_TYPE_ALIAS + self._DIVIDER, '', key)] = value

        fiets = HydratedFiets(fiets_data)
        fiets.set_fiets_type(FietsType(fiets_type_data))

        return fiets

    def get_all(self) -> list[HydratedFiets]:
        fietsen_list = []

        fields = self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + FietsRepository.FIETS_TABLE + ' AS ' + self.__FIETS_ALIAS +
                 (' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                  ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'))

        for query_result in self._fetch_all(query):
            fietsen_list.append(self.__hydrate(query_result))

        return fietsen_list

    def get_by_id(self, id: int) -> HydratedFiets | None:
        fields = self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + FietsRepository.FIETS_TABLE + ' AS ' + self.__FIETS_ALIAS +
                 (' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                  ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'))

        params = {'fiets_id': id}

        query_result = self._fetch_one(query, params)
        if query_result is None:
            return None

        return self.__hydrate(query_result)

    def get_all_beschikbaar_binnen_datum_bereik(self, start_datum: str, eind_datum: str) -> list[HydratedFiets]:
        fietsen_list = []

        fields = self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + FietsRepository.FIETS_TABLE +
                 ' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                 ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'
                 ' LEFT JOIN ' + ContractFietsRepository.CONTRACT_FIETS_TABLE +
                 ' ON ' + FietsRepository.FIETS_TABLE + '.fiets_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.fiets_id' +
                 ' LEFT JOIN ' + ContractRepository.CONTRACT_TABLE +
                 ' ON ' + ContractRepository.CONTRACT_TABLE + '.contract_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_id' +
                 ' WHERE NOT EXISTS (' +
                    'SELECT ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_fiets_id FROM ' + ContractFietsRepository.CONTRACT_FIETS_TABLE +
                    ' INNER JOIN ' + ContractRepository.CONTRACT_TABLE + ' ON ' + ContractRepository.CONTRACT_TABLE + '.contract_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_id' +
                    ' WHERE ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.fiets_id = ' + FietsRepository.FIETS_TABLE + '.fiets_id AND (' +
                    ' %s BETWEEN ' + ContractRepository.CONTRACT_TABLE + '.start_datum AND ' + ContractRepository.CONTRACT_TABLE + '.eind_datum OR ' +
                    ' %s BETWEEN ' + ContractRepository.CONTRACT_TABLE + '.start_datum AND ' + ContractRepository.CONTRACT_TABLE + '.eind_datum' +
                    ')' +
                 ') GROUP BY ' + FietsRepository.FIETS_TABLE + '.fiets_id')

        params = (start_datum, eind_datum)

        for query_result in self._fetch_all(query, params):
            fietsen_list.append(self.__hydrate(query_result))

        return fietsen_list

    def get_beschikbaar_binnen_datum_bereik_by_id(self, start_datum: str, eind_datum: str, id: int) -> HydratedFiets | None:
        fields = self.__fiets_fields() + self.__fiets_type_fields()

        query = ('SELECT ' + ', '.join(fields) + ' FROM ' + FietsRepository.FIETS_TABLE +
                 ' LEFT JOIN ' + FietsTypeRepository.FIETS_TYPE_TABLE + ' AS ' + self.__FIETS_TYPE_ALIAS +
                 ' ON ' + self.__FIETS_ALIAS + '.fiets_type_id = ' + self.__FIETS_TYPE_ALIAS + '.fiets_type_id'
                 ' LEFT JOIN ' + ContractFietsRepository.CONTRACT_FIETS_TABLE +
                 ' ON ' + FietsRepository.FIETS_TABLE + '.fiets_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.fiets_id' +
                 ' LEFT JOIN ' + ContractRepository.CONTRACT_TABLE +
                 ' ON ' + ContractRepository.CONTRACT_TABLE + '.contract_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_id' +
                 ' WHERE ' + FietsRepository.FIETS_TABLE + '.fiets_id = %s' +
                 ' AND NOT EXISTS (' +
                    'SELECT ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_fiets_id FROM ' + ContractFietsRepository.CONTRACT_FIETS_TABLE +
                    ' INNER JOIN ' + ContractRepository.CONTRACT_TABLE + ' ON ' + ContractRepository.CONTRACT_TABLE + '.contract_id = ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.contract_id' +
                    ' WHERE ' + ContractFietsRepository.CONTRACT_FIETS_TABLE + '.fiets_id = ' + FietsRepository.FIETS_TABLE + '.fiets_id AND (' +
                    ' %s BETWEEN ' + ContractRepository.CONTRACT_TABLE + '.start_datum AND ' + ContractRepository.CONTRACT_TABLE + '.eind_datum OR ' +
                    ' %s BETWEEN ' + ContractRepository.CONTRACT_TABLE + '.start_datum AND ' + ContractRepository.CONTRACT_TABLE + '.eind_datum' +
                    ')' +
                 ') GROUP BY ' + FietsRepository.FIETS_TABLE + '.fiets_id')

        params = (id, start_datum, eind_datum)

        query_result = self._fetch_one(query, params)

        if query_result is None:
            return None

        return self.__hydrate(query_result)