import random
import names
import time
import inflect
from os import system, name
from itertools import cycle
# TODO: CONSIDER USING PYINQUIRER


words = inflect.engine()
words.defnoun('two', 'twos')


class Die:
    """A class representing a die"""

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        self.state = random.randint(1, self.sides)
        return self.state


class Player:
    """A class representing a player"""
    # TODO: CONSIDER CHANGING TO SUBCLASSES

    def __init__(self, game, human=True):
        self.game = game
        self.human = human
        if self.human:
            self.init_human()
        else:
            self.init_ai()
        self.active = True
        self.dice = []

    def init_human(self):
        self.name = input('Enter name: ')
        self.eval_wager = self.human_eval_wager

    def init_ai(self):
        self.dice_guess = {}
        self.name = names.get_first_name()
        # ASSIGN WAGER FUNCTION
        self.confidence = random.random()
        ai = [self.ai_incr,
              self.ai_call,
              self.ai_eval_3,
              self.ai_eval_4,
              self.ai_eval_5,
              ]
        self.eval_wager = random.choice(ai)
        self.dice_guess = self.ai_dice_1

    def show_dice(self):
        print(' '.join(str(d.state) for d in self.dice))

    def human_eval_wager(self, wager):
        t = words.number_to_words(wager['state'])
        t = words.plural(t, wager['dice'])
        q = f'CURRENT WAGER: {wager["dice"]} {t}\n'
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
            self.wager = new_wager
            return self.wager

    def ai_incr(self, wager, incr=1):
        # ALWAYS INCREMENT NUMBER OF DICE BY 1
        self.wager = dict(wager)
        self.wager['dice'] += incr
        return self.wager

    def ai_call(self, wager):
        # ALWAYS CALL
        self.wager = dict(wager)
        return self.wager

    def ai_eval_3(self, wager):
        # INCREASES STATE UNLESS SIX
        # BUG: PREVENT FROM BIDDING ZERO
        if wager['state'] < self.dice[0].sides:
            # INCREASE DIE
            dice = self.dice_guess()
            no_dice = dice[wager['state']]
            self.wager = {'dice': no_dice, 'state': wager['state'] + 1}
            return self.wager
        else:
            # EITHER INCREMENT OR CALL
            if random.getrandbits(1):
                self.wager = self.ai_incr(wager)
            else:
                self.wager = self.ai_call(wager)
            return self.wager

    def ai_eval_4(self, wager):
        # RANDOMLY CHOOSE BETWEEN INCREASE STATE AND CALL
        if random.random() < self.confidence:
            return self.ai_eval_3(wager)
        else:
            return self.ai_call(wager)

    def ai_eval_5(self, wager):
        dice = self.dice_guess()
        if wager['dice'] < dice[wager['state']]:
            return self.ai_incr(wager)
        else:
            return self.ai_eval_4(wager)

    def ai_dice_1(self):
        dice = {}
        # VALUES OF OWN DICE
        dice[1] = sum(d.state == 1 for d in self.dice)
        for s in range(2, self.game.sides+1):
            dice[s] = sum(d.state == s for d in self.dice) + dice[1]
        # RANDOM VALUES FOR OPPONENT DICE
        for d in range(len(self.dice), self.game.no_dice):
            side = random.randint(1, self.game.sides)
            if side != 1:
                dice[side] += 1
            else:
                for s in range(1, self.game.sides+1):
                    dice[s] += 1
        return dice

    def get_wager(self):
        # MODIFY FOR COMPUTER
        v = int(input('Which value? '))
        while v > self.dice[0].sides:
            print(f'Value must be 1-{self.dice[0].sides}!')
            v = int(input('Which value? '))
        d = int(input('Number showing? '))
        self.wager = {'state': v, 'dice': d}
        return self.wager

    def lose(self):
        self.dice.pop()
        if len(self.dice):
            print(f'{self.name} lost one die!')
        else:
            self.active = False
            print(f'{self.name} ran out of dice!')
            self.active = False


class Human(Player):
    """An implementation of Player for Human players"""
    # TODO
    def __init__(self, game):
        # TODO: super.__init__()
        self.game = game
        self.human = True
        self.name = input('Enter name: ')
        self.active = True
        self.dice = []

    def eval_wager(self, wager):
        t = words.number_to_words(wager['state'])
        t = words.plural(t, wager['dice'])
        q = f'CURRENT WAGER: {wager["dice"]} {t}\n'
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
            self.wager = new_wager
            return self.wager

    def get_wager(self):
        v = int(input('Which value? '))
        while v > self.dice[0].sides:
            print(f'Value must be 1-{self.dice[0].sides}!')
            v = int(input('Which value? '))
        d = int(input('Number showing? '))
        self.wager = {'state': v, 'dice': d}
        return self.wager


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
            if not self.turn(p, prev_p):
                break
            prev_p = p
            if not p.human:
                time.sleep(2.5)

    def print_results(self):
        """Prints a table of all results"""
        for s in range(1, self.game.sides+1):
            print(f'{s}: {self.results[s]}')

    def turn(self, player, prev_p):
        clear()
        print(f"{player.name}'s turn".upper())
        if player.human:
            player.show_dice()
        if not self.wager:
            self.wager = player.get_wager()
        elif player.eval_wager(self.wager) == self.wager:
            print(f"{player.name} calls!".upper())
            if self.check_wager(prev_p.wager):
                player.lose()
            else:
                prev_p.lose()
            return False
        else:
            self.wager = player.wager
            t = words.number_to_words(self.wager['state'])
            if player.wager['dice'] > 1:
                t = words.plural(t)
            print(f'{player.name} bids {self.wager["dice"]} {t}'.upper())
        return True

    def check_wager(self, wager):
        return self.results[wager['state']] >= wager['dice']


class Game:
    """A class representing a game of Liar's Dice"""

    def __init__(self, no_dice, no_players, sides=6):
        self.sides = sides
        # RAISE EXCEPTION IF DICE DOES NOT DIVIDE AMONG PLAYERS
        while no_dice % no_players:
            print("Dice cannot be evenly distributed. Enter quantities again.")
            no_dice = int(input("Number of dice: "))
            no_players = int(input("Number of players: "))
        self.players = []
        # DIVIDE DICE AMONG PLAYERS
        dice_per = int(no_dice/no_players)
        # SET UP HUMAN PLAYER(S)
        self.players.append(Human(game=self))
        for j in range(0, dice_per):
            self.players[0].dice.append(Die(sides))
        # SET UP AI PLAYER(S)
        for i in range(1, no_players):
            self.players.append(Player(game=self, human=False))
            for j in range(0, dice_per):
                self.players[i].dice.append(Die(sides))

    def play(self):
        while len(self.active_players) > 1:
            # BUG: FIRST COMPUTER PLAYER REMAINING TAKES BID
            # Need to create method for ai to create initial bid
            # TODO: START WITH LOSING PLAYER
            r = Round(self)
            # ONLY PLAY ACTIVE PLAYERS
            r.play(self.active_players)
            r.print_results()
            print(f'{self.no_dice} dice remaining.')
            if len(self.active_players) > 1:
                input('\nPress Enter to continue...')
            else:
                winner = self.active_players[0]
                print(f'{winner.name} wins! Game over.')

    @property
    def all_dice(self):
        d = []
        for i in range(0, len(self.players)):
            d.extend(self.players[i].dice)
        return d

    @property
    def no_dice(self):
        return len(self.all_dice)

    @property
    def active_players(self):
        return [p for p in self.players if p.active]


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
