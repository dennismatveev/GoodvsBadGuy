# Dennis Matveev
# Final Project

import graphics
import random
import winsound
from tkinter import messagebox

images = {"bad": "ProjectGifs/bad_guy.gif",
          "good": "ProjectGifs/good_guy.gif",
          "brick": "ProjectGifs/wall.png",
          "bullet_left": "ProjectGifs/bullet0-1lt.gif",
          "bullet_right": "ProjectGifs/bullet01rt.gif",
          "bullet_up": "ProjectGifs/bullet-10up.gif",
          "bullet_down": "ProjectGifs/bullet10dn.gif"}

sounds = {"gdshot": "ProjectSounds/gdshot.wav",
          "bdshot": "ProjectSounds/bdshot.wav",
          "bd_die": "ProjectSounds/bad_die.wav",
          "endgame": "ProjectSounds/endgame.wav",
          "gd_die": "ProjectSounds/death.wav",
          "victory": "ProjectSounds/victory.wav"}
#
# images = {"bad": "ProjectGifs/bad_guy36.gif",
#           "good": "ProjectGifs/good_guy36.gif",
#           "brick": "ProjectGifs/wall36.png",
#           "bullet_left": "ProjectGifs/bullet0-1lt36.gif",
#           "bullet_right": "ProjectGifs/bullet01rt36.gif",
#           "bullet_up": "ProjectGifs/bullet-10up36.gif",
#           "bullet_down": "ProjectGifs/bullet10dn36.gif"}
IMAGE_SIZE = 72
level = 1
lives = 3
score = 0
board = None
bricks = []
good_guy = [None, None]
bad_guys_list = []
bullet_list = []
temp_cell = [None, None, None]
previous_key = [0, 0]
game_window = None
my_life_label = None
my_score_label = None


def setup_board():
    global bricks
    global board
    global level

    # Create a 15 vertical x 20 horizontal board filled with None
    board = [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None]]

    for row_number in range(len(board)):

        for square_number in range(20):

            # Horizontal Walls on Top
            if row_number == 0 and square_number <= 7 or row_number == 0 and square_number >= 12:
                display_on_board("brick", [row_number, square_number])
                bricks.append([row_number, square_number])

            # Horizontal Walls on Bottom
            if row_number == 14 and square_number <= 7 or row_number == 14 and square_number >= 12:
                display_on_board("brick", [row_number, square_number])
                bricks.append([row_number, square_number])

            # Vertical walls on Left Side
            if square_number == 0 and (row_number >= 1 and row_number <= 13):
                display_on_board("brick", [row_number, square_number])
                bricks.append([row_number, square_number])

            # Vertical walls on right Side
            if square_number == 19 and (row_number >= 1 and row_number <= 13):
                display_on_board("brick", [row_number, square_number])
                bricks.append([row_number, square_number])
            if level == 2:
                # Vertical Obstacle
                if (square_number == 7 or square_number == 12) and row_number < 5:
                    display_on_board("brick", [row_number, square_number])
                    bricks.append([row_number, square_number])
                if (square_number == 7 or square_number == 12) and row_number > 9:
                    display_on_board("brick", [row_number, square_number])
                    bricks.append([row_number, square_number])
            if level == 1:
                # Horizontal Obstacle
                if row_number == 7 and square_number >= 6 and square_number <= 13:
                    display_on_board("brick", [row_number, square_number])
                    bricks.append([row_number, square_number])

                # Vertical Obstacle
                if (square_number == 5 or square_number == 14) and row_number >= 5 and row_number <= 9:
                    display_on_board("brick", [row_number, square_number])
                    bricks.append([row_number, square_number])

    return board


def set_up_warriors(board):
    global bricks
    global bad_guys_list
    global good_guy

    # Generate a random location for good_guy to spawn
    good_guy_row = random.randint(0, 14)
    good_guy_col = random.randint(0, 19)
    while board[good_guy_row][good_guy_col] is not None:
        good_guy_row = random.randint(0, 14)
        good_guy_col = random.randint(0, 19)
    # Display visually and assign coordinates on board
    display_on_board("good", [good_guy_row, good_guy_col])
    good_guy = [good_guy_row, good_guy_col]

    # Create multiple bad guys randomly spawning on board
    for bad_guys in range(4 + 2 * level):
        row = random.randint(0, 14)
        col = random.randint(0, 19)
        while board[row][col] is not None:
            row = random.randint(0, 14)
            col = random.randint(0, 19)
        # Display visually and add the location to list of bad guys
        display_on_board("bad", [row, col])
        bad_guys_list.append([row, col])

    return board


def display_on_board(image, location):
    global images
    global board
    # Graphically show the image
    board[location[0]][location[1]] = graphics.Image(graphics.Point(IMAGE_SIZE / 2 + location[1] * IMAGE_SIZE,
                                                                    IMAGE_SIZE / 2 + location[0] * IMAGE_SIZE),
                                                     images[image])


def move_character_on_board(location, delta, do_back_up):
    global board
    # In situation that two images overlap, backup
    if do_back_up:
        backup_obstacle(location[0] + delta[0], location[1] + delta[1])
    # Move the character on the board variable and graphically
    board[location[0] + delta[0]][location[1] + delta[1]] = board[location[0]][location[1]]
    board[location[0]][location[1]] = None
    board[location[0] + delta[0]][location[1] + delta[1]].move(delta[1] * IMAGE_SIZE, delta[0] * IMAGE_SIZE)
    return board


def is_cell_taken(location):
    # Check what the object at the location is
    if bricks.count(location) > 0:
        return "bk"
    if bad_guys_list.count(location) > 0:
        return "bd"
    if good_guy[0] == location[0] and good_guy[1] == location[1]:
        return "gd"
    if get_bullet_at(location) is not None:
        return "bt"


def reincarnate():
    global images
    global good_guy
    global board

    # If good_guy dies, bring him back in a random location on the board
    if lives > 0:
        # Generate new location
        good_guy_row = random.randint(0, 14)
        good_guy_col = random.randint(0, 19)
        while board[good_guy_row][good_guy_col] is not None:
            good_guy_row = random.randint(0, 14)
            good_guy_col = random.randint(0, 19)
        # Move from old location to new location on board
        jump_row = good_guy_row - good_guy[0]
        jump_col = good_guy_col - good_guy[1]

        # Graphically move good_guy and assign his coordinates
        move_character_on_board(good_guy, [jump_row, jump_col], False)
        good_guy = [good_guy[0] + jump_row, good_guy[1] + jump_col]
        restore_obstacle()


def die():
    global game_window
    global my_life_label
    global lives

    # Upon dying decrease lives, show a message visually change lives and then reincarnate
    lives -= 1
    if lives == 0:
        winsound.PlaySound(sounds["endgame"], winsound.SND_FILENAME)
        messagebox.showerror("GAME OVER", "NICE TRY... LOSER")
        exit()
    else:
        my_life_label.undraw()
        my_life_label = graphics.Text(graphics.Point(17.5 * IMAGE_SIZE, 2 * IMAGE_SIZE), f"Lives: {lives}")
        my_life_label.setOutline("Red")
        my_life_label.setStyle('bold')
        my_life_label.draw(game_window)
        winsound.PlaySound(sounds["gd_die"], winsound.SND_FILENAME)
        messagebox.showwarning("You Died...", f"Lives Remaining: {lives}")
        reincarnate()
        return


def increase_score():
    global my_score_label
    global game_window
    global score
    global level

    # When a bad guy dies, increase the score by 10 and show visually
    score += 10
    my_score_label.undraw()
    my_score_label = graphics.Text(graphics.Point(17.5 * IMAGE_SIZE, 13 * IMAGE_SIZE), f" Score: {score} \n"
                                                                                       f" Level: {level}")
    my_score_label.setOutline("Blue")
    my_score_label.setStyle('bold')
    my_score_label.draw(game_window)


def get_bullet_at(location):
    global bullet_list

    # Get the coordinates of the bullet from the list of bullets
    for bullet in bullet_list:
        if location[0] == bullet[0][0] and location[1] == bullet[0][1]:
            return bullet
    return None


def remove_bullet(bullet):
    global board
    global bullet_list

    # Undraw the bullet, take it out from the board and remove from list
    board[bullet[0][0]][bullet[0][1]].undraw()
    board[bullet[0][0]][bullet[0][1]] = None
    bullet_list.remove(bullet)


def remove_bad(location):
    global bad_guys_list
    global board

    # Undraw bad_guy, remove from board and from list, and increase score
    board[location[0]][location[1]].undraw()
    board[location[0]][location[1]] = None
    bad_guys_list.remove(location)
    winsound.PlaySound(sounds["bd_die"], winsound.SND_FILENAME)
    increase_score()


def movebads():
    global bad_guys_list
    global good_guy
    global bricks
    global board
    # Each bad in the list will do this...

    shooter = bad_guy_shoot()  # not necessrily, the fucntion may return right away

    # Each bad in the list will do this...
    for bad in bad_guys_list:

        if bad == shooter:
            continue
            # if you shoot, you should not move. It is unfair otherwise
            # in case of good guy it is either shoot or move

        move = None
        move1 = None
        move2 = None
        move3 = None
        move4 = None
        distance1 = 0
        distance2 = 0

        # can I move towards the good guy by X ?
        # move 1 is a best move, move 3 is reverse but still and option
        if good_guy[0] < bad[0]:
            move1 = [-1, 0]
            distance1 = bad[0] - good_guy[0]
            move3 = [1, 0]
        elif good_guy[0] > bad[0]:
            move1 = [1, 0]
            distance1 = good_guy[0] - bad[0]
            move3 = [-1, 0]
        else:
            move1 = [1, 0]
            move3 = [-1, 0]

        # can I move towards the good guy by Y ?
        # move 2 is a best move, move 4 is reverse but still and option
        if good_guy[1] < bad[1]:
            move2 = [0, -1]
            distance2 = bad[1] - good_guy[1]
            move4 = [0, 1]
        elif good_guy[1] > bad[1]:
            move2 = [0, 1]
            distance2 = good_guy[1] - bad[1]
            move4 = [0, -1]
        else:
            move2 = [0, 1]
            move4 = [0, -1]

        # pick one of the possible found moves with a 50% change of toward good_guy
        if distance1 > distance2:
            move = random.choice([move1, move1, move1, move2, move3, move4])
        else:
            move = random.choice([move2, move2, move2, move1, move3, move4])

        # if bad moves- check for collisions and remove accordingly
        if move is not None:
            if is_cell_taken([bad[0] + move[0], bad[1] + move[1]]) == "gd":
                die()
            elif is_cell_taken([bad[0] + move[0], bad[1] + move[1]]) == "bk":
                remove_bad(bad)
            elif is_cell_taken([bad[0] + move[0], bad[1] + move[1]]) == "bt":
                remove_bad(bad)
                remove_bullet(get_bullet_at([bad[0] + move[0], bad[1] + move[1]]))
            elif is_cell_taken([bad[0] + move[0], bad[1] + move[1]]) == "bd":
                remove_bad(bad)
                remove_bad([bad[0] + move[0], bad[1] + move[1]])
            elif bad[0] + move[0] < 0:
                remove_bad(bad)
            elif bad[0] + move[0] > 14:
                remove_bad(bad)

            # moving bad on board and graphically
            else:
                move_character_on_board(bad, [move[0], move[1]], False)
                bad[0] = bad[0] + move[0]
                bad[1] = bad[1] + move[1]


def backup_obstacle(row, col):
    global board
    global temp_cell

    # Put the location of the obstacle in a temporary variable
    temp_cell = [row, col, board[row][col]]


def restore_obstacle():
    global board
    global temp_cell

    # Put the temporary variable into certain location on the board and clear temp var.
    if temp_cell[2] is not None:
        board[temp_cell[0]][temp_cell[1]] = temp_cell[2]
        temp_cell = [None, None, None]


def bad_guy_shoot():
    global bullet_list
    global board
    global good_guy
    global bad_guys_list

    if level <= 1 or len(bad_guys_list) == 0:
        return

    to_shoot = (random.choice(range(10)) <= 2)
    if not to_shoot:
        return

    shooter = random.choice(bad_guys_list)

    shot1 = None
    shot2 = None
    shot = None
    distance1 = 0
    distance2 = 0

    if good_guy[0] < shooter[0]:
        shot1 = [-1, 0]
        distance1 = shooter[0] - good_guy[0]
    elif good_guy[0] > shooter[0]:
        shot1 = [1, 0]
        distance1 = good_guy[0] - shooter[0]

    if good_guy[1] < shooter[1]:
        shot2 = [0, -1]
        distance2 = shooter[1] - good_guy[1]
    elif good_guy[1] > shooter[1]:
        shot2 = [0, 1]
        distance2 = good_guy[1] - shooter[1]

    if distance1 > distance2:  # this is against the instructions, but makes more sense, I guess
        shot = shot1
    elif distance2 > distance1:
        shot = shot2
    else:  # equal distance
        shot = random.choice([shot1, shot2])

    new_bullet_location = [shooter[0] + shot[0], shooter[1] + shot[1]]
    if new_bullet_location[0] < 0 or new_bullet_location[0] > 14:
        pass
    if is_cell_taken(new_bullet_location) == "bk":
        pass
    elif is_cell_taken(new_bullet_location) == "gd":
        die()
    elif is_cell_taken(new_bullet_location) == "bd":
        remove_bad(new_bullet_location)
    elif is_cell_taken(new_bullet_location) == "bt":
        remove_bullet(get_bullet_at(new_bullet_location))
    else:  # good to place bullet
        add_bullet(new_bullet_location, shot)

    return shooter  # need to know who shot, we should ot allow him to move.


def shoot():
    global bullet_list
    global previous_key
    global good_guy
    global board
    global sounds

    # Assign coordinates of previous key to direction

    direction = previous_key
    new_bullet_location = [good_guy[0] + direction[0], good_guy[1] + direction[1]]
    if new_bullet_location < [0, 0]:
        return
    elif new_bullet_location > [14, 19]:
        return
    # if the place the good_guy is shooting into is a brick do nothing
    if is_cell_taken(new_bullet_location) == "bk":
        return
    # if it is a bad guy then remove the bad guy
    elif is_cell_taken(new_bullet_location) == "bd":
        winsound.PlaySound(sounds["gdshot"], winsound.SND_FILENAME)
        remove_bad(new_bullet_location)
    elif is_cell_taken(new_bullet_location) == "gd":
        return
    elif is_cell_taken(new_bullet_location) == "bt":
        remove_bullet(get_bullet_at(new_bullet_location))

    # else add the location of the bullet to the list, show graphically and put location on board
    else:
        winsound.PlaySound(sounds["gdshot"], winsound.SND_FILENAME)
        add_bullet(new_bullet_location, direction)


def add_bullet(new_bullet_location, direction):
    global bullet_list
    global board
    bullet_list.append([new_bullet_location, direction])
    bullet_kind = None
    if direction == [0, 1]:
        bullet_kind = "bullet_right"
    elif direction == [0, -1]:
        bullet_kind = "bullet_left"
    elif direction == [1, 0]:
        bullet_kind = "bullet_down"
    elif direction == [-1, 0]:
        bullet_kind = "bullet_up"

    display_on_board(bullet_kind, new_bullet_location)
    board[new_bullet_location[0]][new_bullet_location[1]].draw(game_window)


def move_bullets(fired):
    global bullet_list
    global board

    # if there are bullets to move...
    counter = 0
    while counter < len(bullet_list):
        bullet = bullet_list[counter]
        new_bullet_location = [bullet[0][0] + bullet[1][0], bullet[0][1] + bullet[1][1]]
        # if bullet is going to hit a wall in its next move, remove the bullet
        if is_cell_taken(new_bullet_location) == 'bk':
            remove_bullet(bullet)
        # if bullet will hit a bad guy on next move, remove both bad guy and bullet
        elif is_cell_taken(new_bullet_location) == 'bt':
            remove_bullet(bullet)
            remove_bullet(get_bullet_at(new_bullet_location))
        elif is_cell_taken(new_bullet_location) == 'bd':
            remove_bullet(bullet)
            remove_bad(new_bullet_location)
        # in the case the bullet is about to hit the good_guy remove the bullet and good guy dies
        elif is_cell_taken(new_bullet_location) == 'gd':
            remove_bullet(bullet)
            die()
        # if bullet tries to leave the board on top or bottom, remove the bullet
        elif new_bullet_location[0] < 0 or new_bullet_location[0] > 14 or new_bullet_location[1] < 0 or \
                new_bullet_location[1] > 19:
            remove_bullet(bullet)
        # otherwise, move graphically, rewrite the correct coordinates for each bullet
        else:
            move_character_on_board(bullet[0], bullet[1], False)
            bullet_list[counter] = [new_bullet_location, bullet[1]]
            counter += 1
    # if a shot is fired, call shoot
    if fired:
        shoot()


def win():
    global level
    global score
    global bullet_list
    global board

    # display a victory message, and increase the level by 1, clear the bullet list
    winsound.PlaySound(sounds["victory"], winsound.SND_FILENAME)
    messagebox.showinfo("CONGRATULATIONS!", f"YOU WON \n"
                                            f"Your Score: {score} \n")
    level += 1


def move_characters(window):
    global good_guy
    global board
    global bad_guys_list
    global previous_key
    global bullet_list
    drow_good = 0
    dcol_good = 0
    nomove = False
    won = False

    while True:
        goodmove = False
        fired_new_bullet = False
        key = window.checkKey()
        # Which direction will the good_guy move
        if key:
            if key == "a" or key == "Left":
                drow_good = 0
                dcol_good = -1
                goodmove = True
            elif key == "d" or key == "Right":
                dcol_good = 1
                drow_good = 0
                goodmove = True
            elif key == "w" or key == "Up":
                dcol_good = 0
                drow_good = -1
                goodmove = True
            elif key == "s" or key == "Down":
                dcol_good = 0
                drow_good = 1
                goodmove = True
            elif key == "Return":
                goodmove = True
                dcol_good = 0
                drow_good = 0
            elif key == "space":
                dcol_good = 0
                drow_good = 0
                goodmove = True
                fired_new_bullet = True

            else:
                continue
        else:
            continue
        # if some move was made
        if goodmove:
            # move the bullets
            move_bullets(fired_new_bullet)

            # record the previous direction
            if drow_good != 0 or dcol_good != 0:
                previous_key = [drow_good, dcol_good]

                # if good guy tries to leave map with bad guys still alive loop him back otherwise win
                if good_guy[0] + drow_good < 0:
                    if len(bad_guys_list) == 0:
                        win()
                        won = True
                        drow_good = 14
                    else:
                        drow_good = 14
                # if good guy tries to leave map with bad guys still alive loop him back otherwise win
                elif good_guy[0] + drow_good > 14:
                    if len(bad_guys_list) == 0:
                        win()
                        won = True
                        drow_good = -14
                    else:
                        drow_good = -14

                # check to see if the cell good guy is trying to go to is taken
                if is_cell_taken([good_guy[0] + drow_good, good_guy[1] + dcol_good]) is not None:
                    taken = True
                else:
                    taken = False
                # move good guy graphically and change location on board
                move_character_on_board(good_guy, [drow_good, dcol_good], taken)
                good_guy = [good_guy[0] + drow_good, good_guy[1] + dcol_good]
                # if the cell is taken die
                if taken:
                    die()
            # move all bad guys
            movebads()
        # if the good guy wins, get out of the move characters function
        if won:
            bullet_list = []
            return


def clear_walls():
    global board
    global board
    global bricks
    # Go through the list of bricks and set them all to None and remove from list
    for x in range(len(bricks)):
        board[bricks[0][0]][bricks[0][1]].undraw()
        board[bricks[0][0]][bricks[0][1]] = None
        bricks.remove([bricks[0][0], bricks[0][1]])


def render_board(board):
    global my_life_label
    global my_score_label
    global level

    # create a window
    win = graphics.GraphWin("Goodguy vs. Badguys", 1440, 1080)
    # go through each square and draw the needed objects
    for row in board:
        for square in row:
            if square:
                square.draw(win)

    # display lives
    my_life_label = graphics.Text(graphics.Point(17.5 * IMAGE_SIZE, 2 * IMAGE_SIZE), f"Lives: {lives}")
    my_life_label.setOutline("Red")
    my_life_label.setStyle('bold')
    my_life_label.draw(win)

    # display score
    my_score_label = graphics.Text(graphics.Point(17.5 * IMAGE_SIZE, 13 * IMAGE_SIZE), f" Score: {score} \n"
                                                                                       f" Level: {level}")
    my_score_label.setOutline("Blue")
    my_score_label.setStyle('bold')
    my_score_label.draw(win)

    return win


def main():
    global game_window
    global level
    global bricks
    global board

    # Run level 1
    my_board = setup_board()
    my_board = set_up_warriors(my_board)
    game_window = render_board(my_board)
    move_characters(game_window)
    # after winning, close window and create new
    game_window.close()
    clear_walls()
    # Run level 2
    my_board = setup_board()
    my_board = set_up_warriors(my_board)
    game_window = render_board(my_board)
    messagebox.showinfo(f"Level {level}", "Lets Try A Bit Harder")
    move_characters(game_window)


main()
