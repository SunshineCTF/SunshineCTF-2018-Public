import socket

HOST, PORT = 'localhost', 30001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def readuntil(val=" "):
    l = ""
    k = sock.recv(1)
    while k != val:
        l = "".join([l, k])
        k = sock.recv(1)
    return l


def send(line):
    sock.send(line + "\n")


def readline():
    return readuntil("\n")


def get_number(line):
    loc_paren = line.index("(") + 1
    return int(line[loc_paren:].split()[0])


answers = []
done = False


def recur(name, size, level=0):
    if done:
        return
    sock.send("cd {}\n".format(name))
    first = readuntil()
    if "Hooray" in first:
        global done
        done = True
        return
    second = readuntil()
    send("ls")
    line = readline()
    num_children = get_number(line)
    children = [readline() for line in range(num_children)]
    children = [child.split() for child in children]
    sum_sizes = sum([int(child[2]) for child in children])
    if sum_sizes != size and name != "/":
        print "found:", name
        send("send .".format(name))
        answers.append(first[:-1])
        reply = readline()
        print reply
    for child in children:
        if child[1] == "DIR":
            recur(child[0], int(child[2]), level+1)
    send("cd ..")


while True:
    beg = readuntil()
    print beg
    answers = []
    done = False
    recur("/", 0)
    print answers
    l, j = readline(), readline()
    print l
    print j
    if "sun" in l or "sun" in j:
        break
