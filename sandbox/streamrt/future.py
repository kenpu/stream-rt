#-------------------------------------------------
import streamrt
import streamrt.runtime as runtime
import streamrt.conversion as conversion

#---------- Future -------------------------------
import json
from twisted.internet import interfaces
from twisted.protocols import basic

class F_Consumer:
    
  
  class Protocol(basic.LineReceiver):
    def lineReceived(self, line):
      pass
    def rawDataReceived(self, data):
      pass
  
  class Producer:
    implements(interfaces.IProducer)
    
    def __init__(self, 

if __name__ == '__main__':
  
