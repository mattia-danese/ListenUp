#
# To-Do: Mark
#
# Integration with news-please:
#
# For the first stage of integration, we will have a directory full of json files
# pulled from news-please. There will be no Google search or dynamic fetching 
# for this initial stage.
#
# 1. On startup, our application will index the JSON files into an array,
#    `articles`, with the JSON content stored under each index.
# 
# 2. "Trending world news" and "Trending global news" will be replaced
#    with "Trending news", which is just the most recent 10 articles.
#
# 3. Article selection for trending news will remain the same.
#
# 4. For searching, the search term is split into words, and
#    article MAIN TEXT is searched for those words. Matching
#    articles will be ranked according to relevance. That list
#    of matched articles will be stored under a new variable,
#    `searches`, which is a map from: 
#        phone # -> list of matched articles
#
#    This way, when the user actually makes a selection (1-10),
#    the system can lookup what the searched articles were and
#    read the correct one.


# News-Please filtering steps for NYTimes:
# 1. Delete *.json files in the directory
# 2. Delete anything that doesn't start with "2023"
# 3. Delete "*crossword*"
#
# no need to filter by size. Every news article comes with 
# at least 5 sentences of maintext.


from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather, Redirect
from string import punctuation
from dotenv import load_dotenv
from summarize import summarize
import os
import json

from scan_articles import scan_articles, query_articles 

from make_call import make_call

app = Flask(__name__)
number = None
ZIP = None
query = None

# Use NYTimes articles for now
articles = scan_articles("./nytimes")

# Summarize articles
for article in articles:
    summarize(article['maintext'])

load_dotenv()
server = os.environ['SERVER']


# Answers the initial phone call.
# Rejects the call and makes an outgoing call.
@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    resp = VoiceResponse()
    resp.reject()

    print("From Number:", request.values['From'])
    print("From ZIP:", request.values['FromZip'])

    make_call(request.values['From'], request.values['FromZip'])

    return str(resp)

# Choose an option from the main menu.
@app.route("/choose_option", methods=['GET', 'POST'])
def choose_options(previous_chosen_option = None):
    print("Called: " + str(request.values['Called']))
    global option_chosen
    print("Request: " + str(dir(request)))
    print("Request values: " + str(request.values))
    option_chosen = request.values['Digits'] if previous_chosen_option is None else previous_chosen_option
    resp = VoiceResponse()

    print("Number Pressed:", option_chosen)

    if option_chosen == '3' or option_chosen not in ['1','2']:
        action = f"{server}/choose_option"
        
        gather = Gather(action=action, numDigits=1, method='GET')
        gather.say("Please select 1 for trending news, 2 if you have a specific query, or 3 to repeat these options.")
        resp.append(gather)
        resp.redirect(f"{server}/choose_option?Digits=Timeout", method="GET")

        return str(resp)

    if option_chosen == '1':
        print("Trending News")

        resp.say("Here are the top trending news headlines")
        resp.pause(1)

        # TODO: getting headlines
        # headlines = ["banana", "apple", "orange"]

        gather = Gather(action=f"{server}/read_article", numDigits=1, method='GET', finishOnKey='')
        for idx, article in enumerate(articles[:5]):
            gather.say(f"Press {idx} to listen to {article['title']}")
            gather.pause(1)
        gather.say("Press the pound key to repeat these options")

        resp.append(gather)
        resp.redirect(f"{server}/choose_option?Digits=1", method="GET")

        return str(resp)

    if option_chosen == '2':
        print("Specific Query")
        
        speech_timeout = 3
        gather = Gather(input="speech", action=f"{server}/specific_query", timeout=speech_timeout, method='GET')
        gather.say("What is your Specific Query?")
        #gather.pause(speech_timeout)
        resp.append(gather)
        resp.say("Sorry, we didn't hear that.")
        resp.redirect(f"{server}/choose_option?Digits=2", method='GET')

        return str(resp)

    return str(VoiceResponse().hangup())

@app.route("/specific_query", methods=['GET', 'POST'])
def specific_query(): 
    print("Called: " + str(request.values['Called']))
    global query
    query = request.values['SpeechResult']

    while query[-1] in punctuation:
        query = query[:-1]

    print("The query:", query)
    print("The confidence:", request.values['Confidence'])

    resp = VoiceResponse()

    resp.say("Your query is")
    resp.pause(1)
    resp.say(query)

    gather = Gather(action=f"{server}/query_check", numDigits=1, method='GET')
    gather.say("Please press 1 to confirm this is correct or press 2 to say a new query")
    resp.append(gather)
    resp.redirect(f"{server}/choose_option?Digits=2")

    return str(resp)


# Actually read an article, given the ID number.
@app.route("/read_article", methods=['GET', 'POST'])
def read_article():
    global query
    print("Called: " + str(request.values['Called']))
    print("in read article")

    num = request.values['Digits']

    if num == '#':
        return choose_options(option_chosen)

    num = int(num)

    text_to_read = ""
    if query is None: 
        text_to_read = articles[num]['maintext']
    else:
        text_to_read = query_articles(query, articles)[num]['maintext']
    
    #gather = Gather(action=f"{server}/choose_option", numDigits=1, method='GET')
    resp = VoiceResponse()
    resp.say(f"Reading article {num}. To go back at any time, press any key.")

    # TODO: Read Article
    gather = Gather(action=f"{server}/choose_option", numDigits=1, method='GET', timeout=-1)
    query = None
    #gather.pause(1)
    gather.say(text_to_read)
    resp.append(gather)

    return str(resp)

@app.route("/query_check", methods=['GET', 'POST'])
def query_check():
    global query
    print("Called: " + str(request.values['Called']))
    print("in query check")

    num = int(request.values['Digits'])
    resp = VoiceResponse()


    if num == 1:
        resp.say("Searching for")
        resp.pause(1)
        resp.say(query)
        resp.pause(1)


        resp.say("Here are the headlines we found:")
        resp.pause(1)

        gather = Gather(action=f"{server}/read_article", numDigits=1, method='GET', finishOnKey='')
        for idx, article in enumerate(query_articles(query, articles)):
            print("Found article: " + str(article['title']))
            gather.say(f"Press {idx} to listen to {article['title']}")
            gather.pause(1)
        gather.say("Press the pound key to repeat these options")
        resp.append(gather)

    if num == 2 or num not in [1,2]:
        #gather = Gather(input="speech", action=f"{server}/specific_query")
        #gather.say("What is your Specific Query?")
        #resp.append(gather)
        return choose_options('2')

    return str(resp)



if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=24685)
