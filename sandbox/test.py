from streamrt import fileaccessor
from itertools import *
from datetime import timedelta

D = fileaccessor.ImageDirectory("../../some-video-data")

for (f, (x,y)) in zip(D.files, D.timespans):
  print "%s: %s -> %s" % (f,x,y)

for frame in islice(iter(D), 0, 10):
  print frame
  
D.setParameter('step', timedelta(seconds=30))
print "step=30"

for frame in islice(iter(D), 0, 1000):
  print frame
