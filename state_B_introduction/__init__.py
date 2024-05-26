
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'state_B_introduction'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    INITIAL_ENDOWMENT = cu(1000)
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def set_initial_values(group: Group):
    players = group.get_players()
    for player in players:
        # individual quantities
        player.participant.payoff = C.INITIAL_ENDOWMENT
        player.participant.wealth_evo = [C.INITIAL_ENDOWMENT]
        player.participant.public_evo = []
        player.participant.private_evo = []
        player.participant.reputation_score_evo = []
        player.participant.first_name = player.first_name
    
        # group quantities, stored in the participant fields
        player.participant.group_tot_public_evo = []
        player.participant.group_tot_private_evo = []
        player.participant.group_avg_public_evo = []
        player.participant.group_avg_private_evo = []
    
class Player(BasePlayer):
    first_name = models.StringField(label="Enter your name (first name is sufficient) and click 'Next'.")
class B_intro_info(Page):
    form_model = 'player'
    form_fields = ['first_name']
class MyWaitPage(WaitPage):
    after_all_players_arrive = set_initial_values
page_sequence = [B_intro_info, MyWaitPage]