import csv
import itertools
import numpy
from sys import argv


# def printTable():
#     for i in range(N):
#         for j in range(N):
#             print(f"{TABLE[i][j]:<4}", end=" ")
#         print()


# def printEffectivenessFromConsoleInput():
#     if len(argv) <= 1:
#         return

#     superEffective = set()
#     notSuperEffective = set(TYPES)

#     for i in range(1, len(argv)):
#         if argv[i] not in TYPES:
#             return print(f"There is no pokemon with type of {argv[i]}")

#         index = TYPES.index(argv[i])
#         for j in range(N):
#             if TABLE[index][j] == 2:
#                 superEffective.add(TYPES[j])
#                 if TYPES[j] in notSuperEffective:
#                     notSuperEffective.remove(TYPES[j])

#     print("Your team is super effective against:\n", ", ".join(superEffective))
#     print("\nYour team is NOT super effective against:\n",
#           ", ".join(notSuperEffective))


# def findMostEffectiveTeams(minimumCouters=N, excludedAllies=(), excludedEnemies=()):
#     allySet = set(TYPES) - set(excludedAllies)
#     enemySet = set(TYPES) - set(excludedEnemies)

#     subsets = list(itertools.combinations(allySet, 6))

#     answers = dict()

#     for subset in subsets:
#         group = set()
#         for type in subset:
#             indexOfType = TYPES.index(type)
#             for opponentIndex in range(N):
#                 attackMultiplier = TABLE[indexOfType][opponentIndex]
#                 if attackMultiplier == 2 and TYPES[opponentIndex] in enemySet:
#                     group.add(TYPES[opponentIndex])

#         if group == enemySet:
#             answers[subset] = group

#     file = open("results.txt", "w")
#     for answer in answers:
#         # print(f"Team of types: {', '.join(answer)}")
#         # if minimumCouters == N:
#         #     print("Is super effective against ALL other types")
#         # else:
#         #     print(
#         #         f"Is super effective against types: {', '.join(answers[answer])}")
#         # print("----------------------------------------")

#         file.write(' '.join(answer)+"\n")

#     file.close()


# def whatTypesAreEffectiveAgainst(enemyType):
#     enemyTypeIndex = TYPES.index(enemyType)
#     resultSet = set()

#     for i in range(N):
#         attackMultiplier = TABLE[i][enemyTypeIndex]
#         if (attackMultiplier == 2):
#             resultSet.add(TYPES[i])

#     print(" ".join(resultSet))


# # printEffectivenessFromConsoleInput()

# # excludedAllies = ("fairy", "normal",
# #                   "dark", "ghost", "dragon")
# # excludedEnemies = ("fairy", "ghost")

# # findMostEffectiveTeams(N - len(excludedEnemies),
# #                        excludedAllies, excludedEnemies)

# # whatTypesAreEffectiveAgainst(argv[1])
# file = open("pokemon.csv", encoding="utf8")

# csvreader = csv.reader(file)

# header = []
# header = next(csvreader)

# pokemonInfo = dict()
# for row in csvreader:
#     nameColId = header.index("name")
#     type1ColId = header.index("type1")
#     type2ColId = header.index("type2")

#     pokemonName = row[nameColId]
#     pokemonInfo[pokemonName] = [row[type1ColId], row[type2ColId]
#                                 ] if row[type2ColId] else [row[type1ColId]]

# print(pokemonInfo)
# file.close()

from PokeHelper import PokeHelper


def main():
    helper = PokeHelper()

    if len(argv) < 3:
        return

    if argv[1].lower() == "gpt":
        name = argv[2]
        try:
            types = helper.getPokemonTypes(name)
        except:
            print(f"Error!!! There is no pokemon with the name of {name}")
        else:
            print(f"{name} has types of: {types}")

    elif argv[1].lower() == "gps":
        name = argv[2]
        try:
            types = helper.getPokemonStrengths(name)
        except:
            print(f"Error!!! There is no pokemon with the name of {name}")
        else:
            print(f"{name} is super effective against types of: {', '.join(types)}")

    elif argv[1].lower() == "gpw":
        name = argv[2]
        try:
            types = helper.getPokemonWeaknesses(name)
        except:
            print(f"Error!!! There is no pokemon with the name of {name}")
        else:
            print(f"{name} is not effective types of: {', '.join(types)}")

    elif argv[1].lower() == "gpv":
        name = argv[2]
        try:
            types = helper.getPokemonVulnerabilities(name)
        except:
            print(f"Error!!! There is no pokemon with the name of {name}")
        else:
            print(
                f"{name} is vulnerable against pokemon with types of: {', '.join(types)}")


main()
