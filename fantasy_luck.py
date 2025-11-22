import csv
import matplotlib.pyplot as plt


def load_data(filename):
    """
    Read the fantasy football CSV file and build the following:
    - scores: team -> list of weekly scores
    - actual_wins: team -> number of real wins
    """
    scores = {}
    actual_wins = {}

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)            # skip header

        for week, team1, points1_str, team2, points2_str in reader:
            points1 = float(points1_str)
            points2 = float(points2_str)

            for team in (team1, team2):
                if team not in scores:
                    scores[team] = []
                    actual_wins[team] = 0

            # weekly scores
            scores[team1].append(points1)
            scores[team2].append(points2)

            # update actual_wins
            if points1 > points2:
                actual_wins[team1] += 1
            elif points2 > points1:
                actual_wins[team2] += 1

    return scores, actual_wins


def compute_expected_wins(scores):
    """
    Compute expected wins for each team by comparing weekly scores
    to all other teams' weekly scores in the same week.
    """
    teams = list(scores.keys())
    
    # use first team to find out how many weeks there are
    first_team = teams[0]
    num_weeks = len(scores[first_team])

    # expected wins start at 0
    expected_wins = {}
    for team in teams:
        expected_wins[team] = 0.0
    
    # go week by week
    for week in range(num_weeks):
        weekly_scores = {}
        for team in teams:
            weekly_scores[team] = scores[team][week]

        # comparing every team to every other team
        for team in teams:
            team_score = weekly_scores[team]
            beats = 0

            for other in teams:
                if other == team:
                    continue
                if team_score > weekly_scores[other]:
                    beats += 1
            
            # fractional expected wins
            expected_wins[team] += beats / (len(teams) - 1)

    return expected_wins


def compute_luck(actual_wins, expected_wins):
    """
    Compute_luck = actual_wins - expected_wins for each team
    Positive = lucky
    Negative = unlucky
    """
    luck = {}
    for team in actual_wins:
        luck[team] = actual_wins[team] - expected_wins[team]
    return luck


def plot_luck_scores(luck):
    """
    Makes a bar chart of luck scores for each team.
    Saves the plot as luck_scores.png
    """
    # sorting teams
    teams_sorted = sorted(luck.keys(), key=lambda team: luck[team], reverse=True)
    luck_values = [luck[team] for team in teams_sorted]

    colors = ["green" if value > 0 else "red" for value in luck_values]

    plt.figure(figsize=(10, 6))
    plt.bar(teams_sorted, luck_values, color = colors)
    plt.axhline(0, linewidth=1)
    plt.title("Luck Scores by Team (Actual Wins - Expected Wins)")
    plt.ylabel("Luck Score")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig("luck_scores.png")
    plt.show()


def plot_actual_vs_expected(actual_wins, expected_wins):
    """
    Makes a bar chart comparing actual and expected wins for each team.
    Saves the plot as wins_comparison.png
    """
    # alphabetical sort
    teams = sorted(actual_wins.keys())
    actual = [actual_wins[team] for team in teams]
    expected = [expected_wins[team] for team in teams]

    x = range(len(teams))
    width = 0.25

    actual_color = "navy"
    expected_color = "orange"

    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in x], actual, width=width, label="Actual Wins", color = actual_color)
    plt.bar([i + width/2 for i in x], expected, width=width, label="Expected Wins", color = expected_color)

    plt.title("Actual vs Expected Wins by Team")
    plt.ylabel("Wins")
    plt.xticks(x, teams, rotation=45, ha="right")
    plt.legend(loc="upper center")

    plt.tight_layout()
    plt.savefig("wins_comparison.png")
    plt.show()


if __name__ == "__main__":
    filename = "fantasy_luck_data.csv"
    scores, actual_wins = load_data(filename)
    expected_wins = compute_expected_wins(scores)
    luck = compute_luck(actual_wins, expected_wins)

    # data viz
    plot_luck_scores(luck)
    plot_actual_vs_expected(actual_wins, expected_wins)
