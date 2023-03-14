require('dotenv').config();
const http = require('http');
const express = require('express');
const twilio = require('twilio');
const urlencoded = require('body-parser').urlencoded;

const { makeCall } = require('./make_call.js');

const accountSid   = process.env.ACCOUNT_SID;
const authToken    = process.env.AUTH_TOKEN;
const server       = process.env.SERVER;

// Initialize Twilio client
const client = twilio(accountSid, authToken);

// Initialize Express web server
const app = express();

// Parse incoming POST params with Express middleware
app.use(urlencoded({ extended: false }));

app.post('/answer', (req, res) => {
    let resp = new twilio.twiml.VoiceResponse();
    resp.reject();

    console.log("From Number:", req.body.From);
    console.log("From ZIP::", req.body.FromZip);

    makeCall(req.body.From, req.body.FromZip);

    res.send(resp.toString());
});

// Twilio webhook endpoint to initiate the call
// app.post('/make-call', (req, res) => {
//   const twiml = new twilio.twiml.VoiceResponse();
//   twiml.say('Hello! What would you like to make a Wikipedia search for?');
//   twiml.gather({
//     input: 'speech',
//     action: '/read-wiki-article',
//     speechTimeout: 'auto',
//     language: 'en-US'
//   });
//   res.set('Content-Type', 'text/xml');
//   res.send(twiml.toString());
// });


// Define a route to process the user's input
// app.post('/process_input', (req, res) => {
//   const twiml = new twilio.twiml.VoiceResponse();
//   const input = req.body.Digits;

//   if (input && input.length === 2) {
//     twiml.say(`You entered ${input}. Thank you for your response.`);
//   } else {
//     twiml.say('Invalid input. Please try again.');
//     twiml.redirect('/start');
//   }

//   res.type('text/xml');
//   res.send(twiml.toString());
// });

// start the server
http.createServer(app).listen(24685, () => {
    console.log('Express server listening on port 24685');
});

