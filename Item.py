
class Item:
    def __init__(self):
        self.name = ""
        self.cost = 0

    def __str__(self):
        return f"[Item: {self.name}, Cost: {self.cost}]"