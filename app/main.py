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

    '''
    remove a direction from the list if that direction is determined not allowed
    pass that list of allowed directions to the checkdir function to only evaluate those dirs
    
    '''
    def check_border(head, directions):
        # dont is the list of other snakes and my own body
        # head is the head of my snake 
        # direction is the optimal direction that is to be validated
        # directions are the possible directions. Pop from this list if a move is invalid

         # 1. check if head is at a border and pop invalid directions (one of the coords is 0 or 14)
        if 0 in head:
            if head.index(0) == 0:
                print 'dont go left'
                directions.remove('left')
            else: print 'can move left'
            if head.index(0) == 1:
                print 'dont go up'
                directions.remove('up')
            else: 'can move up'

        if 14 in head: 
            if head.index(14) == 0:
                print 'dont go right'
                directions.remove('right')
            else: print 'can move right'
            if head.index(14) == 1:
                print 'dont go down'
                directions.remove('down')
            else: print 'can move down'

        return directions
                
 

        #check if direction is in directions list 
    
    def check_next_pos(direction, dont, head):
        next_pos = [sum(x) for x in zip(head, direction)]
        print 'next position', next_pos
        if next_pos in dont:
            print 'dont go here'
            return False
        else: 
            print 'go here'
            return True

    def coordinate_conversion(direction):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]

        if direction == up:
            return 'up'
        if direction == down:
            return 'down'
        if direction == left:
            return 'left'
        if direction == right:
            return 'right'
        



    directions = ['up', 'down', 'left', 'right']
    direction = 'up'

    directionlist = [[0, -1], [0, 1], [-1, 0], [1,0]]



    print 'turn ', data['turn']

    # add board boundaries to the list of places not to go
    # dont is a list of 2 element lists 
    # xaxis = []
    # yaxis = []
    dont = []

    # my snake head location
    head = [data["you"]["body"][0]["x"], data["you"]["body"][0]["y"]]
    print 'Head', head

    # grow the list of coordinates not to go
    # populate the list with snakes on the board including myself
    # differentiate between me and others??
    # save the head/tail location to see where they are moving??
    '''for i in data["board"]["snakes"]:
        for j in i['body']:
            pos = [j['x'],j['y']]
            dont += pos
    #print dont  
'''
    # This isn't working, snake runs into itself 
    for i in data["you"]["body"]:
        pos = [i['x'],i['y']]
        dont.append(pos)
    print dont, 'DONT'
    
    # food location
    # change to make this the closest food!!
    food = [data["board"]["food"][0]["x"], data["board"]["food"][0]["y"]]

    '''make a closest food function
    order the directions based on priority
'''
    # find food direction 
    negfood = [-x for x in food]
    dist = [sum(x) for x in zip(head, negfood)]  # this only works for 1 food
    print 'distance x,y', dist 
    # return index of max(dist) to decide x or y move
    distabs = [abs(x) for x in dist]
    print distabs
    ind = distabs.index(max(distabs))
    print 'index', ind

    direc = [0, 0] # direction vector
    # set the direction vector 
    if dist[ind] < 0:
        direc[ind] = 1
    else: direc[ind] = -1
    print 'direction vector', direc # pass direc to checkdir function

    # loop this to try all options if none are valid

    # calling check border returns directions with invalid directions removed 
    directions = check_border(head, directions)
    print 'new directions', directions

    isValid = check_next_pos(direc, dont, head)

    if isValid == True:
        print 'position is valid'
        validdirection = direc
    else: 
        print 'invalid'
        validdirection = [1, 0]     #goes right

    direction = coordinate_conversion(validdirection)

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


