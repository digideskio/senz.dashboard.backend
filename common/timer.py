import threading
import time


class Timer(threading.Thread):
    """
    very simple but useless timer.
    """
    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.runTime)


class CountDownTimer(Timer): 
    """
    a timer that can counts down the seconds.
    """
    def run(self):
        counter = self.runTime
        for sec in range(self.runTime):
            time.sleep(1.0)
            counter -= 1


class CountDownExec(CountDownTimer): 
    """
    a timer that execute an action at the end of the timer run.
    """
    def __init__(self, seconds, action, *args):
        self.args = args
        self.action = action
        CountDownTimer.__init__(self, seconds)

    def run(self):
        CountDownTimer.run(self)
        self.action(self.args)


def myaction(*args):
    print "Performing my action with args:"
    print args


if __name__ == "__main__":
    d = {"hello": "world"}
    myaction({"hello": "world"})
    t = CountDownExec(3, myaction, '123', d)
    t.start()
