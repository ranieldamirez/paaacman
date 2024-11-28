import csv
import os

class ScoreManager:
    _instance = None

    @staticmethod
    def getInstance():
        if ScoreManager._instance is None:
            ScoreManager()
        return ScoreManager._instance

    def __init__(self):
        if ScoreManager._instance is not None:
            raise Exception("This class is a singleton!")
        ScoreManager._instance = self
        self.current_score = 0
        self.high_scores = []
        self.high_score_limit = 5
        self.filename = "./resources/scores.csv"
        self.load_high_scores()

    def add_score(self, points):
        self.current_score += points

    def reset_score(self):
        self.current_score = 0

    def get_current_score(self):
        return self.current_score

    def get_high_scores(self):
        return self.high_scores

    def load_high_scores(self):
        if not os.path.exists(self.filename):
            self.create_default_scores()
        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                self.high_scores = [(row[0], int(row[1])) for row in reader][:self.high_score_limit]
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []

    def create_default_scores(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Score"])

    def sort_scores(self):
        self.high_scores.sort(key=lambda x: x[1], reverse=True)

    def update_high_scores(self, username, score):
        for i, (name, high_score) in enumerate(self.high_scores):
            if name == username:
                if score > high_score:
                    self.high_scores[i] = (username, score)
                break
        else:
            self.high_scores.append((username, score))
        self.sort_scores()
        self.high_scores = self.high_scores[:self.high_score_limit]
        self.save_high_scores()

    def save_high_scores(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Score"])
            writer.writerows(self.high_scores)

    def record_score(self, username, score):
        if not username or not isinstance(score, int) or score < 0:
            print("Invalid username or score. Score not recorded.")
            return
        self.update_high_scores(username, score)

    def print_high_scores(self):
        print("High Scores:")
        for i, (username, score) in enumerate(self.high_scores, 1):
            print(f"{i}. {username}: {score}")
