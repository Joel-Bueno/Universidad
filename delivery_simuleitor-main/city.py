class City:
    def __init__(self, name: str):
        self.name = name.strip()

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()