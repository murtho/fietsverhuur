
class ContractFiets:
    MANDATORY_ATTRIBUTES = [
        'contract_id',
        'fiets_id',
    ]

    contract_fiets_id : int | None = None
    contract_id : int | None = None
    fiets_id : int | None = None

    def __init__(self, contract_fiets_data : dict[str, str | int]):
        # Valideer of alle attributen van de contract fiets aanwezig zijn
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in contract_fiets_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van de contract fiets
        for attribute, value in contract_fiets_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['contract_fiets_id'] = getattr(self, 'contract_fiets_id')

        for attribute in self.MANDATORY_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute)

        return dictionary

    @staticmethod
    def fields() -> list:
        return ['contract_fiets_id'] + ContractFiets.MANDATORY_ATTRIBUTES