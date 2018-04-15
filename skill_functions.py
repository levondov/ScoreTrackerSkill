from db_functions import *

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, ctitle, coutput, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': ctitle,
            'content': coutput
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_card_response(userId):
    ''' builds a list of players and scores for the card output '''
    players,scores = getplayersscore(userId)
    coutput = 'Players - Scores \n'
    
    for player,score in zip(players,scores):
        coutput = coutput + player + ' - ' + str(score) + '\n'
        
    return coutput

# --------------- Functions that control the skill's behavior ------------------
    
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Score Tracker skill. " \
                    "This skill manages and keeps track of player scores for any event. " \
                    "To get started give me a player and how many points they have. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Take a look at the alexa app for some sample phrases."
    coutput = "Some sample phraes: \n" \
            " * add a score for a player \n" \
            " - ask score tracker to add 5 points for John \n" \
            " * Get the score for a single player or all players\n" \
            " - ask score tracker how many points does Sarah have\n" \
            " - ask score tracker for the score \n" \
            " * Remove a player / Remove all players / Start a new round\n" \
            " - ask score tracker to remove John\n" \
            " - ask score tracker to remove everyone\n" \
            " - ask score tracker to start a new round\n"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Welcome', coutput, reprompt_text, should_end_session))

def handle_session_end_request(nostop_flag=False):
    card_title = "Session Ended"
    if nostop_flag:
        speech_output = "I could not understand the phrase you gave me. I need a name and a score to keep track of."
    else:
        speech_output = ""
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, 'Help!', speech_output, None, should_end_session))
        
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
    
 # --------------- Functions that handle intents ------------------
 
def get_addscore_session(intent, session):
    # add points for a player
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
        ppoints = intent['slots']['value']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
    if ppoints is 'stop' or ppoints is 'cancel':
        return handle_session_end_request()        
        
    # add player and name to database along with userId
    newScore = addplayerscore(pname,ppoints,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = pname + ' with ' + str(newScore) + ' points'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))
        
def get_subtractscore_session(intent, session):
    # subtract points from a player
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
        ppoints = intent['slots']['value']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
    if ppoints is 'stop' or ppoints is 'cancel':
        return handle_session_end_request()        
        
    # add player and name to database along with userId
    newScore = subtractplayerscore(pname,ppoints,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = pname + ' with ' + str(newScore) + ' points'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))        
    
def get_changescore_session(intent, session):
    # note assuming when player's invoke this they will say 'set john's score to 10' not 'set john score to 10'
    # as a result I will remove the last 2 elements in the player name because I assume it will be ''s'
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
        ppoints = intent['slots']['value']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
    if ppoints is 'stop' or ppoints is 'cancel':
        return handle_session_end_request()        
        
    # add player and name to database along with userId
    newScore = changeplayerscore(pname,ppoints,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = pname[0:-2] + ' with ' + str(newScore) + ' points'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))        

def remove_player_session(intent, session):
    # Remove a player from the game
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
        
    # add player and name to database along with userId
    newScore = removeplayer(pname,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = pname + ' removed from the game.'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))
        
def reset_player_session(intent, session):
    # Reset a player score
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
        
    # add player and name to database along with userId
    newScore = resetplayerscore(pname,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = 'Score for ' + pname + ' reset'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))        

def startnew_session(intent, session):
    # Reset everyone's scores
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    # reset all scores in db
    resetscores(session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    speech_output = 'Scores have been reset for everyone'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))      
        
def remove_allplayers_session(intent,session):
    # Remove all player from the game
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    # remove all players in db
    removeallplayers(session['user']['userId'])
    
    speech_output = 'All players removed from the game'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'New Game', speech_output, reprompt_text, should_end_session))
        
def get_playerscore_intent(intent,session):
    # add points for a player
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
        
    # add player and name to database along with userId
    score,pFlag = getplayerscore(pname,session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    if pFlag:
        speech_output = pname +' with ' + str(score) + ' points'
    else:
        speech_output = 'I could not find any entry for the name ' + pname
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))
        
def get_playersscore_intent(intent,session):
    # add points for a player
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
        
    # add player and name to database along with userId
    players,scores = getplayersscore(session['user']['userId'])
    ctext = build_card_response(session['user']['userId'])
    
    if not players:
        speech_output = 'There are no players currently'
    else:
            # make into a list of tuples
            playerandscore = []
            for player,score in zip(players,scores):
                playerandscore.append((player,score))
            playerandscore = sorted(playerandscore, key=lambda x: x[1])
            speech_output = ''
            for val in playerandscore:
                speech_output = speech_output + val[0] + ' with ' + str(val[1]) + ' points, '
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'Scores', ctext, reprompt_text, should_end_session))            