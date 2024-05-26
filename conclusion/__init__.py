
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'conclusion'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    N_ROUNDS_B = 6
    N_ROUNDS_T = 6
    N_ROUNDS_R = 6
    N_ROUNDS_TABLE = 3
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def store_email(group: Group):
    players = group.get_players()
    for player in players:
        player.participant
class Player(BasePlayer):
    email = models.StringField(blank=True, label='Enter your email address if you are interested in receiving the results of the study.')
class Email(Page):
    form_model = 'player'
    form_fields = ['email']
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        subsession = player.subsession
        group = player.group
        participant = player.participant
        players = group.get_players()
        overall_round = subsession.round_number + C.N_ROUNDS_B + C.N_ROUNDS_T + C.N_ROUNDS_R
        
        # PLAYER SUMMARY ____________________________________________________
        html = '<p> Here is a summary of the <b>last three rounds</b>.'
        html +='<table>'+\
            '<tr>'+\
            '<th>Round</th><th>Your investment in the private project</th>'+\
            '<th>Your investment in the public project</th>'+\
            '<th>Average investment in the private project</th>'+\
            '<th>Average investment in the public project</th>'+\
            '<th>Your wealth at the end of the round</th>'+\
            '<th>Your reputation score at the end of the round</th>'+\
            '</tr>'
        start_round_table = overall_round-C.N_ROUNDS_TABLE-1
        for r in range(start_round_table,overall_round-1):
            html += '<tr>' + \
            '<td>' + str(r+1) +\
            '</td><td>' + str(player.participant.private_evo[r]) +\
            '</td><td>' + str(player.participant.public_evo[r]) +\
            '</td><td>' + str(player.participant.group_avg_private_evo[r]) +\
            '</td><td>' + str(player.participant.group_avg_public_evo[r]) +\
            '</td><td>' + str(player.participant.wealth_evo[r+1]) 
            if r > C.N_ROUNDS_B + C.N_ROUNDS_T-1:
                html += '</td><td>' + f'{player.participant.reputation_score_evo[r]:.2f}'
            else:
                html += '</td><td> - '
            html += '</td></tr>'
        html += '</table><p>'
        
        # ALL PLAYERS SUMMARY _______________________________________________
        html += '<p> Here are information about how the players invested in the <b>last round</b>. In addition, the last column shows the reputation score of each player.'
        html +='<table>'+\
            '<tr>'+\
            '<th>Player nr.</th><th>Player</th><th>Investment in the private project</th>'+\
            '<th>Investment in the public project</th>'+\
            '<th>Wealth at the end of the round</th>'+\
            '<th>Reputation score at the end of the round</th>'+\
            '</tr>'
        for p in players:
            html += '<tr>' + \
            '<td>' + str(p.participant.id_in_session) +\
            '</td><td>' + str(p.participant.first_name) +\
            '</td><td>' + str(p.participant.private_evo[overall_round-2]) +\
            '</td><td>' + str(p.participant.public_evo[overall_round-2]) +\
            '</td><td>' + str(p.participant.wealth_evo[overall_round-1])+\
            '</td><td>' + f'{p.participant.reputation_score_evo[overall_round - 2]:.2f}' +\
            '</td></tr>'
        html += '</table>'
        
        
        return dict(html=html,overall_round=overall_round)
class MyWaitPage(WaitPage):
    after_all_players_arrive = store_email
class ThankYou(Page):
    form_model = 'player'
page_sequence = [Email, MyWaitPage, ThankYou]