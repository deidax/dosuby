# This code does a port/ports scan for a remote host.
# The list of ports and a remote host are entered as command line args.
# We create a separate thread to check port connection. Hence it is faster and more # efficient. We can now use connect() as we have a separate thread for each port  #connect.
import argparse
from threading import *
from socket import *
# This Thread gets created for each port. Tries to connect to
def check_socket_connection(host, port):
  try:
      server_sock = socket(AF_INET, SOCK_STREAM)
      server_sock.settimeout(5)
      result = server_sock.connect((host, port))
      print('[+] {}/tcp open'.format(port))
  except Exception as exception:
      print('[-] {}/tcp closed, Reason:{}'.format(port, (str(exception))))
  finally:
      server_sock.close()
# Scan the port list by creating threads for each port
def portScanner(host, ports):
  try:
      ip = gethostbyname(host)
      print('[+] Scan Results for: ' + ip)
  except:
      print("[-] Cannot resolve {}: Unknown host".format(host))
      return
  for port in ports:
      t = Thread(target=check_socket_connection, args=(ip, int(port)))
      t.start()
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('H', type=str, help='remote host name')
  parser.add_argument('P', type=str, nargs='*', help='port numbers')
  args = parser.parse_args()
  portScanner(args.H, args.P)