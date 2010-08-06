import os
import itertools
from datetime import datetime, timedelta
import tarfile

"""
Collections of file accessing functions and classes.  Note for the
special timestamp handling.
"""

def getTarDatetime(filename):
  return datetime.strptime(filename[:20], "%Y-%m-%d__%H-%M-%S")

def getTarTimespan(fullpath):
  x = tarfile.open(fullpath)
  members = x.getnames()
  return (getImgDatetime(members[0]), getImgDatetime(members[-1]))
  
def getImgDatetime(filename):
  return datetime.strptime(filename[:20], "%Y-%m-%d__%H:%M:%S")
  
def getImages(tarfilename, open=True):
  untarred = tarfile.open(tarfilename)
  tarinfo = untarred.next()
  while not tarinfo == None:
    if open:
      fileobj = untarred.extractfile(tarinfo)
      yield (getImgDatetime(tarinfo.name), fileobj)
    else:
      yield getImgDatetime(tarinfo.name)
    tarinfo = untarred.next()

class ImageDirectory:
  """
  Allows random access of the image frames in the tar files in the
  directory specified by path.
  
  - Supports a single session.
  """
  def __init__(self, path):
    self.path = path
    self.files = []
    self.param = {}
    self.refresh()
    self.time_pointer = None
    
  def refresh(self):
    self.files = sorted(x for x in os.listdir(self.path) if x.endswith(".tar"))
    self.timespans = [getTarTimespan(os.path.join(self.path, x)) for x in self.files]
    if not self.files:
      raise Exception("%s does not contain any tar files")

    self.param['start_time'] = self.timespans[0][0]
    self.param['end_time'] = self.timespans[-1][1]
    self.param['step'] = timedelta(seconds=10)
  
  def durationInSeconds(self):
    return self.duration * 24 *3600 + self.seconds
  
  def setParameter(self, attr, val, restart=False):
    self.param[attr] = val
      
  def jumpTo(self, t):    
    for (i, (start, end)) in enumerate(self.timespans):
      if t <= end:
        self.file_pointer = i
        self.img_iterator = getImages(os.path.join(self.path, self.files[i]), open=True)
        return start
    
  def getNextFrameInStream(self, next_time):
    for (t, fileobj) in self.img_iterator:
      if next_time <= t:
        return t, len(fileobj.read())
    raise Exception("next_time %s is not in stream" % str(next_time))
    
  def next(self):
    
    if self.time_pointer == None:
      self.time_pointer = self.param['start_time']
      self.jumpTo(self.time_pointer)
      
    next_time = self.time_pointer + self.param['step']
    timespan = self.timespans[self.file_pointer]
    if next_time >= self.param['end_time']:
      self.time_pointer = self.param['start_time']
      next_time = self.jumpTo(self.time_pointer)
    elif not (timespan[0] <= next_time <= timespan[1]):
      next_time = self.jumpTo(next_time)

    frame = self.getNextFrameInStream(next_time)
    self.time_pointer = frame[0]
    return frame
      
  def __iter__(self):
    return self
