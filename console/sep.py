# -*- coding:utf-8 -*-

import string
import re

def checkname(arr,length):
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

def seperate(st,n,ct):
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
                        seperate(st[i:],n+1,ct*rate.get(sep[n],1))

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
        seperate(st,0,1)
        return sep2

f = open("algorithm.txt","rt")
alg = f.read()
f.close()
f = open("deal.txt","rt")
t = f.read()
f.close()
f = open("stbyst.txt","rt")
mark = f.read()
f.close()
f = open("detect.txt","rt")
detect = f.read()
f.close()
f = open("language.txt","rt")
lang = f.read()
f.close()
f = open("learn.txt","rt")
learn = f.read()
f.close()
f = open("familyname.txt","rt")
d = f.read().split("\n")
f.close()
family = {}
for i in range(len(d)):
    family[d[i]] = family.get(d[i],0)
if lang == "1":
    f = open("chn.txt","rt")
    hint = f.read().split("\n")
    f.close()
else:
    f = open("eng.txt","rt")
    hint = f.read().split("\n")
    f.close()
punc = "。，“”：；‘’？/+=~（）！·#￥%……—*、|{}[]《》〈〉 　．，＂：；｀～｛｝［］！＠＃＄％︿＆＊－＿＋＝＇？／＼｜＜＞【】"+string.punctuation
nl = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９"
useless = "二三四五六七八九十去忙要会自在和得带常乱跑跳走想爱哭看瞄观赏瞥见听说唱骂讲读触摸站有打设出住虽伸侧戴耳票猜到傻咬略啊呀呢吗哇嘞哈吧咔啦哦嗷噢唉了你我他她它"
useless2 = "去忙要会在和得带乱跑跳走哭看瞄瞥说唱骂讲读触摸站有打设出住虽侧票猜到傻咬略啊呀呢吗哇嘞哈吧咔啦哦嗷噢唉了你我他她它"
useless3 = "一二两三四五六七八九十"
while 1:
    cmd = input(hint[0]+"\n")
    if cmd == "1":
        filename = input(hint[1])
        fileopen = 1
        try:
            f = open(filename,"rt")
        except:
            print(hint[14])
            fileopen = 0
        if fileopen:
            try:
                t = f.read()
            except:
                print(hint[15])
            f.close()
    elif cmd == "2":
        t = input(hint[2])
        t += "\n"
    elif cmd == "3":
        f = open("ratio_word.txt","rt")
        s = f.read()
        f.close()
        d = s.split("\n")
        rate = {}
        for i in range(len(d)-1):
            w = d[i].split()
            rate[w[0]] = rate.get(w[0],0)+int(w[1])
        if mark == "1":
            s = ""
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
            slc = s.split("\n")
            del slc[len(slc)-1:len(slc)]
            slc2 = []
            for i in range(len(slc)):
                if slc[i] != "":
                    slc2.append(slc[i])
            slc = slc2
            s = "\n".join(slc)
            print(s)
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
        if detect == "1":
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
                                        if (psg[h][l:l+k] in dic) and ((rate.get(psg[h][l:l+k],1)>1) or k==i):
                                            flag = 0
                                            break
                            if flag:
                                new[psg[h][j:j+i]] = new.get(psg[h][j:j+i],0) + 1
                    for i in new:
                        if new[i]/len(psg[h]) > 0.005:
                            name[i] = name.get(i,0)
            for i in name:
                lst.append(i)
                print(str(len(lst))+". "+i)
            name = {}
            if len(lst) > 0:
                while 1:
                    error = 1
                    number = input(hint[3])
                    if number == "end":
                        break
                    m = 0
                    for i in range(len(number)):
                        if ord(number[i])-48 in range(0,10):
                            m = m*10 + ord(number[i])-48
                        else:
                            print(hint[4])
                            error = 0
                            break
                    if error:
                        if m-1 in range(0,len(lst)):
                            dic[lst[m-1]] = dic.get(lst[m-1],0)
                            name[lst[m-1]] = name.get(lst[m-1],0)
                        else:
                            print(hint[4])
        for i in ppl:
            dic[i] = dic.get(i,0)
        if detect == "1":
            for i in name:
                rate[i] = rate.get(i,round(rate["的"]/500))
        i = 0
        tot = punc+nl+"\n"+"\t"
        if alg == "1":
            sep = [""]*1000
            sep2 = [""]*1000
            f = open("seperate.txt","w")
            while mark == "2":
                s = ""
                while (i<len(t)) and (not(t[i] in tot)):
                    s += t[i]
                    i += 1
                minp = 0
                maxc = 0
                if s != "":
                    sep2 = halfsentence(s)
                    (sep2,minp) = checkname(sep2,minp)
                    for j in range(minp-1):
                        f.write(sep2[j]+"|")
                    if i<len(t):
                        if t[i] in nl:
                            f.write(sep2[minp-1]+"|")
                        else:
                            f.write(sep2[minp-1])
                    else:
                        f.write(sep2[minp-1])
                if (i<len(t)) and (t[i] in tot):
                    if i+1<len(t):
                        if (t[i] in punc+"\n"+"\t") or (t[i+1] in punc+"\n"+"\t") or ((t[i] in nl)and(t[i+1] in nl)):
                            f.write(t[i])
                        else:
                            f.write(t[i]+"|")
                    else:
                        f.write(t[i])
                    i += 1
                if i>=len(t):
                    f.close()
                    f = open("seperate.txt","rt")
                    s = f.read()
                    f.close()
                    print(s)
                    out = ""
                    while out != "1" and out != "2":
                        out = input(hint[5]+"\n")
                    if out == "1":
                        filename = input(hint[6])
                        try:
                            f = open(filename,"w")
                            f.write(s)
                            f.close()
                        except:
                            print(hint[4])
                    break
            if mark == "1":
                f.close()
                error = 1
                while 1:
                    number = input(hint[7])
                    if number == "end":
                        break
                    m = 0
                    for i in range(len(number)):
                        if ord(number[i])-48 in range(0,10):
                            m = m*10 + ord(number[i])-48
                        else:
                            print(hint[4])
                            error = 0
                            break
                    if error:
                        if m-1 in range(0,len(slc)):
                            tt = slc[m-1]
                            i = 0
                            while 1:
                                s = ""
                                while (i<len(tt)) and (not(tt[i] in tot)):
                                    s += tt[i]
                                    i += 1
                                minp = 0
                                maxc = 0
                                if s != "":
                                    sep2 = halfsentence(s)
                                    (sep2,minp) = checkname(sep2,minp)
                                    for j in range(minp-1):
                                        print(sep2[j]+"|",end="")
                                    if i<len(tt):
                                        if tt[i] in nl:
                                            print(sep2[minp-1]+"|",end="")
                                        else:
                                            print(sep2[minp-1],end="")
                                    else:
                                        print(sep2[minp-1],end="")
                                if (i<len(tt)) and (tt[i] in tot):
                                    if i+1<len(tt):
                                        if (tt[i] in punc+"\n"+"\t") or (tt[i+1] in punc+"\n"+"\t") or ((tt[i] in nl)and(tt[i+1] in nl)):
                                            print(tt[i],end="")
                                        else:
                                            print(tt[i]+"|",end="")
                                    else:
                                        print(tt[i],end="")
                                    i += 1
                                if i>=len(tt):
                                    break
                            print("")
                        else:
                            print(hint[4])
        else:
            f = open("seperate.txt","w")
            while mark == "2":
                sep = [""]*1000
                sep2 = [0]*1000
                sep3 = [1]*1000
                sep4 = [0]*1000
                sep5 = [""]*1000
                s = ""
                while (i<len(t)) and (not(t[i] in tot)):
                    s += t[i]
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
                    if i<len(t):
                        if t[i] in nl:
                            f.write(sep5[k-1]+"|")
                        else:
                            f.write(sep5[k-1])
                    else:
                        f.write(sep5[k-1])
                if (i<len(t)) and (t[i] in tot):
                    if i+1<len(t):
                        if (t[i] in punc+"\n"+"\t") or (t[i+1] in punc+"\n"+"\t") or ((t[i] in nl)and(t[i+1] in nl)):
                            f.write(t[i])
                        else:
                            f.write(t[i]+"|")
                    else:
                        f.write(t[i])
                    i += 1
                if i>=len(t):
                    f.close()
                    f = open("seperate.txt","rt")
                    s = f.read()
                    f.close()
                    print(s)
                    out = ""
                    while out != "1" and out != "2":
                        out = input(hint[5]+"\n")
                    if out == "1":
                        filename = input(hint[6])
                        try:
                            f = open(filename,"w")
                            f.write(s)
                            f.close()
                        except:
                            print(hint[4])
                    break
            if mark == "1":
                f.close()
                error = 1
                while 1:
                    number = input(hint[7])
                    if number == "end":
                        break
                    m = 0
                    for i in range(len(number)):
                        if ord(number[i])-48 in range(0,10):
                            m = m*10 + ord(number[i])-48
                        else:
                            print(hint[4])
                            error = 0
                            break
                    if error:
                        if m-1 in range(0,len(slc)):
                            tt = slc[m-1]
                            i = 0
                            while 1:
                                sep = [""]*1000
                                sep2 = [0]*1000
                                sep3 = [1]*1000
                                sep4 = [0]*1000
                                sep5 = [""]*1000
                                s = ""
                                while (i<len(tt)) and (not(tt[i] in tot)):
                                    s += tt[i]
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
                                    for j in range(k-1,0,-1):
                                        print(sep5[j]+"|",end="")
                                    if i<len(tt):
                                        if tt[i] in nl:
                                            print(sep5[0]+"|",end="")
                                        else:
                                            print(sep5[0],end="")
                                    else:
                                        print(sep5[0],end="")
                                if (i<len(tt)) and (tt[i] in tot):
                                    if i+1<len(tt):
                                        if (tt[i] in punc+"\n"+"\t") or (tt[i+1] in punc+"\n"+"\t") or ((tt[i] in nl)and(tt[i+1] in nl)):
                                            print(tt[i],end="")
                                        else:
                                            print(tt[i]+"|",end="")
                                    else:
                                        print(tt[i],end="")
                                    i += 1
                                if i>=len(tt):
                                    break
                            print("")
                        else:
                            print(hint[4])              
    elif cmd == "4":
        f = open("storage_new.txt","a")
        f.write(t)
        f.close()
    elif cmd == "5":
        f = open("storage_new.txt","rt")
        tt = f.read()
        f.close()
        f = open("comb.txt","rt")
        s = f.read()
        f.close()
        arr = s.split("\n")
        dic = {}
        tot = ""
        for i in range(len(arr)-1):
            dic[arr[i]] = dic.get(arr[i],0)
        if learn == "1":
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
            f = open("comb.txt","a")
            for i in name:
                lst.append(i)
                print(str(len(lst))+". "+i)
            if len(lst) > 0:
                while 1:
                    error = 1
                    number = input(hint[3])
                    if number == "end":
                        break
                    m = 0
                    for i in range(len(number)):
                        if ord(number[i])-48 in range(0,10):
                            m = m*10 + ord(number[i])-48
                        else:
                            print(hint[4])
                            error = 0
                            break
                    if error:
                        if m-1 in range(0,len(lst)):
                            dic[lst[m-1]] = dic.get(lst[m-1],0)
                            f.write(lst[m-1]+"\n")
                        else:
                            print(hint[4])
            f.close()
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
        f = open("storage.txt","a")
        f.write(tt)
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
    elif cmd == "7":
        while 1:
            f = open("comb.txt","rt")
            a = f.read().split("\n")
            f.close()
            word = input(hint[8])
            if word == "end":
                break
            f = open("comb.txt","w")
            for i in range(len(a)-1):
                if a[i] != word:
                    f.write(a[i]+"\n")
            f.close()
    elif cmd == "6":
        while 1:
            word = input(hint[8])
            if word == "end":
                break
            f = open("comb.txt","a")
            f.write(word+"\n")
            f.close()
    elif cmd == "8":
        alg = ""
        while alg != "1" and alg != "2":
            alg = input(hint[9]+"\n")
        f = open("algorithm.txt","w")
        f.write(alg)
        f.close()
    elif cmd == "9":
        mark = ""
        while mark != "1" and mark != "2":
            mark = input(hint[10]+"\n")
        f = open("stbyst.txt","w")
        f.write(mark)
        f.close()
    elif cmd == "10":
        detect = ""
        while detect != "1" and detect != "2":
            detect = input(hint[11]+"\n")
        f = open("detect.txt","w")
        f.write(detect)
        f.close()
    elif cmd == "11":
        learn = ""
        while learn != "1" and learn != "2":
            learn = input(hint[12]+"\n")
        f = open("learn.txt","w")
        f.write(learn)
        f.close()
    elif cmd == "12":
        lang = ""
        while lang != "1" and lang != "2":
            lang = input(hint[13]+"\n")
        f = open("language.txt","w")
        f.write(lang)
        f.close()
        if lang == "1":
            f = open("chn.txt","rt")
            hint = f.read().split("\n")
            f.close()
        else:
            f = open("eng.txt","rt")
            hint = f.read().split("\n")
            f.close()
    elif cmd == "13":
        if lang == "1":
            f = open("readme_chn.txt","rt")
            print(f.read())
            f.close()
        else:
            f = open("readme_eng.txt","rt")
            print(f.read())
            f.close() 
    elif cmd == "14":
        break
