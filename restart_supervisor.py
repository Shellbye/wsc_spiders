__author__ = 'shellbye'
import xmlrpclib


def xml_rpc():
    username, password = "", ""
    with open('supervisord.conf', 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('username'):
                username = line.split("=")[-1].strip()
            if line.startswith('password'):
                password = line.split("=")[-1].strip()
    server = xmlrpclib.Server('http://' + username + ':' + password + '@localhost:9001/RPC2',
                              allow_none=True)
    server.supervisor.restart()


if __name__ == '__main__':
    xml_rpc()