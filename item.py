
class Item:
    def __init__(self, name, description):
        """
        Initialise un objet avec un nom et une description.
        :param name: Nom de l'objet
        :param description: Description de l'objet
        """
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"