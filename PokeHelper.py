import csv
import sys
from typesTable import TYPES, TABLE
from Errors import BadTypeNameError, BadPokemonNameError


class PokeHelper(object):
    def __init__(self):
        self.team = []
        self.pokemonInfo = dict()

        try:
            file = open("pokemon.csv", encoding="utf8")

            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)

            for row in csvreader:
                nameColId = header.index("name")
                type1ColId = header.index("type1")
                type2ColId = header.index("type2")

                pokemonName = row[nameColId].lower()
                self.pokemonInfo[pokemonName] = [row[type1ColId], row[type2ColId]
                                                 ] if row[type2ColId] else [row[type1ColId]]

            file.close()
        except:
            print("ERROR!!! Couldn't read information from pokemon.csv")
            sys.exit()

        try:
            teamFile = open("team.txt", "r")
            text = teamFile.readline()
            self.setTeam(text.split(), True)
            teamFile.close()
        except:
            print("ERROR!!! Couldn't read information from team.txt")
            sys.exit()

    def setTeam(self, names, load=False):
        if len(names) == 0:
            return

        if len(names) > 6:
            print("Error!!! You can only have 6 pokemon on your team")
            return

        temp = []

        try:
            loweredNames = [value.lower() for value in names]
            for name in loweredNames:
                if name.lower() not in self.pokemonInfo.keys():
                    raise BadPokemonNameError(name.lower())
                elif name not in temp:
                    temp.append(name)

            self.team = temp
            with open("team.txt", "w") as file:
                file.write(" ".join(self.team))
        except BadPokemonNameError:
            print("Error!!! All arguments must be viable pokemon names")
        else:
            if load:
                print(f"Loaded team: {', '.join(self.team)}")
            else:
                print(f"Team set to: {', '.join(self.team)}")

    def findMostEffectiveTeamMember(self, enemyPokemon):
        if len(self.team) == 0:
            print("Warning!!! You have no pokemon in your team")
            return None

        mulsAgainstEnemy = self.getAllAttacksMultipliers(enemyPokemon)

        statsDict = dict()

        for member in self.team:
            allyAttackTypes = self.getPokemonTypes(member)
            enemyAttackTypes = self.getPokemonTypes(enemyPokemon)

            if len(allyAttackTypes) == 2:
                allyMul1 = mulsAgainstEnemy[allyAttackTypes[0]]
                allyMul2 = mulsAgainstEnemy[allyAttackTypes[1]]
                if max(allyMul1, allyMul2) == allyMul1:
                    maxAllyMul = allyMul1
                    allyBestAttackType = allyAttackTypes[0]
                else:
                    maxAllyMul = allyMul2
                    allyBestAttackType = allyAttackTypes[1]
            else:
                maxAllyMul = mulsAgainstEnemy[allyAttackTypes[0]]
                allyBestAttackType = allyAttackTypes[0]

            if len(enemyAttackTypes) == 2:
                enemyMul1 = self.getAttackMultiplier(
                    enemyAttackTypes[0], member)
                enemyMul2 = self.getAttackMultiplier(
                    enemyAttackTypes[1], member)
                maxEnemyMul = max(enemyMul1, enemyMul2)
            else:
                maxEnemyMul = self.getAttackMultiplier(
                    enemyAttackTypes[0], member)

            ratio = maxAllyMul / \
                maxEnemyMul if maxEnemyMul != 0 else float('inf')
            # print(
            #     f"{member} - {allyBestAttackType} | {maxAllyMul} | {maxEnemyMul} | ratio: {maxAllyMul/maxEnemyMul}")
            statsDict[member] = [allyBestAttackType, ratio]

        sortedDict = sorted(statsDict.items(),
                            key=lambda item: item[1][1], reverse=True)
        # for stat in statsDict:
        print(sortedDict)

    def getPokemonTypes(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise BadPokemonNameError(name.lower())

        return self.pokemonInfo[name.lower()]

    def getPokemonStrengths(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise BadPokemonNameError(name.lower())

        result = set()
        for type in self.pokemonInfo[name.lower()]:
            typeId = TYPES.index(type)
            for col, attackMul in enumerate(TABLE[typeId]):
                if attackMul == 2:
                    result.add(TYPES[col])

        return result

    def getPokemonWeaknesses(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise BadPokemonNameError(name.lower())

        result = set()
        for type in self.pokemonInfo[name.lower()]:
            typeId = TYPES.index(type)
            for col, attackMul in enumerate(TABLE[typeId]):
                if attackMul == 0.5 or attackMul == 0:
                    result.add(TYPES[col])

        return result

    def getPokemonVulnerabilities(self, name):
        if name.lower() not in self.pokemonInfo.keys():
            raise BadPokemonNameError(name.lower())

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

    def getAllAttacksMultipliers(self, enemyPokemonName):
        loweredName = enemyPokemonName.lower()
        if loweredName not in self.pokemonInfo.keys():
            raise BadPokemonNameError(loweredName)

        mulDict = dict()
        enemyTypes = self.pokemonInfo[loweredName]

        for attackTypeId, attackType in enumerate(TYPES):
            mul = 1
            for enemyType in enemyTypes:
                enemyTypeId = TYPES.index(enemyType)
                mul *= TABLE[attackTypeId][enemyTypeId]

            mulDict[attackType] = mul

        sortedMulDict = dict(
            sorted(mulDict.items(), key=lambda item: item[1], reverse=True))
        return sortedMulDict
