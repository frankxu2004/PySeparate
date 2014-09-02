# -*- coding:utf-8 -*-
#core algorithm import
import string
import re
import codecs
import time
import os
import threading
import winsound
#gui import
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import BooleanVar, IntVar
from tkinter import simpledialog, messagebox
#web crawler import
import urllib
import http.cookiejar
import socket
import urllib.request
import urllib.parse

#background music threads
class MusicThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global Playing
        Playing = True
        while 1:
            winsound.PlaySound('music.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
            for i in range(160):
                if root.music.get():
                    winsound.PlaySound(None,winsound.SND_FILENAME)
                    Playing = False
                    return
                time.sleep(1)

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global Exited
        global Playing
        while 1:
            if (not Exited) and (not Playing) and (root.music.get()==False):
                music_thread = MusicThread()
                music_thread.start()
            if Exited:
                return
            time.sleep(1)


#core separation algorithms functions
def check(s):
     if s[len(s)-4:len(s)]==".htm" or s[len(s)-5:len(s)]==".html" or s[len(s)-6:len(s)]==".shtml" or s[len(s)-4:len(s)]==".com" or s[len(s)-4:len(s)]==".org" or s[len(s)-4:len(s)]==".net" or s[len(s)-3:len(s)]==".cn":
          return 1
     else:
          for i in range(len(s)-1,len(s)-5,-1):
               if s[i]==".":
                    return 0
     return 1

def findwords(address):
    global recall
    global numweb
    global counter
    newdata=[]
    try:
        socket.setdefaulttimeout(recall)
        mypocket=urllib.request.urlopen(address)
        mypocket=mypocket.read()
        try:
            mypocket=mypocket.decode('utf-8')
        except:
            mypocket=mypocket.decode('gb18030', 'ignore')
        data=str(mypocket)
        newdata=""
        for i in data:
            if i not in punc + nl +"\n"+"\r"+"\t":
                newdata+=i
            else:
                newdata += " "
        newdata=newdata.split()
        numweb+=1
    except:
        pass
    return(newdata)

def checkname(arr,length):
    global ppl
    global name
    global dic
    result = [""]*1000
    j = 0
    i = 0
    while i < length:
        if (i<length-1) and ((i==0) or ((len(arr[i-1])>0) and (not arr[i-1][-1] in useless3))) and (arr[i] in ppl) and (not arr[i] in dicorigin) and (not arr[i] in name) and (len(arr[i])==2) and (arr[i][0] in family) and (not arr[i+1] in useless) and (len(arr[i+1])==1) and (rate.get(arr[i+1],1)<rate["的"]/500):
            result[j] = arr[i]+arr[i+1]
            i += 2
        elif (i<length-2) and ((i==0) or ((len(arr[i-1])>0) and (not arr[i-1][-1] in useless3))) and (arr[i] in family) and (not arr[i+1] in useless2) and (not arr[i+2] in useless) and (len(arr[i+1])==1) and (len(arr[i+2])==1) and (rate.get(arr[i+1],1)<rate["的"]/500) and (rate.get(arr[i+2],1)<rate["的"]/500):
            result[j] = arr[i]+arr[i+1]+arr[i+2]
            i += 3
        elif (i<length-1) and ((i==0) or ((len(arr[i-1])>0) and (not arr[i-1][-1] in useless3))) and (arr[i] in family) and  (not arr[i+1] in useless2) and (len(arr[i+1])==1) and (rate.get(arr[i+1],1)<rate["的"]/500):
            result[j] = arr[i]+arr[i+1]
            i += 2
        else:
            result[j] = arr[i]
            i += 1
        j += 1
    return (result,j)

def separate(st,n,ct):
    global minp
    global maxc
    global sep
    global sep2
    if (n <= minp) or (minp == 0):
        if st == "":
            if (n < minp) or (minp == 0):
                minp = n
                for i in range(n):
                    sep2[i] = sep[i]
                maxc = ct
            if (n == minp) and (ct > maxc):
                maxc = ct
                for i in range(n):
                    sep2[i] = sep[i]
        else:
            for i in range(7,0,-1):
                if len(st)>=i:
                    if (i == 1) or (st[:i] in dic) or ((i == 4) and ((st[0] == st[1])and(st[2] == st[3])and(st[1]+st[2] in dic))) or ((i == 3) and ((st[0] == "一")and(st[1] == st[2])and(st[0]+st[1] in dic))):
                        sep[n] = st[:i]
                        separate(st[i:],n+1,ct*rate.get(sep[n],1))

def halfsentence(st):
    global minp
    global maxc
    global sep2
    if len(st)>=25:
        bestp = 0
        bestc = 0
        sep3 = [""]*1000
        sep4 = [""]*1000
        sep5 = [""]*1000
        for j in range(-3,4,1):
            minp = 0
            maxc = 0
            sep5 = halfsentence(st[:len(st)//2-j])
            for k in range(minp):
                sep3[k] = sep5[k]
            ptot = minp
            ctot = maxc
            minp = 0
            maxc = 0
            sep5 = halfsentence(st[len(st)//2-j:])
            for k in range(minp):
                sep3[ptot+k] = sep5[k]
            ptot += minp
            ctot *= maxc
            if (ptot<bestp) or (bestp==0):
                bestp = ptot
                bestc = ctot
                for k in range(ptot):
                    sep4[k] = sep3[k]
            elif (ptot==bestp) and (ctot>bestc):
                bestc = ctot
                for k in range(ptot):
                    sep4[k] = sep3[k]
        minp = bestp
        return sep4
    else:
        separate(st,0,1)
        return sep2

def highFreq():
    global lst
    global name
    n = len(t)//2000
    psg = []
    for i in range(n-1):
        psg.append(t[i*2000:(i+1)*2000])
    psg.append(t[(n-1)*2000:])
    name = {}
    lst = []
    if n > 0:
        for h in range(n):
            new = {}
            for i in range(2,5,1):
                for j in range(len(psg[h])-i+1):
                    flag = 1
                    for k in range(j,j+i):
                        if psg[h][k] in punc+nl+"\n"+"\t"+"的"+"了":
                            flag = 0
                            break
                    if flag:
                        for k in range(2,i+1):
                            for l in range(j,j+i-k+1):
                                if (psg[h][l:l+k] in dic) and ((rate.get(psg[h][l:l+k],1)>rate["的"]/10000) or k==i):
                                    flag = 0
                                    break
                    if flag:
                        new[psg[h][j:j+i]] = new.get(psg[h][j:j+i],0) + 1
            for i in new:
                if new[i]/len(psg[h]) > 0.005:
                    name[i] = name.get(i,0)
    highfreq = open("highfreq.txt","w")
    for i in name:
        lst.append(i)
        highfreq.write(str(len(lst))+". "+i+"\n")
    highfreq.close()

#web crawler functions
def yuming(s):
     ym=""
     dot=0
     for i in range(len(s)):
          if dot==2:
               if s[i]!="/":
                    ym+=s[i]
               else:
                    break
          if dot==1:
               if s[i]!=".":
                    ym+=s[i]
               else:
                    dot=2
          if (dot==0)and(s[i]=="."):
               dot=1
     return ym

def net_spider(address):
    global repe
    global recall
    global web
    y=[]
    try:
        socket.setdefaulttimeout(recall)
        mypocket=urllib.request.urlopen(address)
        mypocket=mypocket.read()
        try:
            mypocket=mypocket.decode('utf-8')
        except:
            mypocket=mypocket.decode('gb18030','ignore')
        data=str(mypocket)
        data=data.split('href="')
        newaddress=[]
        for i in range(1,len(data)):
            if data[i][0:7]=="http://":
                for x in range(0,len(data[i])):
                    if (data[i][x-5:x]==".html")or(data[i][x]=='"'):
                        a=data[i][0:x]
                        newaddress.append(a)
                        break
            elif data[i][0]=="/":
                for x in range(0,len(data[i])):
                    if (data[i][x-5:x]==".html")or(data[i][x]=='"'):
                         a=address+data[i][0:x]
                         newaddress.append(a)
                         break
        newaddress1=[]
        if root.crawl.get()==False:
             for i in newaddress:
                  if check(i):
                       newaddress1.append(i)
        else:
             for i in newaddress:
                  if check(i) and yuming(i)==web:
                       newaddress1.append(i)
        y=[]
        for i in newaddress1:
            try:
                socket.setdefaulttimeout(recall)
                response=urllib.request.urlopen(i)
                if repe.get(i,0)==0:
                    repe[i]=repe.get(i,1)
                    y.append(i)
                    yy=findwords(i)
                    f=open('storage_new.txt','a')
                    for j in range(len(yy)):
                        if len(yy[j])>1:
                             for k in range(len(yy[j])):
                                  f.write((yy[j][k]).encode('utf-8').decode('utf-8','ignore'))
                             f.write(" ".encode('utf-8').decode('utf-8','ignore'))
                    f.close()
            except:
                pass
    except:
        pass
    return(y)

def webCrawler():
    global recall
    global repe
    global numweb
    global websites
    global address
    global counter
    global web
    global root4
    address = [simpledialog.askstring("Web Crawler","Please input the Website:")]
    number = simpledialog.askinteger("Web Crawler","Please input depth:")
    recall = simpledialog.askfloat("Web Crawler","Please input the max time to try:")
    try:
         web=yuming(address[0])
    except:
         pass
    websites=address
    repe={}
    numweb = 0
    def closeWindow3():
        root4.destroy()
    def startButton():
        global websites
        global address
        try:
             for i in range(0,number):
                 y=[]
                 for x in websites:
                     y+=net_spider(x)
                 websites=y
                 address+=y
        except:
             pass
        counter.config(state=NORMAL)
        counter.delete(0.0, END)
        counter.insert(0.0,numweb)
        counter.config(state=DISABLED)
        b0.config(state=NORMAL)
        b.config(state=DISABLED)
    root4=Tk()
    root4.title("Web Crawler")
    root4.configure(height=100,width=250)
    root4.resizable(width=NO,height=NO)
    root4.iconbitmap('icon.ico')
    counter=Text(root4,height=1,width=8)
    counter.place(x=10,y=13)
    counter.config(state=NORMAL)
    counter.delete(0.0, END)
    counter.insert(0.0,"0")
    counter.config(state=DISABLED)
    l0=Label(root4,text = ' websites have been added.')
    l0.place(x=70,y=10)
    b=Button(root4,command = startButton,text="Start",width=6)
    b.place(x=45,y=50)
    b0=Button(root4,command = closeWindow3,text="Close",width=6)
    b0.place(x=145,y=50)
    b0.config(state=DISABLED)

#data initialization
f = open("familyname.txt","rt")
d = f.read().split("\n")
f.close()
family = {}
for i in range(len(d)):
    family[d[i]] = family.get(d[i],0)
punc = "。，“”：；‘’？/+=~（）！·#￥%……—*、|{}[]《》〈〉 　．，＂：；｀～｛｝［］！＠＃＄％︿＆＊－＿＋＝＇？／＼｜＜＞【】"+string.punctuation
nl = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９"
useless = "二三四五六七八九十去忙要会自在和得带常乱跑跳走想爱哭看瞄观赏瞥见听说唱骂讲读触摸站有打设出住虽伸侧戴耳票猜到傻咬略啊呀呢吗哇嘞哈吧咔啦哦嗷噢唉了你我他她它"
useless2 = "去忙要会在和得带乱跑跳走哭看瞄瞥说唱骂讲读触摸站有打设出住虽侧票猜到傻咬略啊呀呢吗哇嘞哈吧咔啦哦嗷噢唉了你我他她它"
useless3 = "一二两三四五六七八九十"

#gui functions
def center_window(w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def splashScreen():
    def center_window(w, h):
        # get screen width and height
        ws = splash.winfo_screenwidth()
        hs = splash.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        splash.geometry('%dx%d+%d+%d' % (w, h, x, y))
    splash = Tk()
    center_window(500, 300)
    splash.overrideredirect(1)
    s=Canvas(splash,width=500,height=300)
    s.pack()
    im = PhotoImage(file='img.gif')
    s.create_image(250,150,image = im)
    s.create_text(250,150,text="Welcome to Anfield!",font=("Times", "30", "bold italic"))
    splash.after(2000,splash.destroy)
    splash.mainloop()

#confirm button
def confirmButton():
    global t
    global dic
    global rate
    global dicorigin
    global slc
    global name
    global ppl
    global lst
    global sepvalue
    global reseted
    global l5
    global l6
    global root2
    def addHighFreq1():
        try:
             inputwordnumber = int(entry1.get())
             dic[lst[inputwordnumber-1]] = dic.get(lst[inputwordnumber-1],0)
             name[lst[inputwordnumber-1]] = name.get(lst[inputwordnumber-1],0)
             rate[lst[inputwordnumber-1]] = rate.get(lst[inputwordnumber-1],round(rate["的"]/500))
        except:
             pass
        entry1.delete(0,END)
    def closeWindow1():
        global both
        try:
             root2.destroy()
        except:
             pass
        b5.config(state=NORMAL)
        b6.config(state=NORMAL)
        b7.config(state=NORMAL)
        if both == True:
             showBoth()
             both = False
    if reseted == True:
         b5.config(state=NORMAL)
    reseted = False
    name = {}
    try:
         l5.destroy()
         l6.destroy()
    except:
         pass
    if root.sepSentence.get() == True:
         l5=Label(root,text = """  Sep By Sentences:
  ENABLED""")
    else:
         l5=Label(root,text = """  Sep By Sentences:
  DISABLED""")
    l5.place(x=665,y=185)
    if root.highFreq.get() == True:
         l6=Label(root,text = """Detect H-freq Words:
ENABLED""")
    else:
         l6=Label(root,text = """Detect H-freq Words:
DISABLED""")
    l6.place(x=665,y=260)
    t=t1.get(0.0,END)
    f = open("ratio_word.txt","rt")
    s = f.read()
    f.close()
    d = s.split("\n")
    rate = {}
    for i in range(len(d)-1):
        w = d[i].split()
        rate[w[0]] = rate.get(w[0],0)+int(w[1])
    f = open("comb.txt","rt")
    s = f.read()
    f.close()
    d = s.split("\n")
    dic = {}
    for i in range(len(d)-1):
        dic[d[i]] = dic.get(d[i],0)
    dicorigin = {}
    for i in dic:
        dicorigin[i] = dicorigin.get(i,0)
    f = open("namelist.txt","rt")
    d = f.read()
    d = d.split("\n")
    f.close()
    ppl = {}
    for i in range(len(d)-1):
        ppl[d[i]] = ppl.get(d[i],0)
    if root.sepSentence.get()==True:
        s = ""
        sepvalue = True
        for i in range(len(t)):
            if t[i] in "\n"+"\t"+"　":
                s = s + " "
            else:
                s = s + t[i]
        a = re.split("([ 。，：；？！…]+)",s)
        f = open("slice.txt","w")
        j = 1
        for i in range(len(a)):
            if a[i] != "":
                flag = 0
                for k in range(len(a[i])):
                    if a[i][k] in " 。，：；？！…":
                        flag = 1
                        break
                if flag:
                    for k in range(len(a[i])):
                        if a[i][k] in "。，：；？！…":
                            f.write(a[i][k])
                    f.write("\n")
                else:
                    f.write(str(j)+". "+a[i])
                    j += 1
        f.close()
        f = open("slice.txt","rt")
        s = f.read()
        f.close()
        os.remove("slice.txt")
        slc = s.split("\n")
        del slc[len(slc)-1:len(slc)]
        slc2 = []
        for i in range(len(slc)):
            if slc[i] != "":
                slc2.append(slc[i])
        slc = slc2
        s = "\n".join(slc)
        t2.config(state=NORMAL)
        t2.delete(0.0, END)
        t2.insert(0.0,s)
        t2.config(state=DISABLED)
    else:
        sepvalue = False
        t2.config(state=NORMAL)
        t2.delete(0.0, END)
        t2.config(state=DISABLED)
    if root.highFreq.get()==True:
        highFreq()
        highfreq = open("highfreq.txt","rt")
        highfreqtext = highfreq.read()
        highfreq.close()
        os.remove("highfreq.txt")
        if highfreqtext != "":
            b5.config(state=DISABLED)
            b6.config(state=DISABLED)
            b7.config(state=DISABLED)
            root2=Tk()
            root2.title("Confirmation")
            root2.configure(height=250,width=500)
            root2.resizable(width=NO,height=NO)
            root2.iconbitmap('icon.ico')
            text1=ScrolledText(root2,height=10,width=65)
            text1.place(x=10,y=25)
            text1.delete(0.0,END)
            text1.insert(0.0,highfreqtext)
            text1.config(state=DISABLED)
            label1=Label(root2,text="High Frequency Words Detected:")
            label1.place(x=10,y=1)
            label2=Label(root2,text='''Enter the the number of high frequency words to add:''')
            label2.place(x=10,y=160)
            entry1=Entry(root2)
            entry1.place(x=10,y=190)
            buttonAdd=Button(root2,text="Add",command=addHighFreq1)
            buttonAdd.place(x=180,y=180)
            buttonOK=Button(root2,text="Finish",command=closeWindow1)
            buttonOK.place(x=350,y=180)
            def callback(event=None): pass
            root2.protocol('WM_DELETE_WINDOW', callback)
    for i in ppl:
         dic[i] = dic.get(i,0)
    if (root.highFreq.get()==True)and(highfreqtext == ""):
         closeWindow1()

def copyRight():
    global root6
    root6=Tk()
    root6.title("Warning")
    root6.iconbitmap('icon.ico')
    label = Label(root6,text = '''Copyright ownership belongs to team Anfield.
    It shall not be reproduced ,copied, or used in other ways without permission,
    otherwise Anfield will have the right to pursue relative responsibilities.''')
    label.pack()
    root6.resizable(width=NO, height=NO)

def instruction():
    global root5
    root5 = Tk()
    root5.title('Instructions')
    root5.configure(height=500,width=800)
    root5.resizable(width=NO, height=NO)
    root5.iconbitmap('icon.ico')
    center_window(800,500)
    Ins=ScrolledText(root5,height=37,width=110)
    Ins.place(x=5,y=5)
    f = open("readme_eng.txt")
    Ins.config(state=NORMAL)
    Ins.delete(0.0, END)
    Ins.insert(0.0,f.read())
    f.close()
    Ins.config(state=DISABLED)
    def callback(event=None):
        if messagebox.askokcancel("Instructions","Do you get it?"):
            root5.destroy()
    root5.protocol('WM_DELETE_WINDOW', callback)

#add/remove word to/from dictionary
def AddWord():
    wordAdd = simpledialog.askstring("Add a word","Word to add to the dictionary:")
    try:
         f = open("comb.txt","a")
         f.write(wordAdd+"\n")
         f.close()
    except:
         pass

def RemoveWord():
    wordRemove = simpledialog.askstring("Remove a word","Word to remove from the dictionary:")
    try:
         if len(wordRemove)==1 and (not wordRemove in punc+nl+"\n"+"\t"):
              error = messagebox.showinfo("Oops!","Please don't remove single Chinese character from the dictionary!")
              return
         f = open("comb.txt","rt")
         a = f.read().split("\n")
         f.close()
         f = open("comb.txt","w")
         for i in range(len(a)-1):
             if a[i] != wordRemove:
                 f.write(a[i]+"\n")
         f.close()
    except:
         pass

#separate by sentences
def separateSentence(Content,Textbox):
    global sep
    global sep2
    global sep3
    global sep4
    global sep5
    global minp
    global maxc
    global rate
    global dic
    global l7
    i = 0
    tot = punc+nl+"\n"+"\t"
    sttime = time.clock()
    if root.algorithm.get() == 1:
        sep = [""]*1000
        sep2 = [""]*1000
        f = open("separate.txt","w")
        while 1:
            s = ""
            while (i<len(Content)) and (not(Content[i] in tot)):
                s += Content[i]
                i += 1
            minp = 0
            maxc = 0
            if s != "":
                sep2 = halfsentence(s)
                (sep2,minp) = checkname(sep2,minp)
                for j in range(minp-1):
                    f.write(sep2[j]+"|")
                if i<len(Content):
                    if Content[i] in nl:
                        f.write(sep2[minp-1]+"|")
                    else:
                        f.write(sep2[minp-1])
                else:
                    f.write(sep2[minp-1])
            if (i<len(Content)) and (Content[i] in tot):
                if i+1<len(Content):
                    if (Content[i] in punc+"\n"+"\t") or (Content[i+1] in punc+"\n"+"\t") or ((Content[i] in nl)and(Content[i+1] in nl)):
                        f.write(Content[i])
                    else:
                        f.write(Content[i]+"|")
                else:
                    f.write(Content[i])
                i += 1
            if i>=len(Content):
                f.close()
                f = open("separate.txt","rt")
                s = f.read()
                f.close()
                os.remove("separate.txt")
                Textbox.config(state=NORMAL)
                Textbox.delete(0.0, END)
                Textbox.insert(0.0,s)
                Textbox.config(state=DISABLED)
                break
    else:
        f = open("separate.txt","w")
        while 1:
            sep = [""]*1000
            sep2 = [0]*1000
            sep3 = [1]*1000
            sep4 = [0]*1000
            sep5 = [""]*1000
            s = ""
            while (i<len(Content)) and (not(Content[i] in tot)):
                s += Content[i]
                i += 1
            if s != "":
                for j in range(1,len(s)+1):
                    for k in range(1,8):
                        if j >= k:
                            if (k == 1) or (s[j-k:j] in dic) or ((k == 4) and ((s[j-k] == s[j-k+1])and(s[j-k+2] == s[j-k+3])and(s[j-k+1]+s[j-k+2] in dic))) or ((k == 3) and ((s[j-k] == "一")and(s[j-k+1] == s[j-k+2])and(s[j-k]+s[j-k+1] in dic))):
                                if ((sep2[j-k]+1<sep2[j])or(sep2[j] == 0))or((sep2[j-k]+1==sep2[j])and(sep3[j-k]*rate.get(s[j-k:j],1)>sep3[j])):
                                    sep[j] = s[j-k:j]
                                    sep2[j] = sep2[j-k]+1
                                    sep3[j] = sep3[j-k]*rate.get(s[j-k:j],1)
                                    sep4[j] = j-k
                k = 0
                while j>0:
                    sep5[k] = sep[j]
                    k += 1
                    j = sep4[j]
                for j in range(k-1,-1,-1):
                    sep[k-1-j] = sep5[j]
                sep5 = sep
                (sep5,k) = checkname(sep5,k)
                for j in range(k-1):
                    f.write(sep5[j]+"|")
                if i<len(Content):
                    if Content[i] in nl:
                        f.write(sep5[k-1]+"|")
                    else:
                        f.write(sep5[k-1])
                else:
                    f.write(sep5[k-1])
            if (i<len(Content)) and (Content[i] in tot):
                if i+1<len(Content):
                    if (Content[i] in punc+"\n"+"\t") or (Content[i+1] in punc+"\n"+"\t") or ((Content[i] in nl)and(Content[i+1] in nl)):
                        f.write(Content[i])
                    else:
                        f.write(Content[i]+"|")
                else:
                    f.write(Content[i])
                i += 1
            if i>=len(Content):
                f.close()
                f = open("separate.txt","rt")
                s = f.read()
                f.close()
                os.remove("separate.txt")
                Textbox.config(state=NORMAL)
                Textbox.delete(0.0, END)
                Textbox.insert(0.0,s)
                Textbox.config(state=DISABLED)
                break
    if Textbox == t3:
         try:
              l7.destroy()
         except:
              pass
         l7=Label(root,text="Time: "+str(round(time.clock()-sttime,2)))
         l7.place(x=695,y=385)

#select sentence
def selSentence():
     global slc
     sentencenumber = simpledialog.askinteger("Separation by Sentences","Enter Sentence Number to Separate:")
     try:
          if sentencenumber>=1:
               separateSentence(slc[sentencenumber-1],t3)
          else:
               error=messagebox.showinfo("Oops!","Input error!")
     except:
          try:
               if sentencenumber>=1:
                    error=messagebox.showinfo("Oops!","Input error!")
          except:
               pass

def sepButton():
    global t
    global sepvalue
    if sepvalue == True:
        selSentence()
    else:
        separateSentence(t,t3)

#lexicon update
def LexUpdate():
    global root3
    def addHighFreq2():
        try:
            inputwordnumber = int(entry1.get())
            dic[lst[inputwordnumber-1]] = dic.get(lst[inputwordnumber-1],0)
            f = open("comb.txt","a")
            f.write(lst[inputwordnumber-1]+"\n")
            f.close()
        except:
            pass
        entry1.delete(0,END)
    def closeWindow2():
         try:
              root3.destroy()
         except:
              pass
         tot = ""
         for i in range(len(tt)):
             if not (tt[i] in punc+nl+"\n"+"\t"):
                 tot += tt[i]
             else:
                 tot += " "
         arr = tot.split()
         for i in range(len(arr)):
             for j in range(1,8,1):
                 for k in range(len(arr[i])-j+1):
                     if arr[i][k:j+k] in dic:
                         dic[arr[i][k:j+k]] += 1
         for i in range(7,1,-1):
             for j in dic:
                 if len(j)==i:
                     for k in range(1,i):
                         for l in range(0,i-k+1):
                             if j[l:l+k] in dic:
                                 dic[j[l:l+k]] -= dic[j]
         f = open("ratio_word.txt","rt")
         s = f.read()
         f.close()
         d = s.split("\n")
         for i in range(len(d)-1):
             w = d[i].split()
             dic[w[0]] = dic.get(w[0],0)+int(w[1])
         try:
             f = open("storage.txt","a")
             f.write(tt)
             f.close()
         except:
             f = codecs.open("storage.txt","a","utf-8")
             f.write(tt.encode("utf-8").decode("utf-8","ignore"))
             f.close()
         f = open("storage_new.txt","w")
         f.close()
         item = list(dic.items())
         item.sort()
         item.sort(key=lambda item:item[1])
         item = item[::-1]
         f = open("ratio_word.txt","w")
         for i in range(len(item)):
             if item[i][1]>0:
                 f.write(item[i][0]+" "+str(item[i][1])+"\n")
         f.close()
         finish=messagebox.showinfo("Message","Updating completed!")
    if reseted == False:
         error = messagebox.showinfo("Oops!","Please reset before updating!")
         return
    try:
        f = open("storage_new.txt","rt")
        tt = f.read()
        f.close()
    except:
        f = codecs.open("storage_new.txt","r","utf-8")
        tt = f.read()
        f.close()
    f = open("comb.txt","rt")
    s = f.read()
    f.close()
    arr = s.split("\n")
    dic = {}
    for i in range(len(arr)-1):
        dic[arr[i]] = dic.get(arr[i],0)
    if root.lexLearning.get() == True:
        n = len(tt)//2000
        psg = []
        for i in range(n-1):
            psg.append(tt[i*2000:(i+1)*2000])
        psg.append(tt[(n-1)*2000:])
        name = {}
        lst = []
        if n > 0:
            for h in range(n):
                new = {}
                for i in range(2,6,1):
                    for j in range(len(psg[h])-i+1):
                        flag = 1
                        for k in range(j,j+i):
                            if psg[h][k] in punc+nl+"\n"+"\t"+"的"+"了":
                                flag = 0
                                break
                        if flag:
                            for k in range(2,i+1):
                                for l in range(j,j+i-k+1):
                                    if psg[h][l:l+k] in dic:
                                        flag = 0
                                        break
                        if flag:
                            new[psg[h][j:j+i]] = new.get(psg[h][j:j+i],0) + 1
                for i in new:
                    if new[i]/len(psg[h]) > 0.005:
                        name[i] = name.get(i,0)
        highfreq = open("highfreq.txt","w")
        for i in name:
            lst.append(i)
            highfreq.write(str(len(lst))+". "+i+"\n")
        highfreq.close()
        highfreq = open("highfreq.txt","rt")
        highfreqtext = highfreq.read()
        highfreq.close()
        os.remove("highfreq.txt")
        if highfreqtext != "":
            root3=Tk()
            root3.title("Learning")
            root3.configure(height=250,width=500)
            root3.resizable(width=NO,height=NO)
            root3.iconbitmap('icon.ico')
            text1=ScrolledText(root3,height=10,width=65)
            text1.place(x=10,y=25)
            text1.delete(0.0,END)
            text1.insert(0.0,highfreqtext)
            text1.config(state=DISABLED)
            label1=Label(root3,text="High Frequency Words Detected:")
            label1.place(x=10,y=1)
            label2=Label(root3,text='''Enter the the number of high frequency words to add:''')
            label2.place(x=10,y=160)
            entry1=Entry(root3)
            entry1.place(x=10,y=190)
            buttonAdd=Button(root3,text="Add",command=addHighFreq2)
            buttonAdd.place(x=180,y=180)
            buttonOK=Button(root3,text="Finish",command=closeWindow2)
            buttonOK.place(x=350,y=180)
            def callback(event=None): pass
            root3.protocol('WM_DELETE_WINDOW', callback)
    else:
          closeWindow2()
#add to lexicon
def LexAdd():
    global t
    try:
        f = open("storage_new.txt","a")
        f.write(t)
        f.close()
    except:
        f = codecs.open("storage_new.txt","a","utf-8")
        f.write(t.encode("utf-8").decode("utf-8","ignore"))
        f.close()
#open file
def load_file():
    mask = [
    ("Text files","*.txt"),
    ("All files","*.*")]
    filename = askopenfilename(defaultextension=".txt",filetypes=mask)
    try:
       file = codecs.open(filename,'r','utf-16')
       contents = file.read()
       file.close()
       t1.delete(0.0, END)
       f = open("temp.txt","w")
       for i in range(len(contents)):
                 try:
                      f.write(contents[i].encode('utf-8').decode('utf-8','ignore'))
                 except:
                      pass
       f.close()
       f = open("temp.txt","rt")
       t1.insert(0.0,f.read())
       f.close()
       os.remove("temp.txt")
    except:
       try:
            file = codecs.open(filename,'r','gb18030')
            contents = file.read()
            file.close()
            t1.delete(0.0, END)
            f = open("temp.txt","w")
            for i in range(len(contents)):
                 try:
                      f.write(contents[i].encode('utf-8').decode('utf-8','ignore'))
                 except:
                      pass
            f.close()
            f = open("temp.txt","rt")
            t1.insert(0.0,f.read())
            f.close()
            os.remove("temp.txt")
       except:
            try:
                 file = codecs.open(filename,'r','utf-8')
                 contents = file.read()
                 file.close()
                 t1.delete(0.0, END)
                 f = open("temp.txt","w")
                 for i in range(len(contents)):
                      try:
                           f.write(contents[i].encode('utf-8').decode('utf-8','ignore'))
                      except:
                           pass
                 f.close()
                 f = open("temp.txt","rt")
                 t1.insert(0.0,f.read())
                 f.close()
                 os.remove("temp.txt")
            except:
                 pass
#save file
def save_file():
    mask = [
    ("Text files","*.txt"),
    ("All files","*.*")]
    filename = asksaveasfilename(defaultextension=".txt",filetypes=mask)
    try:
       file = open(filename, 'w')
       textoutput = t3.get(0.0, END)
       file.write(textoutput)
       file.close()
    except:
       pass
#clear the textbox
def clear_text1():
     t1.delete(0.0, END)
#close all opened windows
def closeWindow():
     global Exited
     if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
         root.music = BooleanVar(value=True)
         root.destroy()
         try:
              root2.destroy()
         except:
              pass
         try:
              root3.destroy()
         except:
              pass
         try:
              root4.destroy()
         except:
              pass
         try:
              root5.destroy()
         except:
              pass
         try:
              root6.destroy()
         except:
              pass
         try:
              root7.destroy()
         except:
              pass
         Exited = True
#reset button
def resetButton():
     global reseted
     global l7
     t1.delete(0.0, END)
     t2.config(state=NORMAL)
     t2.delete(0.0, END)
     t2.config(state=DISABLED)
     t3.config(state=NORMAL)
     t3.delete(0.0, END)
     t3.config(state=DISABLED)
     confirmButton()
     try:
          l7.destroy()
     except:
          pass
     b5.config(state=DISABLED)
     reseted = True

#separate with both algorithms
def showBoth():
     global algorigin
     global sepSenorigin
     global root7
     root7 = Tk()
     root7.title('Separate and Compare')
     root7.configure(height=500,width=665)
     root7.resizable(width=NO, height=NO)
     root7.iconbitmap('icon.ico')
     lab1=Label(root7,text="DFS + Divide and Conquer:")
     lab1.place(x=5,y=0)
     lab2=Label(root7,text="Dynamic Programming:")
     lab2.place(x=5,y=160)
     lab3=Label(root7,text="Comparison Result:")
     lab3.place(x=5,y=320)
     a1=ScrolledText(root7,height=10,width=90)
     a1.place(x=5,y=25)
     a2=ScrolledText(root7,height=10,width=90)
     a2.place(x=5,y=185)
     a3=ScrolledText(root7,height=10,width=90)
     a3.place(x=5,y=345)
     separateSentence(t,a1)
     root.algorithm = IntVar(value=2)
     separateSentence(t,a2)
     f = open("DFS.txt","w")
     f.write(a1.get(0.0, END))
     f.close()
     f = open("Dynamic.txt","w")
     f.write(a2.get(0.0, END))
     f.close()
     tmp = os.popen("fc DFS.txt Dynamic.txt")
     a3.delete(0.0, END)
     a3.insert(0.0,"".join(tmp))
     os.remove("DFS.txt")
     os.remove("Dynamic.txt")
     root.algorithm = algorigin
     root.sepSentence = sepSenorigin
     a1.config(state=DISABLED)
     a2.config(state=DISABLED)
     a3.config(state=DISABLED)

def sepBoth():
     global both
     global algorigin
     global sepSenorigin
     algorigin = root.algorithm
     root.algorithm = IntVar(value=1)
     sepSenorigin = root.sepSentence
     root.sepSentence = BooleanVar(value=False)
     both = True
     confirmButton()
     if root.highFreq.get() == False:
          showBoth()
          both = False

#Main GUI Building
#splash
splashScreen()

#Main window
root = Tk()
root.title('Welcome to Anfield (Beta 3.3)')
root.configure(height=520,width=800)
root.resizable(width=NO, height=NO)
root.iconbitmap('icon.ico')
center_window(800,520)

#Control Variables
root.highFreq = BooleanVar(value=False)
root.sepSentence = BooleanVar(value=False)
root.lexLearning = BooleanVar(value=False)
root.crawl = BooleanVar(value=False)
root.music = BooleanVar(value=False)
root.algorithm = IntVar(value=1)

#Menus
menubar = Menu(root)
filemenu = Menu(menubar,tearoff = 0)
filemenu.add_command(label = "Import Text",command = load_file)
filemenu.add_command(label = "Save as",command = save_file)
filemenu.add_separator()
filemenu.add_command(label = "Reset",command = resetButton)
filemenu.add_separator()
filemenu.add_command(label = "Exit",command = closeWindow)
menubar.add_cascade(label = 'File',menu = filemenu)

menubar2 = Menu(root)
filemenu = Menu(menubar2,tearoff = 0)
filemenu.add_command(label = "Add the Input Text to Lexicon",command = LexAdd)
filemenu.add_command(label = "Update the Lexicon",command = LexUpdate)
filemenu.add_separator()
filemenu.add_command(label = "Add a Word to Dictionary",command=AddWord)
filemenu.add_command(label = "Remove a Word from Dictionary",command=RemoveWord)
filemenu.add_separator()
filemenu.add_command(label = "Web Crawler",command=webCrawler)
menubar.add_cascade(label = 'Lexicon',menu = filemenu)

menubar3 = Menu(root)
filemenu = Menu(menubar3,tearoff = 0)
filemenu.add_checkbutton(label = "Separate by Sentences",variable=root.sepSentence,onvalue=True,offvalue=False)
filemenu.add_checkbutton(label = "Detect the High-frequency Words",variable=root.highFreq,onvalue=True,offvalue=False)
filemenu.add_separator()
filemenu.add_checkbutton(label = "Enable Lexicon Learning",variable=root.lexLearning,onvalue=True,offvalue=False)
filemenu.add_checkbutton(label = "Crawl ONLY on the Input Domain",variable=root.crawl,onvalue=True,offvalue=False)
filemenu.add_separator()
filemenu.add_radiobutton(label = "DFS + Divide and Conquer",variable=root.algorithm,value=1)
filemenu.add_radiobutton(label = "Dynamic Programming",variable=root.algorithm,value=2)
if os.name=="nt":
     filemenu.add_separator()
     filemenu.add_command(label = "Separate with Both Algorithms",command=sepBoth)
filemenu.add_separator()
filemenu.add_checkbutton(label = "Stop Playing the Music",variable=root.music,onvalue=True,offvalue=False)
menubar.add_cascade(label = 'Options',menu = filemenu)

menubar4 = Menu(root)
filemenu = Menu(menubar4,tearoff = 0)
filemenu.add_command(label = "Instructions",command = instruction)
filemenu.add_command(label = "Copyright",command = copyRight)
menubar.add_cascade(label = 'Help',menu = filemenu)

root['menu'] = menubar

#Texts
t1=ScrolledText(root,height=10,width=90)
t1.place(x=5,y=25)
t2=ScrolledText(root,height=10,width=90,state=DISABLED)
t2.place(x=5,y=185)
t3=ScrolledText(root,height=10,width=90,state=DISABLED)
t3.place(x=5,y=345)

#Labels
l1=Label(root,text="Input:")
l1.place(x=5,y=0)
l2=Label(root,text="Sentences Separated:")
l2.place(x=5,y=160)
l3=Label(root,text="Output:")
l3.place(x=5,y=320)
l4=Label(root,text = 'copyright---------------Anfield')
l4.place(x=620,y=480)

#Buttons
b1=Button(root,command = clear_text1,text="Clear All",width=17)
b1.place(x=665,y=25)
b5=Button(root,text="Separate!",command=sepButton,width=17)
b5.place(x=665,y=345)
b6=Button(root,command=confirmButton,text="Confirm",width=17)
b6.place(x=665,y=100)
b7=Button(root,text="Reset",command=resetButton,width=17)
b7.place(x=665,y=420)

#Pretreatment
t1.delete(0.0, END)
t1.insert(0.0,"请键入需要分词的语段：")
both = False
reseted = False
algorigin = root.algorithm
sepSenorigin = root.sepSentence
confirmButton()

#background music threads
Exited = False
Playing = False
my_thread = MyThread()
my_thread.start()

root.protocol('WM_DELETE_WINDOW', closeWindow)
root.focus_force()
root.mainloop()
