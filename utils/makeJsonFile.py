#!/usr/bin/env python3

#####################################################################
#                                                                   #
#        converts the txt format of run-lumi to the json format     #
#                                                                   #
#        usage : ./makeJsonFile.py <InputFileName>                  #
#                                                                   #
#####################################################################

import json 
import sys

def getJsonFromTxt(fname):
    f=open(fname)
    txt=f.readlines()
    f.close()
    runlumiJson={}
    for l in txt:
        items=l[:-1].split('[')
        run=int(items[0])
        lumistmp=[ int(lms) for lms in items[1].strip().replace("]","").split(',') ]
        lumistmp.sort()
        lumis=[]
        prevLm=-1
        for lms in lumistmp:
            if prevLm==-1:
                sec=[lms]
                prevLm=lms
                continue
            if lms!=prevLm+1:
                sec.append(prevLm)
                lumis.append(sec)
                sec=[lms]
            prevLm=lms
        sec.append(lms)
        lumis.append(sec)
        runlumiJson[run]=lumis    

    return runlumiJson

if __name__== "__main__":

    if len(sys.argv) < 2:
        print("usage ./makeJsonFile.py <InputFileName>")
        sys.exit(0)
    fname=sys.argv[1]
    jsnDict=getJsonFromTxt(fname)
    ofname=fname.replace('.txt','.json')
    if fname==ofname:
        ofname+='.json'
    ofile=open(ofname,'w')
    json.dump(jsnDict,ofile,indent = 6)
    ofile.close()
