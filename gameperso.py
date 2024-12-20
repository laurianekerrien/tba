# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

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

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

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
        print(f"\nBienvenue {self.player.name} dans cette partie de Cluedo déplacez vous sur la map et faites vos hypothèses pour résoudre le crime !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
        self.player.get_history()  # Ajout de la pièce initiale à l'historique
    

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

    def check_inventory(self):
        if self.inventory:
            print(f"Inventaire de {self.name}:")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print(f"Inventaire de {self.name} est vide.")

    def look(self):
        """Affiche la description de la pièce et les items présents."""
        if self.current_room:
            print(f"Vous êtes dans {self.current_room.name}: {self.current_room.description}")
            if self.current_room.items:
                print("Items présents dans cette pièce:")
                for item in self.current_room.items:
                    print(f"- {item}")
            else:
                print("Il n'y a aucun item dans cette pièce.")
        else:
            print("Vous n'êtes dans aucune pièce.")

    def take(self, item_name):
        """Prend un item de la pièce actuelle et le met dans l'inventaire."""
        if self.current_room:
            for item in self.current_room.items:
                if item.name.lower() == item_name.lower():
                    self.inventory.append(item)
                    self.current_room.items.remove(item)
                    print(f"Vous avez pris : {item}")
                    return
            print(f"L'item '{item_name}' n'est pas dans cette pièce.")
        else:
            print("Vous n'êtes dans aucune pièce pour prendre des items.")

    def drop(self, item_name):
        """Repose un item de l'inventaire dans la pièce actuelle."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.current_room.items.append(item)
                print(f"Vous avez reposé : {item}")
                return
        print(f"L'item '{item_name}' n'est pas dans votre inventaire.")

# Création des items
items = [
    Item("ustensiles de cuisine", "Divers ustensiles pour cuisiner."),
    Item("four", "Un four pour cuire des aliments."),
    Item("mixeur", "Un appareil pour mélanger des ingrédients."),
    Item("tableaux de chats", "Deux tableaux représentant des chats."),
    Item("bougie", "Une bougie allumée sur une table."),
    Item("télévision", "Une grande télévision."),
    Item("grand canapé", "Un canapé confortable avec des coussins."),
    Item("livres", "Des livres rangés dans une grande bibliothèque."),
    Item("lampe", "Une lampe de bureau."),
    Item("canapés", "Deux canapés dans le grand salon."),
    Item("table de jeux", "Une table pour jouer à divers jeux."),
    Item("manuscrits", "Des manuscrits anciens dans la bibliothèque."),
    Item("grande table", "Une table pour manger."),
    Item("chaises", "Des chaises autour de la table."),
    Item("table de billard", "Une table pour jouer au billard."),
    Item("boules de billard", "Des boules pour le billard."),
    Item("petit jardin", "Un petit jardin décoratif."),
    Item("table", "Une table dans la véranda.")
]

# Création des pièces
rooms = {
    "cuisine": Room("Cuisine", "Une cuisine avec des ustensiles et un mixeur.", items[:3]),
    "hall": Room("Hall", "Un hall avec des tableaux de chats et une bougie.", items[3:5]),
    "salon": Room("Salon", "Un salon avec une télévision et un canapé.", items[5:7]),
    "bureau": Room("Bureau", "Un bureau avec des livres et une lampe.", items[7:9]),
    "grand_salon": Room("Grand Salon", "Un grand salon avec des canapés et une table de jeux.", items[9:11]),
    "bibliothèque": Room("Bibliothèque", "Une bibliothèque avec des manuscrits anciens.", [items[11]]),
    "salle_à_manger": Room("Salle à Manger", "Une grande salle à manger avec une table et des chaises.", items[12:14]),
    "salle_de_billard": Room("Salle de Billard", "Une salle de billard avec une table de billard.", items[14:16]),
    "veranda": Room("Véranda", "Une véranda avec un petit jardin et une table.", items[16:])
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
    elif command == "quit":
        print("Merci d'avoir joué !")
        break
    else:
        print("Commande inconnue.")
