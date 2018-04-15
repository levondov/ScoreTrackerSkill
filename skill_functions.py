import boto3
from decimal import *

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Score Tracker",
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }



# --------------- Functions that control the skill's behavior ------------------
    
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Score Tracker skill. " \
                    "This skill manages and keeps track of player scores for any event. " \
                    "To get started give me a name and a score to track. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I need a name and a score to keep track of. "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request(nostop_flag=False):
    card_title = "Session Ended"
    if nostop_flag:
        speech_output = "I could not understand the phrase you gave me. I need a name and a score to keep track of."
    else:
        speech_output = ""
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
    
 # --------------- Functions that handle score intents ------------------
def get_addscore_session(intent, session):
    session_attributes = {}
    reprompt_text = {}
    card_title = 'Score Tracker'
    should_end_session = 'True'
    reprompt_text = None
    
    try:
        pname = intent['slots']['player']['value']
        ppoints = intent['slots']['points']['value']
    except:
        return handle_session_end_request(nostop_flag=True)
        
    if pname is 'stop' or pname is 'cancel':
        return handle_session_end_request()
    if ppoints is 'stop' or ppoints is 'cancel':
        return handle_session_end_request()        
        
    # add player and name to database along with userId
    newScore = addplayerscore(pname,ppoints,session['user']['userId'])
    
    speech_output = pname + ' with ' + str(newScore) + ' points'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def addplayerscore(player,score,userId):
    ''' Adds a player and score to a specific userID'''
    
    # initialize DB table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('ScoreKeeperDB')
    
    # grab db entry
    r = table.get_item(
        Key = {
            'userid': userId
        })

    try:
        # see if userId exists
        dbitem = r['Item']
        players = dbitem['players']
        scores = dbitem['scores']
        
        try:
            # see if player exists
            pidx = players.index(player)
            newScore = scores[pidx] + Decimal(score)
            scores[pidx] = newScore
        except:
            # player not in list, need to add manually
            players.append(player)
            scores.append(Decimal(score))
            newScore = Decimal(score)

        # update db
        #print players,scores
        r = table.update_item(
            Key = {
                'userid': userId
            },
            UpdateExpression='set players = :p, scores=:s',
            ExpressionAttributeValues={
                ':p': players,
                ':s': scores
            },
            ReturnValues="UPDATED_NEW")
    except:
        # no user in database, need to add manually
        r = table.put_item(
            Item={
                'userid': userId,
                'players': [player],
                'scores': [Decimal(score)]
            })
        newScore = Decimal(score)
    
    return newScore