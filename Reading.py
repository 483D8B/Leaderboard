import math
import random
import requests
import json
import re
from datetime import datetime, timedelta
import sys

# Check if today is the last day of the month
def is_last_day_of_month():
    today = datetime.today().date()
    # If the next day's month is not equal to today's, it means today is the last day of the month
    return (today + timedelta(days=1)).month != today.month

sheetID = '1db4uqW7hlrYwvUXxOg1kXIHH0RoSYRzlIfGpyUNIYs4'
base = f'https://docs.google.com/spreadsheets/d/{sheetID}/gviz/tq?'
sheetName = '2024'
query = 'Select *'
url = f'{base}&sheet={sheetName}&tq={query}'
data = []
year = '2024'

response = requests.get(url)
response_text = response.text
jsData = json.loads(response_text[47:-2])
colz = []
for heading in jsData['table']['cols']:
    if 'label' in heading:
        colz.append(heading['label'].lower().replace(' ', ''))

for main in jsData['table']['rows']:
    row = {}
    for ele, ind in zip(colz, range(len(colz))):
        if ele == 'date' and main['c'][ind] is not None:
            # Parse the date format
            match = re.match(r'Date\((\d+),(\d+),(\d+)\)', main['c'][ind]['v'])
            if match:
                year, month, day = map(int, match.groups())
                row[ele] = datetime(year, month + 1, day).strftime('%d-%b-%Y')
            else:
                row[ele] = ''
        else:
            row[ele] = main['c'][ind]['v'] if main['c'][ind] is not None else ''
    data.append(row)

# Get today's date in the format of the Google Sheet
today = datetime.now().strftime('%d-%b-%Y')

# Find the minutes of study for today
minutesStudied = None
for record in data:
    if record['date'] == today:
        minutesStudied = record['minutesofstudy']
        break

if minutesStudied is None or minutesStudied == '':
    print(f"No meaningful value found for {today} in the Google Sheets")
    sys.exit(1)  # Exit the script
    

baseline = 60
maxScore = 100

# Define a baseline effort for all bots
baselineEffort = 10

#random.seed('pimpa')

# Define bot personalities and their effort factors
botPersonalities = [
    ("diligent", 1.2, 0.15),
    ("lazy", 0.8, 0.5),
    ("distracted", 0.6, 0.2),
    ("depressed", 0.1, 0.15),
]

totalProbability = sum(personality[2] for personality in botPersonalities)

def getRandomPersonality():
    return random.choices(botPersonalities, weights=[personality[2] for personality in botPersonalities], k=1)[0]

# Fetch the bots data from the local JSON file
with open('bots.json','r',encoding='utf-8') as f:
    bots = json.load(f)

chrisScore = math.sqrt(minutesStudied / baseline) * maxScore

# Create an entry for each bot
entries = []
for bot in bots:
    botName = bot["name"]
    if botName == "christian":
        finalPoints = round(chrisScore, 2)
    else:
        # Generate a random score with a minimum baseline effort
        botEffort = max(random.random() * maxScore, baselineEffort)

        # Choose a personality for the bot based on real-world probabilities
        _, effortFactor, _ = getRandomPersonality()

        # Calculate bot points with adjusted effort
        botPoints = math.pow(botEffort / baseline, 2) * maxScore * effortFactor
        finalPoints = round(botPoints, 2)

    # Add the entry to the entries array
    entries.append({"element": botName, "points": int(finalPoints)})

# Sort the entries array by points in descending order
entries.sort(key=lambda x: x["points"], reverse=True)

response = requests.post('https://483d8b.pythonanywhere.com/addScore/japBoard', headers={'Content-Type': 'application/json'}, data=json.dumps([{"country": entry["element"], "points": entry["points"], "league": "1"} for entry in entries]))

data = response.json()
print(data)
