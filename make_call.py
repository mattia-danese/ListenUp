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
    server = os.environ['SERVER']
    
    client = Client(account_sid, auth_token)

    action = f"{server}/choose_option"
    instructions = f''' 
    <Response>
        <Say voice="alice">Thank you for calling Global News.</Say>
        <Redirect method="GET">
            {server}/choose_option?Digits=Begin
        </Redirect>
    </Response>
    '''

    call = client.calls.create(
        twiml=instructions,
        to=to,
        from_='+18449504572'
    )

    print(call.sid)
