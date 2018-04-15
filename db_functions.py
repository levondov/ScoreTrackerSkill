import boto3
from decimal import *

def resetscores(userId):
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
        
        for idx,player in enumerate(players):
            scores[idx] = Decimal(0)
            
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
            })
            

def resetplayerscore(player,userId):
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
            scores[pidx] = Decimal(0)
        except:
            # player not in list, need to add manually
            players.append(player)
            scores.append(Decimal(0))

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
                'scores': [Decimal(0)]
            })
    
def removeplayer(player,userId):
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
            del players[pidx]
            del scores[pidx]
                    
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
            # player not in list, can't remove a person not there...
            pass
    except:
        # no user in database, can't remove a person not there
        pass
    
def removeallplayers(userId):
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
        
        try:
                    
            # update db
            #print players,scores
            r = table.update_item(
                Key = {
                    'userid': userId
                },
                UpdateExpression='set players = :p, scores=:s',
                ExpressionAttributeValues={
                    ':p': [],
                    ':s': []
                },
                ReturnValues="UPDATED_NEW")
        except:
            # player not in list, can't remove a person not there...
            pass
    except:
        # no user in database, need to add manually
        r = table.put_item(
            Item={
                'userid': userId,
            }) 
    
    
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
    
def subtractplayerscore(player,score,userId):
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
            newScore = scores[pidx] - Decimal(score)
            scores[pidx] = newScore
        except:
            # player not in list, need to add manually
            players.append(player)
            scores.append(-1*Decimal(score))
            newScore = -1*Decimal(score)

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
                'scores': [-1*Decimal(score)]
            })
        newScore = -1*Decimal(score)
    
    return newScore    
    
def changeplayerscore(player,score,userId):
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
            pidx = players.index(player[0:-2])
            newScore = Decimal(score)
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
        newScore = -1*Decimal(score)
    
    return newScore 
    
def getplayerscore(player,userId):
    ''' Gets a player's score'''
    
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
            newScore = scores[pidx]
            return newScore,True
        except:
            # player not in list, need to add manually
            return 0,False
    except:
        # no user in database, need to add manually
        r = table.put_item(
            Item={
                'userid': userId,
            })
        return 0,False
        
def getplayersscore(userId):
    '''returns a list of everyone's scores'''
    
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
        
        return players,scores
    except:
        # no user in database, need to add manually
        r = table.put_item(
            Item={
                'userid': userId,
            })
        return [],[]