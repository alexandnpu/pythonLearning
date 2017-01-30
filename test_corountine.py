
import time


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


def follow(thefile, target):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@coroutine
def printer():
    while True:
        line = yield
        print(line)


@coroutine
def grep(patten):
    print("Looking for {}".format(patten))
    try:
        while True:
            line = (yield)
            if patten in line:
                print(line)
    except GeneratorExit:
        print("Going away. Goodbye")


def countdown(n):
    print("Counting down from {}".format(n))
    while n >= 0:
        newvalue = (yield n)  # yield n if no value is sent in,
        if newvalue is not None: # if there is valude sent in, we use the new value
            n = newvalue
        else:
            n -= 1


def test_countdown():
    c = countdown(5)
    for n in c:
        print(n)
        if n == 3:
            c.send(9)


def test_follow_printer():
    f = open("/tmp/log", "r")
    follow(f, printer())


if __name__ == "__main__":
    #test_countdown()
    test_follow_printer()

