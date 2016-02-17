// -*- C++ -*-
//=============================================================
// A package to create Ntuples for the EMTF Emulator
// Package:    CSCplusRPCTrackAnalyzer
// Class:      CSCplusRPCTrackAnalyzer
//
// Written by David Curry
// ============================================================
   
 
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"


// includes to fetch all reguired data products from the edm::Event
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "DataFormats/L1CSCTrackFinder/interface/L1CSCTrackCollection.h"
#include "DataFormats/L1CSCTrackFinder/interface/L1CSCStatusDigiCollection.h"

#include "L1Trigger/CSCCommonTrigger/interface/CSCTriggerGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/RPCDigi/interface/RPCDigiL1Link.h"
#include "DataFormats/RPCRecHit/interface/RPCRecHitCollection.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

// Sector Receiver LUT class to transform wire/strip numbers to eta/phi observables
#include "L1Trigger/CSCTrackFinder/interface/CSCSectorReceiverLUT.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCTFPtLUT.h"
#include <L1Trigger/CSCTrackFinder/interface/CSCTFSPCoreLogic.h>
#include "CondFormats/L1TObjects/interface/L1MuTriggerScales.h"
#include "CondFormats/DataRecord/interface/L1MuTriggerScalesRcd.h"
#include "CondFormats/L1TObjects/interface/L1MuTriggerPtScale.h"
#include "CondFormats/DataRecord/interface/L1MuTriggerPtScaleRcd.h"

#include "DataFormats/L1CSCTrackFinder/interface/L1CSCStatusDigiCollection.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "DataFormats/L1CSCTrackFinder/interface/L1CSCTrackCollection.h"
#include "DataFormats/L1CSCTrackFinder/interface/CSCTriggerContainer.h"
#include "DataFormats/L1CSCTrackFinder/interface/TrackStub.h"

#include "TMath.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/DataEvtSummaryHandler.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>

//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h"
//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrackFwd.h"
#include <L1Trigger/CSCTrackFinder/interface/CSCTFSectorProcessor.h>
#include <L1Trigger/CSCTrackFinder/src/CSCTFDTReceiver.h>
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/L1TMuon/interface/EMTF/InternalTrack.h"

// === My Functions ====
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillAllLCTs.h"
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillEMTFTracks.h"
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillGenMuons.h"
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillRecoMuons.h"
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillMuonSegments.h"
#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/fillLeg_CSCTFTracks.h"


// class declaration
using namespace edm;
using namespace reco;
using namespace std;
using namespace L1TMuon;
using namespace csc;

class CSCTFSectorProcessor;

class CSCplusRPCTrackAnalyzer : public edm::EDAnalyzer {
public:
  explicit CSCplusRPCTrackAnalyzer(const edm::ParameterSet&);
  ~CSCplusRPCTrackAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  enum { nEndcaps = 2, nSectors = 6};

private:

  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
  
  int convertRPCsectors(float rpcphi);
  int convertRPCphiBits(float GblPhi, int sector);
  int convertRPCetaBits(float GblEta);
  
  //TSelectionMonitor controlHistos_;
  DataEvtSummaryHandler summaryHandler_;
  
  edm::ESHandle<CSCGeometry> cscGeom;

  
  std::vector<edm::InputTag> moduleLabels;
  std::vector<TString> HLT_name;
  std::vector<int> theBitCorr;
  std::vector<std::string> HLT_triggerObjects;
  HLTConfigProvider hltConfig;
  
  int printLevel;
  bool isMC;
  
  //edm::InputTag muonsTag;
  //edm::InputTag cscSegTag;
  
  // Get the tokem for all input collections
  edm::EDGetTokenT<CSCCorrelatedLCTDigiCollection> cscTPTag_token;
  edm::EDGetTokenT<std::vector<l1t::emtf::InternalTrack>> csctfTag_token;
  edm::EDGetTokenT<reco::MuonCollection> muons_token;
  edm::EDGetTokenT<CSCSegmentCollection> cscSegs_token;
  edm::EDGetTokenT<std::vector<reco::GenParticle>> genTag_token;
  edm::EDGetTokenT<std::vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>> > leg_csctfTag_token;
  
  const L1MuTriggerScales  *scale;
  const L1MuTriggerPtScale *ptScale;
 
 
};

 
CSCplusRPCTrackAnalyzer::CSCplusRPCTrackAnalyzer(const edm::ParameterSet& iConfig) {
  
  csctfTag_token =  consumes<std::vector<l1t::emtf::InternalTrack>>(iConfig.getParameter<edm::InputTag>("csctfTag"));
  cscTPTag_token =  consumes<CSCCorrelatedLCTDigiCollection>(iConfig.getParameter<edm::InputTag>("cscTPTag"));
  genTag_token  =  consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genTag"));
  muons_token   =  consumes<reco::MuonCollection>(iConfig.getParameter<edm::InputTag>("muonsTag"));
  cscSegs_token = consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("cscSegTag"));
  leg_csctfTag_token =  consumes<std::vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>>>(iConfig.getParameter<edm::InputTag>("leg_csctfTag"));

  printLevel = iConfig.getUntrackedParameter<int>("printLevel",0);
  
  // Output File
  edm::Service<TFileService> fs;
  summaryHandler_.initTree(  fs->make<TTree>("tree","Event Summary") );
  TFileDirectory baseDir=fs->mkdir(iConfig.getParameter<std::string>("outputDIR"));
 
  // Is Monte Carlo or not?
  isMC = iConfig.getUntrackedParameter<int>("isMC",0);
}


CSCplusRPCTrackAnalyzer::~CSCplusRPCTrackAnalyzer()
{


}


//
// member functions
//



// ------------ method called for each event  ------------
void CSCplusRPCTrackAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  

  if(printLevel>0) cout << "\n\n =================================== NEW EVENT ===================================== " << endl;

  // Get the CSC Geometry
  iSetup.get<MuonGeometryRecord>().get(cscGeom);

  summaryHandler_.initStruct();
  DataEvtSummary_t &ev = summaryHandler_.getEvent();

  //event header
  ev.run    = iEvent.id().run();
  ev.lumi   = iEvent.luminosityBlock();
  ev.event  = iEvent.id().event();
  



  // =========================================================================================================

  if (printLevel > 0 )
    cout << "\n===================== FILLING All LCTs ========================\n"
         <<   "============================================================\n" << endl;
  
  edm::Handle<CSCCorrelatedLCTDigiCollection> lcts;
  iEvent.getByToken(cscTPTag_token, lcts);	 
  
  if ( lcts.isValid() )
    fillAllLCTs(ev, lcts, printLevel);
  
  else cout << "\t----->Invalid CSC LCT collection... skipping it\n";
  
  // =========================================================================================================
  
  

  if (printLevel > 0 )
    
    cout << "\n===================== FILLING All EMTF CSCTF Tracks ========================\n"
         <<   "=======================================================================\n" << endl;
  
  edm::Handle<std::vector<l1t::emtf::InternalTrack> > tracks;
  iEvent.getByToken(csctfTag_token, tracks);
  
  if ( tracks.isValid() )
    fillEMTFTracks(ev, tracks, printLevel);
  
  else cout << "\t----->Invalid EMTF Track collection... skipping it\n";


  // =========================================================================================================
 

  if (printLevel > 0 )
    cout << "\n===================== FILLING All Legacy CSCTF Tracks ========================\n"
         <<   "=======================================================================\n" << endl;

  edm::Handle<vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi> > >> leg_tracks;
  iEvent.getByToken(leg_csctfTag_token, leg_tracks);

  if ( leg_tracks.isValid() )
    fillLeg_CSCTFTracks(ev, leg_tracks, printLevel);

  else cout << "\t----->Invalid Legacy Track collection... skipping it\n";

  // =========================================================================================================

  
  
  if (isMC) {
    
    if (printLevel > 0 )
      cout << "\n===================== FILLING Gen Muons ========================\n"
	   <<   "================================================================\n" << endl;
    
    edm::Handle< vector<reco::GenParticle> > genParticles;
    iEvent.getByToken(genTag_token, genParticles);
    
    if ( genParticles.isValid() )
      fillGenMuons(ev, genParticles, printLevel);
    
    else cout << "\t----->Invalid Track collection... skipping it\n";
  }
  
  
  if (!isMC) {
    
    if(printLevel>0) 
      cout << "\n===================== FILLING RECO Muons ========================\n"
	   <<   "================================================================\n" << endl;
    
    
    edm::Handle<reco::MuonCollection>  muons;
    iEvent.getByToken(muons_token, muons);
    
    //edm::Handle<reco::BeamSpot> beamSpot;
    //iEvent.getByLabel("offlineBeamSpot", beamSpot);
    
    if ( muons.isValid() )
      fillRecoMuons(ev, muons, printLevel);
    
    else cout << "\t----->Invalid RECO Muon collection... skipping it\n";
    
    
    
    if(printLevel>0)
      cout << "\n===================== FILLING RECO Muons Segments ========================\n"
           <<   "================================================================\n" << endl;
    
    edm::Handle<CSCSegmentCollection> cscSegments;
    iEvent.getByToken(cscSegs_token, cscSegments);
    
    if ( cscSegments.isValid() && lcts.isValid())
      fillSegmentsMuons(ev, muons, cscSegments, cscGeom, lcts, printLevel);
    // leaving out csc tracks for now.  Add back in later
    
    else cout << "\t----->Invalid RECO Muon SEGMENT collection... skipping it\n";

  }
  
  // ============================================================================



  /*
  // Initialize CSCTF pT LUTs
  ESHandle< L1MuTriggerScales > scales;
  iSetup.get< L1MuTriggerScalesRcd >().get(scales);
  scale = scales.product();
  
  ESHandle< L1MuTriggerPtScale > ptscales;
  iSetup.get< L1MuTriggerPtScaleRcd >().get(ptscales);
  ptScale = ptscales.product();
    
  // set geometry pointer
  edm::ESHandle<CSCGeometry> pDD;
  iSetup.get<MuonGeometryRecord>().get( pDD );
  CSCTriggerGeometry::setGeometry(pDD);
  */
  

								       
  // =========================================================================
  // End Event methods

  // Fill the tree
  summaryHandler_.fillTree();
  
  // Clear all objects from memory
  summaryHandler_.resetStruct();

} // end analyze



// ------------ method called once each job just before starting event loop  ------------
void
CSCplusRPCTrackAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
CSCplusRPCTrackAnalyzer::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
/*
void
CSCplusRPCTrackAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
CSCplusRPCTrackAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
CSCplusRPCTrackAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
CSCplusRPCTrackAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// Cluster sector must be determined manually.
// Sometimes the rpc sector and the cluster sector are not the same
int
CSCplusRPCTrackAnalyzer::convertRPCsectors(float rpcphi)
{
    if (     rpcphi >= 15.*M_PI/180. && rpcphi < 75.*M_PI/180.)
        return 1;
    else if (rpcphi >= 75.*M_PI/180. && rpcphi < 135.*M_PI/180.)
        return 2;
    else if (rpcphi >= 135.*M_PI/180. && rpcphi < 195.*M_PI/180.)
        return 3;
    else if (rpcphi >= 195.*M_PI/180. && rpcphi < 255.*M_PI/180.)
        return 4;
    else if (rpcphi >= 255.*M_PI/180. && rpcphi < 315.*M_PI/180.)
        return 5;
    else if (rpcphi >= 315.*M_PI/180. || rpcphi < 15.*M_PI/180.)
        return 6;
    else
        return -1;
}


// convert RPC global phi to CSC LUT phi Bits, only for RPC
int
CSCplusRPCTrackAnalyzer::convertRPCphiBits(float GblPhi, int sector)
{
    float phiBit = -999;
    if (sector == 1)
        phiBit = (GblPhi - 0.243) / 1.0835;
    else if (sector == 2)
        phiBit = (GblPhi - 1.2914) / 1.0835;
    else if (sector == 3) {
        if (GblPhi > 0) phiBit = (GblPhi - 2.338) / 1.0835;
        else {
            float sector_distance = abs(GblPhi + 3.1416) + (3.1416 - 2.338);
            phiBit = sector_distance / 1.0835;
        }
    } else if (sector == 4)
        phiBit = (GblPhi + 2.898) / 1.0835;
    else if (sector == 5)
        phiBit = (GblPhi + 1.8507) / 1.0835;
    else if (sector == 6) {
        if (GblPhi < 0) phiBit = (GblPhi + 0.803) / 1.0835;
        else {
            float sector_distance = GblPhi + 0.803;
            phiBit = sector_distance / 1.0835;
        }
    }

    phiBit = phiBit*4096;

    return static_cast<int>(phiBit);
}


// convert global Eta to Eta Bit for pT assignment, for both CSC and RPC
int
CSCplusRPCTrackAnalyzer::convertRPCetaBits(float GblEta)
{
    double theEtaBinning = (CSCTFConstants::maxEta - CSCTFConstants::minEta)/(CSCTFConstants::etaBins);
    int theEta_ = (GblEta-CSCTFConstants::minEta)/theEtaBinning;
    //theEta_*theEtaBinning + CSCTFConstants::minEta
    return theEta_;
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
CSCplusRPCTrackAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(CSCplusRPCTrackAnalyzer);
