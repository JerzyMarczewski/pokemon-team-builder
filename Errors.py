class NotEnoughtArgumentsError(Exception):
    def __init__(self, command):
        self.command = command


class BadTypeNameError(Exception):
    def __init__(self, givenType):
        self.type = givenType


class BadPokemonNameError(Exception):
    def __init__(self, name):
        self.name = name
