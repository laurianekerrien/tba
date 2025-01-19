# Description: Game class

# Import modules

from roomnul import Room
from playernul import Player
from commandenul import Command
from actionnul import Actions
from itemnul import Item
import random

# Variable globale pour le débogage
DEBUG = True

class GameMaster:
    def __init__(self, name, room):
        """
        Initialise le maître du jeu avec un nom et une pièce de départ.
        :param name: Nom du maître du jeu
        :param room: Pièce où commence le maître du jeu
        """
        self.name = name
        self.room = room
        self.messages = [
            "Bienvenue dans ce manoir mystérieux.",
            "Un meurtre vient d'être commis dans ce manoir.",
            "Le célèbre Docteur Lenoir a été retrouvé sans vie.",
            "Votre mission est de résoudre ce mystère en trouvant l'arme, le coupable et le lieu du crime.",
            "Mais attention, les apparences sont souvent trompeuses.",
            "Je ne vous donnerai que des hypothèses fausses. À vous de les trier !"
        ]
        self.weapons = ["Revolver", "Poignard", "Chandelier", "Corde", "Clé_anglaise", "Poison"]
        self.rooms = ['cuisine', 'hall',' salon', 'bureau', 'grand_salon', 'bibliothèque', 'salle_à_manger', 'salle_de_billard', 'véranda']
        self.characteres = ["Professeur_Violet", "Colonel_Moutarde", "Mademoiselle_Rose", "Madame_Leblanc", "Docteur_Olive", "Madame_Pervenche"]

    def move(self):
        """Déplace le maître du jeu aléatoirement dans une pièce adjacente."""
        if random.choice([True, False]):
            self.room = random.choice(list(self.room.exits.values()))
            if DEBUG: print(f"DEBUG: {self.name} s'est déplacé dans {self.room.name}")
            return True
        return False

    def get_msg(self):
        """Retourne et supprime un message de la liste des messages."""
        if self.messages:
            return self.messages.pop(0)
        return "Je n'ai plus rien à dire pour le moment."

    def talk(self):
        """Affiche un message du maître du jeu."""
        print(f"{self.name} : {self.get_msg()}\n")

    def propose_hypothesis(self):
        """Propose une hypothèse fausse."""
        hypothesis = f"Je pense que c'était {random.choice(self.characteres)} avec le {random.choice(self.weapons)} dans {random.choice(self.rooms)}."
        print(f"{self.name} propose une hypothèse fausse : {hypothesis}")
        if DEBUG: print(f"DEBUG: Hypothèse proposée : {hypothesis}")

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.secret_solution = {}
        self.game_master = None
        if DEBUG: print("DEBUG: Initialisation du jeu.")
        
    # Setup the game
    def setup(self):
        """Configure les éléments du jeu."""
        print("\n**************************************************")
        print("            BIENVENUE DANS LE JEU CLUEDO          ")
        print("**************************************************")

        if DEBUG: print("DEBUG: Configuration des commandes et des pièces.")

        # Présentation de l'histoire par le maître du jeu
        print("\n*** LE MAÎTRE DU JEU PREND LA PAROLE ***")
        print("Monsieur Taupe :")
        print("Bienvenue dans ce manoir mystérieux. Un crime abominable vient d'être commis.")
        print("Le célèbre Docteur Lenoir a été retrouvé sans vie dans des circonstances tragiques.")
        print("Votre mission est de résoudre ce mystère en découvrant l'arme, le coupable et la pièce où le crime a eu lieu.")
        print("Mais attention, les apparences peuvent être trompeuses, et je ne vous donnerai que des hypothèses fausses !")
        print("Bonne chance, détective.\n")

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, passage sercret et rester )", Actions.go, 1)
        self.commands["go"] = go
        rester = Command("rester", " vous avez choisi de rester dans cette pièce", Actions.rester, 0)
        self.commands["rester"] = rester
        history = Command("history", " : consulter l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        look = Command("look", " : consulter ce qu'il y a dans la piece", Actions.look, 0)
        self.commands["look"] = look
        drop = Command("drop", " : permet de remettre dans la piece l'objet ", Actions.drop, 1)
        self.commands["drop"] = drop
        take = Command("take", " : permet de prendre l'objet dans la piece", Actions.take, 1)
        self.commands["take"] = take
        check = Command("check", " : vérifier votre inventaire", Actions.check, 0)
        self.commands["check"] = check
        
        # Setup rooms

        cuisine = Room("cuisine", "vous etes dans la cuisine choisissez une arme, et une personne")
        hall = Room("hall", "vous etes dans le hall choisissez une arme, et une personne.")
        salon = Room("salon", "vous etes dans le salon choisissez une arme, et une personne.")
        bureau = Room("bureau", "vous etes dans le bureau choisissez une arme, et une personne")
        grand_salon = Room("grand_salon", "vous etes dans le grand salon choisissez une arme, et une personne")
        bibliothèque = Room("bibliothèque", "vous etes dans la bibliothèque choisissez une arme, et une personne")
        salle_à_manger = Room("salle_à_manger","vous etes dans la salle à manger choisissez une arme, et une personne")
        salle_de_billard = Room("salle_de_billard", "vous etes dans la salle de billard choisissez une arme, et une personne")
        véranda = Room("véranda", "vous etes dans la véranda choisissez une arme, et une personne")

        self.rooms.extend([cuisine, hall, salon, bureau, grand_salon, bibliothèque, salle_à_manger, salle_de_billard, véranda])

        # Create exits for rooms

        cuisine.exits = {"N" : None, "E" : grand_salon, "S" : salle_à_manger, "O" : None, "passage_secret" : bureau }  
        hall.exits = {"N" : None, "E" : bureau, "S" : None, "O" : salon , "passage_secret" : None} 
        salon.exits = {"N" : salle_à_manger, "E" : hall, "S" : None, "O" : None , "passage_secret" : véranda}
        bureau.exits = {"N" : bibliothèque, "E" : None, "S" : None, "O" : hall, "passage_secret" : cuisine}
        grand_salon.exits = {"N" : None, "E" : véranda, "S" : None, "O" : cuisine, "passage_secret" : None}  
        bibliothèque.exits = {"N" : salle_de_billard, "E" : None, "S" : bureau, "O" : None, "passage_secret" : None}
        salle_à_manger.exits = {"N" : cuisine, "E" : None, "S" : salon, "O" : None, "passage_secret" : None}
        salle_de_billard.exits = {"N" : véranda, "E" : None, "S" : bibliothèque, "O" : None, "passage_secret" : None}
        véranda.exits = {"N" : None, "E" : None, "S" : salle_de_billard, "O" : grand_salon, "passage_secret" : salon}

        # Assign items to rooms
        items = [
            Item("Poignard", "Une arme courte et tranchante."),
            Item("Revolver", "Une arme à feu portative."),
            Item("Chandelier", "Un chandelier pouvant servir comme arme."),
            Item("Corde", "Une corde robuste."),
            Item("Clé_anglaise", "Une clé anglaise lourde et solide."),
            Item("Poison", "Du poison très efficace."),
            Item("Livre_ancien", "Un livre avec une couverture poussiéreuse."),
            Item("Tasse", "Une tasse de thé abandonnée."),
            Item("Ustensile_de_cuisine", "Un ustensile pratique pour cuisiner.")
        ]

        room_items = {
            "cuisine": [items[3], items[8]],
            "hall": [items[2], items[6]],
            "salon": [items[0], items[7]],
            "bureau": [items[6]],
            "grand_salon": [items[1]],
            "bibliothèque": [items[4], items[6]],
            "salle_à_manger": [items[8], items[5]],
            "salle_de_billard": [items[1], items[7]],
            "véranda": [items[7]]
        }

        for room in self.rooms:
            room.items = room_items.get(room.name.lower(), [])

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
        if DEBUG: print(f"DEBUG: Solution secrète : {self.secret_solution}")

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()

        # Loop until the game is finished
        while not self.finished:
            self.show_turn_summary()
            command = input("> ").strip().lower()
            if command.startswith("hypothese"):
                self.make_hypothesis(command)
            else:
                self.process_command(command)

    def make_hypothesis(self, command):
        try:
            # Extraire l'arme et le personnage de la commande
            _, weapon, character = command.split(" ", 2)
        except ValueError:
            print("Format de l'hypothèse incorrect. Utilisez : hypothese <arme> <personnage>")
            return

        # La pièce est celle où se trouve le joueur
        current_room = self.player.current_room.name

        # Vérification de l'hypothèse
        incorrect_elements = []
        if weapon.lower() != self.secret_solution["weapon"].lower():
            incorrect_elements.append(f"L'arme {weapon} est incorrecte.")
        if character.lower() != self.secret_solution["character"].lower():
            incorrect_elements.append(f"Le personnage {character} est incorrect.")
        if current_room.lower() != self.secret_solution["room"].lower():
            incorrect_elements.append(f"La pièce {current_room} est incorrecte.")

        # Résultat de l'hypothèse
        if not incorrect_elements:
            print("Bravo ! Vous avez résolu le meurtre !")
            self.finished = True
        else:
            # Afficher une erreur aléatoire parmi les éléments incorrects
            wrong_hint = random.choice(incorrect_elements)
            print(f"Hypothèse incorrecte : {wrong_hint}")

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        if command_string == '':   #si on a une commande vide on ne répond rien
            return

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")

        # If the command is recognized, execute it
        else:
            if DEBUG: print(f"DEBUG: Commande exécutée : {command_word}")
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans cette partie de Cluedo notre cher Docteur Lenoir a été sauvagement assassiné. Déplacez vous sur la map et faites vos hypothèses pour résoudre le crime !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
        self.player.get_history()  # Ajout de la pièce initiale à l'historique
        print("Formulez une hypothèses avec : hypothese <arme> <personnage>")
    
    def show_turn_summary(self):
        """Affiche les informations importantes pour le joueur à chaque tour."""
        current_room = self.player.current_room

        # Afficher les sorties possibles
        print("\nVous êtes dans :", current_room.name)
        print("Description :", current_room.description)
        print("Sorties possibles :")
        for direction, room in current_room.exits.items():
            if room:
                print(f"- {direction.upper()} : {room.name}")

        # Afficher l'historique des pièces visitées
        print("\nHistorique des pièces visitées :")
        for idx, room in enumerate(self.player.history, start=1):
            print(f"{idx}. {room.name}")

        # Proposer une hypothèse aléatoire
        random_weapon = random.choice(self.game_master.weapons)
        random_character = random.choice(self.game_master.characteres)
        print("\n**Mr Taupe** Je pense que l'hypothèse est:")
        print(f"Hypothèse possible : hypothese {random_weapon} {random_character}")
        print("\nEntrez votre commande (par exemple : 'go <direction>', 'hypothese <arme> <personnage>', 'help', etc.)")

def main():
    # Create a game object and play the game
    Game().play()


if __name__ == "__main__":
    main()