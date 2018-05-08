"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from main_game import *





class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.my_color = ""
        self.board = None
        self.other_finished = False
        self.other_reset = False

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def game_to(self, peer):
        msg = json.dumps({"action":"challenged", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"][0:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"][0:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                # gaming
                elif my_msg[0] == "g":
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.game_to(peer) == True:
                        self.state = S_WAIT_FOR_GAME
                        self.out_msg += 'Trying to play with ' + peer + '. Get Ready\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                # elif my_msg == "play":
                #
                elif my_msg[:8] == "single_g":
                    self.state = S_SINGLE_GAME
                    self.board = Board("black", self.me)
                    self.board.bind2()
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)

                if peer_msg["action"] == "connect":
                    name = peer_msg["from"]
                    self.out_msg += "Hello, {0}".format(name)
                    self.state = S_CHATTING
                elif peer_msg["action"] == "challenged":
                    name = peer_msg["from"]
                    self.out_msg += "{0} wants to play GoBang with you, enter yes to accep" \
                                    "t, no to refuse.\n>".format(name)
                    self.state = S_REVEIVE_REQUEST

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "exchange":
                    print("coming message from {0}: {1}".format(peer_msg["from"], peer_msg["message"]))
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "connect":
                    name = peer_msg["from"]
                    self.out_msg += "Hello, {0}".format(name)


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        elif self.state == S_WAIT_FOR_GAME:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                # print(peer_msg)
                if peer_msg["action"] == "waiting":
                    accept = peer_msg["accept"]
                    if accept == "yes":
                        self.state = S_GAMING
                        if peer_msg["color"] == "white":
                            self.my_color = "black"
                        else:
                            self.my_color = "white"
                        self.board = Board(self.my_color, self.me)
                        self.board.bind()
                        # self.board.display_board()
                    else:
                        print("others refused to play")
                        self.state = S_LOGGEDIN
            if len(my_msg) > 0:
                print("Still waiting for others to response...")
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state == S_GAMING:

            # print("I'm here", 1)
            # print(self.board)

            # print("color",self.board.turn(), self.my_color)
            # self.board.move2()
            if len(my_msg) > 0:
                print("Game is not finished.")

            if self.board.turn() == self.my_color:
                # print("I'm here", 2)
                self.board.update()
                move = self.board.current_position()
                # print("move is", move)
                x, y = move
                msg = json.dumps({"action":"move","from":self.me,"x":x, "y":y,"color": self.my_color,"finished":self.board.is_finished(), "reset":self.board.reset_state()})
                mysend(self.s, msg)


            else:
                # print("I'm here", 3)
                self.board.update()

                if len(peer_msg) > 0:
                    peer_msg1 = json.loads(peer_msg)
                    # print(peer_msg1)
                    if "x" in peer_msg1.keys():
                        x = peer_msg1["x"]
                        y = peer_msg1["y"]
                        color = peer_msg1["color"]
                        self.other_finished = peer_msg1["finished"]
                        self.other_reset = peer_msg1["reset"]

                        self.board.other_move(x, y ,color)

                    elif peer_msg1["action"] == "disconnect":
                        self.other_finished = True

            if not self.board.reset_state():
                self.board.retry()

            # print("finish", self.board.is_finished(), self.other_finished)
            # print("reset", self.board.reset_state(), self.other_reset)
            if self.board.reset_state():
                msg = json.dumps({"action": "move", "from": self.me, "x": None, "y": None, "color": self.my_color,
                                  "finished": self.board.is_finished(), "reset": self.board.reset_state()})
                mysend(self.s, msg)
            if len(peer_msg) > 0:
                peer_msg1 = json.loads(peer_msg)
                # print(peer_msg)
                if "reset" in peer_msg1.keys():
                    self.other_reset = peer_msg1["reset"]

            # print("I'm here", 4)
            # self.board.update()
            if self.board.is_finished() or self.other_finished:

                self.disconnect()
                self.state = S_LOGGEDIN
                self.peer = ""
                self.board.quit()
                self.board.is_reset = False
                self.other_reset = False
                self.other_finished = False
                self.out_msg += menu
                self.board = None

            elif self.board.reset_state() and self.other_reset:
                self.board.reset()
                self.board.is_reset = False
                self.other_reset = False
                self.other_finished = False

        elif self.state == S_REVEIVE_REQUEST:
            if len(my_msg) > 0:
                if my_msg == "yes":
                    self.state = S_CHOOSE_COLOR
                    self.out_msg += "please enter the color that you want to play (black or white)\n>"
                elif my_msg == "no":
                    self.out_msg += menu
                    self.state = S_LOGGEDIN
                    mysend(self.s, json.dumps({"action": "refuse", "from":self.me}))
                else:
                    self.out_msg += "Wrong command, please enter yes or no.\n>"

        elif self.state == S_CHOOSE_COLOR:
            if len(my_msg) > 0:
                if my_msg == "black":
                    self.state = S_GAMING
                    self.my_color = "black"
                    mysend(self.s,
                           json.dumps({"action":"accept", "from":self.me, "color":"black"}))
                    self.board = Board("black", self.me)
                    self.board.bind()

                elif my_msg == "white":
                    self.state = S_GAMING
                    self.my_color = "white"
                    mysend(self.s,
                           json.dumps({"action": "accept", "from": self.me, "color": "white"}))
                    self.board = Board("white", self.me)
                    self.board.bind()
                else:
                    self.out_msg += "Wrong color, please enter black or white.\n>"
        elif self.state == S_SINGLE_GAME:
            self.board.update()
            if self.board.is_finished():
                self.board.quit()
                self.state = S_LOGGEDIN
                self.board = None
            if self.state == S_LOGGEDIN:
                self.out_msg += menu


#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
        # print_state(self.state)
        return self.out_msg
