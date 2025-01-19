# Description: The actions module.
from roomnul import Room
from playernul import Player
from commandenul import Command
from itemnul import Item
import random

# Messages d'erreur.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def history(game, list_of_words, number_of_parameters):
        """Affiche l'historique des pièces visitées par le joueur."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        print("\nHistorique des pièces visitées :")
        if player.history:
            for room in player.history:
                print(f" - {room.name}")
        else:
            print("Aucune pièce visitée.")
        return True

    def rester(game, list_of_words, number_of_parameters):
        """Rester dans la même pièce pour effectuer une hypothèse."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        player = game.player
        print("\nVous restez dans la même pièce.")
        player.stay()
        return True

    def go(game, list_of_words, number_of_parameters):
        """Déplace le joueur dans la direction spécifiée."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1]
        player = game.player
        return player.move(direction)

    def look(game, list_of_words, number_of_parameters):
        """Affiche les informations sur la pièce actuelle et les objets présents."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
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
        return True

    def take(game, list_of_words, number_of_parameters):
        """Permet au joueur de prendre un objet dans la pièce actuelle."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        item = next((i for i in current_room.items if i.name.lower() == item_name.lower()), None)
        if item:
            player.take_item(item)
            current_room.items.remove(item)
            print(f"Vous avez pris {item.name}.")
            return True
        else:
            print(f"L'objet '{item_name}' n'est pas dans cette pièce.")
            return False

    def drop(game, list_of_words, number_of_parameters):
        """Permet au joueur de déposer un objet de son inventaire dans la pièce actuelle."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        item = next((i for i in player.inventory if i.name.lower() == item_name.lower()), None)
        if item:
            player.drop_item(item)
            current_room.items.append(item)
            print(f"Vous avez déposé {item.name}.")
            return True
        else:
            print(f"Vous ne possédez pas '{item_name}'.")
            return False

    def check(game, list_of_words, number_of_parameters):
        """Affiche l'inventaire du joueur."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        player.check_inventory()
        return True

    def quit(game, list_of_words, number_of_parameters):
        """Quitte le jeu."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        print(f"\nMerci {player.name} d'avoir joué. Au revoir.")
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """Affiche les commandes disponibles."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print("\nVoici les commandes disponibles :")
        for command in game.commands.values():
            print(f"- {command}")
        return True

# Mise à jour des objets pour les pièces
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

def assign_items_to_rooms(rooms):
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

    for room in rooms:
        room.items = room_items.get(room.name.lower(), [])