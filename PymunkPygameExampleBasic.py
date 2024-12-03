import pygame
import pymunk
import math
import sys

# Initialize pygame
pygame.init()
# Game settings:
SIZE = 300, 300
FPS = 60
BG_COLOR = "black"
# Game setup:
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Pymunk physics world setup:
physics_world = pymunk.Space()  # you need to create a 'space' or 'world' which runs the physics simulation
physics_world.gravity = (0.0, 981.0)  # set the general gravity used in the physics space
physics_world.sleep_time_threshold = 0.3  # saw this in a pymunk example. Apparently it's necessary but Idk what it does :)
# Create a class that combines a dynamic physics box with the pygame image:
class Physics_Box:
    def __init__(self, size, color, x=150, y=150):
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        # Box doesn't exist, so we create a polygon shape with the point coordinates of a square box:
        # Calculate the points for the box based on it's size:
        half_width, half_height = round(size / 2), round(size / 2)
        points = [(-half_width, -half_height), (-half_width, half_height), (half_width, half_height),
                  (half_width, -half_height)]

        mass = 1.0  # box mass
        moment = pymunk.moment_for_poly(mass, points, (0, 0))  # moment required for pymunk body objects
        body = pymunk.Body(mass, moment,
                           body_type=pymunk.Body.DYNAMIC)  # create the main physics box. This contains all the main info like position and speed.
        body.position = (
        self.x, self.y)
        self.body = body
        shape = pymunk.Poly(body,
                            points)  # creating the square box polygon shape. The body will use this to calculate collisions.
        shape.friction = 1
        # Now add the body to the physics space so it will calculate it dynamically inside the space:
        physics_world.add(body, shape)

        # Create an image of the box:
        self.image = pygame.Surface((size, size)).convert()  # convert for optimization
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(self.color)

    # drawing the rectangle on the screen:
    def draw(self):
        # get the x, y and angle of the physics body:
        x, y = self.body.position
        # the body angle is stored in radians, we need to convert it to degrees:
        angle = math.degrees(self.body.angle)
        # rotate the image to the correct angle:
        rotated_image = pygame.transform.rotate(self.image, angle)
        # the body x,y position stores it's center position, so when drawing the image we need to account for that:
        rotated_image_size = rotated_image.get_size()
        x = x - int(rotated_image_size[0] / 2)
        y = y - int(rotated_image_size[1] / 2)
        screen.blit(rotated_image, [x, y])


# Create a class that combines a static physics line that objects collide with and add pygame draw function to it:
class Physics_Line:
    def __init__(self, point_1, point_2, color):
        self.point_1 = point_1
        self.point_2 = point_2
        self.color = color

        # create a segment - a static line that physics objects collide with:
        # don't forget to invert the y values, since pymunk has an inverted y axis:
        line = pymunk.Segment(physics_world.static_body, (point_1[0], point_1[1]), (point_2[0], point_2[1]), 1.0)
        line.friction = 1.0
        # add the line to the physics space so it interacts with other objects in the physics space:
        physics_world.add(line)

    # drawing the line unto the screen:
    def draw(self):
        pygame.draw.line(screen, self.color, self.point_1, self.point_2)


boxes = []
# create 3 dynamic box instances:
for i in range(3):
    box = Physics_Box(30, "yellow", x=130 + i * 20, y=110 + i * 40)
    boxes.append(box)

ground = Physics_Line((0, 280), (300, 280), "red")

# Game loop:
while True:
    screen.fill(BG_COLOR)
    clock.tick(FPS)
    # Update the physics space to calculate physics dynamics (use a constant FPS and not the changing delta time in order to avoid big errors):
    physics_world.step(1 / FPS)
    # draw all physics instances unto screen:
    for box in boxes:
        box.draw()
    ground.draw()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
