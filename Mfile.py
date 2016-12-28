
__file__    = "Mfile.py" 
__version__ = "20110708"
__doc__ = "File access support functions for GUI programs."

from Tkinter import *
import Mcore
  # uses: CompAB, Alabelframe, Abutton, Acanvas, Alabel, Alistbox,
  #       Sjust, QABdialog, DEM
  
import time                # uses localtime
import os                  # uses getcwd, walk, path, chdir
import sys                 # uses path

# Class Directory handles directory operations.
# Class DBfileClass handles file operations.
# Class Cryption handles data encryption/decryption operations.

# ------------------------------------------------------------- File/Folder Info
#    self.name = os.path.join(Path, NameExt)
#    self.dirname = os.path.dirname(self.name)       # Path
#    self.basename = os.path.basename(self.name)     # NameExt
class FileInfo:
  # file name = path + '/' + name + '/' + extension
  def __init__(self, Path, NameExt):
    self.Path = Path                                    # "Path"
    self.NameExt = NameExt                              # "Name.Extension"
    self.PathNameExt = os.path.join(Path, NameExt)      # "Path/Name.Extension"
    self.Ext = os.path.splitext(self.PathNameExt)[1]    # "Extension"
    self.isdir = os.path.isdir(self.PathNameExt)        # True == folder
    self.isfile = os.path.isfile(self.PathNameExt)      # True == file
    self.mtime = os.path.getmtime(self.PathNameExt)     # last modify time stamp
    (Y,M,D,Hour,Min,Sec,Wday, Yday, Isdst) = time.localtime(self.mtime)
    Ys = str(Y)
    Ms = str(M)
    if len(Ms) == 1: Ms = '0' + Ms
    Ds = str(D)
    if len(Ds) == 1: Ds = '0' + Ds
    Hs = str(Hour)
    if len(Hs) == 1: Hs = '0' + Hs
    Mns = str(Min)
    if len(Mns) == 1: Mns = '0' + Mns
    self.mtimeS = Ms + '/' + Ds + '/' + Ys + '  ' + Hs + ':' + Mns
    self.Items = 0                                    # items within PathNameExt
    self.Size = 0                                     # total size of all items
    
    if self.NameExt[0] == '.': return                 # ignore hidden
    else:                                             # get Items and Size
      self.Items = 1                                  # this item
      self.Size = os.path.getsize(self.PathNameExt)   #   and its size

      def GetPathSize(path):               # recursive routine to get total size
        try:
          LD = os.listdir(path)
          items = 0
          size = 0
          for f in LD:                             # for each folder/file in  path
            if f[0] == '.': pass                   # if hidden
            else:                                  # else seen
              PNE = os.path.join(path, f)
              items += 1
              try: size += os.path.getsize(PNE)    # add the size of folder/file
              except: pass
              if os.path.isdir(PNE):                 # recurse for folder contents
                I, S = GetPathSize(PNE)
                items += I
                size += S
          return items, size
        except: return 0,0

      if self.isdir:                # if folder then recurse to get items & size
        I, S = GetPathSize(self.PathNameExt)
        self.Items += I
        self.Size += S

    # enter with a path name to the Directory to search
    # return list of file names that meet the find criteria
def SearchDir(Dir, Tree, Name, Extension, Content): # search Dir for nam/ext/txt
  Folders = []
  Files = []
  def Search(path):
    fols = []
    LD = os.listdir(path)
    for fnam in LD:
      if fnam[0] == '.': pass                    # ignore hidden
      else:
        finfo = FileInfo(path, fnam)
        if finfo.isdir:
          fols.append(finfo)
          if Tree == 'Tree': Search(os.path.join(path, fnam))   # recurse
        else:      # check Extension and Name, then Content
          if ((Extension == '') or (Extension == finfo.Ext)):
            if ((Name == '') or (Name in finfo.NameExt)):
              if Content == '':
                Files.append(finfo)      # no txt criteria => all
              else:                                      # check for text match
                Infile = open(finfo.PathNameExt)
                for line in Infile:
                  if Content in line:
                    Files.append(finfo)
                    break
                Infile.close()
    return fols
  Folders = Search(Dir)
 
  def InfoSort(a, b):
    av = a.NameExt.lower()
    bv = b.NameExt.lower()
    if av < bv: return -1 
    else: return 1
  
  if len(Folders) > 0: Folders.sort(InfoSort)
  if len(Files) > 0: Files.sort(InfoSort)
  return Folders, Files

# -------------------------------------------------------------------- Directory
class Directory:
  Path = None                         # current Path
  Folders = None                      # sorted list of folder Infos
  Files = None                        # sorted list of file Infos
  Index = None                        # index to current file info
  Items = 0
  Size = 0
  Parent = None
  DW = None                           # Dialog Window
  SavePath = None                     # used in SelectDirFile
  SaveIndex = None                    #  ""
  def __init__(self, Parent):
    self.Parent = Parent              # for pop up dialog
    self.GetCWD()                     # get current working directory

  def GetSize(self):
    self.Items = 0
    self.Size = 0
    for f in self.Folders:
      self.Items += f.Items
      self.Size += f.Size
    for f in self.Files:
      self.Items += 1
      self.Size += f.Size

  def GetCWD(self):                     # get current working directory
    self.Path = os.getcwd()
    self.Index = None
    self.Folders, self.Files = SearchDir(self.Path,'Local','','','')
    self.GetSize()
    if len(self.Files) > 0: self.Index = 0

  def LocalFind(self, Name, Extension, Content):
    self.Path = os.getcwd()
    self.Index = 0
    if len(Extension) > 0: ext = '.' + Extension
    else: ext = ''
    self.Folders, self.Files = SearchDir(self.Path,'Local',Name,ext,Content)
    self.GetSize()

  def TreeFind(self, Name, Extension, Content):
    if (Name=='') and (Extension=='') and (Content==''): return
    self.Path = os.getcwd()
    self.Index = 0
    if len(Extension) > 0: ext = '.' + Extension
    else: ext = ''
    self.Folders, self.Files = SearchDir(self.Path,'Tree',Name,ext,Content)
    self.GetSize()

  def GetFile(self, index):
    self.File = None
    if (index >= 0) and (index < len(self.Files)):
      self.Index = index
      self.File = self.Files[self.Index]
    return self.File
    
  def NextFile(self):
    if len(self.Files) > 0:
      if self.Index == None: self.Index = 0
      else:
        self.Index += 1
        if self.Index >= len(self.Files): self.Index = 0
      return self.Index, self.GetFile(self.Index)
    else: return None, None
    
  def PrevFile(self):
    if len(self.Files) > 0:
      if self.Index == None: self.Index = 0
      else:
        self.Index -= 1
        if self.Index < 0: self.Index = len(self.Files) - 1
      return self.Index, self.GetFile(self.Index)
    else: return None, None

  def SetIndex(self, nam):
    self.Index = None
    if (self.Files != None) and (len(self.Files) > 0):
      i = 0
      while i < len(self.Files):
        fi = self.Files[i]
        if (nam == fi.PathNameExt) or (nam == fi.NameExt):
          self.Index = i
          i = len(self.Files)
        else: i += 1
      if self.Index < len(self.Files): return self.Index
      else: return None
    else: return None

  def InfoName(self):
    if self.Index == None: return ''
    else: return self.Files[self.Index].PathNameExt

  def InfoLine(self):
    msg = self.Path + '    '
    msg += str(len(self.Folders)) + ' folders    '
    msg += str(len(self.Files)) + ' files    '
    msg += str(self.Size) + ' bytes    '
    msg += str(self.Items) + ' items'
    return msg

  def SelectDirFile(self):                       # select Dir and File by dialog
    self.SavePath = self.Path                    # save current for cancel
    self.SaveIndex = self.Index
    self.DW = Toplevel(self.Parent)              # toplevel frame
    self.DW.transient(self.Parent)               # attach to parent
    self.DW.title('File Dialog')                 # title it
    
    CB = Mcore.Alabelframe(self.DW,TOP,X,0,FLAT,FALSE)  # frame for buttons
    Bup = Mcore.Abutton(CB,LEFT,'UP',self.UpDir)
    Find = Mcore.Abutton(CB,LEFT,' FIND ',self.FIND)
    Enter = Mcore.Abutton(CB,LEFT,' ENTER ',self.ENTER)
    Cancel = Mcore.Abutton(CB,LEFT,' CANCEL ',self.CANCEL)
    Mcore.Acanvas(self.DW,TOP,1,5,0,None)                 # space for looks
    MB = Mcore.Alabelframe(self.DW,TOP,X,0,FLAT,FALSE)                  # path
    self.MSG = Mcore.Alabel(MB,LEFT,'')
    Mcore.Acanvas(self.DW,TOP,1,5,0,None)                 # space for looks
    Bfolders = Mcore.Alabelframe(self.DW,TOP,BOTH,0,FLAT,FALSE)   # folders
    self.FOL = Mcore.Alistbox(Bfolders, LEFT, self.SelectFolder)  # folders list
    self.FOL.SetMaxHgt(20)
    Bfolders.Title('Folders')
    Mcore.Acanvas(self.DW,TOP,1,5,0,None)                   # space for looks
    Bfiles = Mcore.Alabelframe(self.DW,TOP,BOTH,0,FLAT,TRUE)           # files
    Bfiles.Title('Files')
    self.FIL = Mcore.Alistbox(Bfiles, LEFT, self.SelectFile)     # files list
    self.FIL.config(height=20)
   
    self.GetCWD()
    self.DisplayDirectory()
    
    self.DW.grab_set()                         # make it modal
    self.DW.wait_window()                      # wait for a response

  def DisplayMSG(self, txt):
    self.MSG.Set(txt)
      
  def DisplayFF(self, F, Flist):                # display folders or files
    Flist.Clear()                               # clear previous display
    namlen = 0
    for f in F: namlen = max(namlen, len(f.NameExt))
    for f in F:
      ff = Mcore.Sjust(f.NameExt, namlen, 'l')
      size = Mcore.Sjust(str(f.Size), 11, 'r')
      Flist.AddLine(ff+'  '+size+'  '+f.mtimeS)    # display entries
    if len(F) < Flist.MaxHgt: Flist.SetHeight(len(F))
    else: Flist.SetHeight(Flist.MaxHgt)
        
  def DisplayDirectory(self):
    self.DisplayMSG(self.Path)                  # parent folder path
    self.DisplayFF(self.Folders, self.FOL)      # display folders
    self.DisplayFF(self.Files, self.FIL)        # display files

  def UP(self):
    i = 0
    cnt = 0
    s = self.Path
    while i < len(s):
      if s[i] == '/': cnt += 1
      i += 1
    if cnt > 1:                  # do not access the root directory ('/')
      os.chdir('..')
      self.GetCWD()

  def DOWN(self, index):
    nam = self.Folders[index].NameExt
    os.chdir(os.path.join(os.getcwd(), nam))
    self.GetCWD()

  def UpDir(self, evnt):
    self.UP()
    self.DisplayDirectory()

  def SelectFolder(self, linum, line):
    if len(self.Folders) > linum:
      self.DOWN(linum)
      self.DisplayDirectory()

  def SelectFile(self, linum, line):     # file selection exits the dialog
    if (linum >= 0) and (linum < len(self.Files)):
      self.Index = linum
      self.DW.destroy()

  def FIND(self, evnt):
    EL = [[0,0],['','Name'],['','Extension'],['','Content']]  # entry list
    BL = ['Local Find', 'Tree Find', 'Cancel']                # button list
    LL = ['by Name      : if Name      is in the name',\
          'by Extension : if Extension == the extension',\
          'by Content   : if Content   is in the file']
    # stay in LEBdialog until questions answered
    titl = 'FIND FILES by Name/Extension/Content'
    Mcore.LEBdialog(self.Parent,EL,BL,LL,None,titl)
    button = EL[0][1]                # 'Local Find', 'Tree Find', 'Cancel'
    Name = EL[1][0]                  # name
    Extension = EL[2][0]             # extension
    Content = EL[3][0]               # content
    if button == 'Cancel': return []
    elif button == 'Local Find': self.LocalFind(Name, Extension, Content)
    elif button == 'Tree Find': self.TreeFind(Name, Extension, Content)

  def ENTER(self, evnt):             # used if only path selected, not a file
    self.GetCWD()
    self.Index = None
    self.DW.destroy()

  def CANCEL(self, evnt):
    if self.SavePath != self.Path: os.chdir(self.SavePath)
    self.GetCWD()
    self.Index = self.SaveIndex
    self.DW.destroy()

# ---------------------------------- Menu support - New, Open, Save, Save As
# NOTE:  this class interacts with a Data Base structure that must have
#        Altered, Clear, ReadIn, WriteOut methods
# NOTE:  the file name is in Dir.Files, at Dir.Index
class DBfileClass:
  QAB = None
  DB = None
  Dir = None

  def __init__(self, Parent, DB, Dir):
    self.QAB = Mcore.QABdialog(Parent)
    self.DB = DB
    self.Dir = Dir

    # SaveFileCommon is used by SaveFile and SaveAsFile
    # It returns NotAltered, Cancel, Discard, NoName, OK, WriteFailure
  def SaveFileCommon(self, Cmnd):
    if (Cmnd != 'SaveAs') and (not self.DB.Altered): return 'NotAltered'
    Bname = 'Save'
    if Cmnd == 'Ask':                    # DB altered, so ask if save
      Title = 'Save File Dialog'
      Qs = ['Current DataBase has been modified.', 'Save changes?']
      Bs = ['Save', 'Discard', 'Cancel']
      Bname, Answers = self.QAB.Dialog(Title , Qs, None, None, Bs, 1, 0)
    if (Bname == 'Save') or (Cmnd == 'SaveAs'):
      try: nam = self.Dir.Files[self.Dir.Index].PathNameExt
      except: nam = None
      if (self.Dir.Index == None) or Cmnd == 'SaveAs':       # must ask for name
        Title = 'Untitled File'
        Qs = ['File Name?']
        Anams = ['name']
        Avals = ['']
        Bs = ['Enter', 'Cancel']
        Bnam, Es = self.QAB.Dialog(Title, Qs, Anams, Avals, Bs, 1, 0)
        if Bnam == 'Cancel':  return 'Cancel'
        nam = Es[0]
      if nam in [None, '']: return 'NoName'
      MF = Mcore.DEM(self.QAB.Parent)
      MF.Display('Saving data to ' + nam)
      try:
        OutFile = open(nam, 'w')
        self.DB.WriteOut(OutFile)
        OutFile.close()
        self.Dir.GetCWD()
        self.Dir.SetIndex(nam)
        rtrn = 'OK'
      except: rtrn = 'WriteFailure'
      MF.Erase()
      return rtrn
    else: return Bname

  def SaveFile(self): return self.SaveFileCommon('DonotAsk')

  def SaveAsFile(self): return self.SaveFileCommon('SaveAs')

  def TryLoad(self):           # NoName, OK, ReadFailure
    if self.Dir.Index == None: return 'NoName'
    nam = self.Dir.Files[self.Dir.Index].PathNameExt
    MF = Mcore.DEM(self.QAB.Parent)
    MF.Display('Loading data from ' + nam)
    try:                                 # try getting data
      InFile = open(nam, 'r')
      DBrtrn = self.DB.ReadIn(InFile)           # ReadIn clears DB
      InFile.close()
      if DBrtrn: rtrn = 'OK'                          # if read successful
      else: rtrn =  'ReadFailure'                     # if read not successful
    except: rtrn = 'ReadFailure'
    MF.Erase()
    return rtrn

  def NewFile(self):
    rtrn = self.SaveFileCommon('Ask')
    if rtrn in ['Cancel', 'NoName', 'WriteFailure']: return rtrn
    self.DB.Clear()
    self.Dir.Index = None
    return 'OK'

    # returns  NotAltered, Cancel, Discard, NoName, OK, WriteFailure
  def OpenFile(self):
    rtrn = self.SaveFileCommon('Ask')
    if rtrn in ['Cancel', 'NoName', 'WriteFailure']: return rtrn
    self.Dir.SelectDirFile()
    return self.TryLoad()

# --------------------------------------------------------------------- Cryption

# Password: any string (preferably 5 or more characters)
#           This is used to initialize the cryption process.

class Cryption:
  Username = None                           # any string with meaning
  Password = None                           # any string
  RN = 0                                    # pseudo random number
  def __init__(self, Username, Password):
    self.Username = Username
    self.Password = Password
    self.Reset()

  def Reset(self):                                  # reset the generator
    s = 1
    for c in self.Password: s = s + s + s + ord(c)   # 3x + next keystroke
    self.RN = s

  def Crypt(self, txt):                     # same for encryption and decryption
    if self.Password == None: return(txt)   # default = no cryption
    else:                                   # the heart of encryption/decryption
      s = ''
      for c in txt:                         # the cryption process
        s += chr(xor(ord(c), (self.RN() & 127)))
        self.RN = self.RN + self.RN + self.RN + 769      # 3x + prime
      return s

  def UsernameOK(self, txt):
    if self.Username == None: return True
    else: return self.Username == self.Crypt(txt)
