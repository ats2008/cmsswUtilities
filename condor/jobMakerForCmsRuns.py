#!/usr/bin/env python3
import os
import sys
version='v1'

useStr="\
Usage\n\
    ./jobMakerForCmsRuns.py <InputFileListFname> <destination> <NJOBS> <NEVENTS_PER_JOB> <jobPrefix>\n\
\n\
"

executable='ntuplize_AOD.py'

NJOBS=20000
NEVENTS_PER_JOB = -1
ZERO_OFFSET=0
FILES_PER_JOB=1


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
    print(useStr)
    sys.exit(1)
if len(sys.argv) > 2:
    destination=sys.argv[2]  
if len(sys.argv) > 3:
    NJOBS=int(sys.argv[3])  
if len(sys.argv) > 4:
    FILES_PER_JOB=int(sys.argv[4])  
if len(sys.argv) > 5:
    tag=sys.argv[5]  

if(not os.path.exists(destination)):
    os.system("mkdir -p "+destination)
destination=os.path.abspath(destination)

print("Source file list ",FileSource)
print("destination : ",destination)
print("NJOBS : ",NJOBS)
print("NEVENTS_PER_JOB : ",NEVENTS_PER_JOB)
print("tag : ",tag)

Fnames=open(FileSource,'r')
sourceFileList=Fnames.readlines()
Fnames.close()
print("Number avilable files = ",len(sourceFileList))

configurationTxt="\
@@FNAMES\n\
"

condorScriptString="\
executable = $(filename)\n\
output = $Fp(filename)run.$(Cluster).stdout\n\
error = $Fp(filename)run.$(Cluster).stderr\n\
log = $Fp(filename)run.$(Cluster).log\n\
+JobFlavour = \"longlunch\"\n\
"

condorScript=open('job'+tag+'.sub','w')
condorScript.write(condorScriptString)


runScriptTxt="\
#!/bin/bash\n\
set -x\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
export HOME="+HOME+"\n\
export X509_USER_PROXY="+proxy_path+"\n\
cd @@DIRNAME \n\
eval `scramv1 runtime -sh`\n\
TMPDIR=`mktemp -d`\n\
cd $TMPDIR\n\
cp  "+pwd+"/"+executable+" .\n\
cp @@DIRNAME/@@CFGFILENAME .\n\
mv @@RUNSCRIPT @@RUNSCRIPT.busy \n\
cmsRun -j JobReport.xml " + executable + "\n\
if [ $? -eq 0 ]; then \n\
    mv *.root "+destination+"/bsToMuMuG_run2UL2018_@@IDX.root\n\
    if [ $? -eq 0 ] ; then \n\
        mv @@CFGFILENAME " + destination + "\n\
        mv *.xml " + destination + "\n\
        mv @@RUNSCRIPT.busy @@RUNSCRIPT.sucess \n\
        echo OK\n\
    else\n\
        mv @@RUNSCRIPT.busy @@RUNSCRIPT \n\
        echo FAIL\n\
    fi\n\
else\n\
    mv @@RUNSCRIPT.busy @@RUNSCRIPT \n\
    echo FAIL\n\
fi\n\
"

head='Jobs'+tag
if not os.path.exists(head ):
    os.system('mkdir '+head)

n=int(len(sourceFileList)/FILES_PER_JOB) + 1
if n < NJOBS:
    NJOBS=n
print("Making ",NJOBS," Jobs ")

njobs=0
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
    
    cfgFileName='flist.cfg'
    cfgFile=open(dirName+'/'+cfgFileName,'w')
    tmp=""
    for j in range(FILES_PER_JOB):
      tmp+=sourceFileList.pop(0)[:-1]+"\n"
    tmp=configurationTxt.replace("@@FNAMES",tmp[:-1])
    tmp=tmp.replace("@@IDX",str(i))
    tmp=tmp.replace("@@MAXEVENTS",str(NEVENTS_PER_JOB))
    cfgFile.write(tmp)
    cfgFile.close()   
    
    runScriptName=dirName+'/'+tag+'run'+str(i)+'.sh'
    if os.path.exists(runScriptName+'.sucess'):
       os.system('rm '+runScriptName+'.sucess')
    runScript=open(runScriptName,'w')
    tmp=runScriptTxt.replace("@@DIRNAME",dirName)
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
condorScript.close()
