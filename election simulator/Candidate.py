import Ballot as bal
from collections import deque

class Candidate:
    def __init__(self, name):
        self._name = name
        self._ballots = deque()

    def get_name(self):
        return self._name

    def add_ballot(self, ballot):
        self._ballots.append(ballot)

    def get_ballots(self):
        return self._ballots

    def num_votes(self):
        return len(self._ballots)

    def __eq__(self, other):
        return self._name == other._name

    def __str__(self):
        return "Candidate Name: {}\nNumber of Votes: {}\n".format(self._name, self.num_votes())


     
