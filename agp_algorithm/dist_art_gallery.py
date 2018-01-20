# -*- coding: utf-8 -*-

from cPickle import dumps
from cPickle import loads

from pymote.algorithm import NodeAlgorithm
from pymote.message import Message

from art_gallery import ArtGallery
from preview_control import PreviewControl


class DistributedArtGallery(NodeAlgorithm):
    """ Implements the distributed solution of the Art Gallery problem """

    # Host states
    STATUS = {'INITIATOR': 'initiator',
              'IDLE': 'idle',
              'DONE': 'done'}

    required_params = ('key',)
    default_params = {'neighborsKey': 'Neighbors'}

    def initializer(self):
        """ Method fot host initialization """

        for node in self.network.nodes():

            node.memory['neighbors_data'] = {}
            node._polygon = [node.memory['axis']]
            node.gallery = ArtGallery(node.memory['axis'])
            PreviewControl.add_view(node.gallery, str(node.id))

            # Fills node neighbors and notify each one its axis
            node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
            node.status = 'IDLE'

            self.notify(node, node.id, node.memory['axis'])

    def step(self, node):
        """ The step method is called every time a host receives a message """

        try:
            msg = node.receive()

            if msg is not None and msg.source != node:
                self.procmsg(node, msg)

        except Exception as e:
            raise Exception("Erro during processing message from node %s"
                            % node)

    def procmsg(self, node, msg):
        """ Process incoming messages """

        # deserialize data from message
        rec_data = loads(msg.data)

        # If the message data (host position) is unknown
        if rec_data not in node._polygon:

            node.memory['neighbors_data'][msg.source.id] = rec_data
            node._polygon.append(rec_data)

            # adds new point and recalculates the positions of the guards
            node.gallery.include(rec_data)

            # notifies the node neighbors about the message received
            self.notify(node, msg.source, rec_data)

    def notify(self, node, source, data):
        """ Notify neighbors. Forwarding operation """

        # Starts communication through neighbors nodes
        for neighbor in node.memory[self.neighborsKey]:

            msg = Message(header=NodeAlgorithm.INI, source=source,
                          destination=neighbor, data=dumps(data))

            node.send(msg)
