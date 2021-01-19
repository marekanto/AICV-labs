from model import universe

getProbability = universe.probability([["yes", "no", "yes", "yes", "yes","yes","yes", "yes","yes"]])

print(getProbability)


getProbability = universe.probability([["no", "no", "yes", "yes", "yes","yes","yes", "yes","yes"]])

print(getProbability)