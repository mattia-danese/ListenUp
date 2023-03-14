require('dotenv').config();
const http = require('http');
const express = require('express');
const twilio = require('twilio');

const accountSid   = process.env.ACCOUNT_SID;
const authToken    = process.env.AUTH_TOKEN;
const server       = process.env.SERVER;

// Initialize Twilio client
const client = twilio(accountSid, authToken);

// Initialize Express web server
const app = express();

app.post('/answer', (req, res) => {
    let resp = new twilio.twiml.VoiceResponse();
    resp.reject();

    console.log("From Number:", req.values['From']);
    console.log("From ZIP::", req.values['FromZip']);

    // make_call(request.values['From'], request.values['FromZip'])

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
http.createServer(app).listen(3000, () => {
    console.log('Express server listening on port 3000');
});

// Make the initial outgoing call
// client.calls.create({
//   url: ngrok_url+'/make-call',
//   to: testPhone,
//   from: twilioPhone
// })
// .then(call => console.log(call.sid))
// .catch(error => console.log(error));