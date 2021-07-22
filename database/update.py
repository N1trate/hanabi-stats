import json
import logging

import database.db_load as d
import py.utils as u


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
hanabi_players = u.open_file('../temp/unnest_players_character_varying_.tsv')
for p in hanabi_players:
    try:
        stats = sorted(u.open_stats(p), key=lambda x: x['id'])
    except json.decoder.JSONDecodeError:
        logger.error(p)
        continue
    for s in stats:
        status = d.update_game(s)
        if status == -1:
            break
    d.session.commit()
    logger.info(p)
