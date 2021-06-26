#!/usr/bin/env python3

import os

NJOBS=32
ZERO_OFFSET=0
NEVETS_PER_JOBS = 10000
pwd=os.environ['PWD']
HOME=os.environ['HOME']

cfg_fname='genSim_cfg.py'
cfg_=open(cfg_fname,'r')
cfg=cfg_.readlines()


randomSeederFragment='\n # Adding the randomizer part \n\
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\n\
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\n\
randSvc.populate()\n'

#required if same GEN Files have to be used easily for sim in another release/geometry/ ..
storeTheGenFilterInfo="\n# Adding the generator module data persistance \nprocess.RAWSIMoutput.outputCommands.append('keep *_generator_*_*')\n"


if not os.path.exists('Jobs'):
    os.system('mkdir Jobs')
print("Making ",NJOBS," Jobs ")
for ii in range(NJOBS):
    i=ii+ZERO_OFFSET
    dirName= 'Jobs/Job_'+str(i)
    print(i," Job Made")
    if os.path.exists(dirName):
     #   os.system('rm  '+dirName+'/*.py')
     #   os.system('rm  '+dirName+'/*.sh')
        k=True
    else:
        os.system('mkdir '+dirName)
    runScriptName=dirName+'/run'+str(i)+'.sh'
    cfgFileName=dirName+'/cmsConfig.py'

    cfgFile=open(cfgFileName,'w')
    for l in cfg:
        if '98789' in l:
            l=l.replace('98789',str(NEVETS_PER_JOBS))
        if '@@IDX' in l:
            l=l.replace('@@IDX',str(i))
        cfgFile.write(l)
    cfgFile.write(randomSeederFragment)
    cfgFile.write(storeTheGenFilterInfo)
    cfgFile.close()   
    
    runScript=open(runScriptName,'w')
    runScript.write('#!/bin/bash\n')
    runScript.write('export HOME='+HOME+'\n')
    runScript.write('set -x\n')

    runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh \n')
    runScript.write('cd '+pwd+'/'+dirName+'\n')
    runScript.write('eval `scramv1 runtime -sh`'+'\n')
    runScript.write('cmsRun cmsConfig.py'+'\n')
    runScript.close()
    os.system('chmod +x '+runScriptName)
