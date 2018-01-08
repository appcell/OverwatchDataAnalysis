SUBJECT = [
    'subject player',
    'subject hero',
]

OBJECT = [
    'object player',
    'object hero',
]

SUPPLEMENT = [
    'ability',
    'critical kill',
]

ASSIST = [
    'a player 1',
    'a hero 1',
    'a player 2',
    'a hero 2',
    'a player 3',
    'a hero 3',
    'a player 4',
    'a hero 4',
    'a player 5',
    'a hero 5',
]

TITLE = [
    'time',
    'action',
] + SUBJECT + OBJECT + SUPPLEMENT + ASSIST

PRINT_DATA_FORMAT = {t: i+1 for i, t in enumerate(TITLE)}

TITLE_TOP = [
    '',
    '',
    'subject',
    '',
    'object',
    '',
    '',
    '',
    'assist 1',
    '',
    'assist 2',
    '',
    'assist 3',
    '',
    'assist 4',
    '',
    'assist 5',
    '',
    'PS',
]

TITLE_TOP_MERGE_CELL = {
    '': None,
    'subject': 'C1:D1',
    'object': 'E1:F1',
    'assist 1': 'I1:J1',
    'assist 2': 'K1:L1',
    'assist 3': 'M1:N1',
    'assist 4': 'O1:P1',
    'assist 5': 'Q1:R1',
    'PS': 'S1:S2',
}


DIMENSIONS = {
    'time': 'A',
    'action': 'B',
    'subject player': 'C',
    'subject hero': 'D',
    'object player': 'E',
    'object hero': 'F',
    'ability': 'G',
    'critical kill': 'H',
    'a player 1': 'I',
    'a hero 1': 'J',
    'a player 2': 'K',
    'a hero 2': 'L',
    'a player 3': 'M',
    'a hero 3': 'N',
    'a player 4': 'O',
    'a hero 4': 'P',
    'a player 5': 'Q',
    'a hero 5': 'R',
    'PS': 'S',
}

PLAYER_WIDTH_CONFIG = {DIMENSIONS['a player {}'.format(i)]: 14 for i in range(1, 6)}
HERO_WIDTH_CONFIG = {DIMENSIONS['a hero {}'.format(i)]: 13 for i in range(1, 6)}
CELL_WIDTH_CONFIG = {
    DIMENSIONS['time']: 16.5,
    DIMENSIONS['action']: 20,
    DIMENSIONS['subject player']: 18,
    DIMENSIONS['subject hero']: 14,
    DIMENSIONS['object player']: 18,
    DIMENSIONS['object hero']: 14,
    DIMENSIONS['ability']: 14,
    DIMENSIONS['critical kill']: 14,
    DIMENSIONS['PS']: 23,
}
CELL_WIDTH_CONFIG.update(PLAYER_WIDTH_CONFIG)
CELL_WIDTH_CONFIG.update(HERO_WIDTH_CONFIG)

API_CHANGE_CONFIG = {
    'time': 'time',
    'event': 'action',
    'character1': 'subject hero',
    'character2': 'object hero',
}
