#!/usr/bin/python
import signal
import sys
from random import randint, choice

POSSIBLE_COMMANDS = ["cd", "ls", "send"]


class Node(object):
    def __init__(self, name, ftype, parent=None, size=0):
        self.name = name
        self.fname = name.split("/")[-1] if name != "/" else "/"
        self.ftype = ftype
        self.parent = parent
        self.size = size
        self.children = []

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None


class Game(object):
    MAX_FILE_NAME_LEN = 7

    def __init__(self, ):
        self.num_incorrect = 0
        self.is_done = False
        self.make_file_system()

    def parse_command(self, command):
        command = command.split(" ")
        if command[0] not in POSSIBLE_COMMANDS:
            return "Command not recognized."

        if command[0] == POSSIBLE_COMMANDS[0]:
            if len(command) > 2:
                return "Too many arguments"
            if len(command) == 1:
                self.cur_location = "/"
                return
            path = command[1] if len(command) == 2 else "/"
            # ret_code, val = self.get_full_path(path)
            ret_code, val = self.find_node(path)
            if ret_code:
                raise Exception("wut that")
                return val
            else:
                if not val.ftype:
                    return "Cannot access, that is not a directory."
                self.cur = val
        elif command[0] == POSSIBLE_COMMANDS[1]:
            args = []
            if len(command) == 1:
                self.ls([self.cur.name])
            else:
                self.ls(command[1:])
        else:
            if len(command) > 2:
                return "Too many arguments"
            elif len(command) == 1:
                return "Too few arguments, you must send a path as an argument"
            path = command[1]
            ret_code, val = self.find_node(path)
            if ret_code:
                return val
            else:
                # Then call the check function and add to correct list
                if val.name in self.incorrects:
                    print "Correct!"
                    del self.incorrects[self.incorrects.index(val.name)]
                    if len(self.incorrects) == 0:
                        return -1
                else:
                    print "Sorry, but that is incorrect!"
                    sys.exit(0)

    def find_node(self, path):
        loc = self.cur if path[0] != "/" else self.root
        for fname in path.split("/"):
            if loc.ftype == 0:
                return 1, "Cannot access, that is not a directory."
            if fname == "" or fname == ".":
                continue
            elif fname == "..":
                if loc.parent is not None:
                    loc = loc.parent
            else:
                prepend = "/" if loc.name == "/" else loc.name + "/"
                aname = prepend + fname
                child = loc.get_child(aname)
                if child:
                    loc = child
                else:
                    return 1, "The system cannot find the path specified"
        return 0, loc

    def ls(self, paths):
        for path in paths:
            ret_val, loc = self.find_node(path)
            if ret_val:
                print path + ":", loc
                return
            print path + ":", "({} {})".format(
                len(loc.children),
                "entries" if len(loc.children) - 1 else "entry"
            )
            if loc.ftype:
                for child in loc.children:
                    print "{} {} {}".format(
                        child.fname.ljust(Game.MAX_FILE_NAME_LEN),
                        "DIR " if child.ftype else "FILE",
                        child.size
                    )
            else:
                print "{} {} {}".format(loc.fname, "FILE", loc.size)

    def make_file_system(self):
        level = 0
        low, high = 3, 6
        num_levels = randint(low, high)
        minimum_dirs = 8
        self.num_incorrect = randint(1, minimum_dirs)
        self.incorrects = []
        self.dirs = []
        self.root = Node("/", 1)
        self.cur = self.root
        for child in range(randint(4, 12)):
            new_child = self.recur(self.root, level + 1, num_levels)
            self.root.children.append(new_child)
            self.root.size += new_child.size
        # Rerun if we didn't generate enough folders
        if len(self.dirs) < minimum_dirs:
            self.make_file_system()
            return
        # Select random folders to be "corrupted" and set them as such
        for i in range(self.num_incorrect):
            val = randint(0, len(self.dirs) - 1)
            self.incorrects.append(self.dirs[val])
            del self.dirs[val]
        self.dirs += self.incorrects
        for incorrect in self.incorrects:
            add = randint(1, 4837)
            loc = self.find_node(incorrect)[1]
            while loc is not None:
                loc.size += add
                loc = loc.parent

    def recur(self, parent, level, max_level):
        if level == max_level - 1:
            poss_types = [0]
        else:
            poss_types = [0, 1]
        ftype = choice(poss_types)
        prepend = parent.name if parent.name is "/" else parent.name + "/"
        name = prepend + self.rand_string()
        # print "  " * level + name
        low, high = 20, 400000
        # File type 0 is a regular file and file type 1 is a directory
        if not ftype:
            new_node = Node(name, ftype, parent, randint(low, high))
        else:
            new_node = Node(name, ftype, parent)
            self.dirs.append(new_node.name)
            children = [self.rand_string() for _ in range(randint(4, 10))]
            for child in children:
                new_child = self.recur(new_node, level + 1, max_level)
                new_node.children.append(new_child)
                new_node.size += new_child.size
        return new_node

    def rand_string(self, l=3, h=7):
        return "".join([chr(randint(97, 122)) for i in range(randint(l, h))])


def signal_handler(signum, frame):
    raise Exception("Time's up!")


def run():
    score = 0
    num_games = 20
    game = Game()
    while score < num_games:
        print game.cur.name + ":", "$",
        val = raw_input().strip()
        try:
            run = game.parse_command(val)
        except Exception, msg:
            continue
        if run:
            if run == -1:
                game = Game()
                score += 1
                print "Hooray! You found all the corrupted folders!"
                if score < num_games:
                    print "Now on to the next system"
            else:
                print run
    if score >= num_games:
        with open("flag.txt") as f:
            print f.read().strip()


def instructions():
    print("Some of our file systems have been corrupted recently, we need")
    print("your help to find which folders are corrupted.")
    print("-" * 60)
    print("""
You will be placed in the file systems one by one and you will
need to navigate through the systems. You will see some of
the folders have contents whose sizes don't add up to the same
size of the folder they are in. We need you to find these folders.

There are three available commands:
cd [destination] - Change working directory to destination
ls [destination] - List contents of destination, Leave destination blank for ./
                    Lists contents of destination in the form:
                    [destination]: (number of contents)
                    entry_name entry_type entry_size
                    An example:
                    /: $ ls fdsk
                    fdsk: (2 entries)
                    tfi   DIR  43294
                    abdka FILE 9543
send [destination] - Send destination as an answer, if you get a folder wrong
                        you get kicked out of the system!
    """)
    # print
    print("Below is an example.")
    print("-" * 60)
    print("""
/: $ ls
/: (4 entries)
xkkgj   DIR  7450
ddh     FILE 2
uijuse  FILE 4
kiua    FILE 5
/: $ cd xkkgj
/xkkgj: $ ls
/xkkgj: (5 entries)
qoj     DIR  7
vrikuw  DIR  31
krqg    DIR  4150
vlqhe   FILE 1
jfkmaev DIR  3261
/xkkgj: $ cd qoj
/xkkgj/qoj: $ ls
/xkkgj/qoj: (4 entries)
sepk    FILE 2
ybwi    FILE 3
ecoxtam FILE 1
rlmav   FILE 1
/xkkgj/qoj: $ cd ..
/xkkgj: $ cd vrikuw
/xkkgj/vrikuw: $ ls
/xkkgj/vrikuw: (8 entries)
jns     FILE 4
eaqps   FILE 5
pwdq    FILE 4
rosopj  FILE 5
whicb   FILE 3
gbekky  FILE 4
xvumook FILE 1
btliuft FILE 5
/xkkgj/vrikuw: $ cd ..
/xkkgj: $ cd krqg
/xkkgj/krqg: $ ls
/xkkgj/krqg: (10 entries)
pgfd    FILE 3
bpdi    FILE 4
xpgswzo FILE 5
tyynmoi FILE 1
hqky    FILE 3
pgn     FILE 3
jlnxx   FILE 5
gsmyl   FILE 5
ucarx   FILE 1
epueuow FILE 3
/xkkgj/krqg: $ cd ..
/xkkgj: $ send krqg
Correct!
/xkkgj: $ cd jfkmaev
/xkkgj/jfkmaev: $ ls
/xkkgj/jfkmaev: (10 entries)
qlyq    FILE 3
nzp     FILE 4
vmiai   FILE 4
eayv    FILE 4
ztql    FILE 4
pddu    FILE 1
adf     FILE 5
ejwrlhy FILE 5
fveby   FILE 5
vreqfv  FILE 2
/xkkgj/jfkmaev: $ send .
Correct!
Hooray! You found all the corrupted folders!
Now on to the next system

Notice in the example that /xkkgj/krpg is one of the corrupt folders but /xkkgj
is not. The /xkkgj's size matches the sum of the files and directories under it
including with /xkkgj/krpg's incorrect size, in this case /xkkgj is not
considered wrong.

""")
    print "-" * 60

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(1200)
    try:
        while True:
            print 'Send "instructions" for instructions or "start" to begin.'
            inp = raw_input().strip()
            if inp.lower() == "instructions":
                instructions()
            elif inp.lower() == "start":
                break
            else:
                print("Option not recognized, please try again.")
        run()
    except Exception, msg:
        print "\n" + str(msg)
