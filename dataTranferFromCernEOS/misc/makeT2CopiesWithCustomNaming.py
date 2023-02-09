#!/usr/bin/env python3
import os
import sys
version='v1'
"""
    Usage
    ./dajk.py <InputFileListFname> <destination> <jobPrefix>
"""


NJOBS=20000
NEVENTS_PER_JOB = -1
ZERO_OFFSET=0
FILES_PER_JOB=2


pwd=os.environ['PWD']
proxy_path=os.environ['X509_USER_PROXY']
HOME=os.environ['HOME']
xrdRedirector="root://cms-xrd-global.cern.ch/"

FileSource ="bmm5FileList.txt"
destination='/grid_mnt/t3storage3/athachay/bs2mumug/run2studies/CMSSW_10_6_19_patch2/src/BsMMGAnalysis/MergeWithBMMNtuples/RunLumiEventFileMaker/runLumiList/'
tag=""

if len(sys.argv) > 1:
    FileSource=sys.argv[1]  
else:
    print("Usage\n\t./dajk.py <InputFileListFname> <destination> <FILES_PER_JOB> <NJOBS> <jobPrefix>")
    sys.exit(1)
if len(sys.argv) > 2:
    destination=sys.argv[2]  
if len(sys.argv) > 3:
    FILES_PER_JOB=int(sys.argv[3])  
if len(sys.argv) > 4:
    NJOBS=int(sys.argv[4])  
if len(sys.argv) > 5:
    tag=sys.argv[5]  

Fnames=open(FileSource,'r')
sourceFileList=Fnames.readlines()
Fnames.close()
print("Number avilable files = ",len(sourceFileList))

condorScriptString="\
executable = $(filename)\n\
output = $Fp(filename)run.$(Cluster).stdout\n\
error = $Fp(filename)run.$(Cluster).stderr\n\
log = $Fp(filename)run.$(Cluster).log\n\
"


runScriptTxt="\
#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
export HOME="+HOME+"\n\
export X509_USER_PROXY="+proxy_path+"\n\
cd @@DIRNAME \n\
eval `scramv1 runtime -sh`\n\
set -x\n\
mv @@RUNSCRIPT @@RUNSCRIPT.busy \n\
SUCCESS=1\n\
@@EXECUTION_SCRIPT\n\
if [ $SUCCESS -eq 1 ]; then \n\
    mv @@RUNSCRIPT.busy @@RUNSCRIPT.success\n\
else\n\
    mv @@RUNSCRIPT.busy @@RUNSCRIPT \n\
    echo FAIL\n\
fi\n\
"
exicutionScriptScript="\
if [ @@CFGFNAME ] ; then \n\
    source @@CFGFNAME\n\
    if [ $? -eq 0 ]; then \n\
        echo OK\n\
        mv  @@CFGFNAME @@CFGFNAME.sucess\n\
    else\n\
        SUCCESS=0\n\
        echo FAIL\n\
    fi\n\
fi\
"

cfgTxt="\
xrdcp @@FNAME "+destination+"@@CUSTOMTAG_@@OFNAME\n\
"

head='Condor/Jobs'+tag
if not os.path.exists(head ):
    os.system('mkdir -p '+head)

condorScriptName=head+'/job'+tag+'.sub'
condorScript=open(condorScriptName,'w')
condorScript.write(condorScriptString)

n=int(len(sourceFileList)/FILES_PER_JOB) + 1

if n < NJOBS:
    NJOBS=n
print("Making ",NJOBS," Jobs ")

njobs=0
cTag=''
for ii in range(NJOBS):
    i=ii+ZERO_OFFSET
    
    if len(sourceFileList)<FILES_PER_JOB:
       print("\nfname count less than required .. stoping ")
       FILES_PER_JOB=len(sourceFileList)
    
    if len(sourceFileList) ==0:
       break 

    dirName= pwd+'/'+head+'/Job_'+str(i)
    
    if(ii%10==0) : print("\nJob Made : ",end = " " )
    print(ii,end =" ")

    if os.path.exists(dirName):
        k=True
    else:
        os.system('mkdir '+dirName)
    
    execPart=""
    for j in range(FILES_PER_JOB):
        cfgFileName='copyFile_'+str(i)+'_'+str(j)+'.sh'
        cfgFile=open(dirName+'/'+cfgFileName,'w')
        fName=sourceFileList.pop(0)[:-1]
        cmd = cfgTxt.replace("@@FNAME",fName)
        cTag=fName.split('/')[14]
        cmd = cmd.replace('@@CUSTOMTAG',cTag)
        oFName=fName.split('/')[-1]
        cmd = cmd.replace('@@OFNAME',oFName)
        cfgFile.write(cmd)
        cfgFile.close() 
        execPart+="\n"+exicutionScriptScript.replace("@@CFGFNAME",cfgFileName)      
    
    runScriptName=dirName+'/'+tag+'run'+str(i)+'.sh'
    runScript=open(runScriptName,'w')
    tmp=runScriptTxt.replace("@@DIRNAME",dirName)
    tmp=tmp.replace("@@EXECUTION_SCRIPT",execPart)
    tmp=tmp.replace("@@IDX",str(i))
    tmp=tmp.replace("@@CFGFILENAME",cfgFileName)
    tmp=tmp.replace("@@RUNSCRIPT",runScriptName)
    runScript.write(tmp)
    runScript.close()
    os.system('chmod +x '+runScriptName)
    condorScript.write("queue filename matching ("+runScriptName+")\n")
    njobs+=1
print()
print(" Number of jobs made : ", njobs)
print(" Number of files left : ", len(sourceFileList) )
print(" Condoer Submit file : ",condorScriptName)
condorScript.close()
