
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'state_R_introduction'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class R_intro_info(Page):
    form_model = 'player'
class MyWaitPage(WaitPage):
    pass
page_sequence = [R_intro_info, MyWaitPage]