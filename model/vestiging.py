
class Vestiging:
    MANDATORY_ATTRIBUTES = [
        'naam',
        'straat',
        'huisnummer',
        'postcode',
        'plaats',
    ]

    OPTIONAL_ATTRIBUTES = [
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
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in vestiging_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van de vestiging
        for attribute, value in vestiging_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['vestiging_id'] = getattr(self, 'vestiging_id')

        for attribute in self.MANDATORY_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute)

        for attribute in self.OPTIONAL_ATTRIBUTES:
            if hasattr(self, attribute):
                dictionary[attribute] = getattr(self, attribute)
            else:
                dictionary[attribute] = None

        return dictionary

    @staticmethod
    def fields() -> list:
        return ['vestiging_id'] + Vestiging.MANDATORY_ATTRIBUTES + Vestiging.OPTIONAL_ATTRIBUTES

    def adres(self):
        return '{straat} {huisnummer}{toevoeging}'.format(
            straat = self.straat,
            huisnummer = self.huisnummer,
            toevoeging = self.toevoeging or ''
        )