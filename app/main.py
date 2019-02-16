import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
# check this out
#https://stackoverflow.com/questions/15750681/efficient-way-to-store-and-search-coordinates-in-python
        
    directions = ['up', 'down', 'left', 'right']
    direction = 'up'

    directionlist = [[0, -1], [0, 1], [-1, 0], [1,0]]

    up = [0, -1]
    down = [0, 1]
    left = [-1, 0]
    right = [1,0]

    print 'turn ', data['turn']

    # add board boundaries to the list of places not to go
    # dont is a list of 2 element lists 
    xaxis = []
    yaxis = []
    dont = []

    for x in range(data["board"]["width"]+1):
        xaxis.append(x)
    for x in range(data["board"]["height"]+1):
        yaxis.append(x)
    #print xaxis
    #print yaxis

    dont = [[x, y] for x in xaxis for y in yaxis]

    #print dont

    # my snake head location
    head = [data["you"]["body"][0]["x"], data["you"]["body"][0]["y"]]

    # grow the list of coordinates not to go
    # populate the list with snakes on the board including myself
    # differentiate between me and others??
    # save the head/tail location to see where they are moving??
    for i in data["board"]["snakes"]:
        for j in i['body']:
            pos = [j['x'],j['y']]
            dont.append(pos)
    #print dont  

    # food location
    food = [data["board"]["food"][0]["x"], data["board"]["food"][0]["y"]]

    #print 'head', head
    #print 'food', food  

    # find food direction 
    negfood = [-x for x in food]

    dist = [sum(x) for x in zip(head, negfood)]  # this only works for 1 food
    print dist 
    # return index of max(dist) to decide x or y move
    ind = dist.index(max(dist))
    print 'index', ind

    direc = [0, 0] # direction vector
    # set the direction vector 
    if max(dist) < 0:
        direc[ind] = -1
    else: direc[ind] = 1
    print 'direc', direc

    # check to see if moving that direction is allowed 
    next_pos = [sum(x) for x in zip(head, direc)]
    print 'next position', next_pos

    if next_pos in dont:
        print 'dont go here'
        direction = 'left'
        # check for boundary 
    else: 
        print 'go here'
        direction = directions[directionlist.index(direc)]
        

    print 'direction ', direction

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


