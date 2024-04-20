const fetch = require('node-fetch');
const fs = require('fs');

const baseline = 60;
const maxScore = 100;
const minutesStudied = 60;

const chrisScore = Math.sqrt(minutesStudied / baseline) * maxScore;
const baselineEffort = 10;

const botPersonalities = {
    diligent: { effortFactor: 1.2, probability: 0.15 },
    lazy: { effortFactor: 0.8, probability: 0.5 },
    distracted: { effortFactor: 0.6, probability: 0.2 },
    depressed: { effortFactor: 0.1, probability: 0.15 },
};

fs.readFile('bots.json', 'utf8' , (err, data) => {
    if (err) {
        console.error('Error:', err);
        return;
    }
    const bots = JSON.parse(data);

    const entries = [];

    for (let i = 0; i < bots.length; i++) {
        const botName = bots[i].name;
        let botEffort = Math.max(Math.random() * maxScore, baselineEffort);

        const randomPersonality = getRandomPersonality(botPersonalities);
        const effortFactor = botPersonalities[randomPersonality].effortFactor;

        const botPoints = Math.pow(botEffort / baseline, 2) * maxScore * effortFactor;

        entries.push({ name: botName, points: botPoints.toFixed(2) });
    }

    entries.sort((a, b) => b.points - a.points);

    console.log(entries);

    fetch('https://483d8b.pythonanywhere.com/addScore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entries.map(entry => ({ country: entry.name, points: entry.points, league: 'Bronze' })))
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
});

function getRandomPersonality(botPersonalities) {
    const totalProbability = Object.values(botPersonalities).reduce((total, personality) => total + personality.probability, 0);
    let random = Math.random() * totalProbability;
    let accumulatedProbability = 0;
    for (let personality in botPersonalities) {
        accumulatedProbability += botPersonalities[personality].probability;
        if (random < accumulatedProbability) {
            return personality;
        }
    }
}
