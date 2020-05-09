# Implementation of classic arcade game Pong
## Week 5 - Pong Project Code

try: #this simplegui code doesn't work (prob not updated for python 3.7
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 200 #vertical position of paddle 1
paddle2_pos = 200 #vertical position of paddle 2
paddle1_vel = 0
paddle2_vel = 0 
ball_pos = [ ]
ball_vel = [ ]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction): #function is called when you need to spawn a new ball (start a new game or whenever previous point is over
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2 , HEIGHT / 2]
    ball_vel = [1, 1]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120/60, 240/60) #the draw handler is called 60 times per second, so the values have to be divided by 60
        ball_vel[1] = random.randrange(-180/60, -60/60)
    elif direction == LEFT:
        ball_vel[0] = random.randrange(-240/60, -120/60)
        ball_vel[1] = random.randrange(-180/60, -60/60)
    
# define event handlers - new game should call spawn_ball inside it
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers 
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    spawn_ball(LEFT) #fill in the direction of spawn ball

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball (positional update to the draw handler)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    ##colide and reflect off top and bottom of canvas
    if ball_pos[1] <= BALL_RADIUS: #bounce off top
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS: #bounce off bottom 
        ball_vel[1] = -ball_vel[1]
    
    #spawn a new ball if ball hits gutters, reflect back into play if ball hits paddles:
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * .10
            ball_vel[1] += ball_vel[1] * .10
        else:
            spawn_ball(RIGHT)
            score2 += 1
        
    if ball_pos[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * .10
            ball_vel[1] += ball_vel[1] * .10
        else:
            spawn_ball(LEFT)
            score1 += 1
 
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + paddle1_vel >= HEIGHT - HALF_PAD_HEIGHT:
         paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
      
    if paddle2_pos + paddle2_vel <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + paddle2_vel >= HEIGHT - HALF_PAD_HEIGHT:
         paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polyline([(HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos),
                          (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT)], PAD_WIDTH, 'White')
    
    canvas.draw_polyline([(WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos),
                          (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)], PAD_WIDTH, 'White')
    
    # draw scores
    
    canvas.draw_text(str(score1), [WIDTH / 4, HEIGHT / 6], 50, "White")
    canvas.draw_text(str(score2), [(WIDTH / 4) * 3 , HEIGHT / 6], 50, "White")

#keys will control the velocity of the paddles
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 10
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 10
                                         
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

def button_handler():
    new_game()
                            
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
restart = frame.add_button("Restart", button_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
