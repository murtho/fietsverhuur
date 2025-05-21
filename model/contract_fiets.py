
class ContractFiets:
    MANDATORY_KEYS = [
        'contract_id',
        'fiets_id',
    ]

    contract_fiets_id : int | None = None
    contract_id : int | None = None
    fiets_id : int | None = None

    def __init__(self, contract_fiets_data : dict[str, str | int]):
        # Valideer of alle attributen van de contract fiets aanwezig zijn
        for key in self.MANDATORY_KEYS:
            if key not in contract_fiets_data:
                raise Exception('Missing mandatory key: ' + key)

        # Kopieer alle data van de contract fiets
        for attribute, value in contract_fiets_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['contract_fiets_id'] = getattr(self, 'contract_fiets_id')

        for attribute in self.MANDATORY_KEYS:
            dictionary[attribute] = getattr(self, attribute)

        return dictionary