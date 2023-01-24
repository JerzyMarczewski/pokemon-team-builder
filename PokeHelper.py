import csv
import sys


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

                pokemonName = row[nameColId]
                pokemonInfo[pokemonName] = [row[type1ColId], row[type2ColId]
                                            ] if row[type2ColId] else [row[type1ColId]]

            file.close()
        except:
            print("ERROR!!!")
            sys.exit()

    def getPokemonTypes(self, name):
        if self.pokemonInfo[name] == None:
            print(f"Error!!! There is no pokemon with the name of {name}")
            return

        return self.pokemonInfo[name]
