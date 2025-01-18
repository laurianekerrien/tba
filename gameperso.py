# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from charactere import GameMaster
from item import Item
import random

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.secret_solution = {}
        self.game_master = None
        
    # Setup the game
    def setup(self):
        """Configure les éléments du jeu."""
        print("\n**************************************************")
        print("            BIENVENUE DANS LE JEU CLUEDO          ")
        print("**************************************************")

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
        drop = Command("drop", " : permet de remettre dans la piece l'objet ", Actions.drop, 0)
        self.commands["drop"] = drop
        take = Command("take", " : permet de prendre l'objet dans la piece", Actions.take, 0)
        self.commands["take"] = take
        
        # Setup rooms

        cuisine = Room("cuisine", "vous etes dans la cuisine choisissez une arme, et une personne")
        self.rooms.append(cuisine)
        hall = Room("hall", "vous etes dans le hall choisissez une arme, et une personne.")
        self.rooms.append(hall)
        salon = Room("salon", "vous etes dans le salon choisissez une arme, et une personne.")
        self.rooms.append(salon)
        bureau = Room("bureau", "vous etes dans le bureau choisissez une arme, et une personne")
        self.rooms.append(bureau)
        grand_salon = Room("grand_salon", "vous etes dans le grand salon choisissez une arme, et une personne")
        self.rooms.append(grand_salon)
        bibliothèque = Room("bibliothèque", "vous etes dans la bibliothèque choisissez une arme, et une personne")
        self.rooms.append(bibliothèque)
        salle_à_manger = Room("salle_à_manger","vous etes dans la salle à manger choisissez une arme, et une personne")
        self.rooms.append(salle_à_manger)
        salle_de_billard = Room("salle_de_billard", "vous etes dans la salle de billard choisissez une arme, et une personne")
        self.rooms.append(salle_de_billard)
        véranda = Room("véranda", "vous etes dans la véranda choisissez une arme, et une personne")
        self.rooms.append(véranda)

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
        print(f"\n{self.game_master.name} : {self.game_master.get_msg()}")
        print(f"{self.game_master.name} : {self.game_master.get_msg()}")
        print(f"{self.game_master.name} : {self.game_master.get_msg()}")

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
        print("\nSuggestion d'hypothèse :")
        print(f"Hypothèse possible : hypothese {random_weapon} {random_character}")
        print("\nEntrez votre commande (par exemple : 'go <direction>', 'hypothese <arme> <personnage>', 'help', etc.)")


def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
import random

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"
    



class Room:
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = items if items else []

    def __str__(self):
        return f"{self.name}: {self.description}"

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None



# Création des items
items = [
    Item("Poignard", "Une arme courte et tranchante."),
    Item("Revolver", "Une arme à feu portative."),
    Item("Chandelier", "Un chandelier pouvant servir comme arme."),
    Item("Poison", "Une fiole contenant une substance toxique."),
    Item("Corde", "Une corde robuste."),
    Item("Clé_anglaise", "Une clé anglaise lourde et solide.")
    ]

# Création des pièces
rooms = {
    "cuisine": Room("Cuisine", "Une cuisine avec des ustensiles et un peut être un objet mystère.", items[4]),
    "hall": Room("Hall", "Un hall avec des tableaux de chats, une bougie et un peut être un objet mystère.", items[2]),
    "salon": Room("Salon", "Un salon avec une télévision et un canapé."),
    "bureau": Room("Bureau", "Un bureau avec des livres et une lampe."),
    "grand_salon": Room("Grand Salon", "Un grand salon avec des canapés et une table de jeux et un peut être un objet mystère.", items[3]),
    "bibliothèque": Room("Bibliothèque", "Une bibliothèque avec des manuscrits anciens et un peut être un objet mystère.", items[1]),
    "salle_à_manger": Room("Salle à Manger", "Une grande salle à manger avec une table et un peut être un objet mystère.", items[0]),
    "salle_de_billard": Room("Salle de Billard", "Une salle de billard avec une table de billard."),
    "veranda": Room("Véranda", "Une véranda avec un petit jardin et et un peut être un objet mystère.", items[5])
}

# Création du joueur
player = Player(input("Entrez le nom du joueur : "))
player.current_room = rooms["cuisine"]  # Le joueur commence dans la cuisine

# Boucle de jeu
while True:
    command = input("> ").strip().lower()
    if command.startswith("go "):
        room_name = command[3:]
        if room_name in rooms:
            player.current_room = rooms[room_name]
            print(f"Vous êtes maintenant dans {room_name}.")
        else:
            print(f"La pièce '{room_name}' n'existe pas.")
    elif command == "look":
        player.look()
    elif command.startswith("look "):
        print("La commande 'look' ne prend pas de paramètre.")
    elif command == "check":
        player.check_inventory()
    elif command.startswith("check "):
        print("La commande 'check' ne prend pas de paramètre.")
    elif command.startswith("take "):
        item_name = command[5:]
        player.take(item_name)
    elif command.startswith("drop "):
        item_name = command[5:]
        player.drop(item_name)
    elif command == "talk":
                game_master.talk()
    elif command == "quit":
        print("Merci d'avoir joué !")
        break
    else:
        print("Commande non reconnue. Essayez 'go', 'look', 'take', 'drop', 'check', 'cards', 'talk', 'hypothesis', ou 'quit'.")

if __name__ == "__main__":
    Game().play()