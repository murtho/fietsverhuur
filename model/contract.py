
class Contract:
    MANDATORY_ATTRIBUTES = [
        'klant_id',
        'vestiging_id',
        'start_datum',
        'eind_datum',
    ]

    contract_id : int | None = None
    klant_id : int | None = None
    vestiging_id : int | None = None
    start_datum : str | None = None
    eind_datum : str | None = None

    def __init__(self, contract_data : dict[str, str | int]):
        # Valideer of alle attributen van het contract aanwezig zijn
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in contract_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van het contract
        for attribute, value in contract_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['contract_id'] = getattr(self, 'contract_id')

        for attribute in self.MANDATORY_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute)

        return dictionary

    @staticmethod
    def fields() -> list:
        return ['contract_id'] + Contract.MANDATORY_ATTRIBUTES

    def aantal_dagen(self) -> int:
        return int(abs(self.eind_datum - self.start_datum).days + 1)