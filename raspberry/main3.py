from serial import *
from multiprocessing import *   # IProcess, Queue
from threading import Thread
from config import dispport, path, port

import chess.engine
import enum
# This process handles the 2 serial rx and 2 serial tx streams
def io_process(io_cmd, io_move, disp_cmd, disp_input):
    def cmd_thread(comm: Serial, queue:Queue):
        while(True):
            cmd = queue.get(True)   # Blocking queue receive
            comm.write(f"{cmd}\n".encode())

    def move_thread(comm: Serial, queue:Queue):
        while(True):
            data = comm.readline().decode()[:-1]    # remove \n
            queue.put((data[0], data[1:3]))
    
    def disp_thread(comm: Serial, queue:Queue):
        while(True):
            cmd = queue.get(True)   # Blocking queue receive
            comm.write(f"COM:{cmd}\n".encode())

    def touch_thread(comm: Serial, queue:Queue):
        while(True):
            data = comm.readline().decode()[:-1]    # remove \n
            queue.put(data) # Unsicher wie das format hier aussieht, erstmal ohne vorfilterung

    comm_io = Serial(port=port, baudrate=115200)
    comm_io.reset_input_buffer()
    comm_usb = Serial('/dev/ttyUSB0', baudrate=115200)

    cmd = Thread(target=cmd_thread, args=[comm_io, io_cmd], daemon=True)
    move = Thread(target=move_thread, args=[comm_io, io_move], daemon=True)
    disp = Thread(target=disp_thread, args=[comm_usb, disp_cmd], daemon=True)
    touch = Thread(target=touch_thread, args=[comm_usb, disp_input], daemon=True)
    cmd.run()
    move.run()
    disp.run()
    touch.run()

    cmd.join()
    move.join()
    disp.join()
    touch.join()
    # We should never leave this process, as the threads never return


def handle_chess_action(io_cmd:Queue, io_move:Queue, disp_cmd:Queue, disp_input:Queue):
    engine = chess.engine.SimpleEngine.popen_uci(path)
    board = chess.Board()
    first_taken = ""
    second_taken = ""
    placed = ""
    while(True):
        try:    # First: Handle chess movements
            move = io_move.get(block=False)
            if move[0] == "t":
                if first_taken == "":
                    first_taken = move[1:3]
                    try:
                        allowed_moves = board.find_move(chess.parse_square(first_taken))
                        for move in allowed_moves:
                            io_cmd.put(f"s{move}")  # light up possible moves (like in lichess)
                    except:
                        pass
                else:
                    second_taken = move[1:3]
            elif move[0] == "p":
                placed = move[1:3]
            # do move handler things?
        except:
            pass

        if placed != "":
            if placed != first_taken:   # piece was put back, skip the rest
                if chess.Move.from_uci(first_taken+placed) in board.legal_moves:
                    for move in allowed_moves:
                        io_cmd.put(f"c{move}")  # disable the previously possible moves
            first_taken, second_taken, placed = ""


        try:    # Second: Handle inputs from the dispaly
            user_input = disp_input(block=False)
        except:
            pass
    engine.quit()


def main():
    io_cmd = Queue(maxsize = 16)
    io_move = Queue(maxsize = 16)
    disp_cmd = Queue(maxsize = 16)
    disp_input = Queue(maxsize = 16)

    io = Process(target=io_process, args=[io_cmd, io_move, disp_cmd, disp_input])
    io.start()
    
    state = 0

    if state == 0:
        disp_cmd.put("reboot")
        response = disp_input.get(True, 0.2)  # wait for start up
        if response == "Startup complete":
            state = 1
            scene = 0
    elif state == 1:
        # wait for game start (black/white) or getting saved games
        state = 2
    elif state == 3:
        # startup the engine, wait for pieces
        state = 3
    elif state == 3:
        ret = handle_chess_action(io_cmd, io_move, disp_cmd, disp_input)
        if ret < 0:
            state = 4
    elif state == 4:
        # do some cleanup
        quit() 

if __name__ == "__main__":
    main()