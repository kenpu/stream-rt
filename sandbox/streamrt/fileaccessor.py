import os
import itertools
from datetime import datetime
import tarfile

"""
Collections of file accessing functions and classes.  Note for the
special timestamp handling.
"""

def getTarDatetime(filename):
  return datetime.strptime(filename[:20], "%Y-%m-%d__%H-%M-%S")
  
def getImgDatetime(filename):
  return datetime.strptime(filename[:20], "%Y-%m-%d__%H:%M:%S")
  
def getImages(tarfilename, open=True):
  untarred = tarfile.open(tarfilename)
  tarinfo = untarred.next()
  while not tarinfo == None:
    if open:
      fileobj = untarred.extractfile(tarinfo)
  
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
    self.file_pointer = self.files[0]
    
    
  def refresh(self):
    self.files = sorted(x for x in os.listdir(self.path) if x.endswith(".tar"))
    if not self.files:
      raise Exception("%s does not contain any tar files")
      
    self.param['start_time'] = getTarDatetime(self.files[0])
    x = tarfile.open(os.path.join(self.path, self.files[-1]))
    members = x.getnames()
    self.param['end_time'] = getImgDatetime(members[-1])
    self.param['duration'] = (self.param['end_time'] - self.param['start_time'])
  
  def durationInSeconds(self):
    return self.duration * 24 *3600 + self.seconds
  
  def setParameter(self, attr, val, restart=False):
    self.param[attr] = val
    
  def 
