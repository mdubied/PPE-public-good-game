
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'state_T'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 6
    ALPHA = 2.5
    BETA = 2
    N_ROUNDS_B = 6
    N_ROUNDS_TABLE = 3
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    total_public = models.CurrencyField()
    total_private = models.CurrencyField()
    individual_return_from_public = models.CurrencyField()
def set_payoffs(group: Group):
    players = group.get_players()
    
    # compute the total investment in the public project and the different private projects
    group_contr_public = [p.contribution_public_project for p in players]
    group_contr_private = [p.contribution_private_project for p in players]
    group.total_public = sum(group_contr_public)
    group.total_private = sum(group_contr_private)
    
    # compute average investment
    avg_public = group.total_public / C.PLAYERS_PER_GROUP
    avg_private = group.total_private / C.PLAYERS_PER_GROUP
    
    # compute return on investment from public project, per player
    group.individual_return_from_public = C.BETA / C.PLAYERS_PER_GROUP * (group.total_public-group.total_private)
    
    # compute final payoff for each player, store the evolution in participant fields
    for player in players:
        # individual quantities
        player.participant.payoff = player.participant.payoff - player.contribution_private_project - player.contribution_public_project  + C.ALPHA * player.contribution_private_project + group.individual_return_from_public
        player.participant.wealth_evo.append(player.participant.payoff)
        player.participant.public_evo.append(player.contribution_public_project)
        player.participant.private_evo.append(player.contribution_private_project)
        player.participant.reputation_score_evo.append(0)
    
        # group quantities, stored in the participant fields
        player.participant.group_tot_private_evo.append(group_contr_private)
        player.participant.group_tot_public_evo.append(group_contr_public)
        player.participant.group_avg_private_evo.append(avg_private)
        player.participant.group_avg_public_evo.append(avg_public)
    
class Player(BasePlayer):
    contribution_public_project = models.CurrencyField(initial=0, label='How much do you invest in the public project?', max=10, min=0)
    contribution_private_project = models.CurrencyField(initial=0, label='How much do you invest in the private project?', max=10, min=0)
class T_contribute(Page):
    form_model = 'player'
    form_fields = ['contribution_private_project', 'contribution_public_project']
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        subsession = player.subsession
        group = player.group
        participant = player.participant
        players = group.get_players()
        overall_round = subsession.round_number+C.N_ROUNDS_B
        html = '<p> Here is a summary of the <b>last three rounds</b>.'
        html +='<table>'+\
            '<tr>'+\
            '<th>Round</th><th>Your investment in the private project</th>'+\
            '<th>Your investment in the public project</th>'+\
            '<th>Average investment in the private project</th>'+\
            '<th>Average investment in the public project</th>'+\
            '<th>Your wealth at the end of the round</th>'+\
            '</tr>'
        start_round_table = overall_round-C.N_ROUNDS_TABLE-1
        for r in range(start_round_table,overall_round-1):
            html += '<tr>' + \
            '<td>' + str(r+1) +\
            '</td><td>' + str(player.participant.private_evo[r]) +\
            '</td><td>' + str(player.participant.public_evo[r]) +\
            '</td><td>' + str(player.participant.group_avg_private_evo[r]) +\
            '</td><td>' + str(player.participant.group_avg_public_evo[r]) +\
            '</td><td>' + str(player.participant.wealth_evo[r+1]) +\
            '</td></tr>'
        html += '</table><p>'
        
        if subsession.round_number>1:
            html += '<p> Here are information about how the players invested in the <b>last round</b>. You are Player nr. ' + str(player.participant.id_in_session) +'.'
            html +='<table>'+\
                '<tr>'+\
                '<th>Player nr.</th><th>Player</th><th>Investment in the private project</th>'+\
                '<th>Investment in the public project</th>'+\
                '<th>Wealth at the end of the round</th>'+\
                '</tr>'
            for p in players:
                html += '<tr>' + \
                '<td>' + str(p.participant.id_in_session) +\
                '</td><td>' + str(p.participant.first_name) +\
                '</td><td>' + str(p.participant.private_evo[overall_round-2]) +\
                '</td><td>' + str(p.participant.public_evo[overall_round-2]) +\
                '</td><td>' + str(p.participant.wealth_evo[overall_round-1]) +\
                '</td></tr>'
            html += '</table><p>'
        else:
            html += '<p> You will see how people invested at the end of this round.'
        
        return dict(html=html,overall_round=overall_round)
    @staticmethod
    def error_message(player: Player, values):
        print('values is', values)
        total_contribution = values['contribution_private_project'] + values['contribution_public_project']
        if total_contribution > 10:
            return 'Error: You can invest a maximum of 10 points in total. You invested {} in total.'.format(total_contribution)
class T_ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
page_sequence = [T_contribute, T_ResultsWaitPage]