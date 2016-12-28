#!/usr/bin/python   # make it self-executing.
#

# PyFind.py:  Find and display files.
#

__file__    = "PyFind.py"
__author__  = "Harry Kline"
__version__ = "PyFind 20161224:  find and display files"

# if necessary, add mCore's path to sys.path
#import sys
#sys.path.append('/home/harry/k_PY/mCore')
import Mcore
import Mfile
import os

from Tkinter import\
  TOP, LEFT, RIGHT, BOTH, X, Y, NONE, RIDGE, FLAT, SUNKEN,\
  YES, NO, IntVar, DISABLED, mainloop
#import threading
today = Mcore.FloatDate()

Root = None                              # Root GUI Display
Data = None                              # directory data - folders & files
    
FileFont  = ('fixed', 11, 'normal')
FontSize = 16
Lblue = 'lightblue'
Lgrey = 'lightgrey'                    # background colors
Lgreen = 'lightgreen'
Dleft = None
Dright = None
LGcol = 'lightgreen'
LBcol = 'lightblue'
StructureWords = ['class ', 'def ']
BGfil = LGcol
BGwrd = LBcol

# ----------------------------------------------------- define overall framework
Rwidth = 1500
Rheight = 1200
BigDisplayWidth = 100

# FWdef fields: name, type, parent, side, fill, expand, border, relief,
#               background, font, text
# FWdef types:  Tk=Tk, LF=LabelFrame, F=Frame, L=Label, LB=ListBox, E=entry
FWdef = [\
  ['R', 'Tk', None, LEFT, BOTH, YES, 3, RIDGE, '', '', ''],\
  ['DirLine', 'F', 'R', TOP, X, NO, 3, RIDGE, '', '', ''],\
  ['FindLine', 'F', 'R', TOP, X, NO, 3, RIDGE, '', '', ''],\
  ['DispLine', 'F', 'R', TOP, X, NO, 3, RIDGE, '', '', ''],\
  ['Lists', 'F', 'R', TOP, BOTH, YES, 4, FLAT, '','',''],\

  ['Lab4', 'L', 'FindLine', LEFT, NONE, NO, 3, FLAT, BGfil,'','FIND FILES: '],\
  ['Fdir1', 'F', 'FindLine', LEFT, X, NO, 2, FLAT, '','',''],\
  ['Lab1', 'L', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','',' BY: nam'],\
  ['Enam', 'E', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','',''],\
  ['Lab2', 'L', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','','ext'],\
  ['Eext', 'E', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','',''],\
  ['Lab3', 'L', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','','text'],\
  ['Etxt', 'E', 'FindLine', LEFT, NONE, NO, 3, FLAT, '','',''],\

  ['Lab0', 'L', 'DirLine', LEFT, NONE, NO, 3, FLAT, '','','DIRECTORY: '],\
  ['FdirN', 'F', 'DirLine', LEFT, X, NO, 3, FLAT, '', '', ''],\
  ['namD', 'L', 'FdirN', LEFT, NONE, NO, 3, FLAT, '','',''],\
  ['space', 'L', 'DirLine', LEFT, NONE, NO, 3, FLAT, '','',' '],\
  ['framUP', 'F', 'DirLine', LEFT, NONE, NO, 3, FLAT, '','',''],\
  ['Lab00', 'L', 'DirLine', LEFT, NONE, NO, 3, FLAT, '','','      FILE: '],\
  ['namF', 'L', 'DirLine', LEFT, NONE, NO, 2, FLAT, '','',''],\

  ['FWleft', 'F', 'DispLine', LEFT, X, YES, 2, FLAT, '','',''],\
  ['FWlab', 'L', 'FWleft', LEFT, NONE, NO, 2, FLAT, BGwrd,'','FIND WORDS: '],\
  ['Ewords', 'E', 'FWleft', LEFT, NONE, NO, 3, FLAT, '','',''],\
  ['FWright', 'F', 'DispLine', LEFT, X, YES, 2, FLAT, '','',''],\
  ['FtcR', 'F', 'FWright', LEFT, X, YES, 2, FLAT, '','',''],\
  ['Flab', 'L', 'FWright', LEFT, NONE, NO, 2, FLAT, '','','Display:'],\
  ['FtcM', 'F', 'FWright', LEFT, X, NO, 2, FLAT, '','',''],\

  ['DirLists', 'LF', 'Lists', LEFT, Y, NO, 3, RIDGE, '','',''],\

  ['Ffol', 'LF', 'DirLists', TOP, Y, NO, 2, FLAT, '','',''],\

  ['Ffil', 'LF', 'DirLists', TOP, Y, NO, 2, FLAT, '','',''],\

  ['Fwrd', 'LF', 'DirLists', TOP, Y, NO, 2, FLAT, '','',''],\

  ['FileDisplay', 'LF', 'Lists', LEFT, BOTH, YES, 3, RIDGE, '', '', ''],\
  ]
  
# basic framework  
[R,DirLine,FindLine,DispLine,Lists,\
 Lab4,Fdir1,Lab1,Enam,Lab2,Eext,Lab3,Etxt,\
 Lab0,FdirN,namD,space,framUP,Lab00,namF,\
 FWleft,FWlab,Ewords,FWright,FtcR,FtcM,FtcM,\
 DirLists,Ffol,Ffil,Fwrd,FileDisplay]\
  = Mcore.FWsetup(FWdef)

# Root window setup
R.title(__version__ + '      DATE: ' + today.s)
R.config(width=Rwidth, height=Rheight)                   # window size

Dir = Mfile.Directory(R)                         # Directory instance
FFwidth = 0                                      # file and folder list width


# --------------------------------------------------------------- Listbox Object
class LBO:
  lines = []
  extra = []
  index = None
  maxlength = None
  width = 0
  LB = None
  def __init__(self, parent, side, select, title=None):
    self.LB = Mcore.Alistbox(parent, side, select)
    self.lines = []
    self.extra = []
    self.index = None
    if title != None: parent.Title(title)

  def Clear(self):
    self.lines = []
    self.index = None
    self.LB.Clear()

  def Store(self, lines, extra=[]):
    self.lines = lines
    self.extra = extra
    self.index = 0
    self.LB.Clear()

  def MaxLength(self):
    self.maxlength = 0
    for l in self.lines:
      self.maxlength = max(self.maxlength, len(l))
    return self.maxlength

  def Display(self, width):
    if width != None:
      self.width = width
      self.LB.SetWidth(width)
    self.LB.Clear()
    for l in self.lines:
      self.LB.AddLine(Mcore.Sjust(l, width, 'l'))

  def Highlight(self, line, color):
    if (self.index != None) and (len(self.lines) > 0):
      self.LB.itemconfig(self.index, bg = 'white')
      self.index = line
      self.LB.SeeLine(line)
      self.LB.itemconfig(line, bg = color)

# --------------------------------------------------- Folder/File/Word selection
def FolderSelect(l,c):              # folder selection comes here
  Dir.DOWN(l)
  GetDirectory()

def FileSelect(l,c):          # file selection comes here
  global Lwrd, Lfil, crv, BGfil
  Lfil.Highlight(l, BGfil)
  Lwrd.Clear()
  Dir.Index = l
  TB.select()
  GetTextComboData(Dir.Index)
  BigDisplay(2)
  FindWords(1)
  Lfil.Highlight(Lfil.index, BGfil)

def WordSelect(l,c):           # word selection comes here
  global Lwrd
  if len(Lwrd.lines) > 0:
    Lwrd.Highlight(l, BGwrd)
    Lbig.Highlight(Lwrd.extra[l], BGwrd)
    Lfil.Highlight(Lfil.index, BGfil)

def TextSelect(l,c): pass         # do nothing if line of text is selected

# ---------------------------------------------------------------- Listbox Setup
# Folders listbox setup
Lfol = LBO(Ffol, LEFT, FolderSelect, '         folders')
Lfol.LB.config(font=Mcore.ListFont)
Lfol.LB.SetMaxHgt(13)
Lfol.LB.AutoWidth = False
Lfol.LB.exportselection = False

# Files listbox setup
Lfil = LBO(Ffil, LEFT, FileSelect, '         files')
Lfil.LB.config(font=Mcore.ListFont)
Lfil.LB.SetMaxHgt(13)
Lfil.LB.AutoWidth = False
Lfil.LB.exportselection = False

# Words listbox setup
Lwrd = LBO(Fwrd, LEFT, WordSelect, '         words')
Lwrd.LB.config(font=Mcore.ListFont)
Lwrd.LB.SetMaxHgt(21)
Lwrd.LB.AutoWidth = False
Lwrd.LB.exportselection = False

# text listbox setup
Lbig = LBO(FileDisplay, LEFT, TextSelect)
Lbig.LB.config(font=Mcore.ListFont)
Lbig.LB.exportselection = False
 
# ----------------------------------------------------------------- GetDirectory
def FileType(f):              # f = entry in Dir.Files
  mode = 1                    # assume text
  try:                                         # check file type - text/combo
    InFile = open(f.PathNameExt)
    test = InFile.read(100)
    for c in test:
      if ord(c) > 127: mode = 2
      elif ord(c) in [9, 10, 13]: pass
      elif ord(c) < 32: mode = 2
    InFile.close()
  except: mode = 0
  return mode

def GetDirectory():       # get directory - folders, files, text/combo, words
  global Dir, Lfol, namD, FFwidth, Lwrd, crv
  flist = []                                     # setup the folder list
  for f in Dir.Folders: flist.append(f.NameExt)
  Lfol.Store(flist)

  flist = []                                     # setup the file list
  xlist = []
  for f in Dir.Files:
    flist.append(f.NameExt)
    xlist.append(FileType(f))
  Lfil.Store(flist, xlist)

  FFwidth = max(Lfol.MaxLength(), Lfil.MaxLength()) + 2     # folder/file width
  if FFwidth < 27: FFwidth = 27
  if FFwidth > 42: FFwidth = 42

  GetTextComboData(0)
  GetDirData()

  BigDisplay(1)

# the following three lists all use Lbig for displaying their data
TextData  = []
ComboData = []
DirData   = []    
  
# ------------------------------------------------------------- GetTextComboData
def GetTextComboData(i):            # get TextData and ComboData for use in Lbig
  global Dir, namF, namD, TextData, ComboData
  TextData = []
  ComboData = []
  mode = crv.get()                       # 1=text, 2=combo, 3=directory
  try:                                   # try to access the file
    fi = Dir.Files[i]
    fname = fi.PathNameExt
    namext = fi.NameExt
    namF.Set(namext)
    namF.config(bg=BGfil)
    namD.Set(fi.Path)
  except: return
  if fname == None: return
  try: fmode = Lfil.extra[i]
  except: fmode = 0
  
  if fmode == 1:                         # if text, format the lines
    try:
      InFile = open(fname)
      ln = 0
      for l in InFile:
        lin = l.rstrip('\n')             # ??? use os eol symbols
        lin = lin.rstrip('\r')
        lin = Mcore.Sjust(str(ln), 5, 'l') + lin
        TextData.append(lin)
        ln += 1
      InFile.close()
    except: pass

  InFile = open(fname)                   # now do combo lines = ascii and octal
  chars = InFile.read(fi.Size)           # read whole file as characters
  cpl = 10
  i = 0
  while i < len(chars):
    lin = Mcore.Sjust(str(i), 7, 'l')    # line number in ascii
    j = min(cpl, len(chars) - i)
    linx = ''
    linc = ''
    for k in range(j):
      ch = chars[i+k]
      cho = ord(ch)
      if (cho > 31) and (cho < 128):
        linc += ch
      else: linc += '.'
      linx += Mcore.Sjust(str(cho), 4, 'r')
    lin = lin + linc + '  ' + linx
    ComboData.append(lin)                # display the line
    i += cpl
  InFile.close()

# ------------------------------------------------------------------ Get DirData
def GetDirData():                        # get DirData ready for use in Lbig
  global Dir, DirData
  DirData = []
  Wn = Ws = 0                            # space for name, size, items
  for F in Dir.Folders:                  # get maximum spaces needed
    Wn = max(Wn, len(F.PathNameExt))
    Ws = max(Ws, len(str(F.Size)))
  for F in Dir.Files:                    # get maximum spaces needed
    Wn = max(Wn, len(F.PathNameExt))
    Ws = max(Ws, len(str(F.Size)))
  Wn += 2;  Ws += 2
  Wn = min(Wn, 48)
  title = '  ' + Mcore.Sjust('Name', Wn, 'l')
  title += Mcore.Sjust('Size', Ws, 'l')
  title += Mcore.Sjust('Last Modified', 24, 'l')
  DirData.append(title)
  DirData.append(' ')
  I = 1
  J = 0
  while I <= len(Dir.Folders):           # folders
    lin = Mcore.Sjust(str(I), 3, 'l')
    fi = Dir.Folders[J]
    lin += Mcore.Sjust(fi.PathNameExt, Wn, 'l')
    lin += Mcore.Sjust(str(fi.Size), Ws, 'l')
    lin += Mcore.Sjust(fi.mtimeS, 24, 'l')
    DirData.append(lin)
    I += 1
    J += 1
  if J > 0: DirData.append(' ')
  J = 0
  while J < len(Dir.Files):            # files
    lin = Mcore.Sjust(str(I), 3, 'l')
    fi = Dir.Files[J]
    lin += Mcore.Sjust(fi.PathNameExt, Wn, 'l')
    lin += Mcore.Sjust(str(fi.Size), Ws, 'l')
    lin += Mcore.Sjust(fi.mtimeS, 24, 'l')
    DirData.append(lin)
    I += 1
    J += 1

# ------------------------------------------------------------------ TextOrCombo
def TextOrCombo():
  global mode, Lbig
  mode = crv.get()
  try: fmode = Lfil.extra[Lfil.index]
  except:
    fi = Dir.Files[Lfil.index]
    fmode = FileType(fi)
  if mode == 3: Lbig.Store(DirData)
  elif (mode == 1) and (fmode == 1): Lbig.Store(TextData)
  else:
    Lbig.Store(ComboData)
    crv.set(2)
  Lbig.Display(BigDisplayWidth)
  FindWords(0)

# ------------------------------------------------------------------ Big Display
def BigDisplay(dcon):
  global FFwidth, BGfil, TextData, BigDisplayWidth, ComboData, DirData
  if dcon == 1:                 # display everything
    Lfol.Display(FFwidth)              #   folders
    Lfil.Display(FFwidth)              #   files
    TextOrCombo()
  elif dcon == 2:               # display text or combo
    TextOrCombo()
  elif dcon == 4:               # display directory
    Lbig.Store(DirData)
    Lbig.Display(BigDisplayWidth)
  elif dcon == 5:
    Lfil.Display(FFwidth)
    TextOrCombo()
  Lfil.Highlight(Lfil.index, BGfil)

# ----------------------------------------------------------------- button stuff
def UpDir(evnt):                       # 'UP' button comes here
  global Dir
  Dir.UP()
  GetDirectory()

def WLplus(evnt):                                # next word line
  global Lbig, Lwrd
  numlines = len(Lwrd.lines)
  i = Lwrd.index
  if numlines > 0:
    i += 1
    if i >= numlines: i = 0
    Lwrd.Highlight(i, BGwrd)
    Lbig.Highlight(Lwrd.extra[i], BGwrd)
    Lfil.Highlight(Lfil.index, BGfil)
    
def WLminus(evnt):                               # previous word line
  global Lbig, Lwrd
  numlines = len(Lwrd.lines)
  i = Lwrd.index
  if numlines > 0:
    i -= 1
    if i < 0: i = numlines - 1
    Lwrd.Highlight(i, BGwrd)
    Lbig.Highlight(Lwrd.extra[i], BGwrd)
    Lfil.Highlight(Lfil.index, BGfil)

def SeeText(evnt): BigDisplay(2)                 # 'text' radiobutton comes here

def SeeCombo(evnt): BigDisplay(2)               # 'combo' radiobutton comes here

def SeeFolders(evnt): BigDisplay(4)           # 'folders' radiobutton comes here

# come here for  Ewords, Exact, Caseless, +, -, file select, folder select
def FindWords(evnt):
  global Ewords, Lwrd, FFwidth, Case, crv, Lbig, TextData
  Lwrd.LB.SetWidth(FFwidth)
  Lwrd.Clear()
  xtra = []
  mode = crv.get()             # 1=text, 2=combo, 3=directory
  try:
    filetype = Lfil.extra[Lfil.index]   # 0 = none, 1 = text, 2 = combo
  except: return
  if (mode == 1) and (filetype == 1) and (len(TextData) > 0):
    findtext = Ewords.get()
    if Case == 'caseless': findtext = findtext.upper()
    findtext = findtext.split()
    if len(findtext) > 0:                       # display text
      try:
        ln = 0
        for l in TextData:
          lin = l.rstrip('\n')      # ??? use os eol symbols
          lin = lin.rstrip('\r')
          if Case == 'caseless': lin = lin.upper()
          lin = lin.split()
          for w in findtext:
            if (w in lin) and (ln not in xtra):
              xtra.append(ln)
          ln += 1
      except: pass
  if (len(xtra) > 0) and (len(TextData) > 0):
    displaylines = []
    for l in xtra:
      lin = TextData[l]
      displaylines.append(Mcore.Sjust(lin, FFwidth, 'l'))
    Lwrd.Store(displaylines, xtra)
    Lwrd.Display(FFwidth)
    Lwrd.Highlight(0, BGwrd)
    Lbig.Highlight(Lwrd.extra[0], BGwrd)
  Lfil.Highlight(Lfil.index, BGfil)

Ewords.bind('<Return>', FindWords)

def WordsAndText(): pass
    
Case = 'exact'

def ExactSelection(evnt):
  global Case, ExactButton,CaselessButton
  ExactButton.config(bg=BGwrd)
  CaselessButton.config(bg='lightgrey')
  Case = 'exact'
  FindWords(1)

def CaselessSelection(evnt):
  global Case, ExactButton,CaselessButton
  ExactButton.config(bg='lightgrey')
  CaselessButton.config(bg=BGwrd)
  Case = 'caseless'
  FindWords(1)
  

# -------------------------------------------------------------------- get files
def GetLocalFiles(evnt):             # Local By button comes here
  global Dir, Enam, Eext, Etxt
  Dir.LocalFind(Enam.get(), Eext.get(), Etxt.get())
  Wn = 0
  for N in Dir.Files:                   # get display width for folder/file names
    Wn = max(Wn, len(N.NameExt))
  Wn += 2;
  Wn = min(Wn, 27)
  lines = []
  extra = []
  for f in Dir.Files:
    lines.append(Mcore.Sjust(f.NameExt, Wn, 'l'))
    extra.append(FileType(f))
  Lfil.Store(lines, extra)
  GetTextComboData(0)
  BigDisplay(5)

def GetTreeFiles(evnt):             # Tree By button comes here
  global Dir
  Dir.TreeFind(Enam.get(), Eext.get(), Etxt.get())
  Wn = 0
  for N in Dir.Files:                   # get display width for folder/file names
    Wn = max(Wn, len(N.NameExt))
  Wn += 2;
  Wn = min(Wn, 27)
  lines = []
  extra = []
  for f in Dir.Files:
    lines.append(Mcore.Sjust(f.NameExt, Wn, 'l'))
    extra.append(FileType(f))
  Lfil.Store(lines, extra)
  GetTextComboData(0)
  BigDisplay(5)
 
def NextFile(evnt):
  global Lwrd, Lfil, BGfil
  i = Lfil.index + 1
  if i >= len(Lfil.lines): i = 0
  Lfil.Highlight(i, BGfil)
  Lwrd.Clear()
  Dir.Index = Lfil.index
  TB.select()
  GetTextComboData(Dir.Index)
  BigDisplay(2)
  FindWords(1)
  Lfil.Highlight(Lfil.index, BGfil)

def PrevFile(evnt):
  global Lwrd, Lfil, BGfil
  i = Lfil.index - 1
  if i < 0: i = len(Lfil.lines) -1
  Lfil.Highlight(i, BGfil)
  Lwrd.Clear()
  Dir.Index = Lfil.index
  TB.select()
  GetTextComboData(Dir.Index)
  BigDisplay(2)
  FindWords(1)
  Lfil.Highlight(Lfil.index, BGfil)

# --------------------------------------------------------------------- MAIN 

Mcore.Abutton(framUP, LEFT, 'UP', UpDir)
crv = IntVar()
FOB = Mcore.Aradiobutton(FtcM, RIGHT, 'directory', SeeFolders, crv,3)
CB = Mcore.Aradiobutton(FtcM, RIGHT, 'combo', SeeCombo, crv,2)
TB = Mcore.Aradiobutton(FtcM, RIGHT, 'text', SeeText, crv,1)
ExactButton = Mcore.Abutton(FWleft, LEFT, 'exact', ExactSelection)
CaselessButton = Mcore.Abutton(FWleft, LEFT, 'caseless', CaselessSelection)
Mcore.Abutton(FWleft, LEFT, '+', WLplus)
Mcore.Abutton(FWleft, LEFT, '-', WLminus)
Mcore.Abutton(Fdir1, LEFT, 'Local', GetLocalFiles)
Mcore.Abutton(Fdir1, LEFT, 'Tree', GetTreeFiles)
Mcore.Abutton(FindLine, RIGHT, '-', PrevFile)
Mcore.Abutton(FindLine, RIGHT, '+', NextFile)
Eext.Set('py')
Ewords.Set('class def')
TB.select()
GetDirectory()
GetLocalFiles(1)
ExactSelection(1)
    
if __name__ == '__main__':
  mainloop()
