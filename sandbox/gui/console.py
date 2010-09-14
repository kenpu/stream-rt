from Tkinter import *
from tkFont import Font
import sys
from twisted.internet import tksupport, reactor

class Application:

  def __init__(self, root):
    
    # pack controls into the root
    f1 = Frame(root)
    f1.grid(row = 1, column = 1)
    
    self.play = Button(f1, text = "Play", command = self.quit)
    self.play.grid(row=1, column=1)

    self.pause = Button(f1, text = "Pause")
    self.pause.grid(row=1, column=2)

    self.console = Text(f1, font = Font(family = "Helvetica", size=16))
    self.console.grid(row=2, column=1, columnspan=2)

  def quit(self, *E, **F):
    print "quit called(%s)" % repr(E)
    sys.exit(0)

root = Tk()

app = Application(root)

root.mainloop()
