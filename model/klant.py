
class Klant:
    MANDATORY_KEYS = [
        'voornaam',
        'achternaam',
        'straat',
        'huisnummer',
        'postcode',
        'plaats',
    ]

    OPTIONAL_KEYS = [
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
        for key in self.MANDATORY_KEYS:
            if key not in klant_data:
                raise Exception('Missing mandatory key: ' + key)

        # Kopieer alle data van de klant
        for attribute, value in klant_data.items():
            setattr(self, attribute, value)


    def __dict__(self):
        dictionary = {}

        dictionary['klant_id'] = getattr(self, 'klant_id')

        for attribute in self.MANDATORY_KEYS:
            dictionary[attribute] = getattr(self, attribute)

        for key in self.OPTIONAL_KEYS:
            if hasattr(self, key):
                dictionary[key] = getattr(self, key)
            else:
                dictionary[key] = None

        return dictionary


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