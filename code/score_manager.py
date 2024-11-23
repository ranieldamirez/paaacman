# Singleton
import csv
import os

class ScoreManager:
    _instance = None  # Private class attribute to hold the singleton instance

    @staticmethod
    def getInstance():  # Get Singleton Instance
        if ScoreManager._instance is None:
            ScoreManager()
        return ScoreManager._instance

    def __init__(self):
        if ScoreManager._instance is not None:  # If you try making another instance, raise an error
            raise Exception("This class is a singleton!")
        else:
            ScoreManager._instance = self  # Set singleton instance
        self.current_score = 0
        self.high_scores = []
        self.high_score_limit = 5  # Limit the number of high scores
        self.filename = "./resources/scores.csv"
        self.load_high_scores()

    def add_score(self, points):
        """Add points to the current score."""
        self.current_score += points

    def reset_score(self):
        """Reset the current score."""
        self.current_score = 0

    def get_current_score(self):
        """Return the current score."""
        return self.current_score

    def get_high_scores(self):
        """Return the high scores."""
        return self.high_scores

    def load_high_scores(self):
        """Load high scores from a file."""
        if not os.path.exists(self.filename):  # Handle missing file
            print(f"Warning: {self.filename} not found. Creating a new one.")
            self.create_default_scores()
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                self.high_scores = [
                    (row[0], int(row[1])) for row in reader
                ][:self.high_score_limit]
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []

    def create_default_scores(self):
        """Create a default high scores file if it doesn't exist."""
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Score"])  # Add a header row

    def sort_scores(self):
        """Sort the high scores in descending order."""
        self.high_scores.sort(key=lambda x: x[1], reverse=True)

    def update_high_scores(self, username, score):
        """Add or update the high score for a given username."""
        # Check if the user already exists in the high scores
        for i, (name, high_score) in enumerate(self.high_scores):
            if name == username:
                if score > high_score:
                    self.high_scores[i] = (username, score)
                break
        else:
            # Add a new entry if the username is not in the high scores
            self.high_scores.append((username, score))
        self.sort_scores()
        self.high_scores = self.high_scores[:self.high_score_limit]  # Keep only top scores
        self.save_high_scores()

    def save_high_scores(self):
        """Save high scores to the file."""
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Score"])  # Add a header row
            writer.writerows(self.high_scores)

    def record_score(self, username, score):
        """Record a new score."""
        if not username or not isinstance(score, int) or score < 0:
            print("Invalid username or score. Score not recorded.")
            return
        self.update_high_scores(username, score)

    def print_high_scores(self):
        """Print high scores in a formatted way (for debugging or display)."""
        print("High Scores:")
        for i, (username, score) in enumerate(self.high_scores, 1):
            print(f"{i}. {username}: {score}")


# Example Usage:
if __name__ == "__main__":
    manager = ScoreManager.getInstance()
    manager.record_score("Alice", 500)
    manager.record_score("Bob", 300)
    manager.record_score("Charlie", 400)
    manager.print_high_scores()
