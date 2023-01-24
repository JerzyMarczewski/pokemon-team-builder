import itertools
import numpy
from sys import argv

TYPES = ("normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
         "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy")

N = len(TYPES)

TABLE = ((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1),
         (1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1),
         (1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1),
         (1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1),
         (1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 2,
          0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1),
         (1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1),
         (2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5),
         (1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2),
         (1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1),
         (1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1),
         (1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1),
         (1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5),
         (1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1),
         (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1),
         (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0),
         (1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5),
         (1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2),
         (1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1)
         )


def printTable():
    for i in range(N):
        for j in range(N):
            print(f"{TABLE[i][j]:<4}", end=" ")
        print()


def printEffectivenessFromConsoleInput():
    if len(argv) <= 1:
        return

    superEffective = set()
    notSuperEffective = set(TYPES)

    for i in range(1, len(argv)):
        if argv[i] not in TYPES:
            return print(f"There is no pokemon with type of {argv[i]}")

        index = TYPES.index(argv[i])
        for j in range(N):
            if TABLE[index][j] == 2:
                superEffective.add(TYPES[j])
                if TYPES[j] in notSuperEffective:
                    notSuperEffective.remove(TYPES[j])

    print("Your team is super effective against:\n", ", ".join(superEffective))
    print("\nYour team is NOT super effective against:\n",
          ", ".join(notSuperEffective))


def findMostEffectiveTeams(minimumCouters=N):
    typeSet = set(TYPES)
    subsets = list(itertools.combinations(typeSet, 6))

    answers = dict()

    for subset in subsets:
        group = set()
        for type in subset:
            indexOfType = TYPES.index(type)
            for opponentIndex in range(N):
                attackMultiplier = TABLE[indexOfType][opponentIndex]
                if attackMultiplier == 2:
                    group.add(TYPES[opponentIndex])

        if len(group) >= minimumCouters:
            answers[subset] = group

    file = open("results.txt", "w")
    for answer in answers:
        # print(f"Team of types: {', '.join(answer)}")
        # if minimumCouters == N:
        #     print("Is super effective against ALL other types")
        # else:
        #     print(
        #         f"Is super effective against types: {', '.join(answers[answer])}")
        # print("----------------------------------------")

        file.write(', '.join(answer)+"\n")

    file.close()


printEffectivenessFromConsoleInput()
findMostEffectiveTeams()
