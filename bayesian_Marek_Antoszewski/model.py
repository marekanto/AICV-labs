from pomegranate import *
#************************************
#
#   AI&CV Mateusz Cholewinski
#
#*************************************

# First node
# this node is indpendent for other, thus we are using DiscreteDistribution class
employed = Node(DiscreteDistribution({
    "yes": 0.9,
    "no": 0.1,
}), name="employed")

entrepreneur = Node(DiscreteDistribution({
    "yes": 0.1,
    "no": 0.9,
}), name="entrepreneur")

stationary = Node(ConditionalProbabilityTable([
    ["yes", "yes","yes", 0.98],
    ["yes", "yes","no", 0.02],
    ["yes", "no", "yes", 0.9],
    ["yes", "no","no", 0.1],
    ["no", "yes","yes", 0.99],
    ["no", "yes","no", 0.01],
    ["no", "no","yes", 0],
    ["no", "no","no", 1],
], [employed.distribution,entrepreneur.distribution ]), name="stationary")

online = Node(ConditionalProbabilityTable([
    ["yes", "yes","yes", 0.02],
    ["yes", "yes","no", 0.98],
    ["yes", "no", "yes", 0.1],
    ["yes", "no","no", 0.9],
    ["no", "yes","yes", 0.01],
    ["no", "yes","no", 0.99],
    ["no", "no","yes", 0],
    ["no", "no","no", 1],
], [employed.distribution,entrepreneur.distribution ]), name="online")

covid = Node(ConditionalProbabilityTable([
    ["yes", "yes","yes", 0.15],
    ["yes", "yes","no", 0.85],
    ["yes", "no", "yes", 0.05],
    ["yes", "no","no", 0.95],
    ["no", "yes","yes", 0.1],
    ["no", "yes","no", 0.9],
    ["no", "no","yes", 0],
    ["no", "no","no", 1],
], [stationary.distribution,online.distribution ]), name="covid")

it = Node(ConditionalProbabilityTable([
    ["yes", "yes", 0.04],
    ["yes","no", 0.96],
    ["no", "yes", 0.03],
    ["no", "no", 0.97],
], [covid.distribution]), name="it")

research = Node(ConditionalProbabilityTable([
    ["yes", "yes", 0.05],
    ["yes","no", 0.95],
    ["no", "yes", 0.05],
    ["no", "no", 0.95],
], [covid.distribution]), name="research")

commerce = Node(ConditionalProbabilityTable([
    ["yes", "yes", 0.04],
    ["yes","no", 0.96],
    ["no", "yes", 0.01],
    ["no", "no", 0.99],
], [covid.distribution]), name="commerce")

rich = Node(ConditionalProbabilityTable([
    ["yes", "yes","yes","yes", 0.15],
    ["yes", "yes","no", "yes",0.85],
    ["yes", "no", "yes","yes", 0.05],
    ["yes", "no","no","yes", 0.95],
    ["yes", "yes","yes","no",0.15],
    ["yes", "yes","no","no", 0.85],
    ["yes", "no", "yes","no", 0.05],
    ["yes", "no","no","no", 0.95],
    ["no", "yes","yes","yes", 0.1],
    ["no", "yes","no","yes", 0.9],
    ["no", "no","yes","yes", 0],
    ["no", "no","no","yes", 1],
    ["no", "yes","yes","no", 0.1],
    ["no", "yes","no","no", 0.9],
    ["no", "no","yes","no", 0],
    ["no", "no","no","no", 1],
], [it.distribution,research.distribution,commerce.distribution ]), name="rich")


# Create a Bayesian Network and add states
universe = BayesianNetwork()
universe.add_states(employed, entrepreneur, stationary, online, covid, it, research,commerce,rich)

# Add edges connecting nodes
universe.add_edge(stationary, employed)
universe.add_edge(stationary, entrepreneur)
universe.add_edge(online, employed)
universe.add_edge(online, entrepreneur)
universe.add_edge(covid, stationary)
universe.add_edge(covid, online)
universe.add_edge(it, covid)
universe.add_edge(research, covid)
universe.add_edge(commerce, covid)
universe.add_edge(rich, it)
universe.add_edge(rich, research)
universe.add_edge(rich, commerce)


# Finalize model
universe.bake()