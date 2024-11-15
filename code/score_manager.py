# Singleton
import csv

class ScoreManager():
    _instance = None  # Private class attribute to hold the singleton instance

    @staticmethod
    def getInstance(): # Get Singleton Instance
        if ScoreManager._instance is None:
            ScoreManager()
        return ScoreManager._instance

    def __init__(self):
        if ScoreManager._instance is not None: # if you try making another instance raise error
            raise Exception("This class is a singleton!")
        else:
            ScoreManager._instance = self # set singleton instance
        self.current_score = 0
        self.high_scores = self.load_high_scores()

    def add_score(self, points):
        self.current_score += points

    def reset_score(self):
        self.current_score = 0

    def get_current_score(self):
        return self.current_score

    def get_high_scores(self):
        return self.high_scores
    
    # Load top 5 scores
    def load_high_scores(self, filename = "./resources/scores.csv"):
        top_scores = []
        with open(filename, mode = "r") as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row
            # Read only top 5 rows
            for i, row in enumerate(reader):
                if i < 5:
                    top_scores.append((row[0], int(row[1])))
                else:
                    break # stop after you read the top 5 scores
        return top_scores # returns a list of list items that have the username and scores of the top 5

    def sort_scores(filename="./resources/scores.csv"):
        # Read every score from file
        scores = []
        with open(filename, mode = "r") as file:
            reader = csv.reader(file)
            header = next(reader) # read header
            for row in reader:
                scores.append((row[0], int(row[1])))

        # Sort the scores in descending order
        scores.sort(key = lambda x: x[1], reverse = True)

        # Write everything back to the csv file
        with open(filename, mode = "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(scores)

    def record_score(self, username, score, filename = "./resources/scores.csv"):
        # Open the CSV file in append mode
        with open(filename, mode="a", newline = "") as file:
            writer = csv.writer(file)
            # Write the new username and score as a new row
            writer.writerow([username, score])

        self.sort_scores(filename)