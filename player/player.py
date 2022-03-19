import random
import names
import inflect


# TRY MOVING TO OTHER DIRECTORY
words = inflect.engine()
words.defnoun('two', 'twos')


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
