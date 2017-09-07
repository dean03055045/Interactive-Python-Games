"""
2D space game RickRocks inspired by the classic arcade game Asteroids(1979).

Click the splash screen to start the game.
Control the spaceship via four bottons: right and left key to rotate, 
up key to accelerate and space key to shoot missiles.
Destroy asteroids before they strike the spaceship.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_bzbTdhZT6FYAP9Z.py"
"""
import simplegui
import math
import random

# globals variables
WIDTH = 800
HEIGHT = 600
ANGLE_VEL_INC = 0.04
MISSILE_VEL = 5
ROCK_VEL = 2
MAX_ROCK_NUM = 12


class ImageInfo:
    """
    Class for managing images
    """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self._center = center
        self._size = size
        self._radius = radius
        if lifespan:
            self._lifespan = lifespan
        else:
            self._lifespan = float('inf')
        self._animated = animated

    def get_center(self):
        """
        Getter for image center
        Returns a list of two integers
        """
        return self._center

    def get_size(self):
        """
        Getter for image size
        Returns a list of two integers
        """
        return self._size

    def get_radius(self):
        """
        Getter for image radius
        Returns an integer
        """
        return self._radius

    def get_lifespan(self):
        """
        Getter for image lifespan
        Returns an integer
        """
        return self._lifespan

    def get_animated(self):
        """
        Getter for image animated
        Returns a Boolean
        """
        return self._animated   


############### Register images and sound ###############
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    """
    Convert angle to vector
    Returns a list of two floats
    """
    return [math.cos(ang), math.sin(ang)]

def dist(item1,item2):
    """
    Calculate the distance between item1 and item2
    Returns a float
    """
    return math.sqrt((item1[0] - item2[0]) ** 2+(item1[1] - item2[1]) ** 2)

def process_sprite_group(a_set, canvas):
    """
    Call the update and draw methods for each sprite in the group
    """
    for item in set(a_set):
        item.draw(canvas)
        item.update()
        # remove the sprite when the age is greater than lifespan
        if item.update() == True:
            a_set.remove(item)            
        

class Ship:
    """
    Class for spaceship
    """
    def __init__(self, pos, vel, angle, image, info):
        self._pos = [pos[0],pos[1]]
        self._vel = [vel[0],vel[1]]
        self._thrust = False
        self._angle = angle
        self._angle_vel = 0
        self._image = image
        self._image_center = info.get_center()
        self._image_size = info.get_size()
        self._radius = info.get_radius()
        
    def draw(self,canvas):
        """
        Handler for drawing spaceship
        """
        if self._thrust == False:
            canvas.draw_image(self._image, self._image_center, 
                              self._image_size, self._pos, self._image_size, self._angle)
        else:
            canvas.draw_image(self._image, 
                              (self._image_center[0] + self._image_size[0], self._image_center[1])
                              , self._image_size, self._pos, self._image_size, self._angle)

    def update(self):
        """
        Update the position of spaceship
        """                
        # update position based on velocity
        self._pos[0] = (self._pos[0] + self._vel[0]) % WIDTH 
        self._pos[1] = (self._pos[1] + self._vel[1]) % HEIGHT        
        
        # increment angle by angular velocity
        self._angle += self._angle_vel
        
        # friction
        self._vel[0] *= (1-0.01)
        self._vel[1] *= (1-0.01)
        
        # acceleration
        if self._thrust:
            forward = angle_to_vector(self._angle)
            self._vel[0] += forward[0] / 10
            self._vel[1] += forward[1] / 10     
        
    def angle_vel_update(self, angle_vel_inc):
        """
        Increment the angular velocity by a fixed amount
        """
        self._angle_vel += angle_vel_inc
    
    def thrust_on(self):
        """
        Turn the thrusters on
        """
        self._thrust = True
        ship_thrust_sound.play()
        
    def thrust_off(self):
        """
        Turn the thrusters off
        """
        self._thrust = False
        ship_thrust_sound.rewind()
    
    def shoot(self):
        """
        Spawn a new missile
        Return a Sprite object
        """        
        forward = angle_to_vector(self._angle)        
        # missile's initial position is the tip of ship's "cannon"
        missile_pos = [self._pos[0] + forward[0] * self._radius, 
                       self._pos[1] + forward[1] * self._radius]                 
        missile_vel = [self._vel[0] + forward[0] * MISSILE_VEL, 
                       self._vel[1] + forward[1] * MISSILE_VEL]        
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        return a_missile
            
    def get_radius(self):
        """
        Getter for ship radius
        Returns an integer
        """
        return self._radius
    
    def get_position(self):
        """
        Getter for ship position
        Returns a list of two integers
        """
        return self._pos    

class Sprite:
    """
    Class for rocks and missiles
    """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self._pos = [pos[0],pos[1]]
        self._vel = [vel[0],vel[1]]
        self._angle = ang
        self._angle_vel = ang_vel
        self._image = image
        self._image_center = info.get_center()
        self._image_size = info.get_size()
        self._radius = info.get_radius()
        self._lifespan = info.get_lifespan()
        self._animated = info.get_animated()
        self._age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        """
        Handler for drawing rocks and missiles
        """
        if not self._animated:
            canvas.draw_image(self._image, self._image_center, self._image_size, 
                              self._pos, self._image_size, self._angle)
        else:
            # draw explosions
            index = self._age % 24
            new_center = [self._image_center[0] + index * self._image_size[0], self._image_center[1]]
            canvas.draw_image(self._image, new_center, self._image_size, 
                              self._pos, self._image_size, self._angle)
    
    def update(self):
        """
        Update the position of rocks and missiles
        """
        # update position based on velocity
        self._pos[0] = (self._pos[0] + self._vel[0]) % WIDTH
        self._pos[1] = (self._pos[1] + self._vel[1]) % HEIGHT       
        
        # increment angle by angular velocity
        self._angle += self._angle_vel
        
        # remove the sprite when the age is greater than lifespan
        self._age += 1
        if self._age >= self._lifespan:
            return True
        else:
            return False        
    
    def get_radius(self):
        """
        Getter for radius
        Returns an integer
        """
        return self._radius
    
    def get_position(self):
        """
        Getter for position
        Returns a list of two integers
        """
        return self._pos
    
    def collide(self, other_object):
        """
        Take another object as an argument, decide whether there is a collision or not
        Return a Boolean
        """
        if dist(self._pos, other_object.get_position()) <= (self._radius + other_object.get_radius()):
            return True
        else:
            return False
    
class GameGUI:
    """
    Class to run the game and GUI
    """
    def __init__(self):
        # field of gamestate 
        self._score = 0
        self._lives = 3
        self._time = 0
        self._started = False
        self._my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        self._rock_group = set([])
        self._missile_group = set([])
        self._explosion_group = set([])
        
        #field of GUI
        self._frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_keyup_handler(self.keyup)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.start()
        self._timer = simplegui.create_timer(1000.0, self.rock_spawner)
        self._timer.start()
                
    def keydown(self, key):
        """
        Keydown handler
        """
        if simplegui.KEY_MAP["up"] == key:
            self._my_ship.thrust_on()
        elif simplegui.KEY_MAP["left"] == key:
            self._my_ship.angle_vel_update(-ANGLE_VEL_INC)
        elif simplegui.KEY_MAP["right"] == key:
            self._my_ship.angle_vel_update(ANGLE_VEL_INC)
        elif simplegui.KEY_MAP["space"] == key:
            a_missile = self._my_ship.shoot()
            self._missile_group.add(a_missile)
        
    def keyup(self, key):
        """
        Keyup handler
        """
        if simplegui.KEY_MAP["up"] == key:
            self._my_ship.thrust_off()
        elif simplegui.KEY_MAP["left"] == key:
            self._my_ship.angle_vel_update(ANGLE_VEL_INC)
        elif simplegui.KEY_MAP["right"] == key:
            self._my_ship.angle_vel_update(-ANGLE_VEL_INC)
                 
    def click(self, pos):
        """
        Mouseclick handlers that reset UI and conditions whether splash image is drawn
        """
        center = [WIDTH / 2, HEIGHT / 2]
        size = splash_info.get_size()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (not self._started) and inwidth and inheight:            
            self._started = True
            self._score = 0
            self._lives = 3           
            soundtrack.rewind()
            soundtrack.play()
            
    def draw(self, canvas):
        """
        Draw handler
        """    
        # animiate background
        self._time += 1
        wtime = (self._time / 4) % WIDTH
        center = debris_info.get_center()
        size = debris_info.get_size()
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
        canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

        # draw UI
        canvas.draw_text("Lives", [50, 50], 22, "White")
        canvas.draw_text("Score", [680, 50], 22, "White")
        canvas.draw_text(str(self._lives), [50, 80], 22, "White")
        canvas.draw_text(str(self._score), [680, 80], 22, "White")
    
        # draw ship and sprites
        self._my_ship.draw(canvas)
        process_sprite_group(self._rock_group, canvas)
        process_sprite_group(self._missile_group, canvas)
        process_sprite_group(self._explosion_group, canvas)
    
        # update ship 
        self._my_ship.update()
    
        # draw splash screen if not started
        if not self._started:
            canvas.draw_image(splash_image, splash_info.get_center(), 
                              splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                              splash_info.get_size())

        # midify score and lives                    
        if self.group_collide(self._rock_group, self._my_ship):
            self._lives -= 1    
        self._score += self.group_group_collide(self._rock_group, self._missile_group)
    
        # game over
        if self._lives == 0:
            self._started = False
            self._rock_group = set([])
            
    def rock_spawner(self):
        """
        Timer handler that spawns rocks
        """    
        rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        rock_vel = [random.choice([ROCK_VEL, -ROCK_VEL])*random.random(), 
                    random.choice([ROCK_VEL, -ROCK_VEL])*random.random()]
        rock_ang = random.random()* math.pi * 2
        rock_ang_vel = random.choice([1, -1]) * random.random() * 0.1
    
        # varying the rock velocity based on the score as the game progresses 
        if self._score > 10:   
            rock_vel[0] *= (self._score / 10)
            rock_vel[1] *= (self._score / 10)
        
        # make sure rocks are some distance away from the ship
        if dist(rock_pos, self._my_ship.get_position()) >= 80:        
            # limit the total number of rocks
            if len(self._rock_group) < MAX_ROCK_NUM and self._started:  
                a_rock = Sprite(rock_pos, rock_vel, rock_ang, rock_ang_vel, asteroid_image, asteroid_info)
                self._rock_group.add(a_rock)
    
    def group_collide(self, group, other_object):
        """
        Check the collisions between other_object and elements in the group
        Return a Boolean
        """
        collided = False
        for thing in set(group):
            if thing.collide(other_object):
                # create a new explosion if collided
                new_explosion = Sprite(thing.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
                self._explosion_group.add(new_explosion)            
                group.remove(thing)
                collided = True            
        return collided    

    def group_group_collide(self, group1, group2):
        """
        Check the collisions between two groups and remove the element
        Return an integer which represents the number of elements in first group 
        that collide with the second group 
        """
        collide_number = 0
        for item in set(group1):
            if self.group_collide(group2, item):
                group1.remove(item)
                collide_number += 1
        return collide_number

    
def run_gui():
    """
    Instantiate and run the GUI.
    """
    gui = GameGUI()

run_gui()
