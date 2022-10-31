import Ballot as bal
import Candidate as can
import Voter as vot
import copy
import random

class PollingStation:
    def __init__(self, candidates):
        self._candidates = candidates;
        self._ballots = []

        self._surv_candidates = None
        self._ballots_of_surv_candidates = None

    def get_surv_candidates(self):
        return self._surv_candidates

    def get_num_surv_candidates(self):
        return len(self._surv_candidates);

    def process_voter(self, voter, ranking = None):
        # We give the voter a ballot
        ballot = bal.Ballot(voter, self._candidates)
        # The voter chooses their ranking of candidates
        n = len(self._candidates)
        if (ranking is None):
            ranking = list(range(n))
            random.shuffle(ranking)

        # The voter casts the vote
        voter.vote(ballot, ranking)
        self._ballots.append(ballot)

    def tabulate_votes(self):
        for ballot in self._ballots:
            candidate = ballot.peek_top();
            if (candidate is not None):
                candidate.add_ballot(ballot);

        # Now that all ballots are collected, sort the candidates on the number
        # of votes they've gotten
        my_key = lambda c: c.num_votes();
        self._candidates.sort(key = my_key, reverse = True)

        # We will work on viable candidates only and preserve the original
        # state of voting in self._candidates & self._ballots
        self._surv_candidates = copy.copy(self._candidates)
        self._ballots_of_surv_candidates  = copy.copy(self._ballots)

    def candidate_has_super_majority(self):
        num_all_votes = sum(c.num_votes() for c in self._candidates)
        if (num_all_votes == 0):
            raise ValueError("You are asking for a candidate with a "
                             "super-majority, but no voting has taken "
                             "place yet.")
        return ((self._candidates[0].num_votes()/num_all_votes) >= 0.5 )

    def remove_last_and_reasign_votes(self):
        # 1) find the candidate with the minimal number of votes
        c_min = self._surv_candidates.pop();

        if (c_min.num_votes() == 0):
            # We've just removed that candidate; no ballots, nothing to do
            return


        # 2) go through the list self._ballots_of_surv_candidates
        #    and remove the c_min candidate with minimal number of votes
        [b.remove_candidate(c_min) for b in self._ballots_of_surv_candidates]

        # 3) Candidate c_min has been pruned from self._ballots_of_viable_candidates
        #    Let's apportion her votes (still present in c_min._ballots) to the other
        #    candidates
        for ballot in c_min.get_ballots():
            second_choice_candidate = ballot.peek_top() # c_min was on top but was removed
            idx = self._surv_candidates.index(second_choice_candidate)
            self._surv_candidates[idx].add_ballot(ballot);

        my_key = lambda c: c.num_votes()
        self._surv_candidates.sort(key=my_key, reverse=True)

    def __str__(self):
        # Print candidates and their vote numbers
        out_str = "Number of votes per candidate:\n"
        for i, c in enumerate(self._surv_candidates):
            out_str += str(i) +". " + c.get_name() + " " + str(c.num_votes()) + "\n"

        return out_str

if __name__ == "__main__":
    random.seed(1)
    candidate_names = ["A", "B", "C", "D"]
    voter_names = ["a", "b", "c", "d", "e"]

    candidates = [can.Candidate(name) for name in candidate_names]
    voters = [vot.Voter(name) for name in voter_names]

    polling_station = PollingStation(candidates)

    """
    Let's start voting!
    """
    for voter in voters:
        polling_station.process_voter(voter)

    polling_station.tabulate_votes()

    print(polling_station)

