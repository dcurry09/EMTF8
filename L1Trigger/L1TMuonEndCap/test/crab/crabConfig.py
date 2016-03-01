## Before running:
## source /cvmfs/cms.cern.ch/crab3/crab.sh
## voms-proxy-init --voms cms --valid 168:00 (for 7-day validity)
## crab submit -c crabConfig.py
## crab status -d 

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_('General')
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.psetName = 'runMuonEndCap_dcurry_Feb11.py'
config.JobType.outputFiles = ['EMTF.root']
config.JobType.pluginName = 'Analysis'

config.section_('Data')
config.Data.inputDBS = 'global'
config.Data.inputDataset = '/ZeroBias1/Run2015D-PromptReco-v4/RECO'
config.Data.useParent = True

config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10
#config.Data.totalUnits  = 2

config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
config.Data.runRange = '259721'

config.Data.outLFNDirBase = '/store/user/dcurry/EMTF/rate_v10/'

config.section_('User')

config.section_('Site')

config.Site.storageSite = 'T2_CH_CERN'
