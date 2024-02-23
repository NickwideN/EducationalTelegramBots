from dataclasses import dataclass, field


@dataclass
class User:
    user_id: int
    in_game: bool = False
    secret_number: int = None
    attempts: int = None
    total_games: int = 0
    wins: int = 0


_users = {}


def get_user(user_id):
    if user_id not in _users:
        _users[user_id] = User(user_id)
    return _users[user_id]

