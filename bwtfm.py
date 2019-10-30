#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:41:35 2019

@author: Ayca Begum Tascioglu
ID: 21600907
"""

"""
input: a file in .fa = myText.fa
output: 
    a file with bwt string = myText.fa.bwt
    a file with fm index table = myText.fa.fm
"""
import numpy as np
##FM Table -- Count
def Cnt(bwt_str):
    cnt = dict()
    cnt = {}
    chars = ""
    for i in bwt_str:
        if not i in cnt:
            cnt[i] = 1
            chars += i
        else:
            cnt[i] += 1
    chars = sorted(chars)
    return cnt, chars

##FM Table -- Rank
def Rank(bwt_str,chars,cnt):
    ### fm tables: rank
    rank = {}
    i = 0
    for j in chars:
        rank[j] = i
        i += cnt[j]
    return rank

##FM Table -- Occurancy
def Occ(bwt_str,chars,cnt):
    occ = np.zeros((len(bwt_str)+1,len(cnt)+1), dtype=object)
    for i in range(0,len(chars)):
        occ[0][i+1] = chars[i]
    for i in range(0,len(bwt_str)):
        occ[i+1][0] = bwt_str[i]
    
    
    for i in range(1,len(bwt_str)+1):
        for j in range(1, len(chars)+1):
            if occ[i][0] == occ[0][j] and i>1:
                occ[i,j] = occ[i-1][j] +1 
            elif occ[i][0] == occ[0][j] and i==1:
                occ[i,j] = 1
            elif occ[i][0] != occ[0][j] and i>1:
                occ[i,j] = occ[i-1][j]
    return occ
#%% index method
def index(textFile):
    text = open(textFile, "r") 
    text = text.read()
    text = text.replace("\n","")

    text=text+'$'   #endchar
    ### Suffix Array
    suffixArray = [text[-i:] for i in range(1,len(text)+1)]
    prep1 = [text[-i:] for i in range(1,len(text)+1)]
    suffixDct1 = dict()
    suffixDct1 = {}
    suffixDct = dict()
    suffixDct = {}
    hashing = ""

    for i in range(0,len(suffixArray)):
        prep1[i] = prep1[i] + text[0:len(text)-i-1]
        suffixDct1[prep1[i]] = len(text) - i

    prep1.sort()
    keys = sorted(suffixDct1.keys())
    for i in keys:
        suffixDct[str(i)] = suffixDct1[str(i)]
        hashing = hashing+ i[0] + str(suffixDct[str(i)]) +'\n'

    ### bwt string
    bwt_str =""
    for i in range(0,len(prep1)):
        bwt_str = bwt_str + (prep1[i])[-1:]
        firstColumn = ""
    for i in range(0,len(prep1)):
        firstColumn = firstColumn + (prep1[i])[0]
    
    #fm_tables
    cnt = Cnt(bwt_str)[0]
    chars = Cnt(bwt_str)[1]
    rank = Rank(bwt_str,chars,cnt)
    occ = Occ(bwt_str,chars,cnt)

    ###  files
    bwtFile = textFile+".bwt"
    b = open(bwtFile,"w+")
    b.write(bwt_str)
    b.close()
    fmFile = textFile+".fm"
    f = open(fmFile,"w+")
    f.write(str(hashing))

    f.write("First Column")
    f.write(firstColumn)
    f.write("\n")
    f.write(str(suffixArray))
    f.write("\n")
    f.write("\nOCC\n")

    for i in range(0,len(bwt_str)+1):
        for j in range(0, len(chars)+1):
            tmp = str(occ[i][j])+" "
            f.write(tmp)
        f.write("\n")
    f.write("\n")
    
    f.write("\ncnt\n")
    f.write(str(cnt))
    f.write("\n")
    
    f.write("\nrank\n")
    f.write(str(rank))
    f.write("\n")
    f.close()
#%%
def search(textFile,patternFile):
    fm = textFile+".fm"
    bwt = textFile+".bwt"
    bwt = open(bwt,"r")
    bwt = bwt.read()

    indexTable = [[None for i in range(2)]  for j in range(0,len(bwt))]
    i = 0
    with open(fm) as fp:
        line = fp.readline()
        cnt = 0
        while line != "First Column":
            if cnt == len(bwt):
                break
            indexTable[i][0] = line[0]
            indexTable[i][1] = line[1:]
            indexTable[i][1] = int(indexTable[i][1].replace('\n','').strip())
            i+=1
            cnt += 1
            line = fp.readline()

    #fm_tables
    cnt = Cnt(bwt)[0]
    chars = Cnt(bwt)[1]
    rank = Rank(bwt,chars,cnt)
    occ = Occ(bwt,chars,cnt)
    occ = np.delete(occ,0,1)
    occ = np.delete(occ,0,1)
    occ = np.delete(occ,0,0)
    #A = occ[0][1]
    #C = occ[0][2]
    #G = occ[0][3]
    #T = occ[0][4]
    
    
                
    pattern = open(patternFile,"r")
    pattern = pattern.read()

    start = 1
    end = len(bwt)-1
    counter = 0
    
    for i in pattern[::-1]:
        if i == 'A':
            start = int(rank[i]) + int(occ[start][0])
            end = rank[i] + int(occ[end][0]-1)
            counter+=1

        elif i == 'C':
            start = rank[i] + int(occ[start-1][1])
            end = rank[i] + int(occ[end][1] -1)
            counter += 1

        elif i == 'G':
            start = rank[i] + int(occ[start-1][2])
            end = rank[i] + int(occ[end][2] -1)
            counter += 1

        elif i == 'T':
            start = rank[i] + int(occ[start-1][3])
            end = rank[i] + int(occ[end][3] -1)
            counter += 1

        else:
            break
    if counter == 0:
        print("Given Pattern could not find")
    elif counter >= len(pattern):
        lineCount = 1
        print("Pattern P found in T", end-start+1," times at positions:")
        for i in range(start,end+1):
            print("pos", lineCount,": ", indexTable[i][1])
            lineCount+=1
index("myText.fa")
search("myText.fa","pattern.fa")

