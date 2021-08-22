"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Name:       Thanh Ngoc Dan Tran
Email:      thanh.n.tran@tuni.fi
Student ID: 150119812

BATTLESHIP BOARDGAME

The game is a "digital" version of normal battleship boardgame. This game suits
two players.

Two players can play from their at the same time. This program brings
battleship boardgame to you and your friend regardless of distance between you
two. You just need an extra communication channel for far distance game.
That's it.

No supposed interactions between two players is sacrificed, but with even more
animation effects.
"""


import time
from tkinter import *
from tkinter import messagebox  # create message box
import os  # open file


# Constant lists of coordinates
X_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
Y_LIST = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class Ship:
    """This class defines ship type, coordinates, shot status and sinking
    status per ship"""
    def __init__(self, ship_type, coordinates_list):
        self.__ship_type = ship_type
        self.__coordinates_list = coordinates_list
        self.__shot_coordinates = []
        self.__ship_sank = False

    def get_ship_type(self):
        return self.__ship_type

    def get_ship_coordinates(self):
        return self.__coordinates_list

    def check_sank(self, shot_coordinates):
        """ Check if ship sank or not. Starting with adding the new shot
        coordinate to list of hit coordinates, then if all elements in that
        list match all elements in coordinates list, ship sank

        :param shot_coordinates: str, the newly input coordinates
        :return True, if ship sank
                False, if ship has not sunk yet"""
        self.__shot_coordinates.append(shot_coordinates)
        if all(elem in self.__shot_coordinates for elem in self.__coordinates_list) is True:
            return True
        else:
            return False


class GameStartGui:
    """Create GUI for introductory page of the game"""
    def __init__(self):
        # =========================Game start window===========================
        # Create game start window (gs: game start)
        self.__gs_window = Tk()

        # Set geometry
        self.__gs_window.geometry("1524x857")

        # Set title
        self.__gs_window.title("Battleship")

        # =============================Canvas==================================
        # Create canvas
        self.__bg_canvas = Canvas(self.__gs_window, width=1524, height=857,
                                  bg="#DFEAE2")
        # Pack it
        self.__bg_canvas.pack(fill="both", expand="True")

        # =========================Background image============================
        # Add background image for game start page (gs: game start)
        self.__gs_background = PhotoImage(file="oceanbackground_image.png")
        self.__bg_canvas.create_image(0, 0, image=self.__gs_background,
                                      anchor="nw")

        # =======================Add game box image==========================
        self.__game_box_img = PhotoImage(file="gamebox.png")

        self.__bg_canvas.create_image(700, 300, image=self.__game_box_img,
                                      anchor="center")

        # ===========Game control buttons (quit, review rules)=================
        # =============================Quit button=============================
        # Add button
        self.__quit_button = Button(self.__gs_window, text="Quit!", bg="gray",
                                    fg="#40E0D0", font=("Algerian", "15"),
                                    command=self.quit)

        self.__bg_canvas.create_window(80, 800, window=self.__quit_button)

        # Create tooltip
        self.__quit_tooltip = CreateToolTips(self.__quit_button,
                                             "Click to quit game")

        # ======================Review game rules button=======================
        # Add button
        self.__rule_button = Button(self.__gs_window,
                                    text="Review game rules!", bg="gray",
                                    fg="white", font=("Algerian", "15"),
                                    command=self.open_rules_file)

        self.__bg_canvas.create_window(1300, 40, anchor="ne",
                                       window=self.__rule_button)
        # Create tooltip
        self.__rule_tooltip = CreateToolTips(self.__rule_button,
                                             "Click to open game rule")
        # =============================Start button============================
        # Add button
        self.__start_button = Button(self.__bg_canvas, text="Let's start!",
                                     bg="gray", fg="#40E0D0",
                                     font=("Algerian", "25"),
                                     command=self.start)

        self.__bg_canvas.create_window(700, 700, anchor="center",
                                       window=self.__start_button)
        # Create tooltip
        self.__start_tooltip = CreateToolTips(self.__start_button,
                                              "Click to start game when both "
                                              "players are READY!")

        # This attribute is used to acknowledge if the start button has been
        # clicked or not
        self.__start_button_clicked = False
        # =====================================================================
        # ==============================MAINLOOP===============================
        self.__gs_window.mainloop()

    def quit(self):
        """Destroy window when quit button is clicked and confirmed"""
        # Create messagebox to ask for confirmation
        self.__quit_msgbox = messagebox.askquestion("Exit the game",
                                                    "Are you sure you want to "
                                                    "quit the game?",
                                                    icon="warning")
        if self.__quit_msgbox == "yes":
            # Destroy game start window
            self.__gs_window.destroy()
        else:
            pass

    def open_rules_file(self):
        """Open "game_rules.txt".txt file for game rules"""
        os.startfile("game_rules.txt")

    def start(self):
        """Destroy introductory window, change flag as start button clicked"""
        # Destoy game start window
        self.__gs_window.destroy()
        # Change flag to True as a condition for starting the GamePlayGui
        self.__start_button_clicked = True

    def get_start_gui(self):
        """Return flag of start button to call the game play GUI. This function
        is needed because without it, the GamePlayGui shall be called even if
        this GameStartGui destroy by closing by clicking at the x button of the
        window.
        :return self.__start_button_clicked: True, if start button was clicked
                                            False, if start button was not
                                            clicked"""
        return self.__start_button_clicked


class GamePlayGui:
    """Create GUI for game play"""
    def __init__(self):
        # =============================GamePlay window=========================
        # Create window
        self.__gp_window = Tk()

        # Set geometry
        self.__gp_window.geometry("1524x857")
        # Modify title
        self.__gp_window.title("Hit me if you can!")

        # ================================Canvas===============================
        # Create canvas
        self.__bg_canvas = Canvas(self.__gp_window, width=1524, height=857, bg="#DFEAE2")

        # Pack it
        self.__bg_canvas.pack(fill="both", expand="True")

        # =========Game control buttons (quit, review rules, restart)==========
        # ===========================Quit button===============================
        # Add button
        self.__quit_button = Button(self.__gp_window, text="Quit!", bg="gray",
                                    fg="#40E0D0", font=("Algerian", "15"),
                                    command=self.quit)

        self.__bg_canvas.create_window(80, 800, window=self.__quit_button)

        # Create tooltip
        self.__quit_tooltip = CreateToolTips(self.__quit_button,
                                             "Click to quit game")

        # =======================Review rules button===========================
        # Add button
        self.__rule_button = Button(self.__gp_window, text="Review game rules!"
                                    , bg="gray", fg="white",
                                    font=("Algerian", "15"),
                                    command=self.open_rules_file)

        self.__bg_canvas.create_window(1300, 40, anchor="ne",
                                       window=self.__rule_button)

        # Create tooltip
        self.__rule_tooltip = CreateToolTips(self.__rule_button,
                                             "Click to open game rule")

        # ===========================Restart button============================
        # Add button
        self.__restart_button = Button(self.__gp_window, text="Restart!",
                                       bg="gray",
                                       fg="#40E0D0", font=("Algerian", "15"),
                                       command=self.restart)

        self.__bg_canvas.create_window(1300, 800, anchor="e",
                                       window=self.__restart_button)

        # Create tooltip
        self.__restart_tooltip = CreateToolTips(self.__restart_button,
                                                "Restart game")

        # ===========================Ally's ocean grid=========================
        # Add frame to contain the game board
        self.__ally_frame = Frame(self.__bg_canvas, width=605, height=605,
                                  bg="#219f9c")
        self.__bg_canvas.create_window(30, 120, anchor="nw",
                                       window=self.__ally_frame)

        # Create tooltip for ally's ocean grid frame
        self.__ally_frame_tooltip = CreateToolTips(self.__ally_frame,
                                                   "Ally ocean grid")

        # Create labels to show coordinates
        for i in range(0, len(X_LIST)):
            self.__ally_label = Label(self.__ally_frame, text=X_LIST[i],
                                      font=("Algerian", "20"), height=1,
                                      width=2, fg="white", bg="#219f9c")
            self.__ally_label.grid(row=0, column=i+1)

        for j in range(0, len(Y_LIST)):
            self.__ally_label = Label(self.__ally_frame, text=Y_LIST[j],
                                      font=("Algerian", "20"), height=1,
                                      width=2, fg="white", bg="#219f9c")
            self.__ally_label.grid(row=j+1, column=0)

        for i in range(0, len(X_LIST)):
            self.__ally_label = Label(self.__ally_frame, text=X_LIST[i],
                                      font=("Algerian", "20"), height=1,
                                      width=2, fg="white", bg="#219f9c")
            self.__ally_label.grid(row=11, column=i+1)

        for j in range(0, len(Y_LIST)):
            self.__ally_label = Label(self.__ally_frame, text=Y_LIST[j],
                                      font=("Algerian", "20"), height=1,
                                      width=2, fg="white", bg="#219f9c")
            self.__ally_label.grid(row=j+1, column=11)

        # Add buttons for each coordinates on ally's frame using for loop
        self.__ally_button_id = {}  # Data structure to save all buttons's id

        for y in range(0, len(Y_LIST)):
            for x in range(0, len(X_LIST)):
                # Add button
                self.__coor_button = Button(self.__ally_frame, text=" ",
                                            font=("Algerian", "20"),
                                            height=1, width=2,
                                            bg="#219f9c",
                                            command=lambda x=x, y=y: self.read_coordinate(
                                                "ally", x, y))

                self.__coor_button.grid(row=x + 1, column=y + 1)

                # Create tooltip for each button for show its coordinate
                self.__button_tooltip = CreateToolTips(self.__coor_button,
                                                       X_LIST[y] + Y_LIST[
                                                           x])

                # Save button id to self.__opponent_button_id with its key as
                # its coordinates
                self.__button = {X_LIST[y] + Y_LIST[x]: self.__coor_button}
                self.__ally_button_id.update(self.__button)

        # ========================Opponent's ocean grid========================
        # Add frame to contain the game board
        self.__opponent_frame = Frame(self.__bg_canvas, width=605, height=605,
                                      bg="#88ca9c")

        self.__bg_canvas.create_window(590, 120, anchor="nw",
                                       window=self.__opponent_frame)

        # Create tooltip for opponent's ocean grid frame
        self.__opponent_frame_tooltip = CreateToolTips(self.__opponent_frame,
                                                       "Enemy's ocean grid!")

        # Create labels to show coordinates
        for i in range(0, len(X_LIST)):
            self.__opponent_label = Label(self.__opponent_frame, text=X_LIST[i]
                                          , font=("Algerian", "20"), height=1,
                                          width=2, fg="white", bg="#88ca9c")
            self.__opponent_label.grid(row=0, column=i+1)

        for j in range(0, len(Y_LIST)):
            self.__opponent_label = Label(self.__opponent_frame, text=Y_LIST[j]
                                          , font=("Algerian", "20"), height=1,
                                          width=2, fg="white", bg="#88ca9c")
            self.__opponent_label.grid(row=j+1, column=0)

        for i in range(0, len(X_LIST)):
            self.__opponent_label = Label(self.__opponent_frame, text=X_LIST[i]
                                          , font=("Algerian", "20"), height=1,
                                          width=2, fg="white", bg="#88ca9c")
            self.__opponent_label.grid(row=11, column=i+1)

        for j in range(0, len(Y_LIST)):
            self.__opponent_label = Label(self.__opponent_frame, text=Y_LIST[j]
                                          , font=("Algerian", "20"), height=1,
                                          width=2, fg="white", bg="#88ca9c")
            self.__opponent_label.grid(row=j+1, column=11)

        # Add buttons for each coordinates on opponent's ocean grid using
        # for loop
        self.__opponent_button_id = {}  # Data structure to save all buttons id

        for y in range(0, len(Y_LIST)):
            for x in range(0, len(X_LIST)):
                # Add button
                self.__coor_button = Button(self.__opponent_frame,
                                            text=" ",
                                            font=("Algerian", "20"),
                                            height=1,
                                            width=2,
                                            bg="#88ca9c",
                                            state=DISABLED,
                                            command=lambda x=x, y=y: self.read_coordinate(
                                                "opponent", x, y))

                self.__coor_button.grid(row=x + 1, column=y + 1)

                # Create tooltip for each button for show its coordinate
                self.__button_tooltip = CreateToolTips(self.__coor_button,
                                                       X_LIST[y] + Y_LIST[x])

                # Save button id to self.__opponent_button_id with its key as
                # its coordinates
                self.__button = {X_LIST[y] + Y_LIST[x]: self.__coor_button}
                self.__opponent_button_id.update(self.__button)

        # ===================Save button at set up state=======================
        # Add set_up_label
        self.__set_up_label = self.__bg_canvas.create_text(50, 15,
                                                               anchor="nw",
                                                               text="Set up your ocean grid!",
                                                               fill="#2C7083",
                                                               font=("Chiller",
                                                                   "20","bold"),
                                                               justify="center")
        # Add Save button for at in set up state for setting up ally ocean grid
        self.__save_button = Button(self.__gp_window, text="Save!",
                                    fg="#2C7083",
                                    font=("Chiller", "17", "bold"),
                                    command=self.save_ship_locations)
        self.__bg_canvas.create_window(550, 80, window=self.__save_button)

        # ======================Announcement label=============================
        # Add announcement label which will be modified to match every event
        # throughout the game play
        self.__announcement_label = Label(self.__bg_canvas, anchor="w",
                                          text="", fg="#2C7083", font=(
                "Algerian", "17", "bold"), justify="center", bg="#DFEAE2")

        self.__bg_canvas.create_window(570, 800,
                                       window=self.__announcement_label)

        # ==========================Ship dictionary============================
        # Keys, are named after the ship type, direct to a list with
        # 1st element is the number of coordinates of that ship,
        # 2nd element is the file name of that ship image,
        # 3rd element is the identical color of the ship type,
        # 4th element would be ID address to checkbutton of that ship type to
        # check opponent's ship sank, which is add after set up state
        self.__ship_dict = {"AIRCRAFT CARRIER": [5, PhotoImage(file="aircraftcarrier_token.png"), "#C7CEEA"],
                            "BATTLESHIP": [4, PhotoImage(file="battleship_token.png"), "#B5EAD7"],
                            "CRUISER": [3, PhotoImage(file="cruiser_token.png"), "#FFDAC1"],
                            "SUBMARINE": [3, PhotoImage(file="submarine_token.png"), "#FF9AA2"],
                            "DESTROYER": [2, PhotoImage(file="destroyer_token.png"), "#F07BBB"]}

        # List all the ship types for later use
        self.__ship_name_list = list(self.__ship_dict.keys())

        # This variable is used to mark set up ship at set up state
        self.__set_up_ship = 0

        # ====================Ship list (Save class Ship's objects)============
        # Create a ship list to store all ready set up Ship objects for game
        # play
        self.__ships_list = []

        # ==========Images for creating animation of flying bullets============
        # Add bullet images
        self.__bullet_up_img = PhotoImage(file="bullet_up.png")
        self.__bullet_down_img = PhotoImage(file="bullet_down.png")
        # Create bullet image labels which are placed when the animation needed in
        # def bullet_animation
        self.__bullet_up = Label(self.__gp_window, image=self.__bullet_up_img)
        self.__bullet_down = Label(self.__gp_window,
                                   image=self.__bullet_down_img)

        # Add explosion images for creating animation of explosion and save
        # them into a list for iteration
        self.__explosion_img_list = [PhotoImage(file="explode_1.png"),
                                     PhotoImage(file="explode_2.png"),
                                     PhotoImage(file="explode_3.png"),
                                     PhotoImage(file="explode_4.png"),
                                     PhotoImage(file="explode_5.png"),
                                     PhotoImage(file="explode_6.png"),
                                     PhotoImage(file="explode_7.png"),
                                     PhotoImage(file="explode_8.png")]

        # Create explosion image label which is modified and placed later when
        # the animation needed in def bullet_animation
        self.__explosion_label = Label(self.__gp_window,
                                       image=self.__explosion_img_list[0])

        # ================Game Play starts at set up state=====================
        self.set_up()

        # =====================================================================
        # ============================MAINLOOP=================================
        self.__gp_window.mainloop()

    def set_up(self):
        """Control label and data structure to store selection in all set up
        rounds"""
        # The current ship type which is required to be set up
        self.__ship_name = self.__ship_name_list[self.__set_up_ship]
        # The current to-be-set-up number of needed coordinates of the ship
        # type at the moment
        self.__no_of_coor = self.__ship_dict[self.__ship_name][0]

        # Try to delete old set up label if any
        try:
            self.__bg_canvas.delete(self.__ship_set_up_label)
        except AttributeError:
            pass

        # Create set up label for the current ship
        self.__ship_set_up_label = self.__bg_canvas.create_text(75, 50, anchor="nw", text=f"Anchoring {self.__ship_name}\nplease choose {self.__no_of_coor} locations", fill="#2C7083", font=("Algerian", "20", "bold"), justify="center")
        # Data structure to store all clicked coordinates for current ship.
        # This will be checked check for validity of all selected coordinates
        # before saving a new Ship object
        self.__ship_coordinates = []

    def read_coordinate(self, action, x, y):
        """This function is called whenever a coordinate button on either ally
        or opponent's ocean grid is clicked to read button id and proceed
        further operations.

        :param action: str, "opponent": if the button is located in opponent's
                                    ocean grid. Function proceeds
                                    bullet_animation, confirm hit or miss and
                                    mark the button
                            "ally": if the button is located in ally's ocean
                                    grid. Function checks game state by read
                                    text on the button and proceed to EITHER
                                    save clicked button in set up state OR
                                    confirm selection and start bullet
                                    animation
        :param x: int, coordinates on vertical direction of the frame which
                match also item in Y_LIST
        :param y: int, coordinates on horizontal direction of the frame which
                match also item in X_LIST
        """
        # Take str coordinate
        self.__clicked_coordinate = X_LIST[y] + Y_LIST[x]

        # Take clicked button id
        self.__clicked_button = self.__opponent_button_id[
            self.__clicked_coordinate]

        # When user click a button on opponent's grid, it means a shot from
        # user
        if action == "opponent":
            # Proceed bullet_animation
            self.bullet_animation(action, self.__clicked_button)

            # Create a hit_or_miss yesno messagebox to mark the shot as hit or
            # miss
            self.__hit_or_miss_message = messagebox.askyesno("Your shot", "Was it a hit?", icon="question")

            # When that was a hit
            if self.__hit_or_miss_message is True:
                # Disable the button, change its background color to RED and
                # cursor to default arrow
                self.__clicked_button.configure(state=DISABLED, bg="red",
                                                cursor="")

                # Modify announcement label to announce the event
                self.__announcement_label.configure(
                    text=f"You've just got a HIT at "
                         f"{self.__clicked_coordinate}!", fg="red")

                # Keep a count on the number of hits user gets
                self.__you_hit += 1

                # Check if game is won by any player
                self.check_won()

            # When that was a miss
            elif self.__hit_or_miss_message is False:
                # Disable the button, change its background color to WHITE and
                # cursor to default arrow
                self.__clicked_button.configure(state=DISABLED, bg="white",
                                                cursor="")

                # Modify announcement label to announce the event
                self.__announcement_label.configure(
                    text=f"You've just got a MISS at "
                         f"{self.__clicked_coordinate}!", fg="#2C7083")

        # When user clicks a button on ally's ocean grid, there are two
        # meanings
        elif action == "ally":
            # A list of all buttons's name
            self.__ally_button_name_list = list(self.__ally_button_id.keys())

            # Take button id
            self.__clicked_button = self.__ally_button_id[self.__clicked_coordinate]

            # Game is in set up state, because if it is after the set up state,
            # the text was configured to "O"
            if self.__clicked_button["text"] == " ":
                # The button is chosen
                if self.__clicked_button['bg'] == "#219f9c":
                    self.__clicked_button.configure(bg="white")
                    self.__ship_coordinates.append(self.__clicked_coordinate)
                    self.__ship_coordinates.sort()

                # The button is un-chosen and no event happens yet
                elif self.__clicked_button['bg'] == "white":
                    self.__clicked_button.configure(bg="#219f9c")
                    if self.__clicked_coordinate in self.__ship_coordinates:
                        self.__ship_coordinates.remove(self.__clicked_coordinate)

            # When user clicks a button on own grid after game starts when
            # button text has been modified to "O". The text will be modified
            # again to "X" if there is a hit in ally's ocean grid
            elif self.__clicked_button["text"] == "O":
                # Create messagebox to confirm the clicked button to prevent
                # accidental click
                self.__message = messagebox.askquestion("Opponent\'s shot", f"Did opponent shoot at {self.__clicked_coordinate}?")

                # If it is confirmed as a hit from opponent to ally ocean grid
                if self.__message == "yes":
                    # Proceed bullet_animation
                    self.bullet_animation(action, self.__clicked_button)

                    # Modify button's text to "X", disable button, change
                    # cursor to default arrow
                    self.__clicked_button.configure(text="X", disabledforeground="red", state=DISABLED, cursor="")

                    # Loop through all Ship objects and check if any ally ship
                    # is just sunk
                    for ship in self.__ships_list:
                        # Search for same coordinates of clicked coordinates in
                        # ship_coordinates. Call class Ship's check_sank
                        # function to check if ship is just sunk
                        if self.__clicked_coordinate in ship.get_ship_coordinates():
                            # If ship is just sunk
                            if ship.check_sank(self.__clicked_coordinate) is True:
                                # Modify announcement label to announce the
                                # event
                                self.__announcement_label.configure(
                                    text=f"Opponent sank your "
                                         f"{ship.get_ship_type()}!", fg="red")

                                # Keep a count on the number of ally sunk ship
                                self.__own_sunk_ship_count += 1

                                # Check if opponent wins
                                self.check_won()
                            else:
                                # Modify announcement label to announce which
                                # of user ship is hit
                                self.__announcement_label.configure(
                                    text=f"Opponent hit your {ship.get_ship_type()}!",
                                    fg="#2C7083")

    def check_set_up_locations(self):
        """Check if all selected set up coordinates are anchored vertically or
        horizontally across the ally's ocean grid"""
        # Data structure to store instant check index of all selected
        # coordinates
        self.__check_index = []

        # Loop through the selected coordinates to take its index from
        # ally_button_name_list
        for coordinate in self.__ship_coordinates:
            # Store the index into check_index list
            self.__check_index.append(self.__ally_button_name_list.index(coordinate))

        # Check if all selected coordinates locate vertically, if yes,
        # return True
        if sorted(self.__check_index) == list(range(
                min(self.__check_index), max(self.__check_index)+1)):
            return True

        # Check if all selected coordinates locate horizontally, if yes,
        # return True
        elif sorted(self.__check_index) == list(range(
                min(self.__check_index), max(self.__check_index)+1, 10)):
            return True

        # Mark as invalid selection of coordinates by returning False
        else:
            return False

    def save_ship_locations(self):
        """Check the selection of coordinates and either save or show error
        messagebox and refuse to save the selection"""
        # Check number of selected ship locations, if the number selected
        # buttons does not match the required number of ship type's coordinates
        if len(self.__ship_coordinates) != self.__no_of_coor:
            # Show error messagebox
            self.__errormessage = messagebox.showerror("Error", f"Please choose exactly {self.__no_of_coor} ship locations.")

        # If the selected coordinates are invalid
        elif self.check_set_up_locations() is False:
            # Show error messagebox
            self.__errormessage = messagebox.showerror("Error",
                                                       f"Each ship must be placed horizontally or vertically across grid spaces—not diagonally. Please rechoose ship locations.")

        # If all selected coordinates are valid
        else:
            # Disable all saved button, so that there is no overlapping
            # coordinates between ships. Modify button background color to
            # distinct ship from other ships
            for coordinate in self.__ship_coordinates:
                self.__ally_button_id[coordinate].configure(state=DISABLED, bg=
                self.__ship_dict[self.__ship_name][2])

            # Add new Ship object to list
            self.__ships_list.append(Ship(self.__ship_name, self.__ship_coordinates))

            # Show announcement label
            self.__announcement_label.configure(text=f"{self.__ship_name}'s coordinates are successfully saved!")

            # Set up the next ship
            self.__set_up_ship += 1

            # Move on set up the next ship if not all 5 ships readily set up
            if self.__set_up_ship <= 4:
                self.__ship_coordinates = []
                self.set_up()

            # Stop setting up state when all ships saved
            # Call the battle start from this point
            else:
                self.battle_start()

    def battle_start(self):
        """This function is to mark that the battle starts. Some old widgets
        are deleted and some new ones are created"""
        # Create a message box for confirming game start
        self.__infomessage = messagebox.showinfo("Battle starts", "Hit ok when you ready!")

        # Delete old labels and button and create new ones with new text
        self.__bg_canvas.delete(self.__set_up_label)
        self.__save_button.destroy()  # Destroy save button
        self.__bg_canvas.delete(self.__ship_set_up_label)
        self.__battle_start_label = self.__bg_canvas.create_text(50, 15, anchor="nw", text="Shoot!", fill="#2C7083", font=("Chiller", "30", "bold"), justify="center")

        # Add instruction label for game play
        self.__instruction_label = self.__bg_canvas.create_text(75, 50, anchor="nw", text=f"Mark opponent's hits on your own grid and shoot by click on opponent's grid!\nDon't forget to check ships that you sank", fill="#2C7083", font=("Algerian", "17", "bold"), justify="center")

        # Add ship images and checkbutton to keep track of opponent sunk ships
        # Create frame to contain ship image and sunk ship checkbutton
        self.__ship_img_frame = Frame(self.__bg_canvas, width=200, height=605)
        self.__bg_canvas.create_window(1130, 160, anchor="nw", window=self.__ship_img_frame)

        # Loop through ships
        for ship_index in range(len(self.__ship_name_list)):
            # Add ship image
            self.__ship_img = self.__ship_dict[self.__ship_name_list[ship_index]][1]
            self.__ship_image = Label(self.__ship_img_frame, image=self.__ship_img)
            self.__ship_image.grid(row=ship_index * 2, column=0)

            # Add ship's sunk checkbutton
            self.__sink_ship = IntVar()
            self.__sink_ship_check = Checkbutton(self.__ship_img_frame, onvalue=1, offvalue=0, fg="#88ca9c", disabledforeground="red", text=self.__ship_name_list[ship_index], font=("Chiller", "15", "bold"), variable=self.__sink_ship, cursor="target", command=lambda ship_type=self.__ship_name_list[ship_index]: self.mark_ship_sank(ship_type))
            self.__sink_ship_check.grid(row=ship_index * 2 + 1, column=0)

            # Save id of the checkbutton into ship_dict, add 4th element to per
            # payload of ship_dict
            self.__ship_dict[self.__ship_name_list[ship_index]].append(self.__sink_ship_check)

        # Activate all buttons in opponent's grid
        for button in self.__opponent_button_id.values():
            button.configure(state=NORMAL, cursor="target")

        # Activate buttons at all ships' locations and deactivate all other
        # buttons on ally's grid
        for button in self.__ally_button_id.values():
            if button["state"] == DISABLED:
                button.configure(state=NORMAL, cursor="target")
                button.configure(text="O")
            else:
                button.configure(state=DISABLED, cursor="")

        # Define a variable to count opponent's sunk ships,
        # when this variable reaches 5, user wins
        self.__opponent_sunk_ship_count = 0

        # Define a variable to count user's hits,
        # when this variable reaches 17, user wins
        self.__you_hit = 0

        # Define a variable to count sum of opponent's sunk ships'
        # coordinates which is then used to check if itself matches with
        # user's hits before marking opponent's ship as sunk
        self.__opponent_sunk_ship_coordinates_count = 0

        # Define a variable to count own sunk ships,
        # when this variable reaches 5, opponent wins
        self.__own_sunk_ship_count = 0

    def bullet_animation(self, action, coordinate_button):
        """Create flying bullet and explosion animation

        :param action: str, "opponent", if the clicked button is located in
                                        opponent's ocean grid
                            "ally", if the clicked button is located in ally's
                                    ocean grid
        :param coordinate_button: button id address, the clicked button
        """
        # Take the clicked button winfo to calculate x and y coordinates for
        # destination of flying bullet and explosion
        self.__des_x = int(coordinate_button.winfo_rootx() + coordinate_button.winfo_width() / 2)
        self.__des_y = int(coordinate_button.winfo_rooty() + coordinate_button.winfo_height())

        if action == "opponent":
            # Animate bullet flying upwards from ally ocean grid
            for y in range(450, 0, -5):
                self.__bullet_up.place(x=310, y=y, anchor="s")

                self.__ally_frame.lower()
                self.__bullet_up.lift()

                self.__gp_window.update_idletasks()
                time.sleep(0.00001)

                self.__bullet_up.place_forget()

            # Animate bullet flying downwards to opponent's ocean grid towards
            # the clicked button
            for y in range(0, self.__des_y-55, 5):
                self.__bullet_down.place(x=self.__des_x-10, y=y, anchor="s")

                self.__opponent_frame.lower()
                self.__bullet_down.lift()

                self.__gp_window.update_idletasks()
                time.sleep(0.00001)

                self.__bullet_down.place_forget()

        if action == "ally":
            # Animate bullet flying upwards from opponent's ocean grid
            for y in range(450, 0, -5):
                self.__bullet_up.place(x=870, y=y, anchor="s")

                self.__opponent_frame.lower()
                self.__bullet_up.lift()

                self.__gp_window.update_idletasks()
                time.sleep(0.00001)

                self.__bullet_up.place_forget()

            # Animate bullet flying downwards to opponent's ocean grid towards
            # the clicked button
            for y in range(0, self.__des_y - 55, 5):
                self.__bullet_down.place(x=self.__des_x - 10, y=y, anchor="s")

                self.__opponent_frame.lower()
                self.__bullet_down.lift()

                self.__gp_window.update_idletasks()
                time.sleep(0.00001)

                self.__bullet_down.place_forget()

        # Create explosion animation by looping through the list of explosion
        # images and place it on screen one after another
        for explosion_image in self.__explosion_img_list:
            self.__explosion_label.configure(image=explosion_image)
            self.__explosion_label.place(x=self.__des_x - 5,
                                         y=self.__des_y - 45, anchor="s")
            self.__opponent_frame.lower()
            self.__explosion_label.lift()

            self.__gp_window.update_idletasks()
            time.sleep(0.03)

            self.__explosion_label.place_forget()

    def mark_ship_sank(self, ship_type):
        """This function is called when an opponent's sunk ship checkbox is
        just clicked

        :param ship_type: str, the type of ship that is just checked"""
        # Create yesno confirm messagebox
        self.__confirm_message = messagebox.askyesno(
            "Confirm ship sank",
            f"Did you just sink an opponent's {ship_type}?")

        # If the ship is confirmed as sunk
        if self.__confirm_message is True:
            # Check if the number of sunk ships' coordinates matches the number
            # of hits user got so far
            self.__opponent_sunk_ship_coordinates_count += \
                self.__ship_dict[ship_type][0]

            # Check if the number of hits user gets is greater or equal to the
            # sum of sunk ship coordinates
            # If it is not
            if self.__opponent_sunk_ship_coordinates_count > self.__you_hit:
                # Show error messagebox
                self.__errormessage = messagebox.showerror(
                    "ERROR",
                    "Hits do not match sum of opponent's sunk ships' "
                    "coordinates.\nRecheck needed, Captain!")

                # Deselect the checkbutton
                self.__ship_dict[ship_type][3].deselect()

                # Substract the number of sunk ship's coordinates
                self.__opponent_sunk_ship_coordinates_count -= \
                    self.__ship_dict[ship_type][0]

            # If it is
            else:
                # Disable the check button and change cursor
                self.__ship_dict[ship_type][3].configure(state=DISABLED, cursor="")

                # Modify announcement label to announce the event
                self.__announcement_label.configure(text=f"You have just sunk an opponent's {ship_type}", fg="red")

                # Add 1 to the total number of opponent's sunk ship
                self.__opponent_sunk_ship_count += 1

                # Check if either user or opponent wins
                self.check_won()

        # If the checkbutton ship is confirmed not sunk
        else:
            # De-select the checkbutton
            self.__ship_dict[ship_type][3].deselect()

    def check_won(self):
        """Check if any of user or opponent won the battle to stop the battle,
        disable all coordinates buttons and proceed animation for announce who
        won"""
        # Check if user wins by sink all 5 ships of opponents or hitting at
        # all 17 opponent's ship spots or opponent wins by sinking all 5 ships
        # of user
        # If it is either user or opponent who wins
        if self.__opponent_sunk_ship_count == 5 or self.__you_hit == 17 or \
                self.__own_sunk_ship_count == 5:
            # Deactivate all buttons on both grids
            for button in self.__ally_button_id.values():
                button.configure(state=DISABLED, cursor="")
            for button in self.__opponent_button_id.values():
                button.configure(state=DISABLED, cursor="")

            # Deactivate all checkbuttons
            for ship_name in self.__ship_name_list:
                self.__ship_dict[ship_name][3].configure(state=DISABLED, cursor="")

            # Create label contained in a frame to announce who wins, which is
            # modified right after
            self.__win_lose_frame = Frame(self.__bg_canvas, bg="white")
            self.__bg_canvas.create_window(570, 400,
                                           window=self.__win_lose_frame,
                                           anchor="n")
            self.__win_lose_label = Label(self.__win_lose_frame,
                                          text=f"", fg="red",
                                          font=("Algerian", "20", "bold"),
                                          justify="center")
            self.__win_lose_label.pack()

            # If user wins by sinking all 5 ships of opponents or hitting all
            # 17 opponent's ship spots
            if self.__opponent_sunk_ship_count == 5 or self.__you_hit == 17:
                # screen sleep for 0.5 ms
                self.__gp_window.update_idletasks()
                time.sleep(0.5)

                # Modify announcement label
                self.__announcement_label.configure(text="")
                self.__announcement_label.configure(
                    text=f"Congratulation! You sank all opponent's ships", fg="red")

                # Proceed animation to show "YOU WON!" by zooming the
                # win_lose_label
                self.__win_lose_label.configure(text="YOU WON!")

                for text_size in range(20, 100):
                    self.__win_lose_label.configure(font=("Algerian", f"{text_size}", "bold"))

                    self.__gp_window.update_idletasks()
                    time.sleep(0.0005)

            # If opponent won by checking if opponent sank all 5 ships of user
            elif self.__own_sunk_ship_count == 5:
                # Modify announcement label
                self.__announcement_label.configure(
                    text=f"OUCH! All of your ships has been sunk!", fg="red")

                # Proceed animation to show "YOU WON!" by zooming the
                # win_lose_label
                self.__win_lose_label.configure(text="YOU LOST!")

                for text_size in range(20, 100):
                    self.__win_lose_label.configure(font=("Algerian", f"{text_size}", "bold"))

                    self.__gp_window.update_idletasks()
                    time.sleep(0.0005)

    def restart(self):
        """Adjust the self.__restart_clicked to True or False"""
        self.__restart_clicked = False

        # Show messagebox to confirm user choice of restarting the game
        self.__restart_msgbox = messagebox.askquestion("Restart", "Are you sure you want to restart the game?", icon="question")

        if self.__restart_msgbox == "yes":
            self.__gp_window.destroy()
            self.__restart_clicked = True
        else:
            pass

    def restart_button_clicked(self):
        """Return True or False as the self.__restart_clicked value

        :return True, if the restart button is clicked and confirmed
                False, if the restrart button is not both clicked and confirmed
        """
        if self.__restart_clicked is False:
            return False
        elif self.__restart_clicked is True:
            self.__restart_clicked = False
            return True

    def quit(self):
        """Quit the game, destroy the window"""
        # Show yes or no messagebox to read confirm to destroy the window
        self.__quit_msgbox = messagebox.askquestion("Exit the game",
                                                    "Are you sure you want to "
                                                    "quit the game?",
                                                    icon="warning")

        # If quitting the game is confirmed, destroy window
        if self.__quit_msgbox == "yes":
            self.__gp_window.destroy()

    def open_rules_file(self):
        """Open "game_rules.txt" file"""
        os.startfile("game_rules.txt")


class CreateToolTips:
    """Create a tooltip for a given widget by creating a toplevel window
    whenever mouse is hovered inside the widget and destroyed else-when"""
    def __init__(self, widget, text='widget info'):
        # The widget which when cursor is hover over, a tooltip is created
        self.__widget = widget
        # The text to be shown in the tooltip
        self.__text = text
        # Open tooltip when cursor enter widget
        self.__widget.bind("<Enter>", self.tooltip_open)
        # Close tooltip when cursor leave widget
        self.__widget.bind("<Leave>", self.tooltip_close)
        # Define x coordinate of the to-be-created toplevel window
        self.__tw_x = 0
        # Define y coordinate of the to-be-created toplevel window
        self.__tw_y = 0

    def tooltip_open(self, event=None):
        """When mouse is hover inside the area of the widget, create a toplevel
         window temporarily showing the text"""
        # Set x and y coordinates for toplevel window, x is widget's x
        # coordinate, y is widget's y coordinate plus widget's height
        self.__tw_x = self.__widget.winfo_rootx()
        self.__tw_y = self.__widget.winfo_rooty() + self.__widget.winfo_height()

        # Creates a toplevel window
        self.__tw = Toplevel(self.__widget)

        # Leaves only the label and removes the app window
        self.__tw.wm_overrideredirect(True)
        self.__tw.wm_geometry("+%d+%d" % (self.__tw_x, self.__tw_y))
        self.__tooltip_label = Label(self.__tw, text=self.__text,
                                     justify="left", background="#C5C6D0",
                                     foreground="#373737", relief='solid',
                                     borderwidth=1,
                                     font=("Helvetica", "12", "normal"))

        self.__tooltip_label.pack()

    def tooltip_close(self, event=None):
        """When mouse leaves the area of the widget, destroy toplevel window"""
        if self.__tw:
            self.__tw.destroy()


def main():
    # The program starts by starting the GameStartGui. The loop (re)starts
    # GameStartGui and continue the loop whenever restart_button in GamePlayGui
    # is clicked
    while True:
        start = GameStartGui()
        # To prevent program from continue if user closes the window not by
        # clicking quit button but closing x button top of the window
        try:
            start_button_clicked = start.get_start_gui()
        except TypeError:
            break

        if start_button_clicked is True:
            play = GamePlayGui()
            # To prevent program from continue if user closes the window not by
            # clicking quit button but closing x button top of the window
            try:
                if play.restart_button_clicked() is True:
                    continue
                else:
                    break
            except AttributeError:
                break
        else:
            break


if __name__ == "__main__":
    main()