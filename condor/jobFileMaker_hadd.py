#!/usr/bin/env python3 
import os

NJOBS=2
NEVENTS_PER_JOB = -1
ZERO_OFFSET=0
FILES_PER_JOB=2

destination='/grid_mnt/t3storage3/athachay/l1egamma/triggerPerformance/CMSSW_11_2_2_patch1/src/hadd/mergedFiles/'

FileSource ="haddFileList.txt"

pwd=os.environ['PWD']
proxy_path=os.environ['X509_USER_PROXY']


Fnames=open(FileSource,'r')
sourceFileList=Fnames.readlines()
Fnames.close()

njobs=int(len(sourceFileList)/FILES_PER_JOB)
if (len(sourceFileList)*1.0)/FILES_PER_JOB > njobs:
    njobs+=1

NJOBS = int(min(NJOBS,njobs))

condorScriptString="\
executable = $(filename)\n\
output = $Fp(filename)cdr.stdout\n\
error = $Fp(filename)cdr.stderr\n\
log = $Fp(filename)cdr.log\n\
"
condorScript=open('jobSubmit.sub','w')
condorScript.write(condorScriptString)

runScriptTxt="\
#!/bin/bash\n\
set -x\n\
mkdir /tmp/athachay/scratch -p\n\
cd /tmp/athachay/scratch\n\
condorTmpDir=$PWD\n\
echo $condorTmpDir \n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
export HOME=/home/athachay\n\
export X509_USER_PROXY="+proxy_path+"\n\
cd "+pwd+"/@@DIRNAME \n\
eval `scramv1 runtime -sh`\n\
cd $condorTmpDir \n\
hadd mergedFile@@IDX.root @@HADDFiles \n\
if [ $? -eq 0 ]; then \n\
    echo OK\n\
    mv mergedFile@@IDX.root "+destination+'Charmonium_Run2018A12Nov2019_UL2018_rsbv1_hadd@@IDX.root'+"\n\
    mv @@RUNSCRIPTNAME @@RUNSCRIPTNAME.sucess\n\
else\n\
    echo FAIL\n\
fi\n\
"

if not os.path.exists('Jobs'):
    os.system('mkdir Jobs')

print("Making ",NJOBS," Jobs ")

madeJobs=0
for ii in range(NJOBS):
    i=ii+ZERO_OFFSET
    if len(sourceFileList)<FILES_PER_JOB:
        FILES_PER_JOB=len(sourceFileList)
    if FILES_PER_JOB==0:
        break
    dirName= 'Jobs/Job_'+str(i)
    madeJobs+=1
    print("Job ",i," Made with ",FILES_PER_JOB," files" )
    if os.path.exists(dirName):
        k=True
    else:
        os.system('mkdir '+dirName)
    
    scriptName = 'run'+str(i)+'.sh'
    runScriptName=dirName+'/'+scriptName
    runScript=open(runScriptName,'w')
    
    haddCmd=""
    for j in range(FILES_PER_JOB):
        haddCmd+="\\\n\t"+sourceFileList.pop(0)[:-1]
    haddCmd+="\n"
    
    tmp=runScriptTxt.replace("@@DIRNAME",dirName)
    tmp=tmp.replace("@@IDX",str(i))
    scr = pwd + '/'+ runScriptName
    tmp=tmp.replace("@@RUNSCRIPTNAME",scr)
    tmp=tmp.replace('@@HADDFiles',haddCmd)
    
    runScript.write(tmp)
    
    runScript.close()
    os.system('chmod +x '+runScriptName)
    condorScript.write("queue filename matching ("+runScriptName+")\n")

print(" Number of files left      : ", len(sourceFileList) )
print(" Total Number of Jobs Made : ", madeJobs )

condorScript.close()
