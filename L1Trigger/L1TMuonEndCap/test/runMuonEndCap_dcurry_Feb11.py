## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

# -*- coding: utf-8 -*-

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands

process = cms.Process("L1TMuonEmulation")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

#process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.L1Emulator_cff')

process.load("Configuration.StandardSequences.RawToDigi_cff")
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")

process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load("Configuration.StandardSequences.Generator_cff")
process.load( "HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi" )


# PostLS1 geometry used
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
#process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

# Muons
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

# Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.options = cms.untracked.PSet(
#    SkipEvent = cms.untracked.vstring('ProductNotFound')
)


# Input Source
process.source = cms.Source('PoolSource',
                            fileNames = cms.untracked.vstring(
        
        # For efficiencies
        #'/store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-PromptReco-v4/000/258/159/00000/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/267ACC62-DD6B-E511-92AD-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/2E3BE2CD-E86B-E511-A777-02163E01211D.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/58353698-B56B-E511-9FFD-02163E011F32.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/68266258-D26B-E511-BE87-02163E014126.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/745C2AB6-B56B-E511-B15A-02163E01297A.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/90BBED7C-DD6B-E511-973F-02163E0146B8.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/94E134E9-D26B-E511-A2C2-02163E0143F8.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/A81C747E-D26B-E511-BC71-02163E011A97.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/C697122A-BD6B-E511-8B30-02163E01397A.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/D64E75BB-C56B-E511-975F-02163E0143E4.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/F006B63A-246C-E511-A0DC-02163E011FE7.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/FCCAA76B-D26B-E511-A660-02163E01348B.root'
        
        # for rate
        
        'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/MWGR/RAW/2016_03_09/266423/106D48F5-71E6-E511-B4B6-02163E012236.root'
        
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/12455212-1E85-E511-8913-02163E014472.root'
        
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/0C2E1287-F284-E511-8745-02163E0144A3.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/12455212-1E85-E511-8913-02163E014472.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/1A70F5B3-B084-E511-BC12-02163E0134A5.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/1E89626C-CD84-E511-993A-02163E0133ED.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/244B7B71-D384-E511-AF2B-02163E011CF1.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/24884BD7-C984-E511-A85C-02163E014424.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/2876E111-C684-E511-A68F-02163E01460E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/2A4B1D15-C484-E511-B8AE-02163E012218.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/2AF2EA22-FB84-E511-8626-02163E012062.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/2C800F1B-B384-E511-8A9A-02163E014411.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3475EA27-CE84-E511-9E7D-02163E01432E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3861EB8D-BD84-E511-968E-02163E01446B.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3A5AFE77-CA84-E511-A2A5-02163E0146B9.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3C0513DB-B484-E511-86FD-02163E0126F9.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3CCCCFE1-CA84-E511-9DE0-02163E0142C1.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/3ECE4746-C784-E511-B27C-02163E011AE3.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/4AC0D90E-C484-E511-AB6C-02163E01386D.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/52849AE7-D184-E511-9254-02163E01417C.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/52905784-B784-E511-B8D8-02163E0141A7.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/52DC4A2A-C384-E511-B413-02163E012AB8.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/5EE28464-C984-E511-A7A0-02163E01386D.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/60204D37-E484-E511-96E1-02163E011D48.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/60E2EF3B-B284-E511-BA69-02163E0140EC.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/62956BBF-C684-E511-BECA-02163E0120DC.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/6AB4196C-CC84-E511-833B-02163E014157.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/6E0DF678-AE84-E511-9B5D-02163E014721.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/6E3535B9-D484-E511-93B5-02163E011CF1.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/744F6AC2-C184-E511-8871-02163E01410A.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/748C4EEC-A884-E511-A77E-02163E014560.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/78574E47-AC84-E511-946E-02163E0133E2.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/7C0DC2AE-D584-E511-AB8B-02163E0134F1.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/7CDF0347-CA84-E511-8518-02163E01260E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/7CEE7BC7-B384-E511-AE6C-02163E0141A7.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/82ED927E-D184-E511-81D6-02163E014164.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/84944699-C884-E511-AAAD-02163E01260E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/84FCD10E-C484-E511-A082-02163E011C1A.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/88709E9F-D084-E511-9473-02163E0124C9.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/887CB6DB-C584-E511-89F0-02163E014349.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/C8144BF2-C484-E511-846A-02163E01442E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/D6031C52-BF84-E511-823B-02163E0134A5.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/D6E2BC7E-C784-E511-B7F1-02163E01188D.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/D814B131-BA84-E511-969C-02163E014157.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/D8B3AC1A-AA84-E511-9A2B-02163E0141C9.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/DE25134A-DD84-E511-8167-02163E014709.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/E27FC49C-C684-E511-868C-02163E0146A1.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/E65C0F06-C884-E511-A311-02163E01244F.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/EABC03F8-C884-E511-B4A9-02163E01455E.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/EE760293-CB84-E511-BDC9-02163E013765.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/F0684471-C184-E511-ADF4-02163E011DF2.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/F2650D6D-BC84-E511-BCB6-02163E0134B9.root',
        #'/store/data/Run2015D/DoubleEG/RAW-RECO/ZElectron-PromptReco-v4/000/260/627/00000/F4C68B83-CE84-E511-B26D-02163E0133A5.root',

        )
	                    )

# Global Tags
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '')


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
                                #leg_gmtTag   = cms.InputTag("gtDigis"),
                                printLevel   = cms.untracked.int32(-1),
                                NoTagAndProbe= cms.untracked.bool(True),
                                isMC         = cms.untracked.int32(0),
                                outputDIR    = cms.string('TEST')
                                 ) 


# Output File
process.TFileService = cms.Service(
    "TFileService",
    #fileName = cms.string("root://eoscms//eos/cms/store/user/dcurry/EMTF/EMTF_effStudies_ZMu-PromptReco_v5.root")
    fileName = cms.string("root://eoscms//eos/cms/store/user/dcurry/EMTF/EMTF_MWGR_v3.root")
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
