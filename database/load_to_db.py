import json
import logging

import py.utils as ut
import database.db_load as d


def open_as_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = {}
        for line in file.readlines():
            try:
                line_dict = json.loads(line.rstrip())
                data[line_dict['id']] = line_dict
            except json.decoder.JSONDecodeError:
                print(line)
                exit()
        return data


def load_games(path):
    files = ut.files_in_dir(path)
    data = {}
    for f in files:
        print(f)
        data = data | open_as_json(f'{path}{f}')
    return data


def replace_symbols(name):
    return name.replace(' ', '%20')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# hanabi_players = ut.open_file('../output/unnest_players_character_varying_.tsv')
# for p in hanabi_players:
#     logger.info(p)
#     try:
#         p = replace_symbols(p)
#         stats = ut.open_stats(p)
#     except json.decoder.JSONDecodeError:
#         logger.error(p)
#         continue
#     for s in stats:
#         d.update_game(s)
#     d.session.commit()

dumps = '../temp/games_dumps/'

games = load_games(dumps)
for g in games.values():
    s = ut.open_stats_by_game_id(g['players'][0], g['id'])
    d.load_deck(g)
    d.load_game(g, s)
    d.load_actions(g)
    d.load_notes(g)
    d.session.commit()
    logger.info(g['id'])

d.session.close()
