// -*- C++ -*-
//=============================================================
// A package to create Ntuples for the EMTF Emulator
// Package:    CSCplusRPCTrackAnalyzer
// Class:      CSCplusRPCTrackAnalyzer
//
// Written by David Curry
// ============================================================

//   
 
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

#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h"

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
  bool NoTagAndProbe;
  
  // Get the tokem for all input collections
  edm::EDGetTokenT<CSCCorrelatedLCTDigiCollection> cscTPTag_token;
  edm::EDGetTokenT<std::vector<l1t::emtf::InternalTrack>> csctfTag_token;
  edm::EDGetTokenT<reco::MuonCollection> muons_token;
  edm::EDGetTokenT<CSCSegmentCollection> cscSegs_token;
  edm::EDGetTokenT<std::vector<reco::GenParticle>> genTag_token;
  edm::EDGetTokenT<std::vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>> > leg_csctfTag_token;
  edm::EDGetTokenT<L1MuGMTReadoutCollection> leg_gmtTag_token;

  CSCSectorReceiverLUT* srLUTs_[5][2];
  CSCTFSPCoreLogic* core_;
  
  const L1MuTriggerScales  *scale;
  const L1MuTriggerPtScale *ptScale;

  // To set the phi and eta values of LCTs
  std::unique_ptr<GeometryTranslator> geom;

  // From http://www.phys.ufl.edu/~mrcarver/forAD/L1TMuonUpgradedTrackFinder.h
  const float ptscaleMatt[33] = {
    -1.,   0.0,   1.5,   2.0,   2.5,   3.0,   3.5,   4.0,
    4.5,   5.0,   6.0,   7.0,   8.0,  10.0,  12.0,  14.0,
    16.0,  18.0,  20.0,  25.0,  30.0,  35.0,  40.0,  45.0,
    50.0,  60.0,  70.0,  80.0,  90.0, 100.0, 120.0, 140.0, 1.E6 };
    
};

 
CSCplusRPCTrackAnalyzer::CSCplusRPCTrackAnalyzer(const edm::ParameterSet& iConfig) {
  
  csctfTag_token =  consumes<std::vector<l1t::emtf::InternalTrack>>(iConfig.getParameter<edm::InputTag>("csctfTag"));
  cscTPTag_token =  consumes<CSCCorrelatedLCTDigiCollection>(iConfig.getParameter<edm::InputTag>("cscTPTag"));
  genTag_token  =  consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genTag"));
  muons_token   =  consumes<reco::MuonCollection>(iConfig.getParameter<edm::InputTag>("muonsTag"));
  cscSegs_token = consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("cscSegTag"));
  leg_csctfTag_token =  consumes<std::vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>>>(iConfig.getParameter<edm::InputTag>("leg_csctfTag"));
  leg_gmtTag_token = consumes<L1MuGMTReadoutCollection>(iConfig.getParameter<edm::InputTag>("leg_gmtTag"));
  

  printLevel = iConfig.getUntrackedParameter<int>("printLevel",0);
  
  NoTagAndProbe = iConfig.getUntrackedParameter<bool>("NoTagAndProbe", true);
  
  // HERE

  // Output File
  edm::Service<TFileService> fs;
  summaryHandler_.initTree(  fs->make<TTree>("tree","Event Summary") );
  TFileDirectory baseDir=fs->mkdir(iConfig.getParameter<std::string>("outputDIR"));
 
  // Is Monte Carlo or not?
  isMC = iConfig.getUntrackedParameter<int>("isMC",0);


  bzero(srLUTs_ , sizeof(srLUTs_));
  int sector=1;    // assume SR LUTs are all same for every sector
  bool TMB07=true; // specific TMB firmware
  // Create a pset for SR/PT LUTs: if you do not change the value in the
  // configuration file, it will load the default minitLUTs
  edm::ParameterSet srLUTset;
  srLUTset.addUntrackedParameter<bool>("ReadLUTs", false);
  srLUTset.addUntrackedParameter<bool>("Binary",   false);
  srLUTset.addUntrackedParameter<std::string>("LUTPath", "./");

  // positive endcap
  int endcap = 1;
  for(int station=1,fpga=0; station<=4 && fpga<5; station++)
    {
      if(station==1)
        for(int subSector=0; subSector<2 && fpga<5; subSector++)
          srLUTs_[fpga++][1] = new CSCSectorReceiverLUT(endcap,sector,subSector+1,
                                                        station, srLUTset, TMB07);
      else
        srLUTs_[fpga++][1]   = new CSCSectorReceiverLUT(endcap,  sector,   0,
                                                        station, srLUTset, TMB07);
    }

  // negative endcap
  endcap = 2;
  for(int station=1,fpga=0; station<=4 && fpga<5; station++)
    {
      if(station==1)
        for(int subSector=0; subSector<2 && fpga<5; subSector++)
          srLUTs_[fpga++][0] = new CSCSectorReceiverLUT(endcap,sector,subSector+1,
                                                        station, srLUTset, TMB07);
      else
        srLUTs_[fpga++][0]   = new CSCSectorReceiverLUT(endcap,  sector,   0,
                                                        station, srLUTset, TMB07);
    }
  // -----------------------------------------------------------------------------

  geom.reset(new GeometryTranslator());




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

  bool tagAndProbeExist = false;

  geom->checkAndUpdateGeometry(iSetup);
  // Get the CSC Geometry
  iSetup.get<MuonGeometryRecord>().get(cscGeom);

  summaryHandler_.initStruct();
  DataEvtSummary_t &ev = summaryHandler_.getEvent();

  //event header
  ev.run    = iEvent.id().run();
  ev.lumi   = iEvent.luminosityBlock();
  ev.event  = iEvent.id().event();
  
  // Legacy pT look up tables
  // Initialize CSCTF pT LUTs
  ESHandle< L1MuTriggerScales > scales;
  iSetup.get< L1MuTriggerScalesRcd >().get(scales);
  scale = scales.product();

  ESHandle< L1MuTriggerPtScale > ptscales;
  iSetup.get< L1MuTriggerPtScaleRcd >().get(ptscales);
  ptScale = ptscales.product();

  //ptLUTs_ = new CSCTFPtLUT(ptLUTset, scale, ptScale);
  // Standard Pt LUTs
  edm::ParameterSet ptLUTset;
  ptLUTset.addParameter<bool>("ReadPtLUT", false);
  ptLUTset.addParameter<bool>("isBinary",  false);
  CSCTFPtLUT ptLUT(ptLUTset, scale, ptScale);

  // =========================================================================================================

  if (printLevel > 0 )
    cout << "\n===================== FILLING All LCTs ========================\n"
         <<   "============================================================\n" << endl;
  
  edm::Handle<CSCCorrelatedLCTDigiCollection> lcts;
  iEvent.getByToken(cscTPTag_token, lcts);	 


  
  if ( lcts.isValid() ) {
    
    // Access the global phi/eta from here
    std::vector<L1TMuon::TriggerPrimitive> LCT_collection;
    
    auto chamber = lcts->begin();
    auto chend  = lcts->end();
    for( ; chamber != chend; ++chamber ) {
      auto digi = (*chamber).second.first;
      auto dend = (*chamber).second.second;
      for( ; digi != dend; ++digi ) {
	TriggerPrimitive trigPrimTemp = TriggerPrimitive((*chamber).first,*digi);
	trigPrimTemp.setCMSGlobalPhi( geom->calculateGlobalPhi(trigPrimTemp) );
        trigPrimTemp.setCMSGlobalEta( geom->calculateGlobalEta(trigPrimTemp) );
        LCT_collection.push_back(trigPrimTemp);
      }
    }
    
    fillAllLCTs(ev, LCT_collection, printLevel);
    //fillAllLCTs(ev, lcts, printLevel, srLUTs_, scale, ptScale);
  }

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

  // GMT CSCTF track info for cross checks
  edm::Handle<L1MuGMTReadoutCollection> gmtReadoutCollection;
  iEvent.getByToken(leg_gmtTag_token, gmtReadoutCollection);

  edm::Handle<vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi> > >> leg_tracks;
  iEvent.getByToken(leg_csctfTag_token, leg_tracks);

  std::vector<L1MuGMTReadoutRecord> gmt_records = gmtReadoutCollection->getRecords();
  std::vector<L1MuGMTReadoutRecord>::const_iterator iReadRec;
  for(iReadRec = gmt_records.begin(); iReadRec != gmt_records.end(); iReadRec++) {

    std::vector<L1MuRegionalCand>::const_iterator iCand;
    std::vector<L1MuRegionalCand> gmtCand;

    if(iReadRec->getBxInEvent() == 0)
      //std::cout << "GMT event BX number is " << iReadRec->getBxNr() << std::endl;

    gmtCand = iReadRec->getCSCCands();

    for(iCand = gmtCand.begin(); iCand != gmtCand.end(); iCand++) {
      if ( abs( (*iCand).etaValue() ) > 1.2 ) {

	if (printLevel > 1) {
	  std::cout << "gmtCand etaValue() = " << (*iCand).etaValue() << std::endl;
	  std::cout << "gmtCand phiValue() = " << (*iCand).phiValue() << std::endl;
	  std::cout << "gmtCand ptValue() = " << (*iCand).ptValue() << std::endl;
	  std::cout << "gmtCand pt_packed() = " << (*iCand).pt_packed() << std::endl;
	}

	ev.legGMT_trkPt  -> push_back((*iCand).ptValue());
	ev.legGMT_trkEta -> push_back((*iCand).etaValue());
	ev.legGMT_trkPhi -> push_back((*iCand).phiValue());

      }
    }
  }


  if ( leg_tracks.isValid() ) {

    int nTrks = 0;
    for(std::vector<std::pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>>::const_iterator lt = leg_tracks->begin();lt != leg_tracks->end();lt++){

      if (nTrks > MAXTRK-1) break;
    
      float eta = 0.9 + 0.05*(lt->first.eta_packed()) + 0.025;
      unsigned sector = lt->first.sector();
      float phi = (0.05217*lt->first.localPhi()) + (sector-1)*1.1 + 0.0218;//*(3.14159265359/180)
      if(phi > 3.14159) phi -= 6.28318;

      int bx = lt -> first.BX();
      

      // Find track pT with Matts LUT
      unsigned pti = 0, quality = 0;
      lt->first.decodeRank(lt->first.rank(),pti,quality);//
      float ptMatt = ptscaleMatt[pti+1];
      

      // PtAddress gives an handle on other parameters
      ptadd thePtAddress(lt->first.ptLUTAddress());

      //Pt needs some more workaround since it is not in the unpacked data
      ptdat thePtData  = ptLUT.Pt(thePtAddress);

      int pt_bit = -999;
      
      // front or rear bit?
      if (thePtAddress.track_fr) {
	pt_bit = thePtData.front_rank&0x1f;
	//csctf_.trQuality.push_back((thePtData.front_rank>>5)&0x3);
	//csctf_.trChargeValid.push_back(thePtData.charge_valid_front);
      } else {
	pt_bit = thePtData.rear_rank&0x1f;
	//csctf_.trQuality.push_back((thePtData.rear_rank>>5)&0x3);
	//csctf_.trChargeValid.push_back(thePtData.charge_valid_rear);
      }

      // convert the Pt in human readable values (GeV/c)
      float pt = ptScale->getPtScale()->getLowEdge(pt_bit);

      
      // For EMTF mode definition
      int mode = 0;
      if(lt->first.me1ID())
	mode |= 8;
      if(lt->first.me2ID())
	mode |= 4;
      if(lt->first.me3ID())
	mode |= 2;
      if(lt->first.me4ID())
	mode |= 1;
      
      if (printLevel > 0) {
	cout << "\n Legacy Track # " << nTrks << endl;
	cout << "============" << endl;
	cout << " Track Pt   : " << pt << endl;
	cout << " Track Eta  : " << eta << endl;
	cout << " Track Phi  : " << phi << endl;
	cout << " Track Mode : " << mode << endl;
	cout << " Track Bx   : " << bx << endl;
      }
      
      ev.leg_trkPt   -> push_back(pt);
      ev.leg_trkEta  -> push_back(eta);
      ev.leg_trkPhi  -> push_back(phi);
      ev.leg_trkMode -> push_back(mode);
      ev.leg_trkBx   -> push_back(bx);

      // debug
      ev.leg_trkPtMatt -> push_back(ptMatt);
      
      
      // For each trk, get the list of its LCTs
      CSCCorrelatedLCTDigiCollection LCTs = lt -> second;
      
      std::vector<L1TMuon::TriggerPrimitive> LCT_collection;
      
      auto chamber = LCTs.begin();
      auto chend  = LCTs.end();
      for( ; chamber != chend; ++chamber ) {
	auto digi = (*chamber).second.first;
	auto dend = (*chamber).second.second;
	for( ; digi != dend; ++digi ) {
	  TriggerPrimitive trigPrimTemp = TriggerPrimitive((*chamber).first,*digi);
	  trigPrimTemp.setCMSGlobalPhi( geom->calculateGlobalPhi(trigPrimTemp) );
	  trigPrimTemp.setCMSGlobalEta( geom->calculateGlobalEta(trigPrimTemp) );
	  LCT_collection.push_back(trigPrimTemp);
	}
      }
      
      int LctTrkId_ = 0; // count number of lcts in event
      
      auto Lct = LCT_collection.cbegin();
      auto Lctend = LCT_collection.cend();
      for( ; Lct != Lctend; Lct++) {
	
	if (LctTrkId_ > MAXTRKLCTS-1) break;
	
	if(Lct->subsystem() != 1) continue;
	
	if (printLevel>1) cout << "\n==== Legacy LCT CSC " << LctTrkId_ << endl;
	
	CSCDetId id                = Lct->detId<CSCDetId>();
	auto lct_station           = id.station();
	auto lct_endcap            = id.endcap();
	auto lct_chamber           = id.chamber();
	uint16_t lct_bx            = Lct->getCSCData().bx;
	int lct_ring               = id.ring();
	int lct_sector             = CSCTriggerNumbering::triggerSectorFromLabels(id);
	int lct_subSector          = CSCTriggerNumbering::triggerSubSectorFromLabels(id);
	uint16_t lct_bx0           = Lct->getCSCData().bx0;
	uint16_t lct_cscID         = Lct->getCSCData().cscID;
	uint16_t lct_strip         = Lct->getCSCData().strip;
	//uint16_t lct_pattern       = Lct->getCSCData().pattern;
	uint16_t lct_bend          = Lct->getCSCData().bend;
	uint16_t lct_quality       = Lct->getCSCData().quality;
	uint16_t lct_keywire       = Lct->getCSCData().keywire;
	
	double lct_phi             = Lct->getCMSGlobalPhi();
	double lct_eta             = Lct->getCMSGlobalEta();
	
	if ( printLevel > 0 ) {
	  cout << "\n======\n";
	  cout <<"lctEndcap       = " << lct_endcap << endl;
	  cout <<"lctSector       = " << lct_sector<< endl;
	  cout <<"lctSubSector    = " << lct_subSector << endl;
	  cout <<"lctStation      = " << lct_station << endl;
	  cout <<"lctRing         = " << lct_ring << endl;
	  cout <<"lctChamber      = " << lct_chamber << endl;
	  cout <<"lctTriggerCSCID = " << lct_cscID << endl;
	  cout <<"lctBx           = " << lct_bx << endl;
	  cout <<"lctBx0          = " << lct_bx0 << endl;
	  cout <<"lctKeyWire      = " << lct_keywire << endl;
	  cout <<"lctStrip        = " << lct_strip << endl;
	  cout <<"lctBend         = " << lct_bend << endl;
	  cout <<"lctQuality      = " << lct_quality << endl;
	  cout <<"lct_Gblphi     = " << lct_phi << endl;
	  cout <<"lct_Gbleta     = " << lct_eta << endl;
	}
	
	
	// Do not FIll array over their given size!!
	if (nTrks > MAXTRK-1) {
	  if (printLevel > 1) cout << "-----> nTrks is greater than MAXTRK-1.  Skipping this Track..." << endl;
	  continue;
	}
	
	if (LctTrkId_ > MAXTRKLCTS-1) {
	  if (printLevel > 1)cout << "-----> LctTrkId_ is greater than MAXTRKLCTS-1.  Skipping this Track..." << endl;
	  continue;
	}
	
	
	ev.leg_trkLctEndcap[nTrks][LctTrkId_] = lct_endcap;
	
	// sector (end 1: 1->6, end 2: 7 -> 12)
	//if ( lct_endcap == 1)
	ev.leg_trkLctSector[nTrks][LctTrkId_] = lct_sector;
	//else
	//        lctSector[nTrk][LctTrkId_] = 6+lct_sector;
	
	ev.leg_trkLctStation[nTrks][LctTrkId_] = lct_station;
	
	ev.leg_trkLctRing[nTrks][LctTrkId_] = lct_ring;
	
	ev.leg_trkLctChamber[nTrks][LctTrkId_] = lct_chamber;
	
	ev.leg_trkLctCSCID[nTrks][LctTrkId_] = lct_cscID;
	
	ev.leg_trkLctWire[nTrks][LctTrkId_] = lct_keywire;
	
	ev.leg_trkLctStrip[nTrks][LctTrkId_] = lct_strip;
	
	ev.leg_trkLctGblPhi[nTrks][LctTrkId_] = lct_phi;
	
	ev.leg_trkLctGblEta[nTrks][LctTrkId_] = lct_eta;
	
	LctTrkId_++;
	
      } // end track LCT loop
      
      ev.numLegTrkLCTs -> push_back(LctTrkId_);
      
      nTrks++;
      
    } // end legacy track loop
    
    ev.numLegTrks = nTrks;
    
    //fillLeg_CSCTFTracks(ev, leg_tracks, printLevel, srLUTs_, scale, ptScale);

  }
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
      tagAndProbeExist = fillRecoMuons(ev, muons, printLevel);
    
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
  if (NoTagAndProbe || tagAndProbeExist)
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
