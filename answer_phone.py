from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather
from string import punctuation
from dotenv import load_dotenv
import os

from make_call import make_call

app = Flask(__name__)
number = None
ZIP = None

headlines = [
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

summaries = [
    "Pilots at Delta Air Lines have approved a new contract that will increase wages 34 percent by 2026 and includes improvements to scheduling, retirement and other benefits, raising the standard for contract negotiations underway at other large US airlines. The new contract is widely expected to influence pilot negotiations at American Airlines, United Airlines and Southwest Airlines. American said on Wednesday that the new Delta contract could put more pressure on other airlines to offer pilots better terms.",
    '''Tesla said on Wednesday that it would build a factory in Mexico to manufacture an electric vehicle that would be significantly more affordable than any of the cars it sold now. "We didnâ€™t hear as much about market conditions in electric vehicles as we did about â€˜Here are some very grand goals we have for sustainable energy,â€™" said Tammy Madsen, a professor at the Leavey School of Business at Santa Clara University. President AndrÃ©s Manuel LÃ³pez Obrador of Mexico said on Tuesday that the company had decided to build the plant.''',
    '''The share of Americans who think the United States has given too much to Ukraine has grown from 7 percent a year ago to 26 percent last month, according to the Pew Research Center. "It's this way with every foreign intervention," said Andy Surabian, a Republican strategist who has advised two outspoken Republican voices against Ukraine aid, Senator JD Vance of Ohio and Donald Trump Jr. "In the first few months, it's always popular. People don't like what Russia did; it's awful. But as time goes on, war weariness is a real thing, especially in this country, especially when voters aren't connecting what's happening in Ukraine with their own security."Although skepticism of Ukraine aid has grown on both sides of the aisle, the party breakdown has been striking. "Yes, there are a small number of members on Capitol Hill, in the House Republicans specifically, that have expressed publicly their concerns about support for Ukraine," he said at a recent briefing.''',
    '''Tesla's new factory in the Mexican state of Nuevo LeÃ³n will cost $5 billion, will employ up to 7,000 people and could start churning out cars as early as next year, the state's governor said on Friday. Tesla announced this week that it planned an assembly plant in Mexico â€” its fifth worldwide â€” but provided few details about the investment, including how much it would spend, when construction would start, how many people would work at the factory or how the company would deal with regional water shortages. Tesla's factory will use recycled water, he added.''',
    '''"Let's be clear, some of these characters going into stores that are wearing their mask, they're not doing it because they're afraid of the pandemic, they're doing it because they're afraid of the police," the mayor said in a television interview with PIX 11. Chief Maddrey said New Yorkers should think of dropping their masks as "a peace offering" and "a sign of safety for store workers.""When we walk in, we should take down our masks," the chief said. "We should let them know that they're not in any danger, any harm, that we're customers, we're here to help them."But as a crime prevention strategy, he acknowledged it might have shortcomings.''',
    '''The Japanese space agency said on Tuesday that the country's newest rocket had failed minutes into its first demonstration flight, a technological setback as the country tries to build up its capabilities in space. Japan is not alone in having a new rocket fail on its first flight. A Chinese company, Landspace, lost its Zhuque-2 rocket on its first orbital flight in December.''',
    '''The national debt has grown to $31. In those cases, on net, Republicans added slightly more to the debt than Democrats. Mr. Trump, by comparison, signed laws adding nearly $7 trillion to the debt in his four-year term, by the budget office's estimation.''',
    '''All have said the virus may have accidentally escaped from a laboratory. Fauci is not on the witness list for Wednesday's hearing; in a brief interview, he said he was not asked to testify. Emails that have since been made public indicate that they consulted with virologists who had more experience studying coronaviruses and who said that the features that may initially have looked worrisome did not in fact suggest that the virus had been concocted in a lab.Some of those features of the virus were also identified in related coronaviruses in other species, strengthening the view that the features were not necessarily lab-made.''',
    '''WASHINGTON â€” President Biden on Thursday will propose policies aimed at trimming federal budget deficits by $3 trillion over the next 10 years as his administration embraces the politics of debt reduction amid a fight with Republicans over raising the nation's borrowing limit, a senior administration official said on Wednesday. 41 trillion from $1. Through new laws he has signed and executive actions he has issued, Mr. Biden has approved policies that would add about $5 trillion to the national debt over a decade, according to estimates by the Committee for a Responsible Federal Budget in Washington.''',
    '''A Washington, DC, police sergeant who fatally shot a man found unconscious at the wheel of a car has been charged with murder, according to a federal indictment unsealed on Tuesday. At the scene of the incident, the department has said, officers found Mr. Gilmore with his foot on the brake pedal of a running vehicle with the handgun visible in his waistband. In a statement on Tuesday, Matthew M. Graves, the United States attorney for the District of Columbia, said that criminal charges are not appropriate in the overwhelming majority of cases where officers use deadly force.'''
]

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

# 
@app.route("/choose_option", methods=['GET', 'POST'])
def choose_options(previous_chosen_option = None):
    global option_chosen
    print("Request: " + str(dir(request)))
    print("Request values: " + str(request.values))
    option_chosen = request.values['Digits'] if previous_chosen_option is None else previous_chosen_option
    resp = VoiceResponse()

    print("Number Pressed:", option_chosen)

    if option_chosen == '4' or option_chosen not in ['1','2','3']:
        action = f"{server}/choose_option"
        
        gather = Gather(action=action, method='GET')
        gather.say("Please select 1 for trending local news, 2 for trending world news, 3 if you have a specific query, or 4 to repeat these options.")
        resp.append(gather)

        return str(resp)

    if option_chosen == '1':
        print("Local News")

        resp.say("Here are the top trending local news headlines")
        resp.pause(1)

        # TODO: getting headlines
        # headlines = ["banana", "apple", "orange"]

        gather = Gather(action=f"{server}/read_article", method='GET', finishOnKey='')
        for idx, headline in enumerate(headlines):
            gather.say(f"Press {idx} to listen to {headline}")
            gather.pause(1)
        gather.say("Press the pound key to repeat these options")

        resp.append(gather)

        return str(resp)

    if option_chosen == '2':
        print("World News")

        resp.say("Here are the top trending world news headlines")
        resp.pause(1)

        # TODO: getting headlines
        # headlines = ["banana", "apple", "orange"]

        gather = Gather(action=f"{server}/read_article", method='GET', finishOnKey='')
        for idx, headline in enumerate(headlines):
            gather.say(f"Press {idx} to listen to {headline}")
            gather.pause(1)
        gather.say("Press the pound key to repeat these options")

        resp.append(gather) 

        return str(resp)

    if option_chosen == '3':
        print("Specific Query")
        
        gather = Gather(input="speech", action=f"{server}/specific_query", method='GET')
        gather.say("What is your Specific Query?")
        resp.append(gather)

        return str(resp)

    return str(VoiceResponse().hangup())

@app.route("/specific_query", methods=['GET', 'POST'])
def specific_query(): 
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

    gather = Gather(action=f"{server}/query_check", method='GET')
    gather.say("Please press 1 to confirm this is correct or press 2 to say a new query")
    resp.append(gather)

    return str(resp)


# Actually read an article, given the ID number.
@app.route("/read_article", methods=['GET', 'POST'])
def read_article():
    print("in read article")

    num = request.values['Digits']

    if num == '#':
        return choose_options(option_chosen)

    num = int(num)
    
    resp = VoiceResponse()
    resp.say(f"Reading article {num}")

    # TODO: Read Article
    resp.pause(1)
    resp.say(summaries[num])

    return str(resp)

@app.route("/query_check", methods=['GET', 'POST'])
def query_check():
    print("in query check")

    num = int(request.values['Digits'])
    resp = VoiceResponse()

    if num == 1:
        resp.say("Searching google for")
        resp.pause(1)
        resp.say(query)
        resp.pause(1)

        # TODO: query internet to get headlines
        headlines = ["banana", "apple", "orange"]

        resp.say("Here are the headlines we found on google")
        resp.pause(1)

        gather = Gather(action=f"{server}/read_article", method='GET', finishOnKey='')
        for idx, headline in enumerate(headlines):
            gather.say(f"Press {idx} to listen to {headline}")
            gather.pause(1)
        gather.say("Press the pound key to repeat these options")

    if num == 2 or num not in [1,2]:
        gather = Gather(input="speech", action=f"{server}/specific_query")
        gather.say("What is your Specific Query?")
        resp.append(gather)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=24685)
