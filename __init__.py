import random


class Die:
    """A class representing a die"""

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        self.state = random.randint(1, self.sides)
        return self.state


class Round:
    """A class representing a round"""

    def __init__(self, dice, players, sides=6):
        self.sides = sides
        self.players = players
        # TODO: DIVIDE DICE AMONG PLAYERS
        # TODO: THROW EXCEPTION IF DICE DOES NOT DIVIDE AMONG PLAYERS
        self.dice = []
        for i in range(1, dice+1):
            self.dice.append(Die(self.sides))
        for d in self.dice:
            d.roll()

    def results(self):
        r = {}
        r[1] = sum(d.state == 1 for d in self.dice)
        for s in range(2, self.sides+1):
            r[s] = sum(d.state == s for d in self.dice) + r[1]
        for s in range(2, self.sides+1):
            print(f'{s}: {r[s]}')


def main():
    for i in range(20,1,-1):
        r = Round(dice=i, players=4)
        r.results()
        print('-'*20)

if __name__ == "__main__":
    main()

