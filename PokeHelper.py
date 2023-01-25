import csv
import sys
from typesTable import TYPES, TABLE
from Errors import BadTypeNameError, BadPokemonNameError


class PokeHelper(object):
    def __init__(self):
        try:
            file = open("pokemon.csv", encoding="utf8")

            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)

            self.team = []
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

    def setTeam(self, names):
        if len(names) == 0:
            return

        if len(names) > 6:
            print("Error!!! You can only have 6 pokemon on your team")
            return

        try:
            loweredNames = [value.lower() for value in names]
            for name in loweredNames:
                if name not in self.pokemonInfo.keys():
                    raise ValueError
                elif name not in self.team:
                    self.team.append(name)
        except:
            print("Error!!! All arguments must be viable pokemon names")
        else:
            print(self.team)

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

    def getPokemonVulnerabilities(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise ValueError

        result = set()
        types = self.pokemonInfo[name.lower()]
        if len(types) == 1:
            typeId = TYPES.index(types[0])
            for rowId in range(len(TABLE)):
                attackMul = TABLE[rowId][typeId]
                if attackMul == 2:
                    result.add(TYPES[rowId])

        elif len(types) == 2:
            mulByType = dict()
            type1Id = TYPES.index(types[0])
            type2Id = TYPES.index(types[1])

            for rowId in range(len(TABLE)):
                attackMul = TABLE[rowId][type1Id] * TABLE[rowId][type2Id]
                if attackMul >= 2:
                    result.add(TYPES[rowId])
                    mulByType[TYPES[rowId]] = attackMul

            sortedResult = sorted(mulByType.items(),
                                  key=lambda item: item[1], reverse=True)
            print(sortedResult)

        return result

    def getAttackMultiplier(self, attackType, enemyPokemonName):
        if attackType not in TYPES:
            raise BadTypeNameError(attackType)

        loweredName = enemyPokemonName.lower()
        if loweredName not in self.pokemonInfo.keys():
            raise BadPokemonNameError(loweredName)

        attackTypeId = TYPES.index(attackType)
        mul = 1

        enemyTypes = self.pokemonInfo[loweredName]
        for enemyType in enemyTypes:
            enemyTypeId = TYPES.index(enemyType)
            mul *= TABLE[attackTypeId][enemyTypeId]

        return mul
