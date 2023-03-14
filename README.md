# ListenUp
How to run:
- In one terminal run: `./ngrok http 5000`
- Copy the `Forwarding` URL into the `ngronk_link` variable in `answer_phone.py` and `make_call.py`
- Set the `A CALL COMES IN` field in the Twilio Console to the `Forwarding` URL and add the `/answer` suffix
- In another terminal run: `python3 answer_phone.py`
