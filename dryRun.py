import math
import random
import requests
import json

def run_competition():
    baseline = 60
    maxScore = 100

    # Calculate the score for the player (Chris)
    minutesStudied = 40  # You can change this value

    # Define a baseline effort for all bots
    baselineEffort = 10

    # Define bot personalities and their effort factors
    botPersonalities = {
        "diligent": {"effortFactor": 1.2, "probability": 0.15},  # Diligent bots make more effort but are less common
        "lazy": {"effortFactor": 0.8, "probability": 0.5},  # Lazy bots make less effort and are more common
        "distracted": {"effortFactor": 0.6, "probability": 0.2},  # Easily distracted bots make even less effort and are more common
        "depressed": {"effortFactor": 0.1, "probability": 0.15},  # Depressed bots make very minimal effort and are not so common
    }

    def getRandomPersonality(botPersonalities):
        totalProbability = sum([personality["probability"] for personality in botPersonalities.values()])
        random_num = random.random() * totalProbability
        accumulatedProbability = 0
        for personality in botPersonalities:
            accumulatedProbability += botPersonalities[personality]["probability"]
            if random_num < accumulatedProbability:
                return personality

    # Fetch the bots data from the local JSON file
    with open('bots.json','r',encoding='utf-8') as f:
        bots = json.load(f)

    # Create a dictionary to store the total scores
    total_scores = {bot["name"]: 0 for bot in bots}

    chrisScore = math.sqrt(minutesStudied / baseline) * maxScore

    # Run the competition for 30 days
    for day in range(30):
        print(f"Day {day + 1} of competition")

        # Create an entry for each bot
        for bot in bots:
            botName = bot["name"]
            # Generate a random score with a minimum baseline effort
            botEffort = max(random.random() * maxScore, baselineEffort)

            # Choose a personality for the bot based on real-world probabilities
            randomPersonality = getRandomPersonality(botPersonalities)
            effortFactor = botPersonalities[randomPersonality]["effortFactor"]

            # Calculate bot points with adjusted effort
            botPoints = math.pow(botEffort / baseline, 2) * maxScore * effortFactor

            # If the bot's name is "Christian", use chrisScore instead of botPoints
            finalPoints = round(chrisScore, 2) if botName == "christian" else round(botPoints, 2)

            # Add the points to the bot's total score
            total_scores[botName] += finalPoints
            
            # If it's the last day of the competition, sort the total scores by score in descending order
            if day == 29:  # 0-indexed, so day 29 is the 30th day
                total_scores = dict(sorted(total_scores.items(), key=lambda item: item[1], reverse=True))

        # Write the results of the day to a text file
        with open('results.txt', 'a') as f:
            f.write(f"Day {day + 1} results:\n")
            for botName, points in total_scores.items():
                f.write(f"{botName}: {points}\n")
            f.write("\n")

    # Create an array of entries with the total scores
    entries = [{"element": botName, "points": int(points)} for botName, points in total_scores.items()]

    # Sort the entries array by points in descending order
    entries.sort(key=lambda x: x["points"], reverse=True)

    # Create an array of country data
    countries = [{"name": bot["name"], "bots": bot["emoji"]} for bot in bots]

    # response = requests.post('https://483d8b.pythonanywhere.com/addScore', headers={'Content-Type': 'application/json'}, data=json.dumps([{"country": entry["element"], "points": entry["points"], "league": "Bronze"} for entry in entries]))

    # data = response.json()
    # print(data)

# Call the function to run the competition
run_competition()
