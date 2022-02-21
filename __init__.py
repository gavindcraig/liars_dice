import random


class Die:
    """A class representing a die"""

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        self.state = random.randint(1, self.sides)
        return self.state


class Player:
    """A class representing a player"""

    def __init__(self):
        self.dice = []

    def show_dice(self):
        print(' '.join(str(d.state) for d in self.dice))

    def lose(self):
        self.dice.pop()


class Round:
    """A class representing a round"""

    def __init__(self, game):
        self.game = game
        for p in game.players:
            for d in p.dice:
                d.roll()

    def results(self):
        """Prints a table of all results"""
        r = {}
        r[1] = sum(d.state == 1 for d in self.game.all_dice)
        for s in range(2, self.game.sides+1):
            r[s] = sum(d.state == s for d in self.game.all_dice) + r[1]
        for s in range(2, self.game.sides+1):
            print(f'{s}: {r[s]}')


class Game:
    """A class representing a game of Liar's Dice"""

    def __init__(self, no_dice, no_players, sides=6):
        self.sides = sides
        # THROW EXCEPTION IF DICE DOES NOT DIVIDE AMONG PLAYERS
        while no_dice%no_players:
            print("Dice cannot be evenly distributed. Enter quantities again.")
            no_dice = int(input("Number of dice: "))
            no_players = int(input("Number of players: "))
        self.players = []
        # DIVIDE DICE AMONG PLAYERS
        dice_per = int(no_dice/no_players)
        for i in range(0, no_players):
            self.players.append(Player())
            for j in range(0, dice_per):
                self.players[i].dice.append(Die(sides))

    def play(self):
        # TODO
        # for i in range(self.no_dice,1,-1):
        #     r = Round(self)
        #     r.results()
        #     loser = self.players[random.randint(1, len(self.players))]
        #     loser.lose()
        #     print('-'*20)

    @property
    def all_dice(self):
        d = []
        for i in range(0, len(self.players)):
            d.extend(self.players[i].dice)
        return d

    @property
    def no_dice(self):
        return len(self.all_dice)


def main():
    # Game(20, 4).play()


if __name__ == "__main__":
    main()

