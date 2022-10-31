from collections import deque

class Ballot:
    def __init__(self, voter, candidates):
        self._voter = voter
        self._candidates = deque(candidates)
        self._ranking = None

    def get_candidates(self):
        return self._candidates

    def rank_candidates(self, ranking):
        num_can = len(self._candidates);
        if (len(ranking) != num_can):
            raise ValueError("Incorrect ranking given!")

        for i in range(num_can):
            if (not i in ranking):
                raise ValueError("Incorrect ranking given!")

        self._ranking = ranking
        # self._candidates = deque([self._candidates[i] for i in self._ranking])

        orig_candidates_copy = list(self._candidates)
        for i in range(num_can):
            self._candidates[self._ranking[i]] = orig_candidates_copy[i]


    def remove_candidate(self, candidate):
        if (self._ranking == None):
            raise Exception("Cannot remove candidate before ranking.")

        self._candidates.remove(candidate) # The order in deque give us the ranking

    def peek_top(self):
        return self._candidates[0]

    def remove_top(self):
        self._candidates.popleft()

    def __str__(self):
        out_str = "Voter name: {}\n".format(self._voter.get_name()) + \
                  "Voter Ranking:\n";
        for idx, c in enumerate(self._candidates):
            out_str += str(idx) + ". " + c.get_name() + "\n"

        if (self._ranking is not None):
            out_str += "Completed"
        return out_str



