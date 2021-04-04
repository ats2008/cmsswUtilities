#import CRABClient
#from WMCore.Configuration import Configuration
#config = Configuration()

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'BsToMuMuGamma_GEN-SIM-DIGI-RAW'
config.General.workArea = 'crab_space'
config.General.transferOutputs = True

config.JobType.inputFiles = ['code.tar']
config.JobType.scriptExe = 'gsdrExecute.sh'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfg2023_GSDR.py'
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 500

config.Data.inputDataset = '/BsToMuMuGamma_BMuonFilter_SoftQCDnonD_TuneCP5_14TeV-pythia8-evtgen/athachay-BsToMuMuGamma_2023GENSIM-04df5e51c65593a825d1e8ca6d962a22/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.publication = True
config.Data.outputDatasetTag = 'BsToMuMuGamma_2023GENSIM'
config.Site.storageSite = 'T2_IN_TIFR'
