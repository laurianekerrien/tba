import random

class Room:
    def __init__(self, name):
        """
        Initialise une pièce.
        
        :param name: Nom de la pièce.
        """
        self.name = name
        self.adjacent_rooms = []

    def add_adjacent(self, *rooms):
        """
        Ajoute des pièces adjacentes.
        
        :param rooms: Liste des pièces adjacentes.
        """
        self.adjacent_rooms.extend(rooms)

    def __str__(self):
        return self.name


class GameMaster:
    def __init__(self, name, room):
        """
        Initialise le maître du jeu (PNJ).
        
        :param name: Nom du maître du jeu.
        :param room: Pièce où il commence.
        """
        self.name = name
        self.room = room
        self.messages = [
            "Bienvenue dans ce manoir mystérieux.",
            "Vous devez résoudre le mystère du crime.",
            "Mais attention, les apparences sont trompeuses.",
            "Je ne vous donnerai que des hypothèses fausses, à vous de faire le tri !"
        ]

    def move(self):
        """
        Déplace le maître du jeu aléatoirement dans une pièce adjacente.
        
        :return: True si le PNJ s'est déplacé, False sinon.
        """
        if random.choice([True, False]):  # 1 chance sur 2 de bouger
            self.room = random.choice(self.room.adjacent_rooms)
            return True
        return False

    def get_msg(self):
        """
        Retourne et supprime un message du PNJ.
        
        :return: Un message du PNJ.
        """
        if self.messages:
            return self.messages.pop(0)
        return "Je n'ai plus rien à dire pour le moment."

    def __str__(self):
        """
        Retourne une description du PNJ.
        """
        return f"{self.name}, actuellement dans {self.room}."

    def talk(self):
        """
        Parle au joueur en affichant un message cyclique.
        """
        print(f"{self.name} : {self.get_msg()}")


# Jeu principal
def main():
    # Création des pièces
    salon = Room("Salon")
    cuisine = Room("Cuisine")
    bibliotheque = Room("Bibliothèque")
    salle_manger = Room("Salle à manger")
    hall = Room("Hall")

    # Définition des pièces adjacentes selon la carte
    salon.add_adjacent(cuisine, hall)
    cuisine.add_adjacent(salon, salle_manger)
    salle_manger.add_adjacent(cuisine, hall)
    hall.add_adjacent(salon, salle_manger, bibliotheque)
    bibliotheque.add_adjacent(hall)

    # Création de Monsieur Taupe
    monsieur_taupe = GameMaster(name="Monsieur Taupe", room=salon)

    # Introduction du jeu
    print("""
**************************************************
          BIENVENUE DANS LE JEU CLUEDO
**************************************************

Une scène de crime abominable s'est déroulée dans ce manoir. Une personne a été retrouvée morte dans des circonstances atroces. 
Votre mission : identifier le coupable, l'arme du crime et la pièce où cela s'est produit. Mais attention, 
vous serez guidé par le mystérieux et rusé Monsieur Taupe, le maître du jeu. 

**************************************************
""")
    print(monsieur_taupe)

    # Boucle de jeu
    while True:
        print("\nQue voulez-vous faire ?")
        print("1. Demander une hypothèse à Monsieur Taupe")
        print("2. Parler à Monsieur Taupe")
        print("3. Observer la position de Monsieur Taupe")
        print("4. Fin du tour")
        print("5. Quitter le jeu")
        choice = input("> ")

        if choice == "1":
            print(f"\n{monsieur_taupe.name} dit : Je pense que c'était {random.choice(['Colonel Moutarde', 'Madame Pervenche', 'Professeur Violet'])} avec le {random.choice(['Revolver', 'Poignard', 'Chandelier'])} dans {random.choice(['Cuisine', 'Salon', 'Salle à manger'])}.")
        elif choice == "2":
            monsieur_taupe.talk()
        elif choice == "3":
            print(monsieur_taupe)
        elif choice == "4":
            moved = monsieur_taupe.move()
            if moved:
                print(f"{monsieur_taupe.name} s'est déplacé dans {monsieur_taupe.room}.")
            else:
                print(f"{monsieur_taupe.name} est resté dans {monsieur_taupe.room}.")
        elif choice == "5":
            print("\nMerci d'avoir joué ! Le mystère reste entier... À bientôt.")
            break
        else:
            print("\nChoix invalide. Veuillez entrer un nombre entre 1 et 5.")

# Exécution du jeu
if __name__ == "__main__":
    main()
