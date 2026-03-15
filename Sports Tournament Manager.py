class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.wins = 0
        self.losses = 0

    def record_result(self, result, points_gained):
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        self.points += points_gained

    def __str__(self):
        return f"{self.name:<15} | W: {self.wins} L: {self.losses} | Pts: {self.points}"

class Match:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.score = (0, 0)
        self.played = False

    def play_match(self, home_score, away_score):
        self.score = (home_score, away_score)
        self.played = True
        
        # Logic to assign points
        if home_score > away_score:
            self.home_team.record_result("win", 3)
            self.away_team.record_result("loss", 0)
        elif away_score > home_score:
            self.away_team.record_result("win", 3)
            self.home_team.record_result("loss", 0)
        else:
            self.home_team.record_result("draw", 1)
            self.away_team.record_result("draw", 1)

class Tournament:
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.matches = []

    def add_team(self, team):
        self.teams.append(team)

    def schedule_match(self, team1_name, team2_name):
        t1 = next((t for t in self.teams if t.name == team1_name), None)
        t2 = next((t for t in self.teams if t.name == team2_name), None)
        if t1 and t2:
            new_match = Match(t1, t2)
            self.matches.append(new_match)
            return new_match
        return None

    def show_standings(self):
        print(f"\n--- {self.name} Standings ---")
        # Sort teams by points (highest first) using a lambda function
        sorted_teams = sorted(self.teams, key=lambda t: t.points, reverse=True)
        for team in sorted_teams:
            print(team)

def main():
    # 1. Initialize Tournament and Teams
    league = Tournament("Global Pro League")
    t1 = Team("Strikers FC")
    t2 = Team("Shadow Knights")
    t3 = Team("Titan United")

    league.add_team(t1)
    league.add_team(t2)
    league.add_team(t3)

    # 2. Schedule and Play Matches
    m1 = league.schedule_match("Strikers FC", "Shadow Knights")
    if m1: m1.play_match(2, 1)

    m2 = league.schedule_match("Shadow Knights", "Titan United")
    if m2: m2.play_match(0, 3)

    m3 = league.schedule_match("Titan United", "Strikers FC")
    if m3: m3.play_match(1, 1) # A draw

    # 3. Output results
    league.show_standings()

if __name__ == "__main__":
    main()