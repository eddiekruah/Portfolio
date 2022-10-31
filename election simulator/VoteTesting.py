import unittest
import random

import Voter as vot
import Ballot as bal
import Candidate as can
import PollingStation as pol

class VoteTesting(unittest.TestCase):

    def test_voter_and_ballot(self):
        name = "V"
        voter = vot.Voter(name);
        self.assertEqual(voter.get_name(), "V")

        candidate_names = ["A", "B", "C"];
        candidates = [can.Candidate(name) for name in candidate_names]
        self.assertEqual(candidates[0].get_name(), "A");
        self.assertEqual(candidates[1].get_name(), "B");
        self.assertEqual(candidates[2].get_name(), "C");

        ballot = bal.Ballot(voter, candidates)
        self.assertEqual(ballot._voter.get_name(), "V");
        self.assertEqual(ballot.get_candidates()[0].get_name(), "A")
        self.assertEqual(ballot.get_candidates()[1].get_name(), "B")
        self.assertEqual(ballot.get_candidates()[2].get_name(), "C")


        with self.assertRaises(ValueError):
             ballot.rank_candidates([1, 0])

        with self.assertRaises(ValueError):
             ballot.rank_candidates([1,1,2])

        ballot.rank_candidates([2, 1, 0])
        self.assertEqual(ballot.get_candidates()[0].get_name(), "C")
        self.assertEqual(ballot.get_candidates()[1].get_name(), "B")
        self.assertEqual(ballot.get_candidates()[2].get_name(), "A")

    def test_voting(self):
        name = "V"
        voter = vot.Voter(name);

        candidate_names = ["A", "B", "C"];
        candidates = [can.Candidate(name) for name in candidate_names]

        ballot = bal.Ballot(voter, candidates);
        voter.vote(ballot, [2, 1, 0]);
        self.assertEqual(ballot.__str__(),
                        "Voter name: V\nVoter Ranking:\n0. C\n1. B\n2. A\nCompleted")

        c2 = candidates[2];
        c2.add_ballot(ballot);
        self.assertEqual(c2.num_votes(), 1)

    def test_remove_candidate_from_ballot(self):
        name = "V"
        voter = vot.Voter(name);
        candidate_names = ["A", "B", "C", "D"];
        candidates = [can.Candidate(name) for name in candidate_names]

        ballot = bal.Ballot(voter, candidates);

        with self.assertRaises(Exception):
             ballot.remove_candidate(candidates[2]) # Only after voting you can remove a condidate
        voter.vote(ballot, [3, 2, 1, 0]);
        ballot.remove_candidate(candidates[2])
        self.assertEqual(ballot.__str__(),
                         "Voter name: V\nVoter Ranking:\n0. D\n1. B\n2. A\nCompleted")

    def test_polling_station_first_round(self):
        random.seed(10)
        candidate_names = ["A", "B", "C", "D"]
        voter_names = ["a", "b", "c", "d", "e"]

        candidates = [can.Candidate(name) for name in candidate_names]
        voters = [vot.Voter(name) for name in voter_names]

        polling_station = pol.PollingStation(candidates)

        """
        Let's start voting!
        """
        for voter in voters:
            polling_station.process_voter(voter) # the ranking (i.e., the second) argument is
                                                 # not provided: the voter will vote
                                                 # randomly

        polling_station.tabulate_votes()
        self.assertEqual(polling_station.__str__(),
                         "Number of votes per candidate:\n0. D 3\n1. B 1\n2. C 1\n3. A 0\n")
        self.assertEqual(polling_station.candidate_has_super_majority(), True)

    def test_polling_station_additional_rounds(self):
        random.seed(1)

        candidate_names = ["A", "B", "C", "D"]
        voter_names = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k", "l"]

        candidates = [can.Candidate(name) for name in candidate_names]
        voters = [vot.Voter(name) for name in voter_names]

        polling_station = pol.PollingStation(candidates)

        """
        Let's start voting!
        """
        for voter in voters:
            polling_station.process_voter(voter) # the ranking (i.e., the second) argument is
                                                 # not provided: the voter will vote
                                                 # randomly

        polling_station.tabulate_votes()

        """
        The candidates now contain all ballots with their names on top
        """

        self.assertEqual(polling_station.candidate_has_super_majority(), False)

        # No candidate has a super-majority. Do the ranking rounds
        while (polling_station.get_num_surv_candidates() > 2):
            polling_station.remove_last_and_reasign_votes()

        # The first of the surviving candidates is a winner. Let's print him
        self.assertEqual(polling_station.get_surv_candidates()[0].__str__(),
                         "Candidate Name: B\nNumber of Votes: 6\n" )

    def test_two_candidates(self):
        candidate_names = ["A", "B"]
        voter_names = ["a", "b", "c", "d"]

        candidates = [can.Candidate(name) for name in candidate_names]
        voters = [vot.Voter(name) for name in voter_names]

        voter_rankings = [[0, 1], [1, 0], [1, 0], [1, 0]]

        polling_station = pol.PollingStation(candidates)


        for idx, voter in enumerate(voters):
            polling_station.process_voter(voter, voter_rankings[idx])

        polling_station.tabulate_votes()

        self.assertEqual(polling_station.candidate_has_super_majority(), True)
        self.assertEqual(polling_station.get_surv_candidates()[0].__str__(),
                         "Candidate Name: B\nNumber of Votes: 3\n")

    def test_three_candidates(self):
        candidate_names = ["A", "B", "C"]
        voter_names = ["a", "b", "c", "d", "e"]

        candidates = [can.Candidate(name) for name in candidate_names]
        voters = [vot.Voter(name) for name in voter_names]

        voter_rankings = [[0, 1, 2], [2, 1, 0], [2, 0, 1], [0, 1, 2], [1, 0, 2]]

        polling_station = pol.PollingStation(candidates)

        for idx, voter in enumerate(voters):
            polling_station.process_voter(voter, voter_rankings[idx])

        polling_station.tabulate_votes()
        self.assertEqual(polling_station.candidate_has_super_majority(), False)

        while (polling_station.get_num_surv_candidates() > 2):
            polling_station.remove_last_and_reasign_votes()

        self.assertEqual(polling_station.get_surv_candidates()[0].__str__(),
                         "Candidate Name: B\nNumber of Votes: 3\n")

if __name__ == "__main__":
    unittest.main()






