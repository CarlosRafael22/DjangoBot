import threading
import time

exitFlag = 0

class chatThread(threading.Thread):
    def __init__(self, threadID, chat_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.chat_id = chat_id
        self.counter = counter
    def run(self):
        print("Starting " + self.chat_id)
        print_time(self.chat_id, self.counter, 5)
        print("Exiting " + self.chat_id)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1