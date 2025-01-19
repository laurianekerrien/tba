
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from charactere import GameMaster
import random

# Variable globale pour le débogage
DEBUG = True


class GameMaster:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.secret_solution = {}
        self.game_master = None
        if DEBUG:
            print("DEBUG: Initialisation du jeu.")

    # Setup the game
    def setup(self):
        """Configure les éléments du jeu."""
        print("\n**************************************************")
        print("            BIENVENUE DANS LE JEU CLUEDO          ")
        print("**************************************************")

        if DEBUG:
            print("DEBUG: Configuration des commandes et des pièces.")

        # Présentation de l'histoire par le maître du jeu
        print("\n*** LE MAÎTRE DU JEU PREND LA PAROLE ***")
        print("Monsieur Taupe :")
        print("Bienvenue dans ce manoir mystérieux. Un crime abominable vient d'être commis.")
        print("Le célèbre Docteur Lenoir a été retrouvé sans vie dans des circonstances tragiques.")
        print("Votre mission est de résoudre ce mystère en découvrant l'arme, le coupable et la pièce où le crime a eu lieu.")
        print("Mais attention, les apparences peuvent être trompeuses, et je ne vous donnerai que des hypothèses fausses !")
        print("Bonne chance, détective.\n")

        # Setup commands
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, passage secret)", Actions.go, 1)
        self.commands["rester"] = Command("rester", " : rester dans cette pièce", Actions.rester, 0)
        self.commands["history"] = Command("history", " : consulter l'historique des pièces visitées", Actions.history, 0)
        self.commands["look"] = Command("look", " : consulter ce qu'il y a dans la pièce", Actions.look, 0)
        self.commands["drop"] = Command("drop", " : poser un objet dans la pièce", Actions.drop, 1)
        self.commands["take"] = Command("take", " : prendre un objet dans la pièce", Actions.take, 1)
        self.commands["check"] = Command("check", " : vérifier l'inventaire", Actions.check, 0)
        self.commands["hypothese"] = Command("hypothese", " <arme> <personnage> : Formuler une hypothèse.", self.make_hypothesis, 2)

        # Setup items
        items = [
            Item("Poignard", "Une arme courte et tranchante."),
            Item("Revolver", "Une arme à feu portative."),
            Item("Chandelier", "Un chandelier pouvant servir comme arme."),
            Item("Corde", "Une corde robuste."),
            Item("Clé anglaise", "Une clé anglaise lourde et solide."),
            Item("Tuyau de plomb", "Un tuyau de plomb lourd et solide."),
            Item("Livre ancien", "Un livre avec une couverture poussiéreuse."),
            Item("Tasse", "Une tasse de thé abandonnée."),
            Item("Ustensile de cuisine", "Un ustensile pratique pour cuisiner.")
        ]

        # Setup rooms
        cuisine = Room("cuisine", "vous êtes dans la cuisine.", [items[3], items[8]])
        hall = Room("hall", "vous êtes dans le hall.", [items[2], items[6]])
        salon = Room("salon", "vous êtes dans le salon.", [items[0], items[7]])
        bureau = Room("bureau", "vous êtes dans le bureau.", [items[6]])
        grand_salon = Room("grand_salon", "vous êtes dans le grand salon.", [items[1]])
        bibliothèque = Room("bibliothèque", "vous êtes dans la bibliothèque.", [items[4], items[6]])
        salle_à_manger = Room("salle_à_manger", "vous êtes dans la salle à manger.", [items[8], items[5]])
        salle_de_billard = Room("salle_de_billard", "vous êtes dans la salle de billard.", [items[1], items[7]])
        véranda = Room("véranda", "vous êtes dans la véranda.", [items[7]])

        self.rooms.extend([cuisine, hall, salon, bureau, grand_salon, bibliothèque, salle_à_manger, salle_de_billard, véranda])

        # Create exits for rooms
        cuisine.exits = {"N": None, "E": grand_salon, "S": salle_à_manger, "O": None, "passage_secret": bureau}
        hall.exits = {"N": None, "E": bureau, "S": None, "O": salon, "passage_secret": None}
        salon.exits = {"N": salle_à_manger, "E": hall, "S": None, "O": None, "passage_secret": véranda}
        bureau.exits = {"N": bibliothèque, "E": None, "S": None, "O": hall, "passage_secret": cuisine}
        grand_salon.exits = {"N": None, "E": véranda, "S": None, "O": cuisine, "passage_secret": None}
        bibliothèque.exits = {"N": salle_de_billard, "E": None, "S": bureau, "O": None, "passage_secret": None}
        salle_à_manger.exits = {"N": cuisine, "E": None, "S": salon, "O": None, "passage_secret": None}
        salle_de_billard.exits = {"N": véranda, "E": None, "S": bibliothèque, "O": None, "passage_secret": None}
        véranda.exits = {"N": None, "E": None, "S": salle_de_billard, "O": grand_salon, "passage_secret": salon}

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = salle_à_manger
        self.game_master = GameMaster("Monsieur Taupe", random.choice(self.rooms))
        self.game_master.talk()
        self.secret_solution = {
            "weapon": random.choice(self.game_master.weapons),
            "character": random.choice(self.game_master.characteres),
            "room": random.choice([room.name for room in self.rooms])
        }
        if DEBUG:
            print(f"DEBUG: Solution secrète : {self.secret_solution}")

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()

        # Loop until the game is finished
        while not self.finished:
            self.show_turn_summary()
            command = input("> ").strip().lower()
            self.process_command(command)

    def make_hypothesis(self, game, list_of_words, number_of_parameters):
        """Valide l'hypothèse formulée par le joueur."""
        if len(list_of_words) != 3:
            print("Usage : hypothese <arme> <personnage>")
            return

        weapon, character = list_of_words[1], list_of_words[2]
        current_room = self.player.current_room.name
        incorrect_elements = []

        if weapon.lower() != self.secret_solution["weapon"].lower():
            incorrect_elements.append(f"L'arme {weapon} est incorrecte.")
        if character.lower() != self.secret_solution["character"].lower():
            incorrect_elements.append(f"Le personnage {character} est incorrect.")
        if current_room.lower() != self.secret_solution["room"].lower():
            incorrect_elements.append(f"La pièce {current_room} est incorrecte.")

        if not incorrect_elements:
            print("Bravo ! Vous avez résolu le meurtre !")
            self.finished = True
        else:
            print(f"Hypothèse incorrecte : {random.choice(incorrect_elements)}")

    def process_command(self, command_string):
        if command_string == '':
            return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans cette partie de Cluedo.")
        print("Déplacez-vous sur la map et faites vos hypothèses pour résoudre le crime !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
        self.player.get_history()

    def show_turn_summary(self):
        current_room = self.player.current_room
        print("\nVous êtes dans :", current_room.name)
        print("Description :", current_room.description)
        print("Sorties possibles :")
        for direction, room in current_room.exits.items():
            if room:
                print(f"- {direction.upper()} : {room.name}")

        print("\nHistorique des pièces visitées :")
        for idx, room in enumerate(self.player.history, start=1):
            print(f"{idx}. {room.name}")

        print("\nEntrez votre commande :")


def main():
    Game().play()


if __name__ == "__main__":
    main()
