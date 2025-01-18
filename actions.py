# Description: The actions module.
from room import Room
from player import Player
from command import Command
from charactere import GameMaster
import random
# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces visitées par le joueur.

        Args:
            game (Game): L'objet du jeu.
            list_of_words (list): La liste des mots dans la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Returns:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Affiche l'historique du joueur.
        player = game.player
        print("\nHistorique des pièces visitées :")
        if player.history:
            for room in player.history:
                print(f" - {room.name}")
        else:
            print("Aucune pièce visitée.")
        print()
        return True

    def rester(game, list_of_words, number_of_parameters):
        """
        vous rester dans la même pièce pour effectuer une autre hypothèse

        """
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVous restez dans la même pièce pour effectuer une autre hypothèse")
        print()
        
        player.stay()
        return True

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True
    

    def look(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # Vérifiez le nombre de paramètres.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        current_room = game.player.current_room
        print(f"Vous êtes dans : {current_room.name}")
        print(current_room.description)

        if current_room.items:
            print("Objets dans la pièce :")
            for item in current_room.items:
                print(f"- {item.name}")
        else:
            print("Il n'y a pas d'objets dans cette pièce.")
    
    
    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # Vérifiez le nombre de paramètres.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Obtenez l'objet mentionné.
        item_to_take = list_of_words[1]
        player = game.player
        current_room = player.room

        # Vérifiez si l'objet est dans la pièce.
        if item_to_take in current_room.items:
            current_room.items.remove(item_to_take)
            player.inventory.append(item_to_take)
            print(f"Vous avez pris {item_to_take}.")
            return True
        else:
            print(f"{item_to_take} n'est pas ici.")
            return False
        

    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        # Obtenez l'objet mentionné.
        item_to_drop = list_of_words[1]

        # Obtenez le joueur et la pièce actuelle.
        player = game.player
        current_room = player.room

        # Vérifiez si l'objet est dans l'inventaire du joueur.
        if item_to_drop in player.inventory:
            player.inventory.remove(item_to_drop)
            current_room.items.append(item_to_drop)
            print(f"Vous avez déposé {item_to_drop}.")
            return True
        else:
            print(f"Vous ne possédez pas {item_to_drop}.")
            return False

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True