#!/usr/bin/env python3
import json 
import sys

if __name__=="__main__":
 
    if len(sys.argv) < 3:
        print("\nusage ./makeIntersectionJson.py <InputFileNameA> <InputFileNameB> <OutptFileName>\n")
        sys.exit(0)
    
    f=open(sys.argv[1],'r')
    _runLumiA=json.load(f)
    f.close()
    f=open(sys.argv[2],'r')
    _runLumiB=json.load(f)
    f.close()
    
    ofname="intersection.json"
    if len(sys.argv) > 3:
        ofname=sys.argv[3]
    

    runLumiA={}
    for r in _runLumiA:
        runLumiA[r]=[]
        for ls in _runLumiA[r]:
            for l in range(ls[0],ls[1]+1):
                runLumiA[r].append(l)

    runLumiB={}
    for r in _runLumiB:
        runLumiB[r]=[]
        for ls in _runLumiB[r]:
            for l in range(ls[0],ls[1]+1):
                runLumiB[r].append(l)
    
    _runLumiC={}
    for r in runLumiB:
        if r not in runLumiA: continue;
        _runLumiC[r]=[]
        for l in runLumiB[r]:
            if l not in runLumiA[r]: continue
            _runLumiC[r].append(l)
    
    runLumiC={}
    for r in _runLumiC:
        runLumiC[r]=[]
        _runLumiC[r].sort()
        prev=-1
        for l in _runLumiC[r]:
            if prev==-1:
                sec=[l]
                prev=l
                continue
            if l!=prev+1:
                sec.append(prev)
                runLumiC[r].append(sec)
                sec=[l]
            prev=l
        sec.append(prev)
        runLumiC[r].append(sec)

    f=open(ofname,'w')
    json.dump(runLumiC,f,indent=6)
    f.close()



