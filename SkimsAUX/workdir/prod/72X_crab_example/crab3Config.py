from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'PHYS14_PU20bx25_TTJets'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'treeMaker_stopRA2.py'
config.JobType.allowUndistributedCMSSW = False
config.JobType.pyCfgParams = ['GlobalTag=PHYS14_25_V1', 'cmsswVersion=72X']

config.section_("Data")
config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
#Example config for data
#config.Data.lumiMask = 'json_DCSONLY_Run2015B.txt'
##config.Data.runRange = '193093-193999'
#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter/'
config.Data.publishDataName = 'PHYS14_PU20bx25_PHYS14_25_V1.1-FLAT'
#Use your own username instead of the "lhx". Keep branch tag in the directory name, e.g., PHYS14_720_Dec23_2014.
config.Data.outLFNDirBase = '/store/group/lpcsusyhad/PHYS14_72X_July_2015_v1.1/lhx/PU20bx25_TTJets_MSDecaysCKM_madgraph-tauola/'

config.Data.ignoreLocality = False

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
