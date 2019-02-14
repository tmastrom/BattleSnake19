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

    print 'turn ', data['turn']

    #print(json.dumps(data))

    # board limits
    height = data["board"]["height"]
    width = data["board"]["width"]

    # my snake head location
    head_x = data["you"]["body"][0]["x"]
    head_y = data["you"]["body"][0]["y"]

    print 'head', head_x, head_y

    # location I am coming from 
    neck_x = data["you"]["body"][1]["x"]
    neck_y = data["you"]["body"][1]["y"]

    # list places not to go 
    dont_x = [neck_x, 0, 15]
    dont_y = [neck_y, 0, 15]

    # food location
    food_x = data["board"]['food'][0]['x']
    food_y = data["board"]['food'][0]['y']

    directions = ['up', 'down', 'left', 'right']
    
    direction = 'up'

    # find food direction 
    x_dist = head_x - food_x
    y_dist = head_y - food_y 

    print 'x_dist ', x_dist
    print 'y_dist ', y_dist

    # determine which direction to move toward food
    def food_dir_x(x):
        if x > 0:
            direction = 'left'  
        elif x < 0:
            direction = 'right'
        return direction   
        print 'food_dir_x', direction
        
    
    def food_dir_y(y):
        if y > 0:
            direction = 'up'
            
        elif y < 0:
            direction = 'down'
        return direction    
        print 'food_dir_y', direction


    # final check that chosen direction is ok 
    def check_dir_x(dir, head, dont):
        if dir == 'right':
            if head + 1 not in dont:
                print 'good to go right'
                return dir
            elif head + 1 in dont:
                print 'Dont go right!'
                # actually do something
                if head - 1 not in dont:
                    print 'good to go left tho'
                    dir = 'left'
                    return dir # will this exit check_dir_x??? make sure dir is not reassigned again
                elif head - 1 in dont:
                    print 'Dont go left either!'
                    # check up/down
        if dir == 'left':
            if head -1 not in dont:
                print 'good to go left'
                return dir
            elif head - 1 in dont:
                print 'Dont go left!'
                if head + 1 not in dont:
                    'good to go right tho'
                    dir = 'right'
                    return dir
                else: print "dont go left either"
                    # check up/down

    def check_dir_y(dir, head, dont):
        if dir == 'up':
            if head -1 not in dont:
                print 'good to go up'
                return dir
            elif head -1 in dont:
                print "dont go up!"
                if head +1 not in dont:
                    print 'good to go down tho'
                    dir = 'down'
                    return dir
                else:
                    print 'dont go down either'
                    # check right/left
        if dir == 'down':
            if head + 1 not in dont:
                print 'good to go down'
                return dir
            elif head + 1 in dont:
                print 'dont go down!'
                if head -1 not in dont:
                    print 'good to go up tho'
                    dir = 'up'
                    return dir
                else: print 'dont go up either'
            return dir
                    # check right/left


    # move along the axis that is furthest from food
    if abs(x_dist) >= abs(y_dist):
        direction = food_dir_x(x_dist)
    else: direction = food_dir_y(y_dist)

    if direction == 'right' or direction == 'left':
        print 'entered checkdir'
        direction = check_dir_x(direction, head_x, dont_x)
    if direction == 'up' or direction == 'down':
        print 'entered checkdir'
        direction = check_dir_y(direction, head_y, dont_y)
    
    '''
    # if the snake is going up 
    if direction == 'up':
        # if the snake will hit a wall on the next turn
        if head_y - 1 in dont_y: 
            if head_x + 1 in dont_x:
                direction = 'left'
            else: direction = 'right'
    
    if direction == 'down':
        if head_y + 1 in dont_y:
            if head_x + 1 in dont_x:
                direction = 'left'
            else: direction = 'right'

    if direction == 'right':
        if head_x + 1 in dont_x:
            if head_y + 1 in dont_y:
                direction = 'up'
            else: direction = 'down'

    if direction == 'left':
        if head_x - 1 in dont_x:
            if head_y + 1 in dont_y:
                direction = 'up'
            else: direction = 'down'
'''
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


