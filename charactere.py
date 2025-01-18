
import random
from room import Room

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
        self.weapons = ["Revolver", "Poignard", "Chandelier", "Corde", "Clé anglaise", "Tuyau de plomb"]
        self.rooms = ["Cuisine", "Salon", "Salle à manger", "Bibliothèque", "Bureau"]
        self.characteres = ["Professeur_Violet", "Colonel_Moutarde", "Mademoiselle_Rose", "Madame_Leblanc", "Docteur_Olive", "Madame_Pervenche"]

    def move(self):
        """Déplace le maître du jeu aléatoirement dans une pièce adjacente."""
        if random.choice([True, False]):
            self.room = random.choice(list(self.room.exits.values()))
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
        print(f"{self.name} propose une hypothèse fausse :")
        print(f"Je pense que c'était {random.choice(['Colonel Moutarde', 'Madame Pervenche', 'Professeur Violet'])} avec le {random.choice(self.weapons)} dans {random.choice(self.rooms)}.")
