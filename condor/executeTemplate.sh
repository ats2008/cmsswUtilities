#!/bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
export SCRAM_ARCH=slc7_amd64_gcc820
source /cvmfs/cms.cern.ch/cmsset_default.sh
x=$PWD

#cmsenv -> alias
cd /afs/cern.ch/work/a/athachay/private/bs2mumug/winter_HLT_TDR/CMSSW_11_0_2/src/bs2MuMuGamma/MiniAOD_Analyzer/test/condorGen
eval `scramv1 runtime -sh`
cmsRun cmsrun_!@#$_cfg.py
