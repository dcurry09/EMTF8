## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

# -*- coding: utf-8 -*-

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands

process = cms.Process("L1TMuonEmulation")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
#process.load('Configuration.StandardSequences.L1Emulator_cff')
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load("Configuration.StandardSequences.Generator_cff")
process.load( "HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi" )


# PostLS1 geometry used
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')

# Muons
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

# Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))


# Input Source
process.source = cms.Source('PoolSource',
                            fileNames = cms.untracked.vstring(
        #'/store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-PromptReco-v4/000/258/159/00000/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/267ACC62-DD6B-E511-92AD-02163E011F4B.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/2E3BE2CD-E86B-E511-A777-02163E01211D.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/58353698-B56B-E511-9FFD-02163E011F32.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/68266258-D26B-E511-BE87-02163E014126.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/745C2AB6-B56B-E511-B15A-02163E01297A.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/90BBED7C-DD6B-E511-973F-02163E0146B8.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/94E134E9-D26B-E511-A2C2-02163E0143F8.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/A81C747E-D26B-E511-BC71-02163E011A97.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/C697122A-BD6B-E511-8B30-02163E01397A.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/D64E75BB-C56B-E511-975F-02163E0143E4.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/F006B63A-246C-E511-A0DC-02163E011FE7.root',
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/FCCAA76B-D26B-E511-A660-02163E01348B.root'
        
        #'/cms/data/store/data/Run2015D/ZeroBias/RAW/v1/000/259/721/00000/0A2BA199-5878-E511-B77E-02163E01190D.root',
        #'/cms/data/store/mc/Fall13dr/MuPlus_Pt-1to150_PositiveEndcap-gun/GEN-SIM-RAW/tsg_PU40bx25_POSTLS162_V2-v1/20000/04643A9D-F382-E311-9D3C-0017A4770C34.root'
        )
	                    )

# Global Tags
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '')


####Event Setup Producer
process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff')
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
   toGet = cms.VPSet(
        ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/
        cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
                 data = cms.vstring('L1TMuonEndcapParams'))
        ),
   verbose = cms.untracked.bool(True)
)

process.content = cms.EDAnalyzer("EventContentAnalyzer")

####EMTF Emulator
process.load('L1Trigger.L1TMuonEndCap.simMuonEndCapDigis_cfi')

process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.L1TMuonSeq = cms.Sequence( 
      process.csctfDigis +
      #process.esProd +          
      process.simEmtfDigis 
    )


# # Load the Ntuplizer
process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
                                 process.MuonServiceProxy,
                                 muonsTag     = cms.InputTag("muons", ""),
                                 genTag       = cms.InputTag("genParticles"),
                                 csctfTag     = cms.InputTag("simEmtfDigis", "EMTF"),
                                 leg_csctfTag = cms.InputTag("csctfDigis"),
                                 cscTPTag     = cms.InputTag("csctfDigis"),
                                 cscSegTag    = cms.InputTag("cscSegments"),
                                 printLevel   = cms.untracked.int32(-1),
                                 isMC         = cms.untracked.int32(0),
                                 outputDIR   = cms.string('TEST')
                                 )


# Output File
process.TFileService = cms.Service(
    "TFileService",
    #fileName = cms.string("TEST_EMTF.root")
    fileName = cms.string("root://eoscms//eos/cms/store/user/dcurry/EMTF/TEST_EMTF_v6.root")
    )


process.L1TMuonPath = cms.Path(
    process.L1TMuonSeq +
    process.ntuple
    )

## Keep only a few outputs - AWB 11.02.16
#outCommands=cms.untracked.vstring(                                                                                             
#    'keep l1tRegionalMuonCandBXVector_simEmtfDigis_EMTF_L1TMuonEmulation', 
#    'keep cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_simCsctfTrackDigis__L1TMuonEmulation',
#    'keep cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_csctfDigis__L1TMuonEmulation',               
#    'keep recoMuons_muons__RECO',
#    'keep *_*_EMTF_*',
#    'keep *_*_*_EMTF',
#    )

outCommands = cms.untracked.vstring('keep *')


process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string("l1temtf_superprimitives1.root"),
                               outputCommands = outCommands
                               )

#process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.L1TMuonPath)

#process.schedule.extend([process.output_step])

from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
process = customise_csc_PostLS1(process)
