import pygame

class Room:
    
    class Walls:
    
        class Direction:
        
            def __repr__(self):
                return self.__class__.__name__
            
    
        class North(Direction): pass
        class East(Direction): pass
        class South(Direction): pass
        class West(Direction): pass
        
    
    class StartPoint: pass
    
    
    def __init__(self, walls):
        self.walls = walls
                
    def __repr__(self):
        return "Walls: %s" % self.walls


class Maze:
    
    def __init__(self, size_x, size_y, start_x, start_y):
        self.size = (size_x, size_y)
        self.start = (start_x, start_y)
        self.rooms = [[Room([]) for x in xrange(size_x)] for y in xrange(size_y)]
    
    def get_room(self, x, y):
        """
        Gets the room at x, y.
        """
        return self.rooms[y][x]
        
    def set_room(self, x, y, room):
        """
        Sets the room at x, y.
        """
        # y and x are backwards here because we index by y first, then x. It makes the maze
        # look normal when the arrays are written/printed out.
        self.rooms[y][x] = room
        
    def set_room_binary(self, x, y, value):
        """
        Takes a binary number and uses bitwise AND to check for the existence of
        walls. 0b1000 being north, 0b0100 being east, 0b0010 being south and 0b0001
        being west.
        Sets the specified room in the maze to contain instances of the appropriate
        wall classes.
        Somewhat superceded by set_rooms_nesw().
        """
        walls = []
        
        if value & 0b1000: walls.append(Room.Walls.North())
        if value & 0b0100: walls.append(Room.Walls.East())
        if value & 0b0010: walls.append(Room.Walls.South())
        if value & 0b0001: walls.append(Room.Walls.West())
        
        self.rooms[y][x] = Room(walls)
        
    def set_rooms_binary(self, rooms):
        """
        Takes a two-dimensional list and sets all rooms using the values contained therein.
        """       
        iy = 0
        for y in rooms:
            ix = 0
            for x in y:
                self.set_room_binary(ix, iy, x)
                ix += 1
            iy += 1
            
    def set_room_nesw(self, x, y, nesw):
        """
        Takes a string of letters (n, e, s, w and/or x) which depict walls north, east, south
        and west, and the start position respectively.
        Sets the specified room in the maze to contain instances of the appropriate
        wall classes.
        """
        walls = []
        nesw = nesw.lower()
        
        if "n" in nesw: walls.append(Room.Walls.North())
        if "e" in nesw: walls.append(Room.Walls.East())
        if "s" in nesw: walls.append(Room.Walls.South())
        if "w" in nesw: walls.append(Room.Walls.West())
        if "x" in nesw: walls.append(Room.StartPoint())
        
        self.rooms[y][x] = Room(walls)
        
    def set_rooms_nesw(self, rooms):
        """
        Takes a two-dimensional list and sets all rooms using the values contained therein.
        """
        iy = 0
        for y in rooms:
            ix = 0
            for x in y:
                self.set_room_nesw(ix, iy, x)
                ix += 1
            iy += 1

ROOM_WIDTH = 50
ROOM_HEIGHT = 50
MAZE_START = (4, 4)

def draw_room(maze, position, window):
    """
    Works out the coordinates of the four corners of the room on the screen and draws
    walls where they should be. Draws an X in room containing the starting point.
    """
    width = ROOM_WIDTH
    height = ROOM_HEIGHT
    x = position[0] * width
    y = position[1] * height
    
    tl = (x, y)
    tr = (x + width, y)
    bl = (x, y + height)
    br = (x + width, y + height)
    
    walls = [x.__class__ for x in maze.get_room(position[0], position[1]).walls]
    lines = []
    
    if Room.Walls.North in walls:
        lines.append((tl,tr))
    if Room.Walls.East in walls:
        lines.append((tr,br))
    if Room.Walls.South in walls:
        lines.append((bl,br))
    if Room.Walls.West in walls:
        lines.append((tl,bl))
#    if Room.StartPoint in walls:
    if position == maze.start:
        lines.append((tl,br))
        lines.append((bl,tr))
        
    for coords in lines:
        pygame.draw.line(window, (255,255,255), coords[0], coords[1])
        
def move_pos(maze, position, direction, window):
    """
    Checks whether you're allowed to move in that direction (walls permitting) and
    draws a line from your position to your destination if so. Returns your new position
    or your old one if a wall blocked your way.
    """
    room = maze.get_room(position[0], position[1])
    position = list(position)
    
    if direction in [x.__class__ for x in room.walls]:
        #print "You cannot move that direction for there is a wall."
        return position
    
    half_room_x = ROOM_WIDTH/2
    half_room_y = ROOM_HEIGHT/2
    
    start_middle_x = (position[0] * ROOM_WIDTH) + half_room_x
    start_middle_y = (position[1] * ROOM_HEIGHT) + half_room_y
    line_start = (start_middle_x, start_middle_y)
    
    dest_add_x = dest_add_y = 0
    if direction is Room.Walls.North:
        dest_add_y = -ROOM_HEIGHT
        position[1] -= 1
    elif direction is Room.Walls.East:
        dest_add_x = ROOM_WIDTH
        position[0] += 1
    elif direction is Room.Walls.South:
        dest_add_y = ROOM_HEIGHT
        position[1] += 1
    elif direction is Room.Walls.West:
        dest_add_x = -ROOM_WIDTH
        position[0] -= 1
    
    dest_middle_x = start_middle_x + dest_add_x
    dest_middle_y = start_middle_y + dest_add_y
    line_end = (dest_middle_x, dest_middle_y)
    
    pygame.draw.line(window, (255,0,0), line_start, line_end)
    pygame.display.flip()
    
    return position
    
    
def draw_maze(window, maze):
    """
    Blanks the screen and (re)draws the maze.
    """
    window.fill((0,0,0))
    
    iy = 0
    for y in maze.rooms:
        ix = 0
        for x in y:
            draw_room(maze, (ix, iy), window)
            pygame.display.flip()
            #sleep(0.025)
            ix += 1
        iy += 1
    
    pygame.display.flip()


if __name__ == '__main__':
    from time import sleep
    from random import choice

    maze_rooms = [
        [ "new ", "w   ", "ne  ", "nsw ", "ns  ", "ns  ", "ns  ", "ns  ", "ns  ", "ne  " ],
        [ "ew  ", "ew  ", "w   ", "ns  ", "ns  ", "n   ", "ns  ", "ns  ", "n   ", "e   " ],
        [ "ew  ", "ews ", "ew  ", "nsw ", "ns  ", "s   ", "n   ", "ne  ", "ew  ", "ew  " ],
        [ "ew  ", "new ", "ew  ", "nw  ", "ns  ", "n   ", "e   ", "w   ", "e   ", "ew  " ],
        [ "ew  ", "w   ", "es  ", "esw ", "newx", "ew  ", "ew  ", "ew  ", "sw  ", "e   " ],
        [ "w   ", "es  ", "new ", "new ", "w   ", "s   ", "es  ", "ew  ", "wn  ", "e   " ],
        [ "ew  ", "nw  ", "s   ", "s   ", "    ", "ns  ", "ns  ", "s   ", "es  ", "ew  " ],
        [ "ew  ", "ew  ", "nw  ", "nes ", "ew  ", "nsw ", "ne  ", "nw  ", "ns  ", "es  " ],
        [ "sw  ", "s   ", "s   ", "nes ", "sw  ", "ns  ", "es  ", "sw  ", "ns  ", "nes " ]
    ]
    
    width = len(maze_rooms[0])
    height = len(maze_rooms)
    
    # Set up the maze
    maze = Maze(width, height, MAZE_START[0], MAZE_START[1])
    maze.set_rooms_nesw(maze_rooms)
    
    # Set up pygame window
    pygame.init()
    window = pygame.display.set_mode((width*ROOM_WIDTH, height*ROOM_HEIGHT))
    
    # Draw the maze
    draw_maze(window, maze)
    
    position = MAZE_START
    
    N = Room.Walls.North
    E = Room.Walls.East
    S = Room.Walls.South
    W = Room.Walls.West
    
    directions = (N, E, S, W)
    
    # Run the maze ten times and work out how many moves it takes on average
    attempts = 10
    moves_average = 0
    for i in xrange(attempts):
        draw_maze(window, maze)
        position = (4, 4)
        moves = 0
        while True:
            moves += 1
            try:
                position = move_pos(maze, position, choice(directions), window)
            except IndexError:
                print "You escaped in %d moves!" % moves
                break
        moves_average += moves
    print "On average, it took %s moves to get out of the maze." % (moves_average / attempts)
    
    #dirs = [ S, E, N, N, E, N, W, N, W, W, W, N, W, N ]
    
    #for d in dirs:
    #    position = move_pos(maze, position, d, window)
    #    sleep(0.25)

    
    
    
    
