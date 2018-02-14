"""
Export an object that will handle all the communication with the Walabot.
"""

import json
import select
import socket
from threading import Thread

from tinydb import Query

from DBHandler import DBHandler as TinyDB
from config import DB_PATH, UTF_FORMAT, CAT_STATUS_FIELD, CAT_DATA_TABLE

CONNECTION_CLOSE_MESSAGE = 'Connection is closed'
BACKLOG = 5
MAX_MESSAGE_SIZE = 1024
CONNECTION_SOCKET_INDEX = 0
ADDRESS_INDEX = 1
SELECT_TIMEOUT = 5


class CatServer:
    """
    The server that will listen to Walabot connection and then will store the Walabot data in the db.
    :ivar server_address: The server address containing the ip, port as a tuple.
    :type server_address: C{tuple} of C{str}, C{int}
    :ivar server_socket: The socket that will listen to any new connections.
    :type server_socket: C{socket.socket}
    :ivar cat_db: The db to insert all the values gotten from the Walabot app
    :type cat_db: L{tinydb.TinyDB}
    :ivar room: The Query object for doing queries in the TinyDB object.
    :type room: L{tinydb.Query}
    :ivar connections: The queue to insert to the new connections.
    :type connections: C{SharedList}
    """

    def __init__(self, ip, port):
        """
        Instanitate the server socket.
        :param ip: The ip the server will listen to.
        :type ip: C{str}
        :param port: The port that the server will listen to.
        :type port: C{int}
        """
        self.server_address = ip, port
        self.server_socket = socket.socket()
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(BACKLOG)
        self.cat_db = TinyDB(DB_PATH, default_table=CAT_DATA_TABLE)
        self.cat_in_box = Query()
        self.connections = []

    def start(self):
        """
        The function that will start the server, start a thread that will listen to any clients' connections.
            Also we start a thread that will handle all the clients.
        """
        print("Start server functionality, listen on address: {0}".format(self.server_address))
        connections_thread = Thread(target=self.accept_connections)
        connections_thread.start()
        print("Start handling clients.")
        handle_clients_thread = Thread(target=self.handle_clients)
        handle_clients_thread.start()

    def accept_connections(self):
        """
        Will accept connection and insert them into a shared queue.
        """
        while True:
            print("Waiting for new connections.")
            client_socket, address = self.server_socket.accept()
            print("Got connection from -> {0}".format(address))
            print("Putting connection in the shared queue.")
            self.connections.append((client_socket, address))

    def handle_connection_close(self, client_connection, address):
        """
        Handle the situation that the client connection given in the arguments has closed the connection.
        :param client_connection: The client's socket connected to our server.
        :type client_connection: C{socket.socket}
        :param address: The address of the client
        :type address: C{tuple} of C{str}, C{int}
        """
        print("Connection was closed by the client {0}.".format(address))
        client_connection.close()
        # Removing the the connection tuple that was just closed from the connections list.
        self.connections.remove((client_connection, address))
        print("Client {0} was removed from the connections list.".format(address))

    def handle_client(self, client_connection, address):
        """
        Handle a client, read the data from its connected socket and determine what to do with it.
        :param client_connection: The socket connected to the client
        :type client_connection: C{socket.socket}
        :param address: The address of the connected client.
        :type address: C{tuple} of C{str}, C{int}
        """
        try:
            msg = client_connection.recv(MAX_MESSAGE_SIZE).decode(UTF_FORMAT)
            # if the msg is empty that means that the client closed the connection.
            if msg == CONNECTION_CLOSE_MESSAGE:
                self.handle_connection_close(client_connection, address)
                print("got a message and we need to handle it")
            # It means that we got a message from the Walabot and we need to handle it.
            else:
                data = json.loads(msg)
                print("Got {0} from client {1}".format(data, address))
                # Update the existing row with the new data.
                # If there isn't a cat_status row in the db we insert the row.
                if not self.cat_db.search(self.cat_in_box.cat_status_field.exists()):
                    print("Inserting new row.")
                    self.cat_db.insert(data)
                else:
                    print("Updating box with new data, cat status is: {0}".format(data[CAT_STATUS_FIELD]))
                    self.cat_db.update({CAT_STATUS_FIELD: data[CAT_STATUS_FIELD]})
                    print("updated db successfully")
        except socket.error:
            self.handle_connection_close(client_connection, address)

    def handle_clients(self):
        """
        Handle all the clients by waiting for the clients to be ready for reading from their sockets and
            then handle each socket.
        """
        while True:
            # Getting all the connections that are ready for reading.
            client_connections = [connection_tuple[CONNECTION_SOCKET_INDEX] for connection_tuple in self.connections]
            if client_connections:
                rlist, wlist, exlist = select.select(client_connections, [], [], SELECT_TIMEOUT)
                for connection in rlist:
                    # Getting the corresponding address of the connection socket.
                    address = [connection_tuple[ADDRESS_INDEX] for connection_tuple in self.connections
                               if connection_tuple[CONNECTION_SOCKET_INDEX] == connection]
                    # Taking the first index because its a list with one item.
                    self.handle_client(connection, address[0])
