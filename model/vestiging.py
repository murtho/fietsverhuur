
class Vestiging:
    MANDATORY_KEYS = [
        'naam',
        'straat',
        'huisnummer',
        'postcode',
        'plaats',
    ]

    OPTIONAL_KEYS = [
        'toevoeging'
    ]

    vestiging_id : int | None = None
    naam : str | None = None
    straat : str | None = None
    huisnummer : str | None = None
    toevoeging : str | None = None
    postcode : str | None = None
    plaats : str | None = None

    def __init__(self, vestiging_data : dict[str, str | int]):
        # Valideer of alle attributen van de vestiging aanwezig zijn
        for key in self.MANDATORY_KEYS:
            if key not in vestiging_data:
                raise Exception('Missing mandatory key: ' + key)

        # Kopieer alle data van de vestiging
        for attribute, value in vestiging_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['vestiging_id'] = getattr(self, 'vestiging_id')

        for attribute in self.MANDATORY_KEYS:
            dictionary[attribute] = getattr(self, attribute)

        for key in self.OPTIONAL_KEYS:
            if hasattr(self, key):
                dictionary[key] = getattr(self, key)
            else:
                dictionary[key] = None

        return dictionary

    def adres(self):
        return '{straat} {huisnummer}{toevoeging}'.format(
            straat = self.straat,
            huisnummer = self.huisnummer,
            toevoeging = self.toevoeging or ''
        )