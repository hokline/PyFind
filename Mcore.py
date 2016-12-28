#
# a core set of stuff for GUI programs
#

__file__    = "Mcore.py" 
__version__ = "Mcore  20120531"

# This module implements support functions for several modules/programs.

import time         # uses: strftime, localtime, time

from Tkinter import *

### import os           # uses sep, extsep, linesep, 
### pathsep = os.sep
### extsep = os.extsep
### linesep = os.linesep

zro = ('0',)
nums = ['0','1','2','3','4','5','6','7','8','9']
Tab     = chr(9)
Space   = ' '
Comma   = ','
NewLine = '\n'
DefaultSeparators = [Tab, Space, Comma, NewLine]

# fixed      courier, courier new
# variable   garamond, fixed, palatino, bookman, times, times new roman,
#            helvetica, arial, system,
# Font definition tuples.
Fixed12N  = ('fixed', 12, 'normal')
Cour12N   = ('courier', 12, 'normal')
Arial12N  = ('arial', 12, 'normal')
Times12N  = ('times', 12, 'normal')
LabelFont = ('courier', 12, 'bold')
ListFont  = ('courier', 11, 'bold')
    
# --------------------------------------------------------------------- FormatDH 
# DHrec = data record, a list of data fields
# FD = list of field defs = [[field #, 'WidthJustType'],   ]
# width = total width of display string, including spaces fore and aft
# just = 'l' = left, 'r' = right, 'c' = center)
# type = 'i', 'f', 'f1', 'f2', 'd'=time tuple, 'D'=FloatDate, 's'=string
# example: '6li' (integer left justified in space 6 characters wide)
#
def FormatDH(DHrec, FD, Data=True):
  "Format a Data or Heading record for printing."
  # FD = ((field #, (width,just,type)), (()), ...)
  s = ''                                   # init string
  for fdef in FD:                          # process the fields
    fnum = fdef[0]                         # field number of data in DHrec
    wjt = fdef[1]                          # parse format definition
    fwid = ''
    i = 0
    while wjt[i] in nums:                  # '0' - '9'
      fwid += wjt[i]
      i += 1
    if fwid == '': fwid = '0'
    fwid = int(fwid)                       #   width
    fjst = wjt[i]                          #   justification ('l','c','r')
    if Data: ftyp = wjt[i+1:]              #   type (i,f,f1,f2,d,D,s)
    else: ftyp = 's'                       #     force string for heading
    if len(DHrec) > fnum: d = DHrec[fnum]  # field data, default = string
    else: d = ''
    if d == None: d = ''
    if d == 'N/A': pass
    elif (ftyp == 'f') or (ftyp == 'f1') or (ftyp == 'f2'):
      try:
        f = float(d)                       # convert string/float to float
        if ftyp == 'f': d = '%.f' % f      # f > f., format back to string
        elif ftyp == 'f1': d = '%.1f' % f  # f1 > f.x
        elif ftyp == 'f2': d = '%.2f' % f  # f2 > f.xx
      except: d = ''
    elif ftyp == 'i':
      try: d = str(d)                  # i > integer
      except: d = ''
    elif ftyp == 'd':                  # if type = time tuple date,
      d = time.strftime('%x', d)       #   convert to string
    elif ftyp == 'D':                  # if type = float date,
      fd = FloatDate(d)
      d = fd.s                         #   convert float to string
    elif ftyp == 'b':                  # handle big numbers
      if type(d) == str or unicode:
        dlm = len(d) - 1
        dlc = d[dlm]
        if dlc == 'B':                   # if billions (eg 2.34B)
          f = 1000000000 * float(d[:dlm])
        elif dlc == 'M':                 # if millions (eg 22.6M)
          f = 1000000 * float(d[:dlm])
        else: f = float(d)
      else: f = float(d)               # else just big number
      if f < 10000: d = '%f' % f                    # number
      elif f < 10000000: d = '%.2fM' % (f/1000000)  # number as millions
      else: d = '%.2fB' % (f/1000000000)            # number as billions
    d = Sjust(d, fwid, fjst)           # justify in display area
    s = s + d
  return s 

# ------------------------------------------------------------------------ Sjust  
#   String justification within a display area 
def Sjust(s, w, j):
  " String justification within a display area"
  ls = s.lstrip()                       # strip spaces front and back
  ls = ls[0:w]                        # chop off right excess
  nl = 1
  nr = 1
  nt = w - len(ls)
  if nt > 0:
    if j == 'l': nr = nr + nt           # left justification
    elif j == 'r': nl = nl + nt         # right justification
    else:
      ntl = int(nt/2)                   # center justification
      nr = nr + nt - ntl
      nl = nl + ntl
  for i in range(0, nr): ls = ls + ' '
  for i in range(0, nl): ls = ' ' + ls
  return ls  

# ----------------------------------------------------------------------- CompAB
def CompAB(A, B):
  "Compare strings A and B, return -1, 0, +1"
  if A == B: return 0
  if A[0] == '.' and B[0] != '.': return 1
  elif A[0] != '.' and B[0] == '.': return -1
  else:
    au = A.upper()
    bu = B.upper()
    if au < bu: return -1
    else: return 1

# ---------------------------------------------------------------------- GetLine
def GetLine(cp, t):         # start at character position cp, end at newline
  i = cp
  s = ''
  if (len(t) > 0) and (type(t) == str or unicode) and (i < len(t)):
    lng = len(t)
    while (i < lng) and (t[i] != NewLine):
      s += t[i]
      i += 1
    if (i < lng) and (t[i] == NewLine): i += 1
  return (i, s)

# -------------------------------------------------------------------- Partition
def Partition(txt, separators=None):          # text to list
#  e.g., separators = [Tab, Space, Comma, NewLine]
  if separators == None: separators = DefaultSeparators
  p = []
  i = 0
  s = ''
  if len(separators) > 0:
    while i < len(txt):
      if txt[i] not in separators: s += txt[i]
      else:
        if len(s) > 0:
          p.append(s)
          s = ''
      i += 1
  else:
    while i < len(txt):
      c = txt[i]
      if (ord(c) <= 64) or (ord(c) >= 128):
        if len(s) > 0:
          p.append(s)
          s = ''
      else: s += c
      i += 1
  while (len(s) > 0) and (s[len(s)-1] == '\n'):
    s = s[:len(s)-1]                 # delete final end-of-line characters
  if len(s) > 0: p.append(s)
  return p
# ---------------------------------------------------------------- end Partition
 
# ------------------------------------------------------------------ NextInt 
def NextInt(st, i, lo, hi):
  "Parse string from i for next integer, check it against limits."
  s = '';  lng = len(st)
  while (i < lng) and (not st[i].isdigit()):
    i = i + 1                                # bypass non-digits
  while (i < lng) and (st[i].isdigit()):
    s = s + st[i];  i = i + 1                # get the digits
  if len(s) > 0: nn = int(s)                 # convert to integer
  else: nn = 0                               # None defaults to 0
  if (nn < lo) or (nn > hi): nn = -1         # -1 > outside limits
  return (i, nn)                             # return index and integer

# -------------------------------------------------------------------- FloatDate
# A date as floating point number = 10000 x year + 100 x month + day
#
class FloatDate:
  "A date as floating point number = 10000 x year + 100 x month + day"
  f = None;  s = None
  def __init__(self, fd=None):
    if fd == None: self.Today()
    elif type(fd) == type(1.0):
      self.f = fd
      self.SfromFlt(fd)
    elif (type(fd) == str or unicode) and (len(fd) > 0):
      self.FfromStr(fd)
      self.SfromFlt(self.f)
    else: self.Today()            # default = today's date 
    
  def FfromStr(self, st):
    "Set f and s by parsing a string date in format MM/DD/YY."
    i = 0;  s = st
    if s == None: s = ''
    (i,m) = NextInt(s,i,1,12)                    # get the month
    (i,d) = NextInt(s,i,1,31)                    # get the day
    (i,y) = NextInt(s,i,0,10000)                 # get the year
    if (m==-1) or (d==-1) or (y==-1): return -1  # -1 > error
    CY = int(time.localtime()[0])                # Y = current year
    if y <= (CY-2000): y = y + 2000              # convert 06 to 2006
    else:
      if y < 100: y = y + 1900                   # convert 95 to 1995
    Fmdy = float(d) + 100*float(m) + 10000*float(y)
    self.f = Fmdy
    
  def GetYMD(self, fd):
    "Float Date to (year, month, day) tuple."
    y = int(fd/10000)
    mf = fd - (y * 10000)
    m = int(mf/100)
    d = int(mf-(m*100))
    return (y, m, d)
    
  def SfromFlt(self, fd):
    "Set f and s by converting a Float Date."
    (y, m, d) = self.GetYMD(fd)
    self.s = str(m).zfill(2)+'-'+str(d).zfill(2)+'-'+str(y).zfill(2)

  def Today(self):
    self.FfromStr(time.strftime('%x', time.localtime()))
    self.SfromFlt(self.f)
    
  def FltIn(self, fd):
    self.f = fd
    self.SfromFlt(fd)
    
  def StrIn(self, st):
    self.FfromStr(st)
    self.SfromFlt(self.f)
    
  def DaysThisYear(self, m, d):
    Mdays = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30,\
             7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    dty = d
    if m > 1:
      for i in range(m-1): dty = dty + Mdays[i+1]
    return dty
    
  def DaysApart(self, fd):
    "Calculate number of days between self and another date."
    F1 = max(self.f, fd)                         # F1 = more recent date
    F2 = min(self.f, fd)
    (y1, m1, d1) = self.GetYMD(F1)
    (y2, m2, d2) = self.GetYMD(F2)
    dty1 = self.DaysThisYear(m1, d1)
    dty2 = self.DaysThisYear(m2, d2)
    if y1 == y2: return dty1 - dty2
    else: return dty1 + (365-dty2) + (365 * (y1 - y2 - 1))
# ---------------------------------------------------------------- end FloatDate
    
# ---------------------------------------------------------------------- Abutton
class Abutton(Button):
  def __init__(self, parent, sid, txt, retrn, BG=None):
    Button.__init__(self, parent)
    self.config(font=Fixed12N, text=txt, width=len(txt)-2)
    if BG != None: self.config(bg=BG)
    self.pack(anchor=NW, side=sid)
    self.bind('<ButtonRelease>', retrn)
    
  def Clear(self): self.config(text='')
  def Width(self, wid): self.config(width=wid)
  def Set(self, txt): self.config(text=txt, width=len(txt))
  def Get(self): return self.__getitem__('text')
    
# ---------------------------------------------------------------------- Acanvas
class Acanvas(Canvas):
  def __init__(self, parent, sid, wid, hgt, bd, retrn, BG=None):
    Canvas.__init__(self, parent)
    self.config(width=wid, height=hgt, bd=bd)
    self.pack(side=sid)
    if BG != None: self.config(bg=BG)
    if retrn != None: self.bind('<ButtonRelease>', retrn)
    
# ------------------------------------------------------------------------ Adrop  
class Adrop(Menubutton):
  def __init__(self, parent, Mname, buttons=None):
    Menubutton.__init__(self, parent, text=Mname, underline=0)
    self.pack(side=LEFT)
    self.DM = Menu(self)
    if buttons != None: self.SetDrops(buttons)

  def SetDrops(self, buttons):
      for LC in buttons:         # LC = [['name', routine], ...]
        self.DM.add_command(label=LC[0], command=LC[1], underline=0)
      self.config(menu=self.DM)

# ----------------------------------------------------------------------- Aentry
class Aentry(Entry):
  def __init__(self, parent, sid, txt, BG=None):
    Entry.__init__(self,parent)
    self.config(font=Fixed12N)
    if BG != None: self.config(bg=BG)
    if txt == None: self.insert(0,'')
    else: self.insert(0, txt)            # initial value
    self.pack(side=sid)
  def Clear(self):
    self.delete(0, END)
  def Width(self, wid): self.config(width=wid)
  def Set(self, txt):
    self.Clear()
    self.insert(0, txt)
  def ShowStar(self): self.config(show='*')

# ----------------------------------------------------------------------- Alabel  
class Alabel(Label):
  def __init__(self, parent, sid, txt, BG=None):
    Label.__init__(self, parent)
    self.config(bd=3, font=LabelFont, text=txt)
    if BG != None: self.config(bg=BG)
    self.pack(side=sid)

  def Clear(self): self.config(text='')
  def Width(self, wid): self.config(width=wid)
  def Set(self, txt): self.config(text=txt)
  def Get(self): return self.__getitem__('text')
  def BGcolor(self, color): self.config(bg=color)
  def FGcolor(self, color): self.config(FG=color)
    
# ------------------------------------------------------------------ Alabelframe 
class Alabelframe(LabelFrame):
  # Relief: FLAT, GROOVE, RAISED, RIDGE, SOLID, SUNKEN
  # Fill  : X, Y, BOTH, NONE(?)
  # Expand: TRUE, FALSE
  def __init__(self, parent, Side, Fill, Border, Relief, Expand, BG=None):
    LabelFrame.__init__(self, parent)
    self.config(relief=Relief, bd=Border)
    if BG != None: self.config(bg=BG)
    self.pack(side=Side, fill=Fill, expand=Expand)
    
  def Title(self, title):  self.config(text=title)
  def Clear(self):
    for s in self.slaves(): s.destroy()
# -------------------------------------------------------------- end Alabelframe 
     
# -------------------------------------------------------------------- Alistbox
class Alistbox(Listbox):
  LineSelectReturn = None
  AutoWidth = True                   # automatic width adjustment
  Width = 20
  Height = 1
  MaxWid = 120
  MaxHgt = 40                        # maximum lines to display
  Cursor = None
  def __init__(self, parent, Side, rtrn=None):
    Listbox.__init__(self, parent)
    self.config(bd=3, font=ListFont, width=self.Width, height=self.Height)
    self.pack(anchor=NW, fill=BOTH, side=Side, expand=TRUE)
#    self.bind('<<ListboxSelect>>', self.SelectLine)
    self.bind('<ButtonRelease-1>', self.SelectLine)
    sbar = Scrollbar(parent)
    sbar.config(command=self.yview)
    sbar.pack(side=RIGHT, fill=Y)
    self.config(yscrollcommand=sbar.set)
    if rtrn != None: self.SetReturn(rtrn)

  def SetMaxHgt(self, max): self.MaxHgt = max
  def Clear(self):                                   # clear list display
    self.delete(0,END)
    self.config(height=self.MaxHgt)
  def SetWidth(self, wid):
    self.Width = wid
    self.config(width=wid)    # set width
  def SetHeight(self, hgt):
    self.Height = hgt
    self.config(height=hgt)  # set height
  def AddLine(self,lin,where='end'):                 # add a line
    if (self.AutoWidth) and (len(lin) > self.Width):
      self.Width = min(self.MaxWid, len(lin)+1)
      self.config(width=self.Width)
    if self.Width == None: wid = 20
    else: wid = self.Width
    if len(lin) > wid: l = lin[:wid]
    else: l = lin
    if self.Height < self.MaxHgt:               # adjust lines displayed
      self.Height += 1
      self.config(height=self.Height)
    if where == 'end': self.insert(END, l)    # add line at the end (default)
    else: self.insert(0, l)                   # or add it at the beginning
  def SelectLine(self, evnt):
    (l,c) = self.GetCurrent()
    if self.LineSelectReturn != None:           # return line # and contents
      self.LineSelectReturn(l,c)
  def GetCurrent(self):                         # return line and contents
    sel = self.curselection()
    if sel == (): sel = ('0',)
    self.Cursor = sel
    linum = int(sel[0])
    return (linum, self.get(sel))
  def GetLine(self, lnum): return self.get((str(lnum),))
  def SetReturn(self, Ret): self.LineSelectReturn = Ret
  def ClearHighlight(self):
    if self.Cursor != None: self.select_clear(self.Cursor) # clear highlight
  def SetHighlight(self):
    if self.Cursor != None: self.select_set(self.Cursor)   # set highlight
  def SeeLine(self, Lnum):
    Cursor = self.Cursor
    self.ClearHighlight()
#    self.ML.activate(Lnum)   ???
    Cursor = (str(Lnum),)
    self.see(Cursor)
    self.select_set(Cursor)
#    self.ML.focus()   ???
    self.Cursor = Cursor
  def SetCursor(self, Lnum):
    self.ClearHighlight()
    self.Cursor = (str(Lnum),)
    self.see(self.Cursor)
    self.select_set(self.Cursor)
 
  def Sort(self):
    TL = list(self.get(0, END))
    TL.sort(key=str.lower)              # case insensitive
    self.Clear()
    # load listbox with sorted data
    for I in TL: self.insert(END, I)
# ----------------------------------------------------------------- end Alistbox
    
# ------------------------------------------------------------- Aradiobutton
# RV = Tkinter.IntVar() = a variable common to a set of radio buttons
#    = the number of the currently active radio button
# val = a number unique to each radio button
class Aradiobutton(Radiobutton):
  def __init__(self, parent, sid, txt, retrn, RV, val=27):
    Radiobutton.__init__(self, parent, text=txt, variable=RV, value=val)
    self.pack(anchor=NW, side=sid)
    self.bind('<ButtonRelease>', retrn)
    self.Nam = Alabel(parent, sid, '')
    
  def BGcolor(self, color): self.config(bg=color)
  def FGcolor(self, color): self.config(FG=color)

  def Set(self, nam, color):
    self.Nam.Set(nam)
    self.config(bg=color)
    
# ------------------------------------------------------------------------ Atext
# cursor stuff
# NOTE: index = 'line.char', e.g., '1.0' (before 1st char), END (after last)
#       the index lies before the character specified
#       .index(1.0) converts a number to a string, 1.0 to '1.0'
#       .index(CURRENT) = index nearest the mouse pointer
#       .index(END)     = index of first character of last line + 1
#       .index(INSERT)  = index of blinking cursor, where insertion occcurs

# KeyPad codes and names
# 79 KP_Home	87 KP_End	81  KP_Prior	89 KP_Next
# 80 KP_Up	88 KP_Down	83  KP_Left	85 KP_Right
# 91 KP_Delete	90 KP_Insert	106 KP_Divide	63  KP_Multiply
# 86 KP_Add	82 KP_Subtract  104 KP_Enter

# non-KeyPad codes and names
# 112 Prior	117 Next	110 Home	115 End
# 111 Up	116 Down	113 Left	114 Right
# 36  Return	22  BackSpace	119 Delete	118 Insert
# 65  Space	23  Tab		9   Escape	66  Caps_Lock


class Cursor:
  lin = None                        # line number as integer
  col = None                        # column number as integer
  hom = None                        # beginning of line as string
  def __init__(self, c):
    self.c = c                      # c = string in the form of 'line.column'
    idot = c.find('.')
    self.hom = c[:idot] + '.0'
    self.lin = int(c[:idot])        # extract and convert line number
    self.col = int(c[idot+1:])      # extract and convert column number

  def modify(self, linC, colC):     # line change, column change
    self.lin += linC
    self.col += colC
    self.c = str(self.lin) + '.' + str(self.col)
    return self.c

class Atext(Text):
  def __init__(self, parent, Side):
    Text.__init__(self, parent)
    self.config(relief=SUNKEN, bd=3, wrap=WORD)
    self.pack(side=LEFT, anchor=NW, expand=YES, fill=BOTH)
#    self.bind('<Button-1>', self.B1_Enter)           # testing
#    self.bind('<ButtonRelease-1>', self.B1_Leave)    # testing
#    self.bind('<KeyRelease>', self.KeyCheck)         # testing
    self.bind('<KP_End>', self.KP_End)                # KeyPad End
    self.bind('<KP_Delete>', self.KP_Del)             # KeyPad Del
    self.bind('<KP_Home>', self.KP_Home)              # KeyPad Home

    sbar = Scrollbar(parent)
    sbar.config(command=self.yview)
    sbar.pack(side=RIGHT, fill=Y)
    self.config(yscrollcommand=sbar.set)
    self.focus()

  def KeyCheck(self, evnt):  pass
#    print('char = ', evnt.char, '  keycode = ', evnt.keycode, '  keysym = ', evnt.keysym)

  def Modified(self):
    return self.edit_modified()

  def GetText(self):
    return self.get(1.0, END)

  def Clear(self):
    self.delete(1.0, END)

  def PutText(self, txt):
    self.Clear()
    self.insert(END, txt)

  def KP_End(self, evnt):
    icnow = self.index(INSERT)                # cursor 'line.char', '1.0' = SOL 
    icend = self.search('\n', icnow, END)     # get end of current line
    if icnow == icend:
      self.mark_set(INSERT, END)              # end of entire text
      self.see(END)                           # scroll to see it
    else: self.mark_set(INSERT, icend)        # set new cursor position

  def KP_Del(self, evnt):
    icnow = Cursor(self.index(INSERT))                 # current cursor
    icend = Cursor(self.search('\n', icnow.c, END))    # end of line cursor
    if icnow.c != icend.c:
      self.delete(icnow.c, icnow.modify(0, 1))
    else: self.delete(icnow.c, icnow.modify(1, -icnow.col))

  def KP_Home(self, evnt):
    icnow = Cursor(self.index(INSERT))         # current cursor
    ichom = Cursor(self.index(INSERT))
    ichom.modify(0, -icnow.col)        # beginning of line cursor
    if icnow.c != ichom.c:
      self.mark_set(INSERT, ichom.c)           # home of current line
    else:
      if icnow.lin > 1:
        self.mark_set(INSERT, '1.0')           # home of entire text
        self.see(INSERT)
# -------------------------------------------------------------------- end Atext

# -------------------------------------------------------------------- LEBdialog
class LEBdialog(Toplevel):       # List, Entries, and Buttons Dialog
  "List / Entries / Buttons Dialog"
  # dialog pops up over parent: has title, list, entries, buttons
  # title at top
  # LL = line list = [l1, l2,...], displayed in list box
  # EL = entry list = [[0,0], [value 1, name 1], ...]
  #      Note: EL[0][0] = number of entries per line, 0=all
  # Bl = button list = ['name 1', 'name 2', ...]
  #      Note 1: any button pressed returns its name in EL[0][1]
  #      Note 2: any button pressed returns entry values in EL[i][0]
  myParent = None
  mySelect = None
  EBL = None
  Ents = []
  Btns = []
  def __init__(self, parent, EL, BL, LL=None, LLselect=None, title=None):
    self.EL = EL
    Toplevel.__init__(self, parent)            # toplevel frame
    self.transient(parent)                     # attach to parent
    if title: self.title(title)                # title it
    self.myParent = parent                     # keep parent for return
    self.mySelect = LLselect
    
    if (LL != None) and len(LL) > 0:           # if display lines wanted
      LF = Alabelframe(self,TOP,BOTH,3,SUNKEN,TRUE)
      LB = Alistbox(LF, LEFT)                     # list box
      for i in LL: LB.AddLine(i)
      if self.mySelect != None: LB.SetReturn(self.mySelect)
    
    self.Ents = []
    lenEL = len(EL)
    ELleft = lenEL
    if EL[0][1] == 'Buttons': Entries = False
    else: Entries = True
    if lenEL > 1:                              # if entries wanted
      Epl = EL[0][0]                           # number of entries per line
      if Epl == 0: Epl = lenEL
      nf = (lenEL + Epl - 1) / Epl             # number of frames needed
      ELi = 1                                  # El index
      for j in range(nf):                      # for each line of entries
        FE = Alabelframe(self,TOP,X,1,SUNKEN,TRUE)   # frame for entries
             # (parent, Side, Fill, Border, Relief, Expand, BG=None)
        for k in range(Epl):
          if ELi < lenEL:              # label & initialize entries
            ELF = Alabelframe(FE,LEFT,X,1,FLAT,TRUE)
            if Entries:
              ELF.Title(EL[ELi][1])
              self.Ents.append(Aentry(ELF,LEFT,EL[ELi][0]))
                        # (self, parent, sid, txt, BG=None):
            else:
              b = Abutton(ELF,LEFT,EL[ELi], self.Exit)
              b.pack(side=LEFT, fill=X, expand=TRUE)
              self.Btns.append(b)
                    # (self, parent, sid, txt, retrn, BG=None)
            ELi += 1
    
    BF = Alabelframe(self,TOP,X,1,FLAT,TRUE)
    BF.config(pady=10)
    for B in BL:                           # label and set Buttons
      self.Btns.append(Abutton(BF,LEFT,B,self.Exit))
   
    try: self.grab_set()                      # make it modal
    except: pass
    if len(self.Ents) > 0:
      self.Ents[0].focus()                    # set the focus
    self.wait_window()                        # wait for a response

  def SetEntry(self, Enum, txt):
    self.Ents[Enum].insert(0,txt)
    
  def Exit(self, evnt):
    Btext = evnt.widget.__getitem__('text')   # which button?
    self.EL[0][1] = Btext                     # EL[0][1] = button name
    if len(self.Ents) > 0:
      for i in range(0, len(self.Ents)):      # for each entry i
        Value = self.Ents[i].get()              # get value
        self.EL[i+1][0] = Value                 # return in EL[i+1][0]
    self.myParent.focus_set()
    self.destroy()
# ---------------------------------------------------------------- end LEBdialog

# -------------------------------------------------------------------- QABdialog
# NOTE: setup QAB = QABdialog(RootWindow) in the main program
#       and pass it around to anything that needs a dialog.
#       If the RootWindow is needed, simply use QAB.Parent.

class QABdialog:              # Questions Answers Buttons dialog
  "Questions / Answers / Buttons Dialog"
  # dialog pops up over parent: has title, questions, answers, buttons
  # title at top
  # Answers = line list = [l1, l2,...], displayed in list box
  # Anames = list of answer names
  # Avalues = list of initial answer values
  # Bnames = list of button names
  # APL = answers per line, default = 1
  #   Note 1: any button pressed ends the dialog
  #   Note 2: return = (button name, list of values)
  Parent = None
  TLF = None                      # Top Level Frame
  LB = None                       # listbox for questions
  Anames = None
  Entries = None                  # name to value dictionary
  Bname = None                    # button name that ended the dialog
  Answers = None                  # values of the entries
  def __init__(self, Parent):
    self.Parent = Parent                       # parent frame
    self.TLF = None                            # toplevel frame

  def Active(self): return self.TLF != None

  def Dialog(self, Title, Questions, Anames, Avalues, Bnames, APL=1, foc=0):
    if Anames == []: self.Anames = None
    else: self.Anames = Anames
    FWdef = [\
      ['TLF', 'TL', self.Parent, LEFT, BOTH, YES, 3, RIDGE, '', '', Title],\
      ['QF',  'LF', 'TLF', TOP, BOTH, NO, 3, FLAT, '', '', ''],\
      ['AF',  'LF', 'TLF', TOP, BOTH, NO, 3, RIDGE, '','',''],\
      ['BF',  'LF', 'TLF', TOP, X, NO, 3, SUNKEN, '','','']]
    [self.TLF, self.QF, self.AF, self.BF] = FWsetup(FWdef)    # toplevel frames
    self.TLF.transient(self.Parent)                 #   as a temporary window
    self.TLF.title(Title)
      # do Questions first
    if (Questions != None) and len(Questions) > 0:     # if display lines wanted
      self.LB = Alistbox(self.QF, LEFT)                     # list box
      for i in Questions: self.LB.AddLine(i)
      # do Answers next
    self.Entries = {}
    if (Anames != None) and len(Anames) > 0:         # if answers wanted
      nf = (len(Anames) + APL - 1) / APL             # number of frames needed
      for Ai in range(len(Anames)):                  # answer index
        LF = Frame(self.AF)                          # frame for line of answers
        LF.pack(side=TOP, fill=X, expand=NO)         # pack it
        LAi = 0                                      # index for line
        while (Ai < len(Anames)) and (LAi < APL):
          FE = Alabelframe(LF,LEFT,X,1,SUNKEN,TRUE)   # frame for answer
          FE.Title(Anames[Ai])                        # name it
          self.Entries[Anames[Ai]] = Aentry(FE, LEFT, Avalues[Ai])   # answer
          Ai += 1
          LAi += 1
      self.Entries[Anames[foc]].focus()
      # now do the buttons
    for b in Bnames: Abutton(self.BF, LEFT, b, self.Exit)
    if (Anames != None) and (len(Anames) > 0):
      self.Entries[Anames[0]].focus()       # set the focus
    self.TLF.wait_window()                        # wait until TLF is destroyed
    return (self.Bname, self.Answers)

  def SetQuestionsReturn(self, Qreturn):
    if Qreturn != None: self.LB.SetReturn(Qreturn)

  def SetEntry(self, aname, txt):
    if self.Anames != None: self.Entries[aname].Set(txt)
    
  def Exit(self, evnt):
    self.Bname = evnt.widget.__getitem__('text')   # which button?
    self.Answers = []
    if (self.Anames != None) and (len(self.Anames) > 0):
      for nam in self.Anames:
        self.Answers.append(self.Entries[nam].get())
    self.Parent.focus_set()
    if self.TLF != None: self.TLF.destroy()
    self.TLF = None
    self.Anames = None
# ---------------------------------------------------------------- end QABdialog
  
# --------------------------------------------------------------------- QAdialog
DialogReturn = None   # return variable must be global to survive ".destroy()"

def QAdialog(Parent, Questions, EntryText, show=True):   # Q & A dialog
  global DialogReturn
  TL = Toplevel(Parent)
  TL.transient(Parent)
  DialogReturn = None
  inner = Alabelframe(TL, TOP, X, 3, SUNKEN, NO)
  wid = 30
  for Q in Questions:
    wid = max(wid, len(Q))
    x = Alabel(inner, TOP, Q)
    x.pack(anchor=W)
    x.config(width=wid)
  def Exit(evnt):
    global DialogReturn
    DialogReturn = evnt.widget.get()            # entry contents
    TL.destroy()
  SDC = Alabelframe(TL, TOP, X, 3, RAISED, NO)
  ent = Aentry(SDC,LEFT,EntryText)            # create a normal entry
  if not show: ent.ShowStar()                 # allow it to be a password entry
  ent.bind('<Return>', Exit)
  ent.focus()
  Parent.wait_window(TL)
  return DialogReturn

# --------------------------------------------------------------------- QBdialog
def QBdialog(Parent, Questions, Buttons):   # Questions and Buttons dialog
  global DialogReturn
  TL = Toplevel(Parent)
  TL.transient(Parent)
  DialogReturn = None
  inner = Alabelframe(TL, TOP, X, 3, SUNKEN, NO)
  wid = 30
  for Q in Questions:
    wid = max(wid, len(Q))
    x = Alabel(inner, TOP, Q)
    x.pack(anchor=W)
    x.config(width=wid)
  def Exit(evnt):
    global DialogReturn
    DialogReturn = evnt.widget.__getitem__('text')      # button name
    TL.destroy()
  SDC = Alabelframe(TL, TOP, X, 3, RAISED, NO)
  for B in Buttons: Abutton(SDC,LEFT,B,Exit)            # create the Buttons
  Parent.wait_window(TL)
  return DialogReturn                                   # return button name
# ----------------------------------------------------------- end Simple Dialogs

# --------------------------------------------------------------------- Messages
class DEM:                            # display now, erase later
  def __init__(self, Parent):
    self.Parent = Parent

  def Display(self, msg):
    self.TL = Toplevel(self.Parent)
    self.TL.transient(self.Parent)
    inner = Alabelframe(self.TL, TOP, X, 3, SUNKEN, NO)
    wid = max(len(msg), 30)
    dm = Alabel(inner, TOP, msg)
    dm.config(width=wid)
    dm.update()                     # needed to see dm message
    xtra = Alabel(inner, TOP, '')   # needed to see dm message
    xtra.update()                   # needed to see dm message

  def Erase(self): self.TL.destroy() 

def Tmsg(Parent, Time, msg):        # Timed Message
  M = DEM(Parent)                   # display the message
  M.Display(msg)
#  TL = Toplevel(Parent)
#  TL.transient(Parent)
#  inner = Alabelframe(TL, TOP, X, 3, SUNKEN, NO)
#  dm = Alabel(inner, TOP, msg)
#  dm.update()
  time.sleep(Time)                  # wait 'Time' seconds
#  TL.destroy()
  M.Erase()                         # erase the message

# -------------------------------------------------------------- Framework setup
# 
# enter with a list of Widget definitions:
#   [widget name, type, parent name, side, fill, expand,
#                border, relief, bg, font, text]
# types: 'Tk' Tk, 'TL' Toplevel, 'LF' Labelframe, 'L' Label,
#        'LB' Listbox, 'E' Entry, 'T' Text
def FWsetup(WL):
  PD = {}
  rtrn = []
  i = 0
  while i < len(WL):
    d = WL[i]
    if d[2] in PD.keys(): parent = PD[d[2]]
    if d[1] == 'Tk':  F = Tk()                         # Tk frame
    elif d[1] == 'TL': F = Toplevel(d[2])              # Toplevel frame
    elif d[1] == 'F': F = Frame(parent)                # frame
    elif d[1] == 'LF': F = Alabelframe(parent,d[3],d[4],d[6],d[7],d[5])
    elif d[1] == 'L':  F = Alabel(parent,d[3],d[10])   # label
    elif d[1] == 'LB': F = Alistbox(parent, d[3])      # list box
    elif d[1] == 'E': F = Aentry(parent, d[3], d[10])  # entry
    elif d[1] == 'T': F = Atext(parent, d[3])          # text
    if d[1] not in ['Tk', 'TL']:                             # Configure & Pack
      if type(d[6]) == int: F.config(bd=d[6])    # border width
      if d[7] != None: F.config(relief=d[7])     # relief
      if len(d[8]) > 0: F.config(bg=d[8])        # background color
      if len(d[9]) > 0: F.config(font=d[9])      # font
      F.pack(side=d[3], fill=d[4], expand=d[5])  # pack it
    if len(d[10]) > 0:                           # text
      if d[1] in ['Tk']: F.title(d[10])
      elif d[1] in ['LF', 'L']: F.config(text=d[10])
      elif d[1] == 'E': F.insert(END, d[10])
      elif d[1] == 'LF': F.Title(d[10])
    nam = d[0]
    PD[nam] = F                              # { name:frame-instance }
    rtrn.append(F)
    i += 1
  return rtrn

def SetDrop(Fdrop, name, Drop):
  DF = Adrop(Fdrop, name)
  DF.config(font=Fixed12N)
  DF.SetDrops(Drop)
  DF.DM.config(font=Fixed12N)
# ---------------------------------------------------------- end Framework setup


# ------------------------------------------------------------------- TimerClass
# 
class TimerClass:
  Times = None
  def __init__(self):
    self.Times = {}
    
  def Clear(self):
    self.Times = {}
  
  def Start(self, Name):
    TimeNow = time.time()
    if Name in self.Times.keys(): self.Times[Name][0] = TimeNow
    else: self.Times[Name] = [TimeNow, 0]

  def Pause(self, Name):
    TimeNow = time.time()
    if Name in self.Times.keys():
      delta = TimeNow - self.Times[Name][0]
      self.Times[Name][1] += delta

  def Resume(self, Name):
    TimeNow = time.time()
    if Name in self.Times.keys(): self.Times[Name][0] = TimeNow

  def Print(self, Name):
    print(Name + '  %.4f' % self.Times[Name][1])

  def PrintAll(self):
    for nam in self.Times.keys(): self.Print(nam)

Timer = TimerClass()                         # a timer instance

# ------------------------------------------------------ List of Lists Functions
#
SortField = 0
def SortOnField(List, Field, Up):          # sort on a field in a list of lists
  global SortField
  SortField = Field
  if Up: List.sort(CompUp)          # use CompUp to sort instead of default
  else:  List.sort(CompDown)

def CompUp(a, b):
  global SortField
  av = a[SortField]           # assume text field
  bv = b[SortField]
  try:                             # check if numeric field
    av = float(av)
    bv = float(bv)
  except: pass
  if av < bv: return -1 
  else: return 1
   
def CompDown(a, b):
  global SortField
  av = a[SortField]           # assume text field
  bv = b[SortField]
  try:                             # check if numeric field
    av = float(av)
    bv = float(bv)
  except: pass
  if av > bv: return -1 
  else: return 1


def Ifirst(List, Field, Value):     # first index of value in field
  i = 0
  while (i < len(List)) and (List[i][Field] != Value): i += 1
  if i >= len(List): i = -1
  return i

