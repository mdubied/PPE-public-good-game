from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='my_session', num_demo_participants=4, app_sequence=['state_B_introduction', 'state_B', 'state_T_introduction', 'state_T', 'state_R_introduction', 'state_R', 'conclusion'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['wealth_evo', 'private_evo', 'public_evo', 'group_tot_private_evo', 'group_tot_public_evo', 'group_avg_private_evo', 'group_avg_public_evo', 'reputation_score_evo', 'first_name', 'email']
SESSION_FIELDS = []
ROOMS = [dict(name='room_1', display_name='Room 1'), dict(name='room_2', display_name='Room 2'), dict(name='room_3', display_name='Room 3'), dict(name='room_4', display_name='Room 4'), dict(name='room_5', display_name='Room 5'), dict(name='room_6', display_name='Room 6'), dict(name='room_7', display_name='Room 7')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


