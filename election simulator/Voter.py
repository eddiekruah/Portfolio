class Voter:
    def __init__(self, name):
        self._name = name;
        self._ranked_candidates = []

    def get_name(self):
        return self._name

    def vote(self, ballot, ranking):
        ballot.rank_candidates(ranking)
        self._ranked_candidates = ballot.get_candidates();
        return ballot;   # return is not necessary, added for clarity

if __name__ == "__main__":
    import Ballot as bal
    import Candidate as can

    name = "V"
    voter = Voter(name);
    candidate_names = ["A", "B", "C", "D"];
    candidates = [can.Candidate(name) for name in candidate_names]

    ballot = bal.Ballot(voter, candidates);
    voter.vote(ballot, [3, 2, 1, 0]);
    print(ballot)

    ballot.remove_candidate(candidates[2])

    print(ballot)

