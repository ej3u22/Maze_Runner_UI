__author__ = "Eden Jack"
__credits__ = ["Eden Jack"]
__email__ = "ej3u22@soton.ac.uk"
# Date Created:    28/10/2025
"""
 A top layer of code, taking the underlying maze functions of rest of the module.
"""

# Going to take a maze, create a UI based around it.

# Imports
import time
import tkinter


import maze
import runner
import math
import maze_runner

# Globals
root = tkinter.Tk()
CELL_SIZE       = 40
CANVAS_PADDING  = 2
EXPLORE_LIVE    = False
EXPLORE_AVATAR  = "Mouse" #Mouse/Wolf/Bugbin
EXPLORE_TIME    = 5 #Seconds taken to visibly complete maze, if the LIVE config is disabled.

# Holders for maze drawing functions
def draw_horizontal(maze_canvas, maze_object):
    pass


def draw_vertical(maze_canvas, maze_object):
    pass


global mouse_coord

def update_mouse_coord(event):
    '''
    This serves as a method of determining the location of the users mouse (pointer) coordinates in the maze.
    Useful for debugging what has happened and where.
    
    :param event: The information containing the mouse's coordinates.
    '''
    global mouse_coord
    global CELL_SIZE
    global CANVAS_PADDING

    canvas = event.widget
    x = (
        canvas.canvasx(event.x) + CANVAS_PADDING + (CELL_SIZE / 2)
    ) / CELL_SIZE - 1  # As the grid starts at 0, we need to reduce by 1!
    y = (
        canvas.winfo_height() - canvas.canvasy(event.y) + (CELL_SIZE / 2)
    ) / CELL_SIZE - 1  # This needs actually be the inverse of the correct number.

    mouse_coord.config(text=f"x: {int(x)} y: {int(y)}")


def create_maze(maze_canvas: tkinter.Canvas, maze_object):
    '''
    Recreates a maze from the information given.
    '''
    import time

    global CELL_SIZE
    global CANVAS_PADDING

    m_size_x, m_size_y = maze.get_dimensions(
        maze_object
    )  # Fetch the dimensions of the given maze.
    if m_size_x * CELL_SIZE > 1000 and m_size_y * CELL_SIZE > 1000:
        CELL_SIZE = math.floor(1000 / m_size_x)

    if m_size_x > 10000:
        print("Cannot fathom printing a file of this size")
        print(" A blank display is now being presented")
        maze_canvas.config(
            width=(100 * CELL_SIZE) + CANVAS_PADDING,
            height=(100 * CELL_SIZE) + CANVAS_PADDING,
        )

        return
    m_start_x = CANVAS_PADDING
    m_start_y = CANVAS_PADDING
    m_end_x = m_size_x * CELL_SIZE
    m_end_y = m_size_y * CELL_SIZE
    maze_canvas.config(
        width=(m_size_x * CELL_SIZE) + CANVAS_PADDING,
        height=(m_size_y * CELL_SIZE) + CANVAS_PADDING,
    )

    # Walls, extract the information for the maze using the "get_walls" function.
    # This was purpose built for a specific method of reading walls.
    Deconstructed_maze = {
        "vertical":[],
        "horizontal":[]
        }
    def fill_list(this_list):
        for _ in range(0, m_size_y+1):
            this_row = []
            for _ in range(0, m_size_x+1):
                this_row.append(".")
            this_list.append(this_row)

    fill_list(Deconstructed_maze["horizontal"])
    fill_list(Deconstructed_maze["vertical"])

    for y_coord in range(0, m_size_y):
        for x_coord in range(0, m_size_x):
            n, e, s, w = maze.get_walls(maze_object, x_coord, y_coord)
            if n:
                Deconstructed_maze["horizontal"][y_coord+1][x_coord] = "-"
            if s:
                Deconstructed_maze["horizontal"][y_coord][x_coord] = "-"
            if w: 
                Deconstructed_maze["vertical"][y_coord+1][x_coord] = "|"
            if e: 
                Deconstructed_maze["vertical"][y_coord+1][x_coord+1] = "|"

    # Verticals
    this_vertical = Deconstructed_maze["vertical"][::-1]
    for this_row in range(0, len(this_vertical)):
        for index, wall in enumerate(this_vertical[this_row]):
            wall_x = CANVAS_PADDING + (index * CELL_SIZE)
            wall_y = CANVAS_PADDING + (this_row * CELL_SIZE)
            if wall == "|":
                wall_x_end = wall_x
                wall_y_end = wall_y + CELL_SIZE
                maze_canvas.create_line(wall_x, wall_y, wall_x_end, wall_y_end)
                # time.sleep(0)

    # Horizontals
    this_horizontal = (Deconstructed_maze["horizontal"])[::-1]
    for this_row in range(0, len(this_horizontal)):
        for index, wall in enumerate(this_horizontal[this_row]):
            wall_x = CANVAS_PADDING + (index * CELL_SIZE)
            wall_y = CANVAS_PADDING + (this_row * CELL_SIZE)
            if wall == "-":
                wall_x_end = wall_x + CELL_SIZE
                wall_y_end = wall_y
                maze_canvas.create_line(wall_x, wall_y, wall_x_end, wall_y_end)
                # time.sleep(0)
    maze_canvas.bind("<Motion>", update_mouse_coord)
    return


def render_runner(maze_canvas, maze_object, runner_object, exploring, runner_name = "Mouse"):
    # As tkinter does not like having image rapidly created and destroyed, we instead need to think slightly oddly.
    # Instead of tkinter rapidly destroying and creating an image, we will simply initialize our images at the start.
    # All frames needed for the mouse will now be created and stored in one place, all other images will be held outside of view.
    # This *should* stop the rapid "flickering" effect, but testing will need to find out.

    global CELL_SIZE
    global CANVAS_PADDING
    global EXPLORE_TIME
    global done

    def MakeImageSet(file_path, runner_name):
        images = ["run0", "run1", "jump", "dead"]
        frames = {}
        pics = {}
        for index, name in enumerate(images):
            this_img = tkinter.PhotoImage(
                file=str(f"{file_path}/{runner_name}({index}).png")
            )
            this_ui = maze_canvas.create_image(
                (100, 100), image=this_img, anchor="nw", tags=(name)
            )
            maze_canvas.itemconfig(this_ui, state="hidden")
            maze_canvas.move(this_ui, 10 * index, 10)
            frames[name] = this_ui
            pics[name] = this_img
            #time.sleep(0.1)
        return frames, pics

    runner_frames, pics = MakeImageSet(
        "Images", runner_name
    )  # Frames, then table of images so they stay existing in memory

    _, m_size_y = maze.get_dimensions(
        maze_object
    )  # Fetch the dimensions of the given maze.
    height = (m_size_y * CELL_SIZE) - CANVAS_PADDING
    runner_ui = runner_frames[
        "run0"
    ]  # maze_canvas.create_image((0,0), image=runner_img, anchor="nw")

    mouse_frame = 1
    time.sleep(0)
    current_x = 0
    current_y = height

    index_crumbs    = [] #numerical key for
    placed_crumbs   = [] #placed crumbs

    #Create local runner animations
    def move_avatar(step_x, step_y):
        nonlocal mouse_frame
        nonlocal current_x
        nonlocal current_y
        nonlocal index_crumbs
        nonlocal placed_crumbs

        target_x = CANVAS_PADDING + (step_x * CELL_SIZE)
        target_y = CANVAS_PADDING + (height - (step_y * CELL_SIZE)) # 24 pixels high

        mouse_frame = mouse_frame == 0 and 1 or 0

        current_runner = (
            mouse_frame == 0 and runner_frames["run0"] or runner_frames["run1"]
        )
        old_runner = mouse_frame == 1 and runner_frames["run0"] or runner_frames["run1"]
        old_x = current_x
        old_y = current_y

        show_me_x, show_me_y = maze_canvas.coords(current_runner)
        hide_me_x, hide_me_y = maze_canvas.coords(old_runner)
    
        current_x = old_x + 0.5 * (target_x - old_x)
        current_y = old_y + 0.5 * (target_y -(24) - old_y) #24 pixels high.
        maze_canvas.itemconfig(old_runner, state="hidden")
        maze_canvas.itemconfig(current_runner, state="normal")
    
        # For whatever reason, there may be a frame or two that this hangs for.
        maze_canvas.move(current_runner, current_x - show_me_x, current_y - show_me_y)
        maze_canvas.move(old_runner, hide_me_x - current_x, hide_me_y - current_y)

        if not ((target_x, target_y) in index_crumbs):
            index_crumbs.append((step_x, step_y))
            placed_crumbs.append(maze_canvas.create_rectangle((target_x + CELL_SIZE/2,target_y- CELL_SIZE/2), (target_x+ CELL_SIZE/2,target_y- CELL_SIZE/2), fill="grey"))
        

    while exploring[0] == "Searching": # We are moving our runner in real time, this requires us using threads and messy systems.

        current_step = (runner.get_x(runner_object), runner.get_y(runner_object))

        move_avatar(current_step[0], current_step[1])
        
        time.sleep(1/60)

    while exploring[0] == "Tracing": # We have already got a list of steps, we are now just tracing over them.
        if not isinstance(exploring[1], list): continue #Ensure we have the list, otherwise do not continue

        breadcrumbs = exploring[1]
        time_per_step = EXPLORE_TIME/len(breadcrumbs)
        for step in range(0, len(breadcrumbs)):
            max_steps = 13
            for i in range(0, max_steps):
                move_avatar(breadcrumbs[step][0], breadcrumbs[step][1])
                time.sleep(time_per_step / max_steps)
        exploring[0] = "Finished"
    
        while exploring[0] == "Finished":
            time.sleep(0.1)


    if exploring[0] == "Shortest" and isinstance(exploring[1], list):
        shortestpath = exploring[1]
        for coord_string in shortestpath:
            coord_index = coord_string[0], coord_string[1]
            if coord_index in index_crumbs:
                this_index = index_crumbs.index(coord_index)
                given_crumb = placed_crumbs[this_index]
                maze_canvas.itemconfig(given_crumb, outline="green", width=4)
        

def create_window(maze_object, given_goal):
    '''
    Docstring for create_window
    
    :param maze_object: The actual maze object that has been created
    :param given_goal: If the user has passed a goal in the terminal, it is passed here, otherwise it defaults as None
    '''
    import threading

    global done
    global EXPLORE_AVATAR

    # Window properties
    root.title("Maze Viewer")
    root.configure(background="black")
    root.minsize(400, 400)
    root.maxsize(10000, 10000)
    root.geometry("1000x1000+00+0")
    photo = tkinter.PhotoImage(file="Images/Mouse.ico")
    root.iconphoto(False, photo)

    global mouse_coord

    maze_name = "Test Maze"

    title_list = tkinter.Label(
        root, text=f"This is a maze called {maze_name}"
    )
    mouse_coord = tkinter.Label(root, text="x: 0, y: 0")
    maze_window = tkinter.Canvas(root, width=400, height=400)

    create_maze(maze_window, maze_object)

    #Check that runner has it's fundamental functions, create and explore
    if "create_runner" in dir(runner) and "explore" in dir(runner):
        runner_object = runner.create_runner()
        global EXPLORE_LIVE
        explore_state = [EXPLORE_LIVE and "Searching" or "Tracing", None] # This is keyed into an array so that the given value can be read and changed dynamically

        explore_display_thread = threading.Thread(
            target=render_runner,
            args=(maze_window, maze_object, runner_object, explore_state, EXPLORE_AVATAR),
            daemon=True,
        )
        explore_display_thread.start()

        def hold(runner_object, maze_object):
            global EXPLORE_LIVE
            breadcrumbs = runner.explore(runner_object, maze_object, given_goal)

            if not EXPLORE_LIVE:
                explore_state[1] = breadcrumbs
                explore_state[0] = "Tracing"
                while not explore_state[0] == "Finished":
                    time.sleep(0.1)

            if "shortest_path" in dir(maze_runner): # Checks that the shortest path function exists, ignores if not
                shortestpath = maze_runner.shortest_path(maze_object, starting=(0,0), goal=given_goal)# runner=runner_object, breadcrumbs=breadcrumbs)
                explore_state[1] = shortestpath
                explore_state[0] = "Shortest"
            else:
                explore_state[0] = "Complete"

        explore_thread = threading.Thread(
            target=hold, args=(runner_object, maze_object), daemon=True
        )
        explore_thread.start()

    title_list.grid(row=0, column=0, pady=2)
    maze_window.grid(row=1, column=0, pady=2)
    mouse_coord.grid(row=0, column=1, pady=2)

    root.mainloop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.description = "ECS Maze Runner"
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")

    parser.add_argument("-r", "--runner", type=int, choices=[0,1,2], help="chooses the runner 0 is Mouse, 1 is Wolf, 2 is Bugbin")
    parser.add_argument("-s", "--speed", type=int, help="determines the length of time the runner will solve the maze in")
    parser.add_argument("-l", "--live", action="store_true", help="will attempt to display the runner at it's live position, requires the runner to use time.sleep")
    parser.add_argument("-g", "--goal", nargs="+", type=int, help="Select your goal target; x y")

    args = parser.parse_args()
    if args.speed != None:
        EXPLORE_TIME = args.speed
    if args.runner != None:
        if args.runner == 0:
            EXPLORE_AVATAR = "Mouse"
        elif args.runner == 1:
            EXPLORE_AVATAR = "Wolf"
        elif args.runner == 2:
            EXPLORE_AVATAR = "Bugbin"
    if args.live:
        EXPLORE_LIVE = True
    given_goal = None
    if args.goal != None:
        given_goal = tuple(args.goal)
    maze_object = maze_runner.maze_reader(args.maze)
    create_window(maze_object, given_goal)
