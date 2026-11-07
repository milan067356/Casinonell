import random
import math
import time
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Round:
    round_id: str
    crash_point: float
    start_time: float
    betting_ends: float
    status: str = "betting"
    bets: Dict[int, float] = field(default_factory=dict)
    cashed_out: Dict[int, float] = field(default_factory=dict)

class GameEngine:
    def __init__(self):
        self.current_round: Round | None = None
        self.round_counter = 0

    def generate_crash_point(self) -> float:
        r = random.random()
        if r < 0.08:
            return round(random.uniform(1.01, 1.38), 2)
        crash = (0.97 / (1 - r))
        crash = math.floor(crash * 100) / 100
        return min(max(crash, 1.01), 100.0)

    def start_new_round(self):
        self.round_counter += 1
        now = time.time()
        self.current_round = Round(
            round_id=f"R{self.round_counter}",
            crash_point=self.generate_crash_point(),
            start_time=now,
            betting_ends=now + 7,
            status="betting"
        )
        return self.current_round

    def place_bet(self, user_id: int, amount: float) -> bool:
        if not self.current_round or self.current_round.status != "betting":
            return False
        if time.time() > self.current_round.betting_ends:
            return False
        if amount < 5:
            return False
        self.current_round.bets[user_id] = amount
        return True

    def cash_out(self, user_id: int, current_mult: float) -> float | None:
        if not self.current_round:
            return None
        if user_id not in self.current_round.bets:
            return None
        if user_id in self.current_round.cashed_out:
            return None
        if self.current_round.status == "crashed":
            return None
        if current_mult >= self.current_round.crash_point:
            return None
        self.current_round.cashed_out[user_id] = current_mult
        return current_mult

    def get_public_state(self):
        if not self.current_round:
            return None
        r = self.current_round
        fake_players = [
            {"name": "Кирилл", "bet": 11.8, "avatar": "🏒"},
            {"name": "AM010_", "bet": 4.87, "avatar": "✨"},
            {"name": "Player_88", "bet": 25.0, "avatar": "🎯"},
            {"name": "NightWolf", "bet": 7.5, "avatar": "🐺"},
            {"name": "Luna", "bet": 15.0, "avatar": "🌙"},
        ]
        return {
            "round_id": r.round_id,
            "status": r.status,
            "crash_point": r.crash_point if r.status == "crashed" else None,
            "betting_left": max(0, r.betting_ends - time.time()),
            "fake_players": fake_players,
        }

engine = GameEngine()
