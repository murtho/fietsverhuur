from component.klant_table import KlantTable
from repository.klant_repository import KlantRepository
from rich.table import Table
from rich.console import Console
from model.klant import Klant
import re # regex

# Interactie met de gebruiker voor het tonen, invoeren en wijzigen van klant gegevens
class KlantController:

    __klant_repo : KlantRepository = None

    def __init__(self, klant_repo : KlantRepository) -> None:
        self.__klant_repo = klant_repo

    # Maak een nieuwe klant aan
    def nieuwe_klant(self) -> None:
        print('Voer de gevraagde gegevens in om een nieuwe klant in te voeren.')

        voornaam = self.__prompt_for_voornaam()
        achternaam = self.__prompt_for_achternaam()
        straat = self.__prompt_for_straat()
        huisnummer = self.__prompt_for_huisnummer()
        toevoeging = self.__prompt_for_toevoeging()
        postcode = self.__prompt_for_postcode()
        plaats = self.__prompt_for_plaats()

        klant = Klant({
            'voornaam': voornaam,
            'achternaam': achternaam,
            'straat': straat,
            'huisnummer': huisnummer,
            'toevoeging': toevoeging,
            'postcode': postcode,
            'plaats': plaats,
        })

        print('Valideer of je deze klant definitief wil toevoegen?')
        table = Table(title='Nieuwe klant')
        table.add_column('Eigenschap')
        table.add_column('Waarde')

        table.add_row('voornaam', klant.voornaam)
        table.add_row('achternaam', klant.achternaam)
        table.add_row('straat', klant.straat)
        table.add_row('huisnummer', str(klant.huisnummer))
        table.add_row('toevoeging', klant.toevoeging)
        table.add_row('postcode', klant.postcode)
        table.add_row('plaats', klant.plaats)

        console = Console()
        console.print(table)

        proceed = input('Wil je deze klant toevoegen? (j/n)')

        if proceed == 'j':
            # TODO: test of insert van klant werkt
            self.__klant_repo.insert(klant)

            print('De klant is toegevoegd.')
        else:
            print('De klant is niet toegevoegd.')

    # Bewerk een bestaande klant
    def bewerk_klant(self) -> None:
        klanten_list = self.__klant_repo.get_all()
        klant_table = KlantTable(klanten_list)
        klant_table.print()

        print('om een klant te bewerken, dient u deze te selecteren.')
        klant_id = self.__prompt_for_klant_id()

        klant = self.__klant_repo.get_by_id(klant_id)

        klant_bewerkt = {}
        klant_bewerkt.update(klant.__dict__())
        klant_bewerkt['klant_id'] = klant_id

        print('Wat wil je aan de klant bewerken?')
        if 'j' == input('Wil je de naam van de klant wijzigen? (j/n)'):
            klant_bewerkt['voornaam'] = self.__prompt_for_voornaam()

        if 'j' == input('Wil je de achternaam van de klant wijzigen? (j/n)'):
            klant_bewerkt['achternaam'] = self.__prompt_for_achternaam()

        if 'j' == input('Wil je de straat van de klant wijzigen? (j/n)'):
            klant_bewerkt['straat'] = self.__prompt_for_straat()

        if 'j' == input('Wil je het huisnummer van de klant wijzigen? (j/n)'):
            klant_bewerkt['huisnummer'] = self.__prompt_for_huisnummer()

        if 'j' == input('Wil je de toevoeging van de klant wijzigen? (j/n)'):
            klant_bewerkt['toevoeging'] = self.__prompt_for_toevoeging()

        if 'j' == input('Wil je het postcode van de klant wijzigen? (j/n)'):
            klant_bewerkt['postcode'] = self.__prompt_for_postcode()

        if 'j' == input('Wil je de plaats van de klant wijzigen? (j/n)'):
            klant_bewerkt['plaats'] = self.__prompt_for_plaats()

        print('Valideer of je deze klant definitief wil wijzigen?')
        table = Table(title='Bewerk klant')
        table.add_column('Eigenschap')
        table.add_column('Oude waarde')
        table.add_column('Nieuwe waarde')

        table.add_row('voornaam', klant.voornaam, klant_bewerkt['voornaam'])
        table.add_row('achternaam', klant.achternaam, klant_bewerkt['achternaam'])
        table.add_row('straat', klant.straat, klant_bewerkt['straat'])
        table.add_row('huisnummer', str(klant.huisnummer), str(klant_bewerkt['huisnummer']))
        table.add_row('toevoeging', klant.toevoeging, klant_bewerkt['toevoeging'])
        table.add_row('postcode', klant.postcode, klant_bewerkt['postcode'])
        table.add_row('plaats', klant.plaats, klant_bewerkt['plaats'])

        console = Console()
        console.print(table)

        proceed = input('Wil je deze klant wijzigen? (j/n)')

        if proceed == 'j':
            self.__klant_repo.update(Klant(klant_bewerkt))

            print('De klant is gewijzigd.')
        else:
            print('De klant is niet gewijzigd.')

    # Verwijder een bestaande klant
    def verwijder_klant(self) -> None:
        klanten_list = self.__klant_repo.get_all()
        klant_table = KlantTable(klanten_list)
        klant_table.print()

        print('om een klant te verwijderen, dient u deze te selecteren.')
        klant_id = self.__prompt_for_klant_id()

        klant = self.__klant_repo.get_by_id(klant_id)

        if 'j' == input('Weet je zeker dat je de klant {naam} wil verwijderen? (j/n)'.format(naam = klant.naam())):
            self.__klant_repo.delete_by_id(int(klant_id))
            print('De klant is verwijderd.')
        else:
            print('De klant is niet verwijderd.')

    # Zoek een klant op naam of adres gegevens
    def zoek_klant(self) -> None:

        print('U kunt een klant op naam zoeken')
        search_term = self.__prompt_for_search_term()

        klanten_list = self.__klant_repo.search('%' + search_term + '%')

        if len(klanten_list) == 0:
            print('Er zijn geen klanten gevonden met de naam {search_term}.'.format(search_term = search_term))

            if 'j' == input('Wil je opnieuw naar een klant zoeken? (j/n)'):
                self.zoek_klant()
        else:
            print('Er zijn {aantal} klanten gevonden met de naam {search_term}.'.format(aantal = len(klanten_list), search_term = search_term))
            klant_table = KlantTable(klanten_list)
            klant_table.print()


    def __prompt_for_voornaam(self) -> str:
        while True:
            voornaam = input('Wat is de voornaam?')
            if voornaam == '':
                print('Voornaam mag niet leeg zijn')
                return self.__prompt_for_voornaam()
            elif voornaam.__len__() > Klant.VOORNAAM_MAX_LENGTH:
                print('Voornaam mag maximaal {max} tekens bevatten'.format(max = Klant.VOORNAAM_MAX_LENGTH))
                return self.__prompt_for_voornaam()
            else:
                return voornaam

    def __prompt_for_achternaam(self) -> str:
        while True:
            achternaam = input('Wat is de achternaam?')
            if achternaam == '':
                print('Achternaam mag niet leeg zijn')
                return self.__prompt_for_achternaam()
            elif achternaam.__len__() > Klant.ACHTERNAAM_MAX_LENGTH:
                print('Achternaam mag maximaal {max} tekens bevatten'.format(max = Klant.ACHTERNAAM_MAX_LENGTH))
                return self.__prompt_for_achternaam()
            else:
                return achternaam

    def __prompt_for_straat(self) -> str:
        while True:
            straat = input('Wat is de straat?')
            if straat == '':
                print('Straat mag niet leeg zijn')
                return self.__prompt_for_straat()
            elif straat.__len__() > Klant.STRAAT_MAX_LENGTH:
                print('Straat mag maximaal {max} tekens bevatten'.format(max = Klant.STRAAT_MAX_LENGTH))
                return self.__prompt_for_straat()
            else:
                return straat

    def __prompt_for_huisnummer(self) -> int:
        while True:
            huisnummer = input('Wat is het huisnummer?')
            if re.match(r'^\d+$', huisnummer) is None:
                print('Huisnummer dient een geldig heel getal te zijn.')
                return self.__prompt_for_huisnummer()
            else:
                return int(huisnummer)

    def __prompt_for_toevoeging(self) -> str:
        while True:
            toevoeging = input('Wat is de toevoeging?').upper()
            if toevoeging == '':
                return '' # toevoeging is optioneel
            elif re.match(r'^[A-Z]{1,2}$', toevoeging) is None:
                print('Toevoeging dient 1 of 2 letters te zijn.')
                return self.__prompt_for_toevoeging()
            else:
                return toevoeging

    def __prompt_for_postcode(self) -> str:
        while True:
            postcode = input('Wat is het postcode?').upper()
            if re.match(r'^[0-9]{4}[A-Z]{2}$', postcode) is None:
                print('Postcode dient 4 getallen gevolgd door 2 letters te zijn.')
                return self.__prompt_for_postcode()
            else:
                return postcode

    def __prompt_for_plaats(self) -> str:
        while True:
            plaats = input('Wat is de plaats?')
            if plaats == '':
                print('Plaats mag niet leeg zijn')
                return self.__prompt_for_plaats()
            elif plaats.__len__() > Klant.PLAATS_MAX_LENGTH:
                print('Plaats mag maximaal {max} tekens bevatten'.format(max = Klant.PLAATS_MAX_LENGTH))
                return self.__prompt_for_straat()
            else:
                return plaats

    def __prompt_for_klant_id(self) -> int:
        while True:
            klant_id = input('Welke klant wil je selecteren? (id)')
            if re.match(r'^\d+$', klant_id) is None:
                print('U dient een geldig heel getal in te voeren om de klant te selecteren.')
                return self.__prompt_for_klant_id()
            elif self.__klant_repo.get_by_id(int(klant_id)) == None:
                print('U dient een ID in te voeren dat voorkomt in de lijst van klanten.')
                return self.__prompt_for_klant_id()
            else:
                return int(klant_id)

    def __prompt_for_search_term(self) -> str:
        while True:
            search_term = input('Waar wilt u op zoeken?')
            if search_term == '':
                print('U dient een waarde in te voeren om een klant te zoeken.')
                return self.__prompt_for_search_term()
            else:
                return search_term