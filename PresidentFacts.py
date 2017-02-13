"""
President Facts Lambda Function

Created by Zac Patel on 2/12/17

Code skeleton taken from Lambda python template

Facts compiled by Anil Patel on 2/12/17
"""

from __future__ import print_function
from random import randint
# --------------- Helpers that build all of the responses ----------------------

def get_fact_intent_handler(intent):
    """
    grabs a random fact from the list of facts, and returns it to the user
    """
    # finding the index of the fact to get, and pulling it from the list
    rand = randint(0, len(FACTS_ARRAY) - 1)
    fact = FACTS_ARRAY[rand]

    # session attributes remain empty
    session_attributes = {}
    # getting a fact should end the session
    should_end_session = False
    # no reprompt text because the session should end after a single fact is returned
    reprompt_text = ""
    # the title displayed on the phone app
    title = "President Fact #" + str(rand + 1)
    
    # generating our speechlet response
    sp_res = build_speechlet_response(title, fact, reprompt_text, should_end_session)
    return build_response(session_attributes, sp_res)

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to President Facts. Ask me for a fact."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I know " + str(len(FACTS_ARRAY)) + " facts about the US Presidents."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for using President facts."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GETFACTINTENT":
        return get_fact_intent_handler(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# Array to hold all our facts
# storing all our facts in an array is just generally less of a hassle than a text file
# (though facts are stored in their formatted form in Facts.docx for spellcheck purposes)
FACTS_ARRAY=[
    "George Washington was unanimously elected by the Electoral College to his first two terms as president.",
    "George Washington defeated the British Army in the battles of Trenton and Princeton after crossing the Deleware River in the middle of winter.",
    "George Washington's face is carved into Mount Rushmore.",
    "The first United States Congress voted to pay George Washington a salary of $25,000 a year in 1789.  This amount is equivalent to $340,000 in 2015 dollars.",
    "John Adams was the first United States president to reside in the White House.",
    "John Adams major accomplishment during his presidency was the a peaceful resolution to the undeclared naval Quasi-war against France.",
    "John Adams was a lawyer who was retained by the British Schooner Dartmouth which was famously involved in the Boston Tea Party.  Adams called the defiant boarding of the vessels and destruction of the tea onboard as the grandest event in the history of the colonial movement.",
    "Thomas Jefferson was a founding father and principal author of the Declaration of Independence.",
    "Thomas Jefferson organized the Louisiana Purchase, almost doubling the United States territory at the time.",
    "Thomas Jefferson's face is carved into Mount Rushmore.",
    "James Madison was a founding father of the United States Constitution and he also drafted the first ten ammendments to the Constitution, known as the Bill of Rights.",
    "Along with Alexander Hamilton and John Jay, James Madison produced the Federalist Papers, among the most important treasties in support of the Constitution.",
    "James Monroe was injured in the Battle of Trenton by a musket ball to his shoulder.",
    "James Monroe supported founding African colonies for free slaves.  The capital of Liberia, Monrovia, is named in his honor.",
    "John Quincy Adams is best known for shaping United States foreign policy aligned with his nationalist commitment to republican values.",
    "John Quincy Adams played a pivotal role in negotiating the Treaty of Ghent, which ended the War of 1812.",
    "Andrew Jackson denied the right of South Carolina to secede from the Union over the Tarriff of Abominations, a treaty designed to protect industry in the northern United States.",
    "Andrew Jackson is the founder of the Democratic Party.",
    "Martin Van Buren was blamed for the depression of 1837.  Newspapers at the time labeled him as Martin Van Ruin.",
    "Martin Van Buren denied the application of Texas for admission to the Union.",
    "William Henry Harrison, who was 68 years old at the time of his innaguration, died 31 days into his presidency, making his term the shortest in United States history.",
    "John Tyler firmly believed in territorial expansion  and is most notably known for the annexation of the independent Republic of Texas.",
    "When Mexico rejected the United States annexation of the Republic of Texas, James Polk led the United States to victory in the Mexican American War resulting in the cession by Mexico of nearly the whole of what we now know as the American Southwest.",
    "Zachary Taylor defeated Mexican troops in the Mexican American War and was considered a national hero.  This led to his election to the White House.",
    "Millard Filmore, who was the 12th Vice President, was elevated to president when Zachary Taylor died in office.",
    "Franklin Peirce enforced the Fugitive Slave Act and alienated anti-slavery groups which ultimately led to the Southern secession and the United States Civil War.",
    "James Buchanon was the only president to remain a lifelong bachelor.",
    "Abraham Lincoln led the United States through the Civil War.  He preserved the Union, abolished slavery and strengthened the federal government.",
    "Abraham Lincoln was a leader in building the new Republican Party.",
    "Abraham Lincoln was assasinated on April 14, 1864 by John Wilkes Booth, a Confederate sympathizer.",
    "Abraham Lincoln's face is carved into Mount Rushmore.",
    "Andrew Johnson favored quick addition of the seceded states to the Union after the Civil War.  However, his plans did not give protection to the former slaves, which culmiated in him being the first President to be impeached by the Houe of the Representatives.  He was acquitted in the Senate by one vote.",
    "Ulysses S. Grant led the Republicans in efforts to protect African-American citizenship.",
    "Rutherford B. Hayes won a intensely disputed Electoral College vote after winning twenty contested votes. This led to the Compromise of 1877 in which Democrats accepted his election after he withdrew U.S. troops protecting Republican office holders in the South.",
    "James A. Garfield was shot by Charles Guiteau and died after eleven weeks after serving only 200 days in office.",
    "Chester A. Arthur embraced civil service reform. The enforcement of the Pendleton Civil Service Reform Act was his administration's centerpiece.",
    "Grover Cleveland served as President in three terms and is the only President to serve in two non-consecutive terms in office.",
    "Benjamin Harrison was the grandson of William Henry Harrison making them the only grandfather-grandson duo to become President.",
    "William McKinley led the United States to victory in the Spanish-American War.",
    "William McKinley was shot on September 6, 1901 by Leon Czolgosz and died eight days later.",
    "Theodore Roosevelt gained office after William McKinley's assasinatin.  At age 42, he was the youngest United States President in history.",
    "Theodore Roosevelt overcame debilitating astma through a strenous lifestyle.",
    "Theodore Roosevelt's face is carved into Mount Rushmore.",
    "William Howard Taft focused on East Asian affairs more than European affairs.  He also propped up or removed several Latin American governments.",
    "Woodrow Wilson called a special session of Congress, whose work culminated in the Revenue Act of 1913 which introduced an income tax.",
    "Woodrow Wilson won the 1919 Nobel Peace Prize for sponsorship of the League of Nations.",
    "Woodrow Wilson suffered from a severe stroke in 1919 during a campaign trip to promote the formation of the League of Nations.",
    "Warren G. Harding died in office of a cerebral hemmorage caused by heart disease.",
    "Calvin Coolidge gained a reputation as a conservative favoring small goverment. His reputation underwent a renaissance during Ronald Regan's administration.",
    "Herbert Hoover served as President during the Great Depression after the Wall Street Crash of 1929.",
    "Herbert Hoover tried to combat the Great Depression with large public works projects like the Hoover Dam.",
    "Franklin D. Roosevelt won a record four Presidential elections",
    "Franklin D. Roosevelt instituted the New Deal, a variety of programs designed to produce relive and recovery from the Great Depression.",
    "Franklin D. Roosevelt famously called the Japanese surprise attack on Pearl Harbor on December 7, 1941 a date which will live in infamy.",
    "Franklin D. Roosevelt died in office shortly into his fourth term as President.",
    "Harry S. Truman shares the record for vetoes at 180 with Gerald Ford.",
    "Harry S. Truman desegregated the armed forces",
    "Harry S. Truman is known for launching the Marshall Plan to rebuild the Western European economy.",
    "Harry S. Truman led the Cold War against Soviet and Chinese communism through the Truman Doctrine and NATO.",
    "Dwight D. Eisenhower was a five-star general in the U.S. Army during World War II.",
    "Dwight D. Eisenhower was the first supreme commander of NATO.",
    "Dwight D. Eisenhower threatened the use of nuclear weapons in an effort to conclude the Korean War.",
    "Dwight D. Eisenhower authorized the establishment of NASA in 1957.",
    "John F. Kennedy oversaw a failed attempt at the Bay of Pigs to overthrow Cuban leader Fidel Castro in April 1961.",
    "John F. Kennedy was assasinated in Dallas, Texas on November 22, 1963 by Lee Harvey Oswald.",
    "John F. Kennedy is the only President to win the Pulitzer Prize for his biography Profiles in Courage.",
    "John F. Kennedy established the Presidential Medal of Freedom in 1963",
    "John F. Kennedy famously said, at the Berlin Wall, the phrase Ich bin ein Berliner, which means I am a citizen of Berlin.",
    "Lyndon B. Johnson was known for his domineering, abrasive personality known as the Johnson Treatment.",
    "Lyndon B. Johnson signed civil rights bills that banned racial discrimination in public facilities, commerce, the workplace, and housing.",
    "Lyndon B. Johnson escalated American involvement in the Vietnam War.",
    "Richard Nixon was the only President to resign from office in 1974.",
    "Richard Nixon ended American involvement in the Vietnam War in 1973.",
    "Richard Nixon's visit to the People's Republic of China in 1972 opened diplomatic relations between the two countries.",
    "Richard Nixon signed the Anti-Ballistic Missle Treaty with the Soviet Union in 1972.",
    "Gerald Ford granted Richard Nixon a Presidential pardon for his role in the Watergate scandal.",
    "Gerald Ford signed the Helsinki Accords moving towards detente in the Cold War.",
    "Jimmy Carter pardoned all draft dodgers of the Vietnam War on his second day in office",
    "Jimmy Carter created two new cabinet departments, the Departement of Energy and the Department of Education.",
    "Jimmy Carter pursued the Camp David Accords which were two framework agreements which led to the 1979 Egypt-Isreal Peace Treaty.",
    "Ronald Reagan was a famous movie actor who was twice elected Screen Actors Guild President.",
    "Ronald Reagan is known for his supply-side economic policies dubbed Reagonmics.",
    "Ronald Reagan survived an assasination attempt in his first term in office.",
    "Ronald Reagan spoke in the Brandenburg Gate in Berlin and challenged Gorbachov to tear down this wall!",
    "George H. W. Bush served as Director of Central Intelligence.",
    "George H. W. Bush oversaw military operations in Panama and the Persian Gulf.",
    "Bill Clinton signed into law the North American Free Trade Agreement.",
    "Bill Clinton passed welfare reform and provided health coverage for millions of children.",
    "Bill Clinton was impeached by the House of Representatives for perjury relating to a scandal involving White House employee Monica Lewinsky.",
    "Bill Clinton was President during the longest period of peacetime econmoic expansion in American history.",
    "George W. Bush co-owned the Texas Rangers baseball team.",
    "George W. Bush responded to the September 11 terrorist attacks with the Bush Doctrine, launching a War on Terror.",
    "George W. Bush led the war in Afghanistan in 2001 and the Iraq War in 2003.",
    "Barack Obama was the first African-American to serve as President.",
    "Barack Obama signed into law the Patient Protection and Affordable Care Act, often referred to as Obamacare.",
    "Barack Obama increased U.S. troop levels in Afghanistan."
    "Barack Obama approved the military operation that resulted in the death of Osama bin Laden",
    "Barack Obama was named the 2009 Nobel Peace Prize laureate.",
    "Donald Trump is the first President without prior military or governmental service",
    "Donald Trump's platform emphasizes renegotiation of the North American Free Trade Agreement.",
]


