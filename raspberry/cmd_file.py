import queue
import threading

cmdlist = ["stop","takeback","stable"]



def cmd_fun(q:queue.Queue):
    print("CMD Ready")
    while True:
        cstr = input().strip()

        #print("got CMD " + cstr)

        if cstr not in cmdlist:
            print(f"Unkonwn Command: {cstr}")
            continue

        q.put(cstr)

        print("put: " + cstr)
        if cstr == "stop":
            return


class CMD_HANDLER:
    def __init__(self):
        self.q = queue.Queue()
        self.t = threading.Thread(target=cmd_fun,args=(self.q,))
        self.t.start()

    def get_cmd(self):
        if not self.q.empty():
            return self.q.get()

    def cmd_ready(self):
        return not self.q.empty()

    def cmd_close(self):
        self.t.join()
