
class Fiets:
    MANDATORY_KEYS = [
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
        for key in self.MANDATORY_KEYS:
            if key not in fiets_data:
                raise Exception('Missing mandatory key: ' + key)

        # Kopieer alle data van de fiets
        for attribute, value in fiets_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['fiets_id'] = getattr(self, 'fiets_id')

        for attribute in self.MANDATORY_KEYS:
            dictionary[attribute] = getattr(self, attribute)

        return dictionary