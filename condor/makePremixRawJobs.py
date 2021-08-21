#!/usr/bin/env python3

import os

NJOBS=120
NEVETS_PER_JOBS = 20000
PU_FNAMES_PER_JOB=5
PU_NEVENTS=-1

cfg_fname='BPH-RunIIFall18GS-00217_1_cfg.py'
puPremixRaw_cfg='BPH-RunIIAutumn18DRPremix-00148_1_cfg.py'
puFileList ="PUFnames.txt"

flowFileNameTemplate='file:BPH-RunIIFall18GS-00217_@@IDX'

pwd=os.environ['PWD']
proxy_path=os.environ['X509_USER_PROXY']

xrdRedirector="root://cms-xrd-global.cern.ch/"

PUFnames=open(puFileList,'r')
pileUpFiles=PUFnames.readlines()
PUFnames.close()

cfg_=open(cfg_fname,'r')
cfg=cfg_.readlines()

premixCfg_=open(puPremixRaw_cfg,'r')
premixCfg=premixCfg_.readlines()

if not os.path.exists('Jobs'):
    os.system('mkdir Jobs')
print("Making ",NJOBS," Jobs ")
for i in range(NJOBS):
    dirName= 'Jobs/Job_'+str(i)
    print(i," Job Made")
    if os.path.exists(dirName):
     #   os.system('rm  '+dirName+'/*.py')
     #   os.system('rm  '+dirName+'/*.sh')
        k=True
    else:
        os.system('mkdir '+dirName)
    

    #TODO : make gensim fout name to be based on flowFileNameTemplate
    flowFileName_GS_OUT=flowFileNameTemplate.replace("@@IDX",str(i)) + '.root'
    ## GEN SIM STEP
    runScriptName=dirName+'/run.sh'
    cfgFileName=dirName+'/cmsConfig.py'
    cfgFile=open(cfgFileName,'w')
    for l in cfg:
        if '@@COUNT' in l:
            l=l.replace('@@COUNT',str(NEVETS_PER_JOBS))
        if '@@IDX' in l:
            l=l.replace('@@IDX',str(i))
        cfgFile.write(l)
    cfgFile.close()   
    
    runScript=open(runScriptName,'w')
    runScript.write('#!/bin/bash\n')
    runScript.write('set -x\n')
    runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh \n')
    runScript.write('export X509_USER_PROXY='+proxy_path+'\n')
    runScript.write('cd '+pwd+'/'+dirName+'\n')
    runScript.write('eval `scramv1 runtime -sh`'+'\n')
    runScript.write('cmsRun cmsConfig.py'+'\n')
    runScript.close()
    os.system('chmod +x '+runScriptName)

   ## PU PREMIX Step
    flowFileName_PUPreMix_IN =flowFileName_GS_OUT
    flowFileName_PUPreMix_OUT=flowFileNameTemplate.replace("@@IDX",str(i)) + '_puPremixRaw.root'
    runScriptName=dirName+'/premixRaw_run.sh'
    cfgFileName=dirName+'/premixRaw_cmsConfig.py'
    cfgFile=open(cfgFileName,'w')
    for l in premixCfg:
        if '@@COUNT' in l:
            l=l.replace('@@COUNT',str(PU_NEVENTS))
        if '@@GS_SOURCE' in l:
            l=l.replace('@@GS_SOURCE',flowFileName_GS_OUT)
        if '@@RAW_OUT' in l:
            l=l.replace('@@RAW_OUT',flowFileName_PUPreMix_OUT)
        if '@@PU_FLIST' in l:
             tmp=" "
             if len(pileUpFiles)<PU_FNAMES_PER_JOB:
                 print("PU fname count less than required .. assigning the PU files again ")
                 PUFnames=open(puFileList,'r')
                 pileUpFiles_=PUFnames.readlines()
                 PUFnames.close()
                 for ff in pileUpFiles_:
                     pileUpFiles.append(ff)
             
             for j in range(PU_FNAMES_PER_JOB):
                tmp+= "'"+xrdRedirector+pileUpFiles.pop(0)[:-1]+"',"
             tmp=tmp[:-1]
             l=l.replace("@@PU_FLIST",tmp)
        cfgFile.write(l)
    cfgFile.close()   
    
    runScript=open(runScriptName,'w')
    runScript.write('#!/bin/bash\n')
    runScript.write('set -x\n')
    runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh \n')
    runScript.write('export X509_USER_PROXY='+proxy_path+'\n')
    runScript.write('cd '+pwd+'/'+dirName+'\n')
    runScript.write('eval `scramv1 runtime -sh`'+'\n')
    runScript.write('cmsRun premixRaw_cmsConfig.py'+'\n')
    runScript.close()
    os.system('chmod +x '+runScriptName)

 
