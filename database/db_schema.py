from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.types import ARRAY
from database.db_connect import Base


class Game(Base):
    __tablename__ = 'games'
    game_id = Column(Integer, primary_key=True)
    players = Column(ARRAY(String))
    variant = Column(String)
    starting_player = Column(Integer)
    speedrun = Column(Boolean)
    seed = Column(String)

    def __init__(self, game_id, players, variant, starting_player, speedrun, seed):
        self.game_id = game_id
        self.players = players
        self.variant = variant
        self.starting_player = starting_player
        self.speedrun = speedrun
        self.seed = seed


class Card(Base):
    __tablename__ = 'decks'
    seed = Column(String, primary_key=True)
    card_index = Column(Integer, primary_key=True)
    suit_index = Column(Integer)
    rank = Column(Integer)

    def __init__(self, seed, card_index, suit_index, rank):
        self.seed = seed
        self.card_index = card_index
        self.suit_index = suit_index
        self.rank = rank


class GameAction(Base):
    __tablename__ = 'game_actions'
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    turn = Column(Integer, primary_key=True)
    # 0 - play, 1 - discard, 2 - color clue, 3 - rank clue, 4 - game over
    action_type = Column(Integer)
    # If a play or a discard, corresponds to the order of the the card that was played/discard
    # If a clue, corresponds to the index of the player that received the clue
    # If a game over, corresponds to the index of the player that caused the game to end
    target = Column(Integer)
    # If a play or discard, then 0 (as NULL)
    # If a color clue, then 0 if red, 1 if yellow, etc.
    # If a rank clue, then 1 if 1, 2 if 2, etc.
    # If a game over, then the value corresponds to the 'endCondition' values
    value = Column(Integer)

    def __init__(self, game_id, turn, action_type, target, value):
        self.game_id = game_id
        self.turn = turn
        self.action_type = action_type
        self.target = target
        self.value = value


class PlayerNotes(Base):
    __tablename__ = 'player_notes'
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    player = Column(String, primary_key=True)
    notes = Column(ARRAY(String))

    def __init__(self, game_id, player, notes):
        self.game_id = game_id
        self.player = player
        self.notes = notes
