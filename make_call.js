require('dotenv').config();
const twilio = require('twilio');

function makeCall(to, zip){
    const accountSid   = process.env.ACCOUNT_SID;
    const authToken    = process.env.AUTH_TOKEN;
    const server       = process.env.SERVER;
    const client = twilio(accountSid, authToken);

    action = `${server}/choose_option`
    instructions = ` \
    <Response> \
        <Say voice="alice">Thank you for calling Global News.</Say> \
        <Gather action="${action}" numDigits="3" timeout="10"> \
            <Say voice="alice">Please select 1 for trending local news, 2 for trending world news, 3 if you have a specific query, or 4 to repeat these options.</Say> \
        </Gather> \
    </Response> \
    `
    // Make the initial outgoing call
    client.calls.create({
    //   url: server+'/choose_option',
      to: to,
      from: "+18449504572",
      twiml: instructions,
    })
    .then(call => console.log(call.sid))
    .catch(error => console.log(error));
}

module.exports = { makeCall };