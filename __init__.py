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

    def __init__(self, game):
        # TODO: DIVIDE DICE AMONG PLAYERS
        # TODO: THROW EXCEPTION IF DICE DOES NOT DIVIDE AMONG PLAYERS
        self.game = game
        for d in game.dice:
            d.roll()

    def results(self):
        r = {}
        r[1] = sum(d.state == 1 for d in self.game.dice)
        for s in range(2, self.game.sides+1):
            r[s] = sum(d.state == s for d in self.game.dice) + r[1]
        for s in range(2, self.game.sides+1):
            print(f'{s}: {r[s]}')


class Game:
    """A class representing a game of Liar's Dice"""

    def __init__(self, no_dice, players, sides=6):
        self.sides = sides
        self.players = players
        self.dice = []
        for i in range(1, no_dice+1):
            self.dice.append(Die(self.sides))

    def play(self):
        for i in range(len(self.dice),1,-1):
            r = Round(self)
            r.results()
            self.dice.pop()
            print('-'*20)


def main():
    Game(20, 4).play()


if __name__ == "__main__":
    main()

