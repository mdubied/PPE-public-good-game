
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'state_T_introduction'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    N_ROUNDS_B = 6
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class T_intro_info(Page):
    form_model = 'player'
class MyWaitPage(WaitPage):
    pass
page_sequence = [T_intro_info, MyWaitPage]