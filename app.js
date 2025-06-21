// frontend/app.js

const express = require('express');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

// Show form on page load
app.get('/', (req, res) => {
  res.render('index', { result: null, error: null });
});

// Handle form submit
app.post('/check', async (req, res) => {
  const { city, crop } = req.body;

  try {
    const response = await fetch(`http://127.0.0.1:5000/crop_health?city=${city}&crop=${crop}`);
    const data = await response.json();

    if (response.ok) {
      // Prepare the entry to store
      const entry = {
        city,
        crop,
        result: data
      };

      const filePath = path.join(__dirname, 'userstored.json');

      let fileData = [];

      // Check if file exists and read it

      if (fs.existsSync(filePath)) {
        const existingData = fs.readFileSync(filePath, 'utf8');
        if (existingData) {
          fileData = JSON.parse(existingData);
        }
      }

      // Add new entry

      fileData.push(entry);

      // Write back to file
      
      fs.writeFileSync(filePath, JSON.stringify(fileData, null, 2));

      res.render('index', { result: data, error: null });
    } else {
      res.render('index', { result: null, error: data.error });
    }
  } catch (err) {
    console.error('Fetch error:', err);
    res.render('index', { result: null, error: "Server Error" });
  }
});

app.listen(PORT, () => {
  console.log(`🌐 Frontend running at http://localhost:${PORT}`);
});
