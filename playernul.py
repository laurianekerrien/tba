#Define_the_Player_class

class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None
        self.history=[]
        self.cards = []

    def stay(self):
        print(self.current_room.get_long_description())
    # Define the historique method.
    def get_history(self):
        """Ajoute la pièce actuelle à l'historique si ce n'est pas la dernière visitée."""
        if not self.history or self.history[-1] != self.current_room:
            self.history.append(self.current_room)

    def check_inventory(self):
        """Affiche l'inventaire du joueur."""
        if not self.inventory:
            print("Votre inventaire est vide.")
        else:
            print("Votre inventaire contient :")
            for item in self.inventory:
                print(f"- {item.name}")

    def look(self):
        current_room = self.player.current_room
        print(current_room.description)
        print(current_room.list_items())
        """Affiche la description de la pièce actuelle et les objets présents."""
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
        """Prend un objet de la pièce actuelle et l'ajoute à l'inventaire."""
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"Vous avez pris : {item.name}")
                return
        print(f"L'objet '{item_name}' n'est pas dans cette pièce.")

    def drop(self, item_name):
        """Repose un objet de l'inventaire dans la pièce actuelle."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.current_room.items.append(item)
                self.inventory.remove(item)
                print(f"Vous avez déposé : {item.name}")
                return
        print(f"Vous ne possédez pas l'objet '{item_name}'.")


    def take_item(self, item):
        """Ajoute un objet à l'inventaire du joueur."""
        self.inventory.append(item)

    def drop_item(self, item):
        """Supprime un objet de l'inventaire."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def __str__(self):
        items = ', '.join([item.name for item in self.inventory]) or "Aucun objet"
        return f"Joueur: {self.name}, Inventaire: {items}"
            
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        dico={"N": ["N",'n', "nord","Nord", "NORD","Haut","haut",'HAUT','H',"h" ], "S": ['SUD', 'Sud', 'sud', 'su', 's', 'S', 'bas', 'Bas', 'BAS','b', 'B'],"O": ['OUEST', 'Ouest', 'ouest','O','o','gauche', 'Gauche','GAUCHE', "g", "G" ],"E": ['EST', 'Est', 'est','E','e','droite', 'Droite','DROITE', "d", "D" ], 'passage_secret': ["passage_secret", "Passage_secret", 'PASSAGE_SECRET','passage secret', 'Passage secret','PASSAGE SECRET','PS', 'ps', 'Ps' ]}
        
        # On cherche la clé correspondant à la direction
        next_room = None
        for key, directions in dico.items():
            if direction in directions:
                # Trouver la direction correspondante et récupérer la salle suivante
                direction = key  # Mettre la clé correspondante de la direction
                next_room = self.current_room.exits.get(direction)  # Récupérer la salle correspondante
                break
       
        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            """
            permet de bouger le personnage dans une direction donnée

            attributs: name, current_room

            méthodes: __init__,move

            Args:
            direction (str): La direction dans laquelle le joueur souhaite se déplacer 
                             (par exemple, "nord", "sud", "est", "ouest").

            Returns:
                bool: True si le joueur a été déplacé avec succès, False sinon.


            doctest: 
            >>> player = Player("Aventurier")
            >>> room1 = Room("Salle 1", "la cuisine")
            >>> room2 = Room("Salle 2", "la bibliothèque")
            >>> room1.exits = {"nord": room2, "sud": None}
            >>> room2.exits = {"sud": room1}
            >>> player.current_room = room1
            >>> player.move("nord")
            la bibliothèque
            True
            >>> player.move("sud")
            la cuisine.
            True
            >>> player.move("ouest")
            \nAucune porte dans cette direction !\n
            False

            """
            return False
        
        # Set the current room to the next room.
        
        self.current_room = next_room
        self.get_history()
        print(self.current_room.get_long_description())
        return True
    
