
class Fiets:
    MANDATORY_ATTRIBUTES = [
        'merk',
        'aankoop_datum',
        'fiets_type_id'
    ]

    MERK_MAX_LENGTH = 32

    fiets_id : int | None = None
    merk : str | None = None
    aankoop_datum : str | None = None
    fiets_type_id : int | None = None

    def __init__(self, fiets_data : dict[str, str | int]):
        # Valideer of alle attributen van de fiets aanwezig zijn
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in fiets_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van de fiets
        for attribute, value in fiets_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['fiets_id'] = getattr(self, 'fiets_id')

        for attribute in self.MANDATORY_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute)

        return dictionary

    @staticmethod
    def fields() -> list:
        return ['fiets_id'] + Fiets.MANDATORY_ATTRIBUTES