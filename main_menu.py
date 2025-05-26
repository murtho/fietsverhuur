from containers import Container

# Interactie met de gebruiker in het hoofd menu
class MainMenu:

    def __init__(self):
        pass

    # Toon het menu
    def display_menu(self):
        print('Hoofd Menu')
        print('[1] klant toevoegen')
        print('[2] klant wijzigen')
        print('[3] klant verwijderen')
        print('[4] klant zoeken')
        print('[5] fiets toevoegen')
        print('[6] contract opstellen')
        print('[7] contract tonen')
        print('[8] overzicht alle gegevens')
        print('[9] programma beëindigen')
        print('')
        choice = int(input('Welke actie wil je uitvoeren?'))
        self.__handle_menu_choice(choice)

    # handel de keuze van de gebruiker af
    def __handle_menu_choice(self, choice):
        match choice:
            case 1:
                self.__vastleggen_klant()
            case 2:
                self.__wijzigen_klant()
            case 3:
                self.__verwijderen_klant()
            case 4:
                self.__zoeken_klant()
            case 5:
                self.__toevoegen_fiets()
            case 6:
                self.__vastleggen_contract()
            case 7:
                self.__toon_contract()
            case 8:
                self.__toon_alle_gegevens()
            case 9:
                exit()
            case _:
                choice = int(input('Onbekende optie. Probeer opnieuw.'))
                self.__handle_menu_choice(choice)

    def __vastleggen_klant(self):
        container = Container()
        container.klant_controller().nieuwe_klant()
        self.__return_to_menu()

    def __wijzigen_klant(self):
        container = Container()
        container.klant_controller().bewerk_klant()
        self.__return_to_menu()

    def __verwijderen_klant(self):
        container = Container()
        container.klant_controller().verwijder_klant()
        self.__return_to_menu()

    def __zoeken_klant(self):
        container = Container()
        container.klant_controller().zoek_klant()
        self.__return_to_menu()

    def __toevoegen_fiets(self):
        container = Container()
        container.fiets_controller().nieuwe_fiets()
        self.__return_to_menu()

    def __vastleggen_contract(self):
        container = Container()
        container.contract_controller().nieuw_contract()
        self.__return_to_menu()

    def __toon_contract(self):
        container = Container()
        container.contract_controller().toon_contract()
        self.__return_to_menu()

    def __toon_alle_gegevens(self):
        container = Container()
        container.overzicht_controller().totaal_overzicht()
        self.__return_to_menu()

    # Vraag of de gebruiker terug wil naar het menu
    def __return_to_menu(self):
        answer = input('Wilt u terug naar het menu? (j/n)')

        if answer == 'j':
            self.display_menu()
        else:
            exit()