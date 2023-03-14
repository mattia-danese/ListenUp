# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from dotenv import load_dotenv
import os


def make_call(to, zip):

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables
    load_dotenv()
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    
    client = Client(account_sid, auth_token)
    ngronk_link = "https://8747-73-159-114-175.ngrok.io"

    action = f"{ngronk_link}/choose_option"
    instructions = f''' 
    <Response>
        <Say voice="alice">Thank you for calling Global News.</Say>
        <Gather action="{action}" numDigits="3" timeout="10">
            <Say voice="alice">Please select 1 for trending local news, 2 for trending world news, 3 if you have a specific query, or 4 to repeat these options.</Say>
        </Gather>
    </Response>
    '''

    call = client.calls.create(
        twiml=instructions,
        to=to,
        from_='+18449504572'
    )

    print(call.sid)
