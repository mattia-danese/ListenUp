# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


def make_call(to, zip):

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC393095068bbebf913fc0ad98f0f1b929'
    auth_token = '62ceb6dd15058054d5729ae5e165a65f'
    client = Client(account_sid, auth_token)
    ngronk_link = "https://2937-2601-189-8000-5006-fd87-aaf7-9aed-903f.ngrok.io"

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
