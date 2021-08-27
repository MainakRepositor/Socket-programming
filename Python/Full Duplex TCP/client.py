import socket
import select
import sys


def main():
    """
    main - Runs the Full Duplex Chat Client
    """

    serverHost = 'localhost'
    serverPort = 22222

    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print "ERROR: Cannot create client side socket:", err
        exit(1)

    while True:
        try:
            clientSocket.connect((serverHost, serverPort))
        except socket.error as err:
            print "ERROR: Cannot connect to chat server", err
            print "* Exiting... Goodbye! *"
            exit(1)
        except:
            print "ERROR: Something awful happened!"
            exit(1)
        break

    recvList = [clientSocket, sys.stdin]

    print "* You are now connected to chat server %s as %s *" % (clientSocket.getpeername(), clientSocket.getsockname())

    try:
        while True:
            readyRecvList, readySendList, readyErrList = select.select(recvList, [], [])

            for fd in readyRecvList:
                if fd == sys.stdin:
                    message = sys.stdin.readline().rstrip()
                    clientSocket.sendall("~" + str(message) + "~")

                    if (message == "quit()"):
                        print "* Exiting chat room! *"
                        clientSocket.close()
                        exit(0)
                        break

                elif fd == clientSocket:
                    clientSocket.settimeout(3)
                    try:
                        message = clientSocket.recv(2048)
                    except socket.timeout as err:
                        print "ERROR: The recv() function timed out after 3 seconds! Try again."
                    except:
                        print "ERROR: Something awful happened!"
                    else:
                        if message == "":
                            break
                        else:
                            print "%s\n" % (message)
                    clientSocket.settimeout(None)
                    break

    except select.error as err:
        for fd in recvList:
            try:
                tempRecvList, tempSendList, tempErrList = select.select([fd], [], [], 0)
            except select.error:
                if fd == clientSocket:
                    fd.close()
                    exit(1)
                else:
                    if fd in recvList:
                        recvList.remove(fd)
                        fd.close()

    except socket.error as err:
        print "ERROR: Cannot connect to chat server", err
        print "* Exiting... Goodbye! *"
        exit(1)

        if fd in recvList:
            fd.close()

    except KeyboardInterrupt:
        print "\nINFO: KeyboardInterrupt"
        print "* Closing all sockets and exiting chat server... Goodbye! *"
        clientSocket.close()
        exit(0)


if __name__ == '__main__':
    main()
