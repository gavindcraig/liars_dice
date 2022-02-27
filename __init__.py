import random
import names
from itertools import cycle
# TODO: CONSIDER USING PYINQUIRER


class Die:
    """A class representing a die"""

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        self.state = random.randint(1, self.sides)
        return self.state


class Player:
    """A class representing a player"""

    def __init__(self, name=None, human=True):
        # TODO: ALLOW ENTRY OF NAME FOR HUMAN PLAYERS
        self.name = name if name else names.get_first_name()
        self.human = human
        self.dice = []
        self.active = True

    def show_dice(self):
        print(' '.join(str(d.state) for d in self.dice))

    def eval_wager(self, wager):
        if self.human:
            # TODO: CORRECT PLURAL, SPELL DIE STATE
            q = f'CURRENT WAGER: {wager["dice"]} {wager["state"]}s\n'
            q += '(c)all or (b)id?\n'
            action = input(q)
        # TODO: FUNCTION FOR AI
        if action[0].lower() == 'c':
            return wager
        else:
            new_wager = {'state': 0, 'dice': 0}
            while new_wager['state'] < wager['state'] or \
                    (new_wager['dice'] < wager['dice'] and
                     new_wager['state'] <= wager['state']) \
                    or new_wager == wager:
                new_wager = self.get_wager()
            self.guess = new_wager
            return self.guess

    def get_wager(self):
        self.show_dice()
        v = int(input('Which value? '))
        while v > self.dice[0].sides:
            print(f'Value must be 1-{self.dice[0].sides}!')
            v = int(input('Which value? '))
        d = int(input('Number showing? '))
        self.guess = {'state': v, 'dice': d}
        return self.guess

    def lose(self):
        # CURRENTLY SET UP FOR ONE PLAYER
        if len(self.dice) > 1:
            self.dice.pop()
            print(f'{self.name} lost one die!')
        else:
            self.active = False
            # TODO: CHANGE TO REMOVE PLAYER FROM GAME
            print(f'{self.name} ran out of dice!')
            self.active = False


class Round:
    """A class representing a round"""

    def __init__(self, game):
        self.game = game
        for p in game.players:
            for d in p.dice:
                d.roll()
        # STORE RESULTS IN DICT
        r = {}
        r[1] = sum(d.state == 1 for d in self.game.all_dice)
        for s in range(2, self.game.sides+1):
            r[s] = sum(d.state == s for d in self.game.all_dice) + r[1]
        self.results = r

    def play(self, players):
        self.wager = None
        prev_p = None
        for p in cycle(players):
            print(f"{p.name}'s turn")
            # TAKE IN WAGER, COMPARE TO PREVIOUS
            if not self.wager:
                self.wager = p.get_wager()
            elif p.eval_wager(self.wager) == self.wager:
                if self.check_wager(prev_p.guess):
                    p.lose()
                else:
                    prev_p.lose()
                break
            else:
                self.wager = p.guess
            prev_p = p

    def print_results(self):
        """Prints a table of all results"""
        for s in range(1, self.game.sides+1):
            print(f'{s}: {self.results[s]}')

    def turn(self, player):
        # CURRENTLY SET UP FOR ONE PLAYER
        player.get_wager()
        if not self.check_wager(player.guess['dice'], player.guess['state']):
            print('Incorrect guess!')
            player.lose()

    def check_wager(self, wager):
        return self.results[wager['state']] >= wager['dice']


class Game:
    """A class representing a game of Liar's Dice"""

    def __init__(self, no_dice, no_players, sides=6):
        self.sides = sides
        # THROW EXCEPTION IF DICE DOES NOT DIVIDE AMONG PLAYERS
        while no_dice % no_players:
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
        while self.no_dice > 1:
            r = Round(self)
            r.play(self.players)
            r.print_results()

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
    # TODO: INPUT NUMBER OF PLAYERS AND DICE
    Game(20, 4).play()


if __name__ == "__main__":
    main()
