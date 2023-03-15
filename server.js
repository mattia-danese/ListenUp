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

const headlines = [
    "Delta Pilots Approve Contract Raising Pay by 34%",
    "Tesla Offers a New ‘Master Plan’ but Few Big Revelations",
    "Biden Challenged by Softening Public Support for Arming Ukraine",
    "Tesla Could Start Making Cars in Mexico Next Year, Governor Says",
    "Eric Adams to Shoppers: Drop that Mask",
    "New Japanese Rocket Is Destroyed During First Test Flight to Space",
    "Republican Votes Helped Washington Pile Up Debt",
    "Hearing on Covid’s Origins Promises Politics Mixed With Substance",
    "Biden Is Set to Detail $3 Trillion in Measures to Reduce Deficits",
    "D.C. Police Officer Who Shot Man in Car Is Charged With Murder"
]

const summaries = [
    "Pilots at Delta Air Lines have approved a new contract that will increase wages 34 percent by 2026 and includes improvements to scheduling, retirement and other benefits, raising the standard for contract negotiations underway at other large US airlines. The new contract is widely expected to influence pilot negotiations at American Airlines, United Airlines and Southwest Airlines. American said on Wednesday that the new Delta contract could put more pressure on other airlines to offer pilots better terms.",
    `Tesla said on Wednesday that it would build a factory in Mexico to manufacture an electric vehicle that would be significantly more affordable than any of the cars it sold now. "We didnâ€™t hear as much about market conditions in electric vehicles as we did about â€˜Here are some very grand goals we have for sustainable energy,â€™" said Tammy Madsen, a professor at the Leavey School of Business at Santa Clara University. President AndrÃ©s Manuel LÃ³pez Obrador of Mexico said on Tuesday that the company had decided to build the plant.`,
    `The share of Americans who think the United States has given too much to Ukraine has grown from 7 percent a year ago to 26 percent last month, according to the Pew Research Center. "It's this way with every foreign intervention," said Andy Surabian, a Republican strategist who has advised two outspoken Republican voices against Ukraine aid, Senator JD Vance of Ohio and Donald Trump Jr. "In the first few months, it's always popular. People don't like what Russia did; it's awful. But as time goes on, war weariness is a real thing, especially in this country, especially when voters aren't connecting what's happening in Ukraine with their own security."Although skepticism of Ukraine aid has grown on both sides of the aisle, the party breakdown has been striking. "Yes, there are a small number of members on Capitol Hill, in the House Republicans specifically, that have expressed publicly their concerns about support for Ukraine," he said at a recent briefing.`,
    `Tesla's new factory in the Mexican state of Nuevo LeÃ³n will cost $5 billion, will employ up to 7,000 people and could start churning out cars as early as next year, the state's governor said on Friday. Tesla announced this week that it planned an assembly plant in Mexico â€” its fifth worldwide â€” but provided few details about the investment, including how much it would spend, when construction would start, how many people would work at the factory or how the company would deal with regional water shortages. Tesla's factory will use recycled water, he added.`,
    `"Let's be clear, some of these characters going into stores that are wearing their mask, they're not doing it because they're afraid of the pandemic, they're doing it because they're afraid of the police," the mayor said in a television interview with PIX 11. Chief Maddrey said New Yorkers should think of dropping their masks as "a peace offering" and "a sign of safety for store workers.""When we walk in, we should take down our masks," the chief said. "We should let them know that they're not in any danger, any harm, that we're customers, we're here to help them."But as a crime prevention strategy, he acknowledged it might have shortcomings.`,
    `The Japanese space agency said on Tuesday that the country's newest rocket had failed minutes into its first demonstration flight, a technological setback as the country tries to build up its capabilities in space. Japan is not alone in having a new rocket fail on its first flight. A Chinese company, Landspace, lost its Zhuque-2 rocket on its first orbital flight in December.`,
    `The national debt has grown to $31. In those cases, on net, Republicans added slightly more to the debt than Democrats. Mr. Trump, by comparison, signed laws adding nearly $7 trillion to the debt in his four-year term, by the budget office's estimation.`,
    `All have said the virus may have accidentally escaped from a laboratory. Fauci is not on the witness list for Wednesday's hearing; in a brief interview, he said he was not asked to testify. Emails that have since been made public indicate that they consulted with virologists who had more experience studying coronaviruses and who said that the features that may initially have looked worrisome did not in fact suggest that the virus had been concocted in a lab.Some of those features of the virus were also identified in related coronaviruses in other species, strengthening the view that the features were not necessarily lab-made.`,
    `WASHINGTON â€” President Biden on Thursday will propose policies aimed at trimming federal budget deficits by $3 trillion over the next 10 years as his administration embraces the politics of debt reduction amid a fight with Republicans over raising the nation's borrowing limit, a senior administration official said on Wednesday. 41 trillion from $1. Through new laws he has signed and executive actions he has issued, Mr. Biden has approved policies that would add about $5 trillion to the national debt over a decade, according to estimates by the Committee for a Responsible Federal Budget in Washington.`,
    `A Washington, DC, police sergeant who fatally shot a man found unconscious at the wheel of a car has been charged with murder, according to a federal indictment unsealed on Tuesday. At the scene of the incident, the department has said, officers found Mr. Gilmore with his foot on the brake pedal of a running vehicle with the handgun visible in his waistband. In a statement on Tuesday, Matthew M. Graves, the United States attorney for the District of Columbia, said that criminal charges are not appropriate in the overwhelming majority of cases where officers use deadly force.`
]

app.post('/answer', (req, res) => {
    let resp = new twilio.twiml.VoiceResponse();
    resp.reject();

    console.log("From Number:", req.body.From);
    console.log("From ZIP::", req.body.FromZip);

    makeCall(req.body.From, req.body.FromZip);

    res.send(resp.toString());
});

app.post('/choose_option', (req, res) => {
    var option_chosen = req.body.Digits;
    let resp = new twilio.twiml.VoiceResponse();

    console.log("Number Pressed:", option_chosen);

    if(option_chosen == '4' || !['1', '2', '3'].includes(option_chosen)) {
        resp.say("Please select 1 for trending local news, 2 for trending world news, 3 if you have a specific query, or 4 to repeat these options.")
        
        resp.gather({
            action: `${server}/choose_option`
        });

        res.send(resp.toString());
        return;
    }

    if(option_chosen == '1'){
        console.log("LOCAL NEWS");

        resp.say("Here are the top trending local news headlines")
        resp.pause(1)

        // TODO: getting headlines
        // headlines = ["banana", "apple", "orange"]

        for(i=0; i < headlines.length; i++){
            resp.say(`Press ${i} to listen to ${headlines[i]}`);
        }
        
        resp.gather({
            action: `${server}/read_article`,
            finishOnKey: ''
        });

        res.send(resp.toString());
        return;
    }

    if(option_chosen == '2'){
        console.log("WORLD NEWS");

        resp.say("Here are the top trending world news headlines")
        resp.pause(1)

        // TODO: getting headlines
        // headlines = ["banana", "apple", "orange"]

        for(i=0; i < headlines.length; i++){
            resp.say(`Press ${i} to listen to ${headlines[i]}`);
        }
        
        resp.gather({
            action: `${server}/read_article`,
            finishOnKey: ''
        });

        res.send(resp.toString());
        return;
    }

    if(option_chosen == '3'){
        console.log("SPECIFIC QUERY");

        resp.say("What is your Specific Query?");
        resp.gather({
            action: `${server}/specific_query`
        });

        res.send(resp.toString());
        return;
    }

    res.end(resp.hangup());
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

// start the server
http.createServer(app).listen(24685, () => {
    console.log('Express server listening on port 24685');
});

