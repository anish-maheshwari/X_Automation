const express = require('express');
const { exec } = require('child_process');
const MongoClient = require('mongodb').MongoClient;

const path = require('path'); // Adjust the path to where your index.html is located

const app = express();
const port = 3000;


// MongoDB connection setup
const uri = 'mongodb://localhost:27017';
const dbName = 'twitter_trends';
const collectionName = 'trends_data';

// Serve the index.html when accessing the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/index.html')); });

// Endpoint to trigger Python Selenium script
app.get('/run-scraping', (req, res) => {
    exec('python Project10.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Error running the script');
        }
        console.log(stdout);
        res.send('Scraping completed successfully!');
    });
});

// Endpoint to get trends data from MongoDB
app.get('/get-trends', async (req, res) => {
    try {
        const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection(collectionName);

        // Retrieve the latest trends
        const trendsData = await collection.find().sort({ date_time: -1 }).limit(1).toArray();
        res.json(trendsData[0] || {});
        client.close();
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching data');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
