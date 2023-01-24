import csv
import sys
from typesTable import TYPES, TABLE


class PokeHelper(object):
    def __init__(self):
        try:
            file = open("pokemon.csv", encoding="utf8")

            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)

            self.pokemonInfo = dict()
            for row in csvreader:
                nameColId = header.index("name")
                type1ColId = header.index("type1")
                type2ColId = header.index("type2")

                pokemonName = row[nameColId].lower()
                self.pokemonInfo[pokemonName] = [row[type1ColId], row[type2ColId]
                                                 ] if row[type2ColId] else [row[type1ColId]]

            file.close()
        except:
            print("ERROR!!!")
            sys.exit()

    def getPokemonTypes(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise ValueError

        return self.pokemonInfo[name.lower()]

    def getPokemonStrengths(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise ValueError

        result = set()
        for type in self.pokemonInfo[name.lower()]:
            typeId = TYPES.index(type)
            for col, attackMul in enumerate(TABLE[typeId]):
                if attackMul == 2:
                    result.add(TYPES[col])

        return result

    def getPokemonWeaknesses(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise ValueError

        result = set()
        for type in self.pokemonInfo[name.lower()]:
            typeId = TYPES.index(type)
            for col, attackMul in enumerate(TABLE[typeId]):
                if attackMul == 0.5 or attackMul == 0:
                    result.add(TYPES[col])

        return result
