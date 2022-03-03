import random
import names
import time
from os import system, name
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
    # TODO: CHANGE GUESS TO WAGER

    def __init__(self, name=None, human=True):
        self.human = human
        if self.human:
            self.name = input('Enter name: ')
            self.eval_wager = self.human_eval_wager
        else:
            self.name = name if name else names.get_first_name()
            # ASSIGN WAGER FUNCTION
            # TODO: RANDOM FOR COMPUTER
            ai = [self.ai_eval_1,
                  self.ai_eval_2,
                  self.ai_eval_3]
            self.eval_wager = ai[random.randint(0, len(ai)-1)]
        self.active = True
        self.dice = []

    def show_dice(self):
        print(' '.join(str(d.state) for d in self.dice))

    def human_eval_wager(self, wager):
        # TODO: CORRECT PLURAL, SPELL DIE STATE
        q = f'CURRENT WAGER: {wager["dice"]} {wager["state"]}s\n'
        q += '(c)all or (b)id?\n'
        action = input(q)
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

    def ai_eval_1(self, wager):
        # ALWAYS INCREMENT NUMBER OF DICE BY 1
        self.guess = dict(wager)
        self.guess['dice'] += 1
        return self.guess

    def ai_eval_2(self, wager):
        # ALWAYS CALL
        self.guess = dict(wager)
        return self.guess

    def ai_eval_3(self, wager):
        if wager['state'] < self.dice[0].sides:
            # INCREASE DIE
            self.guess = {'dice': 1, 'state': wager['state'] + 1}
            return self.guess
        else:
            # EITHER INCREMENT OR CALL
            if random.randint(0, 1):
                self.guess = self.ai_eval_1(wager)
            else:
                self.guess = self.ai_eval_2(wager)
            return self.guess

    def get_wager(self):
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
            clear()
            print(f"{p.name}'s turn")
            # MOVE TO TURN?
            # TAKE IN WAGER, COMPARE TO PREVIOUS
            p.show_dice()
            if not self.wager:
                self.wager = p.get_wager()
            elif p.eval_wager(self.wager) == self.wager:
                print(f'{p.name} CALLS!')
                if self.check_wager(prev_p.guess):
                    p.lose()
                else:
                    prev_p.lose()
                break
            else:
                self.wager = p.guess
                print(f'{p.name} BIDS {self.wager["dice"]} '
                      f'{self.wager["state"]}')
            prev_p = p
            if not p.human:
                time.sleep(2.5)

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
        # SET UP HUMAN PLAYER(S)
        self.players.append(Player(human=True))
        for j in range(0, dice_per):
            self.players[0].dice.append(Die(sides))
        # SET UP AI PLAYER(S)
        for i in range(1, no_players):
            self.players.append(Player(human=False))
            for j in range(0, dice_per):
                self.players[i].dice.append(Die(sides))

    def play(self):
        while self.no_dice > 1:
            # TODO: START WITH LOSING PLAYER
            r = Round(self)
            # ONLY PLAY ACTIVE PLAYERS
            r.play(self.players)
            r.print_results()
            print(f'{self.no_dice} dice remaining.')
            input('\nPress Enter to continue...')

    @property
    def all_dice(self):
        d = []
        for i in range(0, len(self.players)):
            d.extend(self.players[i].dice)
        return d

    @property
    def no_dice(self):
        return len(self.all_dice)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    # TODO: INPUT NUMBER OF PLAYERS AND DICE
    Game(20, 4).play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print('Game cancelled.\n')
