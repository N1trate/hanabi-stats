from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.types import ARRAY

db_name = 'hanabi_db'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'localhost'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
Session = sessionmaker(bind=db)
Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'
    game_id = Column(Integer, primary_key=True)
    num_players = Column(Integer)
    players = Column(ARRAY(String))
    starting_player = Column(Integer)
    variant_id = Column(Integer)
    variant = Column(String)
    timed = Column(Boolean)
    time_base = Column(Integer)
    time_per_turn = Column(Integer)
    speedrun = Column(Boolean)
    card_cycle = Column(Boolean)
    deck_plays = Column(Boolean)
    empty_clues = Column(Boolean)
    one_extra_card = Column(Boolean)
    one_less_card = Column(Boolean)
    all_or_nothing = Column(Boolean)
    detrimental_characters = Column(Boolean)
    score = Column(Integer)
    num_turns = Column(Integer)
    end_condition = Column(Integer)
    date_time_started = Column(DateTime)
    date_time_finished = Column(DateTime)
    num_games_on_this_seed = Column(Integer)
    tags = Column(String)
    seed = Column(String)

    def __init__(self, game_id, num_players, players, starting_player, variant_id, variant, timed, time_base,
                 time_per_turn, speedrun, card_cycle, deck_plays, empty_clues, one_extra_card, one_less_card,
                 all_or_nothing, detrimental_characters, score, num_turns, end_condition, date_time_started,
                 date_time_finished, num_games_on_this_seed, tags, seed):
        self.game_id = game_id
        self.num_players = num_players
        self.players = players
        self.starting_player = starting_player
        self.variant_id = variant_id
        self.variant = variant
        self.timed = timed
        self.time_base = time_base
        self.time_per_turn = time_per_turn
        self.speedrun = speedrun
        self.card_cycle = card_cycle
        self.deck_plays = deck_plays
        self.empty_clues = empty_clues
        self.one_extra_card = one_extra_card
        self.one_less_card = one_less_card
        self.all_or_nothing = all_or_nothing
        self.detrimental_characters = detrimental_characters
        self.score = score
        self.num_turns = num_turns
        self.end_condition = end_condition
        self.date_time_started = date_time_started
        self.date_time_finished = date_time_finished
        self.num_games_on_this_seed = num_games_on_this_seed
        self.tags = tags
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


Base.metadata.create_all(db)
session = Session()
session.commit()

# delete from games where 1 = 1
