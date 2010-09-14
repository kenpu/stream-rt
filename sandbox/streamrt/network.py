import json
from zope.interface import implements
from twisted.internet import interfaces
from twisted.protocols import basic

class Packet(dict):
  """ a payload container for Map + Binary data
  If key name ends with "_", then the content is assumed to be
  binary.
  """
  def __init__(self, *E, **F):
    super(Packet, self).__init__(*E, **F)
    
  def __getattr__(self, attr):
    return self.get(attr)
  
  def __setattr__(self, attr, value):
    self[attr] = value

  def serialize(self, fileobj):
    text = dict()
    binary = dict()
    for (k, v) in self.items():
      if k.endswith("_"):
        binary[k] = v
      else:
        text[k] = v
    fileobj.write(json.dumps(text) + "\n")
    for k, v in binary.items():
      fileobj.write("%s\t%d\n" % (k, len(v)))
      fileobj.write(v)


class PacketReceiver(basic.LineReceiver):
  
  def lineReceived(self, line):
    _ = line.split("\t", 1)
    jsonData = _[0]
    payloadSizes = [int(x) for x in _[1:]]
    self.packet = Packet(json.loads(jsonData))
    self.payloadSizes = payloadSizes
    self.payloadSum = sum(payloadSizes) if payloadSizes else 0
    if self.payloadSum:
      self.setRawMode()
      self.buffer = ''
    else:
      self.packetReceived(self.packet)

  def rawDataReceived(self, data):
    self.buffer += data
    if len(self.buffer) >= self.payloadSum:
      overflow = self.buffer[self.payloadSum:]
      i = 0
      for n in self.payloadSizes:
        self.packet.addBinary(self.buffer[i:(i+n)])
        i += n
      self.packetReceived(self.packet)
      self.setLineMode(overflow)

  def packetReceived(self, packet):
    raise Exception("Not implemented")

  def sendPacket(self, packet):
    self.transport.write(packet.serialize())
