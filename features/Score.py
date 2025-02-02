
class Score:

    MULTIPLIER = 1

    def __init__(self):
        self.score = 0

    def tick(self):
        # Lower the score on tick
        self.score -= 10 * self.MULTIPLIER

        self.score = max(self.score, 0)
    
    def bullet_fired(self):
        self.score -= 50 * self.MULTIPLIER
    
    def asteroid_hit(self, size):
        self.score += size * 1000 * self.MULTIPLIER
    
    def player_hit(self):
        self.score -= 1000 * self.MULTIPLIER
