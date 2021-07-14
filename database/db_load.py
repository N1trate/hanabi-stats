from database.db_schema import Game, Card, GameAction, PlayerNotes
from database.db_connect import session


def load_game(g):
    g_id = g['id']
    try:
        opt = g['options']
        try:
            var = opt['variant']
        except KeyError:
            var = None
        try:
            starting_player = opt['startingPlayer']
        except KeyError:
            starting_player = None
        try:
            speedrun = opt['speedrun']
        except KeyError:
            speedrun = None
    except KeyError:
        var = None
        starting_player = None
        speedrun = None
    game = Game(
        g_id,
        g['players'],
        var,
        starting_player,
        speedrun,
        g['seed']
    )
    session.add(game)


def load_deck(g):
    deck = g['deck']
    seed = session.query(Card.seed) \
        .filter(Card.seed == g['seed'])\
        .first()
    print(g['id'])
    if seed is not None:
        return
    for i in range(len(deck)):
        card = Card(
            g['seed'],
            i,
            deck[i]['suitIndex'],
            deck[i]['rank']
        )
        session.add(card)


def load_actions(g):
    g_id = g['id']
    actions = g['actions']
    for i in range(len(actions)):
        action = GameAction(
            g_id,
            i,
            actions[i]['type'],
            actions[i]['target'],
            actions[i]['value'],
        )
        session.add(action)


def load_notes(g):
    g_id = g['id']
    try:
        game_notes = g['notes']
        for i in range(len(game_notes)):
            player_notes = PlayerNotes(
                g_id,
                g['players'][i],
                game_notes[i]
            )
            session.add(player_notes)
    except KeyError:
        return


def load_column(g):
    g_id = g['id']
    try:
        opt = g['options']
        starting_player = opt['startingPlayer']
    except KeyError:
        starting_player = None
    game = session.query(Game).filter(Game.game_id == g_id).first()
    game.starting_player = starting_player
