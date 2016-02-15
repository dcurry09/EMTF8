// -*- C++ -*-
//=============================================================
// Fill all Legavy tracks in the event record for: 
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


using namespace std;

const Double_t ptscale[31] =  { 0,
				1.5,   2.0,   2.5,   3.0,   3.5,   4.0,
				4.5,   5.0,   6.0,   7.0,   8.0,  10.0,  12.0,  14.0,
				16.0,  18.0,  20.0,  25.0,  30.0,  35.0,  40.0,  45.0,
				50.0,  60.0,  70.0,  80.0,  90.0, 100.0, 120.0, 140.0 };

void fillLeg_CSCTFTracks(DataEvtSummary_t &ev, edm::Handle<vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi> > > > legacyTracks, int printLevel) {

  int nTrks = 0;

  for(std::vector<std::pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>>::const_iterator lt = legacyTracks->begin();lt != legacyTracks->end();lt++){
    
    float eta = 0.9 + 0.05*(lt->first.eta_packed()) + 0.025;
    unsigned sector = lt->first.sector();
    float phi = (0.05217*lt->first.localPhi()) + (sector-1)*1.1 + 0.0218;//*(3.14159265359/180)
    if(phi > 3.14159)
      phi -= 6.28318;
    
    int mode = 0;
    unsigned pti = 0, quality = 0;
    
    lt->first.decodeRank(lt->first.rank(),pti,quality);//
    
    float pt = ptscale[pti+1];
    
    //std::cout<<"phi =  "<<phi<<" and eta = "<<eta<<", sector = "<<sector<<", diff = "<<phi - GM.phi()<<"\n";
    
    if(lt->first.me1ID())
      mode |= 8;
    if(lt->first.me2ID())
      mode |= 4;
    if(lt->first.me3ID())
      mode |= 2;
    if(lt->first.me4ID())
      mode |= 1;
    
    ev.leg_trkPt   -> push_back(pt);
    ev.leg_trkEta  -> push_back(eta);
    ev.leg_trkPhi  -> push_back(phi);
    ev.leg_trkMode -> push_back(mode);
    
    //std::cout<<"Legacy Mode = "<<mode<<"\n";
    
    //if(mode == 10 || mode > 12)
    //std::cout<<"Legacy Found Good Track\n";
    nTrks++;
    
  }
  
  ev.numLegTrks = nTrks;


} // end fill Tracks
