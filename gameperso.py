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
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        
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

        cuisine.exits = {"N" : None, "E" : grand_salon, "S" : salle_à_manger, "O" : None, "passage_secret" : bureau}  
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
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
