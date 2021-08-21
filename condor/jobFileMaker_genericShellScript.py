#!/usr/bin/env python3
import os

NJOBS=1000
NEVENTS_PER_JOB = -1
ZERO_OFFSET=0
FILES_PER_JOB=1
PU_NEVENTS=-1
destination='/grid_mnt/t3storage3/athachay/bs2mumug/hltDev/CMSSW_11_3_0/src/Analysis/HLTAnalyserPy/Run3HLTNtuplizer/Run3HLTNtuples'

FileSource ="fileSource.txt"

pwd=os.environ['PWD']
proxy_path=os.environ['X509_USER_PROXY']

xrdRedirector="root://cms-xrd-global.cern.ch/"

Fnames=open(FileSource,'r')
sourceFileList=Fnames.readlines()
Fnames.close()


condorScriptString="\
executable = $(filename)\n\
output = $Fp(filename)cdr.stdout\n\
error = $Fp(filename)cdr.stderr\n\
log = $Fp(filename)cdr.log\n\
"
condorScript=open('jobSubmit.sub','w')
condorScript.write(condorScriptString)

cfgTxt="\
@@FNAMES\
"

runScriptTxt="\
#!/bin/bash\n\
set -x\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
export HOME=/home/athachay\n\
export X509_USER_PROXY="+proxy_path+"\n\
cd /home/athachay/t3store3/bs2mumug/run2studies/CMSSW_11_2_2_patch1/src\n\
cd "+pwd+"/@@DIRNAME \n\
cp /grid_mnt/t3storage3/athachay/bs2mumug/hltDev/CMSSW_11_3_0/src/Analysis/HLTAnalyserPy/Run3HLTNtuplizer/makeRun3Ntup.py . \n\
eval `scramv1 runtime -sh`\n\
python makeRun3Ntup.py @@CFGFILENAME -o bs2MMGRun3HLTNtuple_@@IDX.root\n\
if [ $? -eq 0 ]; then \n\
    echo OK\n\
    mv *.root "+destination+"\n\
    mv @@RUNSCRIPTNAME @@RUNSCRIPTNAME.sucess\n\
else\n\
    echo FAIL\n\
fi\n\
"

if not os.path.exists('Jobs'):
    os.system('mkdir Jobs')
print("Making ",NJOBS," Jobs ")

for ii in range(NJOBS):
    i=ii+ZERO_OFFSET
    if len(sourceFileList)<FILES_PER_JOB:
        FILES_PER_JOB=len(sourceFileList)
        print("fname count less than required .. stoping after seting final script to  have ",FILES_PER_JOB," files ")
        
    if FILES_PER_JOB==0:
        print("Filelist empty exiting")
        break
    dirName= 'Jobs/Job_'+str(i)
    print(i," Job Made")
    if os.path.exists(dirName):
        k=True
    else:
        os.system('mkdir '+dirName)
    cfgFileName='fnames.txt'
    cfgFile=open(dirName+'/'+cfgFileName,'w')
    cfgTxttmp=cfgTxt.replace("@@IDX",str(i))
    tmp=""
    srcFiles=[]
    for j in range(FILES_PER_JOB):
        srcFiles.append(sourceFileList.pop(0)[:-1])
        tmp+=srcFiles[-1]+"\n"
    cfgTxttmp=cfgTxttmp.replace("@@FNAMES",tmp)
    cfgFile.write(cfgTxttmp)
    cfgFile.close()   
    
    runScriptName=dirName+'/run'+str(i)+'.sh'
    runScriptNameFull=pwd+'/'+dirName+'/run'+str(i)+'.sh'
    runScript=open(runScriptName,'w')
    tmp=runScriptTxt.replace("@@IDX",str(i))
    tmp=tmp.replace("@@DIRNAME",dirName)
    tmp=tmp.replace("@@CFGFILENAME",cfgFileName)
    tmp=tmp.replace("@@RUNSCRIPTNAME",runScriptNameFull)
    runScript.write(tmp)
    runScript.close()
    os.system('chmod +x '+runScriptName)
    condorScript.write("queue filename matching ("+runScriptName+")\n")

print(" Number of files left : ", len(sourceFileList) )

condorScript.close()
