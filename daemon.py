#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, time, socket, pathlib

def run_daemon(socketpath, startup_time):
    if socketpath.exists():
        return
    timeout = 10
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
#        print('Binding to', socketpath)
        server.bind(str(socketpath).encode('UTF-8'))
    except OSError:
        raise
    server.settimeout(timeout)
    server.listen(1)
    time.sleep(startup_time)
    while True:
        conn, address = server.accept()
        data = conn.recv(1)
        conn.sendall(b'b')
        conn.close()

if __name__ == '__main__':
    starttime = time.time()
    #print('Compiler daemon begin.')
    socketpath = pathlib.Path(sys.argv[1]) / 'daemonsocket'
    startup_time = int(sys.argv[2])
    try:
        run_daemon(socketpath, startup_time)
    except TimeoutError:
        socketpath.unlink()
    endtime = time.time()
    #print('Compiler daemon finish.')
    duration = endtime - starttime
    if duration > 10:
        print('Daemon ran for', duration, 'seconds')
