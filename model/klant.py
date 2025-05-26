
class Klant:
    MANDATORY_ATTRIBUTES = [
        'voornaam',
        'achternaam',
        'straat',
        'huisnummer',
        'postcode',
        'plaats',
    ]

    OPTIONAL_ATTRIBUTES = [
        'toevoeging'
    ]

    VOORNAAM_MAX_LENGTH = 64
    ACHTERNAAM_MAX_LENGTH = 64
    STRAAT_MAX_LENGTH = 64
    PLAATS_MAX_LENGTH = 64

    klant_id : int | None = None
    voornaam : str | None = None
    achternaam : str | None = None
    straat : str | None = None
    huisnummer : str | None = None
    toevoeging : str | None = None
    postcode : str | None = None
    plaats : str | None = None

    def __init__(self, klant_data : dict[str, str | int]):
        # Valideer of alle attributen van de klant aanwezig zijn
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in klant_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van de klant
        for attribute, value in klant_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['klant_id'] = getattr(self, 'klant_id')

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
        return ['klant_id'] + Klant.MANDATORY_ATTRIBUTES + Klant.OPTIONAL_ATTRIBUTES

    def naam(self):
        return '{voornaam} {achternaam}'.format(
            voornaam = self.voornaam,
            achternaam = self.achternaam
        )

    def adres(self):
        return '{straat} {huisnummer}{toevoeging}'.format(
            straat = self.straat,
            huisnummer = self.huisnummer,
            toevoeging = self.toevoeging or ''
        )