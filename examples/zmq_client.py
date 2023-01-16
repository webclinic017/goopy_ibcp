# ZeroMQ client

import zmq
from time import sleep


def thread():
    context = zmq.Context()
    socket_es = context.socket(zmq.SUB)

    socket_es.connect("tcp://localhost:5555")
    socket_es.setsockopt_string(zmq.SUBSCRIBE, "es")

    poller = zmq.Poller()
    poller.register(socket_es, zmq.POLLIN)

    while True:
        try:
            sock = dict(poller.poll(5000))
        except KeyboardInterrupt:
            break

        msg = None

        if socket_es in sock:
            msg = socket_es.recv_string()
            symbol, time, last = msg.split(",")
            print(f"{time}:{symbol}={last}")

        sleep(0.001)


if __name__ == "__main__":
    thread()