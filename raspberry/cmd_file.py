import queue
import threading

cmdlist = ["stop","takeback"]



def cmd_fun(q:queue.Queue):
    print("CMD Ready")
    while True:
        cstr = input().strip()

        if cstr not in cmdlist:
            print(f"Unkonwn Command: {cstr}")
            continue

        q.put(cstr)

        if cstr == "stop":
            break


class CMD_HANDLER:
    def __init__(self):
        self.q = queue.Queue()
        self.t = threading.Thread(target=cmd_fun,args=(self.q,),daemon=True)
        self.t.start()

    def get_cmd(self):
        if not self.q.empty():
            return self.q.get()

    def cmd_ready(self):
        return not self.q.empty()
