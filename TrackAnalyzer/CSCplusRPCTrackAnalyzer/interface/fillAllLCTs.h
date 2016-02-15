// -*- C++ -*-
//=============================================================
// Fill all LCTs in the event record for: 
// Package:    CSCplusRPCTrackAnalyzer
// Class:      CSCplusRPCTrackAnalyzer
//
// Written by David Curry
// ============================================================

#include <string.h>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <set>
#include <cmath>
#include <vector>
#include "L1Trigger/L1TMuonEndCap/plugins/L1TMuonEndCapTrackProducer.h"
#include "L1Trigger/CSCCommonTrigger/interface/CSCPatternLUT.h"
#include "L1Trigger/CSCTrackFinder/test/src/RefTrack.h"

#include "L1Trigger/L1TMuon/interface/deprecate/SubsystemCollectorFactory.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <TMath.h>
#include <TCanvas.h>
#include <TLorentzVector.h>

#include <TStyle.h>
#include <TLegend.h>
#include <TF1.h>
#include <TH2.h>
#include <TH1F.h>
#include <TFile.h>
#include "L1Trigger/L1TMuon/interface/deprecate/GeometryTranslator.h"
#include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h"

#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h"
//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrackFwd.h"

//#include "L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h"
#include "L1Trigger/L1TMuonEndCap/interface/PhiMemoryImage.h"
#include "L1Trigger/L1TMuonEndCap/interface/EmulatorClasses.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCTFPtLUT.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCSectorReceiverLUT.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h"

using namespace std;
using namespace edm;
using namespace reco;
using namespace csc;

void fillAllLCTs(DataEvtSummary_t &ev, edm::Handle<CSCCorrelatedLCTDigiCollection> LCTs, int printLevel) {
  
  std::vector<L1TMuon::TriggerPrimitive> LCT_collection;
  
  auto chamber = LCTs->begin();
  auto chend  = LCTs->end();
  for( ; chamber != chend; ++chamber ) {
    auto digi = (*chamber).second.first;
    auto dend = (*chamber).second.second;
    for( ; digi != dend; ++digi ) {
      LCT_collection.push_back(TriggerPrimitive((*chamber).first,*digi));
    }
  }
  
  int lctId = 0; // count number of lcts in event
  
  auto Lct = LCT_collection.cbegin();
  auto Lctend = LCT_collection.cend();
  for( ; Lct != Lctend; Lct++,lctId++ ) {

    if(Lct->subsystem() != 1) continue;
    
    CSCDetId id                = Lct->detId<CSCDetId>();
    auto lct_station           = id.station();
    auto lct_endcap            = id.endcap();
    auto lct_chamber           = id.chamber();
    uint16_t lct_bx            = Lct->getCSCData().bx;
    int lct_ring               = id.ring();
    int lct_sector             = CSCTriggerNumbering::triggerSectorFromLabels(id);
    int lct_subsector          = CSCTriggerNumbering::triggerSubSectorFromLabels(id);
    uint16_t lct_bx0           = Lct->getCSCData().bx0;
    uint16_t lct_cscID         = Lct->getCSCData().cscID;
    uint16_t lct_strip         = Lct->getCSCData().strip;
    uint16_t lct_pattern       = Lct->getCSCData().pattern;
    uint16_t lct_bend          = Lct->getCSCData().bend;
    uint16_t lct_quality       = Lct->getCSCData().quality;
    uint16_t lct_keywire       = Lct->getCSCData().keywire;

    // not working
    double lct_phi             = Lct->getCMSGlobalPhi();
    double lct_eta             = Lct->getCMSGlobalEta();
    
    if ( printLevel > 0 ) {
      cout << "\nLCT CSC " << lctId
	   << "\n======\n";
      cout <<"lctEndcap       = " << lct_endcap << endl;
      cout <<"lctSector       = " << lct_sector<< endl;
      cout <<"lctSubSector    = " << lct_subsector << endl;
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
      cout <<"lct_pattern     = " << lct_pattern << endl;
      //cout <<"lct_phi         = " << lct_phi << endl;
      //cout <<"lct_eta         = " << lct_eta << endl;
    }
    
    // Fill the branch vectors
    ev.lctGlobalPhi -> push_back(lct_phi);
    ev.lctGlobalEta -> push_back(lct_eta);
    ev.lctEndcap -> push_back(lct_endcap);
    ev.lctSector -> push_back(lct_sector);
    ev.lctSubSector -> push_back(lct_subsector);
    ev.lctStation -> push_back(lct_station);
    ev.lctRing -> push_back(lct_ring);
    ev.lctChamber -> push_back(lct_chamber);
    ev.lctTriggerCSCID -> push_back(lct_cscID);
    ev.lctBx -> push_back(lct_bx);
    ev.lctBx0 -> push_back(lct_bx0);
    ev.lctWire -> push_back(lct_keywire);
    ev.lctStrip -> push_back(lct_strip);
    
  } // end LCT loop
  
  ev.numLCTs = lctId;
  
} // end fillAllLCTs



/*
  for(CSCCorrelatedLCTDigiCollection::DigiRangeIterator csc=LCTs.product()->begin(); csc!=LCTs.product()->end(); csc++) {
  CSCCorrelatedLCTDigiCollection::Range range1 = LCTs.product()->get((*csc).first);
  for(CSCCorrelatedLCTDigiCollection::const_iterator Lct = range1.first; Lct != range1.second; Lct++, lctId++) {
  
  int lct_endcap    = (*csc).first.endcap()-1;
  int lct_station   = (*csc).first.station()-1;
  int lct_sector    = (*csc).first.triggerSector()-1;
  int lct_subSector = CSCTriggerNumbering::triggerSubSectorFromLabels((*csc).first);
  int lct_ring      = (*csc).first.ring();
  int lct_cscId     = (*csc).first.triggerCscId()-1;
  int lct_chamber   = (*csc).first.chamber()-1;
*/
