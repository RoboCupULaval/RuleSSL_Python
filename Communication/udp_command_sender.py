# Under MIT License, see LICENSE.txt
""" Le module regroupe les services d'envoies de paquets. """
# TODO: refactor les 2 modules ensembles

import pickle

from .command_sender import CommandSender
from .protobuf import grSim_Packet_pb2 as grSim_Packet
from .udp_utils import udp_socket

class UDPCommandSender(CommandSender):
    """ Service qui envoie les commandes de mouvements aux robots. """

    def __init__(self, host, port):
        """ Constructeur """
        self.server = udp_socket(host, port)

    def _send_packet(self, packet):
        """
            Envoie un paquet en sérialisant au préalable.

            :param packet: Un paquet prêt à l'envoie
        """
        self.server.send(packet.SerializeToString())

    def send_packet(self, command):
        """
            Construit le paquuet à envoyer à partir de la commande reçut.

            :param command: Command pour un robot
        """
        packet = grSim_Packet.grSim_Packet()
        packet.commands.isteamyellow = command.team.is_team_yellow
        packet.commands.timestamp = 0
        grsim_command = packet.commands.robot_commands.add()
        grsim_command.id = command.player.id
        grsim_command.wheelsspeed = False
        grsim_command.veltangent = command.pose.position.x
        grsim_command.velnormal = command.pose.position.y
        grsim_command.velangular = command.pose.orientation
        grsim_command.spinner = True
        grsim_command.kickspeedx = command.kick_speed
        grsim_command.kickspeedz = 0

        self._send_packet(packet)

class UDPDebugSender(CommandSender):
    """
        Définition du service capable d'envoyer des paquets de débogages au
        serveur et à l'interface de débogage. S'occupe de la sérialisation.
    """
    def __init__(self, host, port):
        """ Constructeur """
        self.server = udp_socket(host, port)

    def _send_packet(self, p_packet):
        """ Envoi un seul paquet. """
        self.server.send(pickle.dumps(p_packet))

    def send_packet(self, p_packets):
        """ Reçoit une liste de paquets et les envoies. """
        for packet in p_packets:
            self._send_packet(packet)
