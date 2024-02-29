# Name: Video Poker Simulation
# Date: 02/25/2024
# Author: Larry Campbell Harris, Jr. lcharris346@gmail.com
# Description:
#  -Video Poker Simulation executes games based on initial balance, bet amount, num-hands,
#    algorithm (hold random, hold all, hold none, optimization algorithm, or user input),
#    bonus type (JoB, Double Bonus, or Triple Double Bonus), 
#    multiplier type (Ultimate-X, Super-Time-Pay or None), and
#    exit condition (time, return, profit, or empty balance)
#  -Stats and Plots can be generated for analysis.

# RESOURCES
import os
import sys
import argparse
import random
import time
import copy
import matplotlib.pyplot as plt
import numpy as np

# CONSTANTS
CARDS = {
    "022S": {"val": 2, "cat": 4},
    "033S": {"val": 3, "cat": 4},
    "044S": {"val": 4, "cat": 4},
    "055S": {"val": 5, "cat": 4},
    "066S": {"val": 6, "cat": 4},
    "077S": {"val": 7, "cat": 4},
    "088S": {"val": 8, "cat": 4},
    "099S": {"val": 9, "cat": 4},
    "10TS": {"val": 10, "cat": 4},
    "11JS": {"val": 11, "cat": 4},
    "12QS": {"val": 12, "cat": 4},
    "13KS": {"val": 13, "cat": 4},
    "14AS": {"val": 14, "cat": 4},
    "022H": {"val": 2, "cat": 3},
    "033H": {"val": 3, "cat": 3},
    "044H": {"val": 4, "cat": 3},
    "055H": {"val": 5, "cat": 3},
    "066H": {"val": 6, "cat": 3},
    "077H": {"val": 7, "cat": 3},
    "088H": {"val": 8, "cat": 3},
    "099H": {"val": 9, "cat": 3},
    "10TH": {"val": 10, "cat": 3},
    "11JH": {"val": 11, "cat": 3},
    "12QH": {"val": 12, "cat": 3},
    "13KH": {"val": 13, "cat": 3},
    "14AH": {"val": 14, "cat": 3},
    "022D": {"val": 2, "cat": 2},
    "033D": {"val": 3, "cat": 2},
    "044D": {"val": 4, "cat": 2},
    "055D": {"val": 5, "cat": 2},
    "066D": {"val": 6, "cat": 2},
    "077D": {"val": 7, "cat": 2},
    "088D": {"val": 8, "cat": 2},
    "099D": {"val": 9, "cat": 2},
    "10TD": {"val": 10, "cat": 2},
    "11JD": {"val": 11, "cat": 2},
    "12QD": {"val": 12, "cat": 2},
    "13KD": {"val": 13, "cat": 2},
    "14AD": {"val": 14, "cat": 2},
    "022C": {"val": 2, "cat": 1},
    "033C": {"val": 3, "cat": 1},
    "044C": {"val": 4, "cat": 1},
    "055C": {"val": 5, "cat": 1},
    "066C": {"val": 6, "cat": 1},
    "077C": {"val": 7, "cat": 1},
    "088C": {"val": 8, "cat": 1},
    "099C": {"val": 9, "cat": 1},
    "10TC": {"val": 10, "cat": 1},
    "11JC": {"val": 11, "cat": 1},
    "12QC": {"val": 12, "cat": 1},
    "13KC": {"val": 13, "cat": 1},
    "14AC": {"val": 14, "cat": 1},
}

CARDS_KEYS = list(CARDS.keys())

CATEGORY = {"s": 4, "h": 3, "d": 2, "c": 1}

CATEGORY_KEYS = list(CATEGORY.keys())

RETURNS_JoB = {
    "RF": 800,
    "SF": 50,
    "4K": 25,
    "FH": 9,
    "F": 5,
    "S": 4,
    "3K": 3,
    "2P": 2,
    "JoB": 1,
}

RETURNS_KEYS = list(RETURNS_JoB.keys())

RETURNS_DBJoB = {
    "RF": 800,
    "4KA": 160,
    "4K2_4": 80,
    "4K": 50,
    "SF": 50,
    "FH": 9,
    "F": 5,
    "S": 4,
    "3K": 3,
    "2P": 1,
    "JoB": 1,
}

RETURNS_KEYS2 = list(RETURNS_DBJoB.keys())

RETURNS_TDBJoB = {
    "RF": 800,
    "4KA_2_4": 800,
    "4K2_4_A_4": 400,
    "4KA": 160,
    "4K2_4": 80,
    "4K": 50,
    "SF": 50,
    "FH": 9,
    "F": 5,
    "S": 4,
    "3K": 2,
    "2P": 1,
    "JoB": 1,
}

RETURNS_KEYS3 = list(RETURNS_TDBJoB.keys())

ULTIMATE_X_MULTIPLIER = {
    "RF": 2,
    "4K": 2,
    "4KA": 2,
    "4K2_4": 2,
    "4K5_K": 2,
    "SF": 50,
    "FH": 12,
    "F": 10,
    "S": 8,
    "3K": 4,
    "2P": 3,
    "JoB": 2,
}


NUM_CARDS = range(1, 6)

ALL_CARDS = "12345"

NO_CARDS = ""

STRAIGHT = [1, 1, 1, 1]
AL_STRAIGHT = [1, 1, 1, 9]
FLUSH = [0, 0, 0, 0]
FOUR_TO_A_STRIGHT = [1, 1, 1]
FOUR_TO_A_STRIGHT2 = [1, 1, 9]
FOUR_TO_A_FLUSH = [0, 0, 0]
THREE_TO_A_FLUSH = [0, 0]

THREE_TO_RF = (
    [10,11,12],
    [10,11,13],
    [10,11,14],
    [10,12,13],
    [10,12,14],
    [10,13,14],
    [11,13,14],
    [12,13,14],
    [11,12,13],
    [11,12,14],
    [11,13,14],
    [12,13,14],
)


QUIT = ("q", "quit")

ALL = ("a", "all")
NONE = ("n", "none")

ULTIMATE_X_MULTIPLIER = {
    "RF": 2,
    "4K": 2,
    "4KA": 2,
    "4K2_4": 2,
    "4K5_K": 2,
    "SF": 50,
    "FH": 12,
    "F": 10,
    "S": 8,
    "3K": 4,
    "2P": 3,
    "JoB": 2,
}

SUPER_T_TIMER = list(range(15))
SUPER_T_MULTIPLER = list([2, 2, 2, 2, 2, 3, 4, 5, 8, 10])

MULTIPLER_OPTIONS = ("supt", "ultx")

# SAMPLE INPUTS
GROUP_RF = ["10Ts", "11Js", "12Qs", "13Ks", "14As"]
GROUP_SF = ["022s", "033s", "044s", "055s", "066s"]
GROUP_ALSF = ["14As", "022s", "033s", "044s", "055s"]
GROUP_4K = ["022s", "022h", "022d", "022c", "055d"]
GROUP_FH = ["022s", "022h", "022d", "055h", "055d"]
GROUP_F = ["022s", "033s", "044s", "055s", "077s"]
GROUP_S = ["022s", "033s", "044s", "055s", "066h"]
GROUP_3K = ["022s", "022h", "022d", "055h", "088d"]
GROUP_2P = ["022s", "022h", "055s", "055h", "088d"]
GROUP_JoB = ["11Js", "11Jh", "055s", "077h", "088d"]


# FUNCTIONS
def is_rf(group):
    condition = False
    if (
        group["d_cats"] == FLUSH
        and group["d_vals"] == STRAIGHT
        and group["vals"][4] == 14
    ):
        condition = True
    return condition


def is_sf(group):
    condition = False
    if group["d_cats"] == FLUSH and group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
        condition = True
    return condition


def is_4k(group):
    condition = False
    if group["d_vals"].count(0) == 3 and (
        (
            group["d_vals"][0] == 0
            and group["d_vals"][1] == 0
            and group["d_vals"][2] == 0
        )
        or (
            group["d_vals"][1] == 0
            and group["d_vals"][2] == 0
            and group["d_vals"][3] == 0
        )
    ):
        condition = True
    return condition


def is_4ka(group):
    condition = False
    if (
        group["d_vals"].count(0) == 3
        and (
            (
                group["d_vals"][0] == 0
                and group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
            )
            or (
                group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
                and group["d_vals"][3] == 0
            )
        )
        and group["vals"][2] == 14
    ):
        condition = True
    return condition


def is_4k2_4(group):
    condition = False
    if (
        group["d_vals"].count(0) == 3
        and (
            (
                group["d_vals"][0] == 0
                and group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
            )
            or (
                group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
                and group["d_vals"][3] == 0
            )
        )
        and group["vals"][2] in (2, 3, 4)
    ):
        condition = True
    return condition


def is_4ka_2_4(group):
    condition = False
    if (
        group["d_vals"].count(0) == 3
        and (
            (
                group["d_vals"][0] == 0
                and group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
            )
            or (
                group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
                and group["d_vals"][3] == 0
            )
        )
        and group["vals"][2] == 14
        and group["vals"][0] <= 4
    ):
        condition = True
    return condition


def is_4k2_4_a_4(group):
    condition = False
    if (
        group["d_vals"].count(0) == 3
        and (
            (
                group["d_vals"][0] == 0
                and group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
            )
            or (
                group["d_vals"][1] == 0
                and group["d_vals"][2] == 0
                and group["d_vals"][3] == 0
            )
        )
        and group["vals"][2] in (2, 3, 4)
        and (group["vals"][4] == 14 or group["vals"][4] <= 4)
    ):
        condition = True
    return condition


def is_fh(group):
    condition = False
    if group["d_vals"].count(0) == 3 and (
        (
            group["d_vals"][0] == 0
            and group["d_vals"][1] == 0
            and group["d_vals"][3] == 0
        )
        or (
            group["d_vals"][0] == 0
            and group["d_vals"][2] == 0
            and group["d_vals"][3] == 0
        )
    ):
        condition = True
    return condition


def is_f(group):
    condition = False
    if group["d_cats"] == FLUSH:
        condition = True
    return condition


def is_s(group):
    condition = False
    if group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
        condition = True
    return condition


def is_3k(group):
    condition = False
    if group["d_vals"].count(0) == 2 and (
        (group["d_vals"][0] == 0 and group["d_vals"][1] == 0)
        or (group["d_vals"][1] == 0 and group["d_vals"][2] == 0)
        or (group["d_vals"][2] == 0 and group["d_vals"][3] == 0)
    ):
        condition = True
    return condition


def is_2p(group):
    condition = False
    if group["d_vals"].count(0) == 2:
        condition = True
    return condition


def is_job(group):
    condition = False
    if group["d_vals"].count(0) == 1:
        index = group["d_vals"].index(0)
        if group["vals"][index] > 10:
            condition = True
    return condition


# MAIN CLASS
class VideoPokerSimulation(object):
    def __init__(self, args):
        self.debug = args.debug
        self.alg = args.alg
        self.game = args.game
        self.balance = round(args.stack,2)
        self.bet_denom = round(args.bet_denom,2)
        self.hands = args.hands
        self.plot = args.plot
        self.multi = args.multi
        self.exit = args.exit
        self.reduce_bet = args.reduce_bet
        self.max_balance = copy.deepcopy(args.stack)
        self.init_balance = copy.deepcopy(args.stack)
        self.shuffled_cards = None
        self.group = {}
        self.prev_group = {}
        self.group[0] = {
            "cards": [],
            "vals": [],
            "cats": [],
            "d_vals": [],
            "d_cats": [],
            "type": None,
            "ret": 0,
            "multi": 1,
        }
        for i in range(1, self.hands):
            self.group[i] = copy.deepcopy(self.group[0])
        self.keep = None
        self.max_ret = 0
        self.max_group = {"type": None, "profit": 0, "num_steps": 0, "balance": 0}
        self.algorithms = {
            "i": self.algorith_input,
            "r": self.algorith_random,
            "k": self.algorithm_keep_all,
            "d": self.algorithm_discard_all,
            "s1": self.algorithm_strategy1,
        }
        self.algorithm = self.algorithms[self.alg]
        self.hist = {
                "RF": 0,
                "SF": 0,
                "4KA_2_4": 0,
                "4K2_4_A_4": 0,
                "4KA": 0,
                "4K2_4": 0,
                "4K": 0,
                "FH": 0,
                "F": 0,
                "S": 0,
                "3K": 0,
                "2P": 0,
                "JoB": 0,
            }

        self.num_steps = 0
        self.prev_balance = 0
        self.balance_list = [0] * 100000
        self.delta_balance_list = [0] * 100000
        self.init_bet_denom = self.bet_denom
        

    def algorith_input(self):
        keep = input("Algorithm Input: Keep: ")
        if keep == "r":
            keep = self.algorith_random()
        elif keep == "s1":
            keep = self.algorithm_strategy1()
        return keep

    def algorith_random(self):
        if self.debug:
            print("Algorithm Random:")
        num_choices = random.choice(NUM_CARDS)
        keep_list = random.sample(NUM_CARDS, num_choices)
        keep_list_str = [str(x) for x in keep_list]
        keep = "".join(keep_list_str)
        return keep

    def algorithm_keep_all(self):
        keep = "a"
        return keep

    def algorithm_discard_all(self):
        keep = "n"
        return keep

    def algorithm_strategy1(self):
        if self.debug:
            print("Algorithm Strategy 1:")
        keep = ""
        # Check for Straight Flushes:
        if self.group[0]["d_cats"] == FLUSH and self.group[0]["d_vals"] in (
            STRAIGHT,
            AL_STRAIGHT,
        ):
            keep = "12345"

        # Check for Quads
        if keep == "":
            if self.group[0]["d_vals"] == [0, 0, 0]:
                keep = "12345"

        # Check for Full Houses:
        if keep == "":
            if (
                self.group[0]["d_vals"][:2] == [0, 0]
                and self.group[0]["d_vals"][3] == 0
            ):
                keep = "12345"
            elif self.group[0]["d_vals"][0] == 0 and self.group[0]["d_vals"][2:] == [
                0,
                0,
            ]:
                keep = "12345"

        # Check for Straights or Flushes
        if keep == "":
            if self.group[0]["d_cats"] == FLUSH:
                keep = "12345"
            elif self.group[0]["d_vals"] in (STRAIGHT, AL_STRAIGHT):
                keep = "12345"

        # Check for Trips
        if keep == "":
            if self.group[0]["d_vals"][:2] == [0, 0]:
                keep = "123"
            if self.group[0]["d_vals"][1:3] == [0, 0]:
                keep = "234"
            if self.group[0]["d_vals"][2:] == [0, 0]:
                keep = "345"

        # Check for Pairs
        if keep == "":
            for i, x in enumerate(self.group[0]["d_vals"]):
                if x == 0 and i < 4:
                    if str(i + 1) not in keep:
                        keep += str(i + 1)
                    if str(i + 2) not in keep:
                        keep += str(i + 2)

        if keep == "":
            # Check for 4 to a Flush
            if self.group[0]["d_cats"][:3] == FOUR_TO_A_FLUSH:
                keep = "1234"

            elif self.group[0]["d_cats"][1:] == FOUR_TO_A_FLUSH:
                keep = "2345"

            # Check for 4 to a Straight
            elif self.group[0]["d_cats"][:3] == FOUR_TO_A_STRIGHT:
                keep = "1234"

            elif self.group[0]["d_cats"][1:] in (FOUR_TO_A_STRIGHT, FOUR_TO_A_STRIGHT2):
                keep = "2345"

            # Check for 3 to a Royal Flush
            elif (
                self.group[0]["vals"][:3] in THREE_TO_RF
                and self.group[0]["d_cats"][:2] == THREE_TO_A_FLUSH
            ):
                keep = "123"
            elif (
                self.group[0]["vals"][1:4] in THREE_TO_RF
                and self.group[0]["d_cats"][1:3] == THREE_TO_A_FLUSH
            ):
                keep = "234"
            elif (
                self.group[0]["vals"][2:] in THREE_TO_RF
                and self.group[0]["d_cats"][2:] == THREE_TO_A_FLUSH
            ):
                keep = "345"

            # Check for High Value Items
            else:
                num_cards = 0
                suits = []
                vals = []
                for i, card in enumerate(self.group[0]["cards"]):
                    if CARDS[card]["val"] > 10:
                        keep += str(i + 1)
                        num_cards += 1
                        suits.append(self.group[0]["cats"][i])
                        vals.append(self.group[0]["vals"][i])

                if len(keep) == 3:
                    #print("Debug: 3 High Cards:", vals, suits)
                    if (suits[1] == suits[2]) or (vals[2] - vals[1]) == 1:
                        keep = keep[1] + keep[2]
                    elif suits[0] == suits[2]:
                        keep = keep[0] + keep[2]
                    else:
                        keep = keep[0] + keep[1]

        return keep

    def deal(self):
        
        # Bet Payment
        self.prev_balance = copy.deepcopy(self.balance)
        self.balance = self.balance - self.hands * self.bet_denom

        if self.keep in QUIT:
            return
        cards = copy.deepcopy(CARDS_KEYS)

        random.shuffle(cards)

        self.shuffled_cards = copy.deepcopy(cards[:10])
        self.group[0]["cards"] = copy.deepcopy(self.shuffled_cards[:5])

        

        if self.alg in ("s1",):
            self.group[0]["cards"].sort()
            self.group[0]["vals"] = [CARDS[x]["val"] for x in self.group[0]["cards"]]
            self.group[0]["vals"].sort()
            self.group[0]["cats"] = [CARDS[x]["cat"] for x in self.group[0]["cards"]]
            self.group[0]["cats"].sort()
            self.group[0]["d_vals"] = [
                x - self.group[0]["vals"][i - 1]
                for i, x in enumerate(self.group[0]["vals"])
            ][1:]
            self.group[0]["d_cats"] = [
                x - self.group[0]["cats"][i - 1]
                for i, x in enumerate(self.group[0]["cats"])
            ][1:]

        if self.alg == "i":
            print("\nInitial Group:", " ".join([x[2:] for x in self.group[0]["cards"]]))

        # multiple
        self.other_shuffled_cards = {}
        for index in range(1, self.hands):
            shuffled_cards_5_52 = copy.deepcopy(cards[5:])
            random.shuffle(shuffled_cards_5_52)
            self.group[index]["cards"] = copy.deepcopy(self.group[0]["cards"])
            self.other_shuffled_cards[index] = (
                self.group[index]["cards"] + shuffled_cards_5_52[:5]
            )

        

    def update_multiplier(self):

        if self.multi == "supt":

            self.balance = self.balance - self.bet_denom * self.hands * 0.2
            if self.balance <= 0:
                return
            multipler = 1
            if random.choice(SUPER_T_TIMER) == 14:
                random.shuffle(SUPER_T_MULTIPLER)

                if self.alg == "i":
                    print("Super Time Pay: Multiplier Spin!")
                    for m in SUPER_T_MULTIPLER:
                        time.sleep(0.2)
                        print(m)

                    print("   Multiplier = ", multipler)

                multipler = SUPER_T_MULTIPLER[-1]

            for index in range(self.hands):
                self.group[index]["multi"] = multipler

        elif self.multi == "ultx":
            self.balance = self.balance - self.bet_denom * self.hands
            if self.balance <= 0:
                return
            for index in range(self.hands):
                self.group[index]["multi"] = 1
                if self.group[index]["type"] in ULTIMATE_X_MULTIPLIER:
                    self.group[index]["multi"] = ULTIMATE_X_MULTIPLIER[
                        self.group[index]["type"]
                    ]
                if self.alg == "i":
                    print("Ultimate X: Multiplier = ", self.group[index]["multi"])

    def draw(self):
        if self.keep in QUIT:
            return

        if self.debug:
            print("Step", self.num_steps, "Shuffled cards", self.shuffled_cards)

        self.keep = self.algorithm()
        if self.debug:
            print("Keep", self.keep)

        if self.keep in QUIT:
            return

        elif self.keep in ALL:
            self.keep = ALL_CARDS

        elif self.keep in NONE:
            self.keep = NO_CARDS

        next_card = 5

        for card in NUM_CARDS:
            card_str = str(card)

            if card_str not in self.keep:
                self.group[0]["cards"][card - 1] = self.shuffled_cards[next_card]

                for i in range(1, self.hands):
                    self.group[i]["cards"][card - 1] = self.other_shuffled_cards[i][
                        next_card
                    ]

                next_card += 1

        self.group[0]["cards"].sort()
        self.group[0]["vals"] = [CARDS[x]["val"] for x in self.group[0]["cards"]]
        self.group[0]["vals"].sort()
        self.group[0]["cats"] = [CARDS[x]["cat"] for x in self.group[0]["cards"]]
        self.group[0]["cats"].sort()
        self.group[0]["d_vals"] = [
            x - self.group[0]["vals"][i - 1]
            for i, x in enumerate(self.group[0]["vals"])
        ][1:]
        self.group[0]["d_cats"] = [
            x - self.group[0]["cats"][i - 1]
            for i, x in enumerate(self.group[0]["cats"])
        ][1:]

        for i in range(1, self.hands):

            self.group[i]["cards"].sort()
            self.group[i]["vals"] = [CARDS[x]["val"] for x in self.group[i]["cards"]]
            # self.group[i]["vals"].sort()
            self.group[i]["cats"] = [CARDS[x]["cat"] for x in self.group[i]["cards"]]
            # self.group[i]["cats"].sort()
            self.group[i]["d_vals"] = [
                x - self.group[i]["vals"][j - 1]
                for j, x in enumerate(self.group[i]["vals"])
            ][1:]
            self.group[i]["d_cats"] = [
                x - self.group[i]["cats"][j - 1]
                for j, x in enumerate(self.group[i]["cats"])
            ][1:]

        if self.debug:
            print("Updated Group:", " ".join([x[2:] for x in self.group[0]["cards"]]))

        if self.debug:
            print("Values", self.group[0]["vals"])
            print("Values Diffs", self.group[0]["d_vals"])
            print("Categories", self.group[0]["cats"])
            print("Categories Diffs", self.group[0]["d_cats"])

    def evaluate_job(self, index):

        self.group[index]["type"] = None
        self.group[index]["ret"] = 0

        if is_rf(self.group[index]):
            self.group[index]["type"] = "RF"
        elif is_sf(self.group[index]):
            self.group[index]["type"] = "SF"
        elif is_4k(self.group[index]):
            self.group[index]["type"] = "4K"
        elif is_fh(self.group[index]):
            self.group[index]["type"] = "FH"
        elif is_f(self.group[index]):
            self.group[index]["type"] = "F"
        elif is_s(self.group[index]):
            self.group[index]["type"] = "S"
        elif is_3k(self.group[index]):
            self.group[index]["type"] = "3K"
        elif is_2p(self.group[index]):
            self.group[index]["type"] = "2P"
        elif is_job(self.group[index]):
            self.group[index]["type"] = "JoB"

        if self.group[index]["type"] in RETURNS_KEYS3:
            self.group[index]["ret"] = (
                self.group[index]["multi"]
                * RETURNS_JoB[self.group[index]["type"]]
                * self.bet_denom
            )
            self.hist[self.group[index]["type"]] += 1

    def evaluate_db(self, index):

        self.group[index]["type"] = None
        self.group[index]["ret"] = 0

        if is_rf(self.group[index]):
            self.group[index]["type"] = "RF"
        elif is_4ka(self.group[index]):
            self.group[index]["type"] = "4KA"
        elif is_4k2_4(self.group[index]):
            self.group[index]["type"] = "4K2_4"
        elif is_4k(self.group[index]):
            self.group[index]["type"] = "4K"
        elif is_sf(self.group[index]):
            self.group[index]["type"] = "SF"
        elif is_fh(self.group[index]):
            self.group[index]["type"] = "FH"
        elif is_f(self.group[index]):
            self.group[index]["type"] = "F"
        elif is_s(self.group[index]):
            self.group[index]["type"] = "S"
        elif is_3k(self.group[index]):
            self.group[index]["type"] = "3K"
        elif is_2p(self.group[index]):
            self.group[index]["type"] = "2P"
        elif is_job(self.group[index]):
            self.group[index]["type"] = "JoB"

        if self.group[index]["type"] in RETURNS_KEYS3:
            self.group[index]["ret"] = (
                self.group[index]["multi"]
                * RETURNS_DBJoB[self.group[index]["type"]]
                * self.bet_denom
            )
            self.hist[self.group[index]["type"]] += 1

    def evaluate_tdb(self, index):

        self.group[index]["type"] = None
        self.group[index]["ret"] = 0

        if is_rf(self.group[index]):
            self.group[index]["type"] = "RF"
        elif is_4ka_2_4(self.group[index]):
            self.group[index]["type"] = "4KA_2_4"
        elif is_4k2_4_a_4(self.group[index]):
            self.group[index]["type"] = "4K2_4_A_4"
        elif is_4ka(self.group[index]):
            self.group[index]["type"] = "4KA"
        elif is_4k2_4(self.group[index]):
            self.group[index]["type"] = "4K2_4"
        elif is_4k(self.group[index]):
            self.group[index]["type"] = "4K"
        elif is_sf(self.group[index]):
            self.group[index]["type"] = "SF"
        elif is_fh(self.group[index]):
            self.group[index]["type"] = "FH"
        elif is_f(self.group[index]):
            self.group[index]["type"] = "F"
        elif is_s(self.group[index]):
            self.group[index]["type"] = "S"
        elif is_3k(self.group[index]):
            self.group[index]["type"] = "3K"
        elif is_2p(self.group[index]):
            self.group[index]["type"] = "2P"
        elif is_job(self.group[index]):
            self.group[index]["type"] = "JoB"

        if self.group[index]["type"] in RETURNS_KEYS3:
            self.group[index]["ret"] = (
                self.group[index]["multi"]
                * RETURNS_TDBJoB[self.group[index]["type"]]
                * self.bet_denom
            )
            self.hist[self.group[index]["type"]] += 1

    def analyze(self, index):

        # Update Balance
        
        self.balance += self.group[index]["ret"]
        if self.balance > self.max_balance:
            self.max_balance = self.balance

        if self.group[index]["ret"] > self.max_ret:
            self.max_group = copy.deepcopy(self.group[index])
            self.max_group["balance"] = self.balance
            self.max_group["profit"] = self.balance - self.init_balance
            self.max_group["num_steps"] = self.num_steps
            self.max_ret = copy.deepcopy(self.group[index]["ret"])

        if self.debug or self.alg == "i":
            print(
                "Hand",
                self.group[index]["cards"],
                "Type",
                self.group[index]["type"],
                "Ret",
                self.group[index]["ret"],
                "Multi",
                self.group[index]["multi"],
            )

    def bet(self):
        self.balance_list[self.num_steps] = self.balance
        self.num_steps += 1

        if self.multi in MULTIPLER_OPTIONS:
            self.update_multiplier()
        if self.balance <= 0:
            return

        self.deal()
        if self.balance <= 0:
            return

        self.draw()
        if self.keep in QUIT:
            return

        for index in range(self.hands):
            if self.game == "tdb":
                self.evaluate_db(index)
            elif self.game == "db":
                self.evaluate_db(index)
            elif self.game == "job":
                self.evaluate_job(index)
            self.analyze(index)

        self.delta_balance_list[self.num_steps] = self.balance - self.prev_balance

        if self.debug or self.alg == "i":
            print(
                "Step = %d, Balance = %5.2f"
                % (
                    self.num_steps,
                    self.balance,
                )
            )

        # Adjust bet based on balance
        if self.reduce_bet == True:
            if (self.bet_denom > 0.1*self.balance) and (self.bet_denom > 0.05):
                self.bet_denom = round(self.bet_denom - 0.05,2)
                print("New Bet Denom:", self.bet_denom)

        self.prev_group = copy.deepcopy(self.group)

    def gen_plot(self):

        plt.style.use("dark_background")

        # using tuple unpacking for multiple Axes
        fig, axs = plt.subplots(2, 1)

        # fig, ax = plt.subplots()

        x = list(range(0, self.num_steps))
        y = self.balance_list[0 : self.num_steps]

        axs[0].plot(x, y)
        axs[0].set_title("Balance vs Num Steps")

        #types = list(self.hist.keys())
        #frequency = list(self.hist.values())
        #axs[1].bar(types, frequency, color="maroon", width=0.4)
        #axs[1].set_title("Counts vs Hand Type")

        y2 = self.delta_balance_list[0 : self.num_steps]

        axs[1].plot(x, y2)
        axs[1].set_title("Delta Balance vs Num Steps")

        plt.show()

    def play(self):
        random.seed()
        while (self.keep not in QUIT) and (self.balance >= self.hands * self.bet_denom):

            self.bet()

            # End Gaame based on exit condition
            if self.exit == "t":
                if self.num_steps >= 720:
                    break
            elif self.exit == "r":
                if self.max_ret >= 25 * self.bet_denom:
                    break
            elif self.exit == "b":
                if (self.balance >= 1.2 * self.init_balance) or (self.balance <= 0.8 * self.init_balance):
                    break

        if self.plot == True:
            self.gen_plot()

        

        
# MAIN FUNCTION
def main(args):
    p4 = VideoPokerSimulation(args)
    if args.mcruns > 1:
        balance = 0.0
        num_steps = 0.0
        max_balance = 0
        max_balance_num_steps = 0
        for i in range(int(args.mcruns)):
            p4.play()
            balance   += p4.balance
            num_steps += p4.num_steps
            if p4.balance > max_balance:
                max_balance = p4.balance
                max_balance_num_steps = p4.num_steps
            p4.__init__(args)
        print(
            "\nave_balance", balance/args.mcruns, 
            "\nave_time_min", num_steps/args.mcruns/12.0, 
            "\nmax_balance", max_balance, 
            "\nmax_balance_time_min", max_balance_num_steps/12.0
            )
    else:
        p4.play()
        print(
            "max_group",
            p4.max_group,
            "\nhistogram",
            p4.hist,
            "\nend_balance",
            p4.balance,
            "\nnum_steps",
            p4.num_steps,
            "\ntime_spent",
            p4.num_steps / 12,
        )

# COMMAND-LINE EXECUTION
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Video Poker Simulation",
        description="Simulation, Analyze, and Play Video Poker.",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Debug")
    parser.add_argument("-r", "--reduce_bet", action="store_true", help="Reduce Bet based on Balance")
    parser.add_argument("-p", "--plot", action="store_true", help="Create Anaylsis Plots")
    parser.add_argument("-z", "--mcruns", default=1, help="Run Z Monte Carlo Sims", type=int)
    parser.add_argument("-a", "--alg", default="s1", choices=["s1","r","d","k","i"], 
        help="Algorithm choice. r=random, k=hold all, d = discard all, i = user input, s1 = optimizate")
    parser.add_argument("-g", "--game", default="job", choices=["job","db","tdb"],
        help="Game. job: Jacks or Better, db: Double Bonus, tdb: Tripler Double Bonus")
    parser.add_argument("-m", "--multi", default=None, choices=[None, "ultx","supt"],
        help="Multiplier Type. ultx: Ultimate X, supt: Super Times Pay")
    parser.add_argument("-s", "--stack", default=100, type=float, help="Enter balance in $")
    parser.add_argument("-b", "--bet_denom", default=0.05, type=float, help="Enter bet amount in $")
    parser.add_argument("-n", "--hands", default=10, type=int, help="Enter number of hands")
    parser.add_argument("-e","--exit",default=None, choices=["t","r","b"],
        help="Exit Condition. t: num-bets = 720, r:return >= 25*bet-amount, b: 0.8*stack < balance < 1.8*stack")

    args = parser.parse_args()
    if args.debug == True:
        os.system("cls")
    main(args)
