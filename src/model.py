from pydantic import BaseModel


class BaseIto(BaseModel):
    players: set[int] = set()
    cards: dict[int, int] = {}
    state: bool = False

    def join(self, user_id: int) -> bool:
        if user_id in self.players:
            return False
        else:
            self.players.add(user_id)
            return True
