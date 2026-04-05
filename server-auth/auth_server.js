const express = require('express');
const bodyParser = require('body-parser');
const { io } = require("socket.io-client");

const app = express();
app.use(bodyParser.json());

// Connect to the Python Bridge (running on port 5000)
const pythonBridge = io("http://localhost:5000");

// Mock Database for User Credentials
const USERS = { "rigel": "password123" };

// Login Endpoint
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (USERS[username] && USERS[username] === password) {
        // Return a session token upon successful login
        res.json({ success: true, token: "secure-session-token-001" });
    } else {
        res.status(401).json({ success: false, message: "Invalid credentials" });
    }
});

// Relay endpoint: Receives commands from the PyQt5 App and sends them to the Bridge
app.post('/robot/move', (req, res) => {
    const { token, linear, angular } = req.body;
    
    // Validate the token before processing the command
    if (token === "secure-session-token-001") {
        pythonBridge.emit("move_command", { linear, angular });
        res.json({ status: "Success", message: "Command relayed to MiRo" });
    } else {
        res.status(403).json({ error: "Unauthorized access" });
    }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Auth Server is running on port ${PORT}`));