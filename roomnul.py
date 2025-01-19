import random

class Room:
    # Define the constructor. 
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Rester dans la même pièce ou sorties possibles: " 
        for direction, room in self.exits.items():
            if room:
                exit_string += f"{direction}, "
        return exit_string.strip(', ')

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
    
    def add_item(self, item):
        """Ajoute un objet dans la pièce."""
        self.items.append(item)

    def remove_item(self, item):
        """Supprime un objet de la pièce."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def list_items(self):
        if not self.items:
            return "Il n'y a aucun objet ici."
        return "Objets disponibles : " + ", ".join(item.name for item in self.items)
