#include "TrackAnalyzer/CSCplusRPCTrackAnalyzer/interface/DataEvtSummaryHandler.h"

using namespace std;

//
DataEvtSummaryHandler::DataEvtSummaryHandler()
{

 

}

//
bool DataEvtSummaryHandler::initTree(TTree *t)
{
    if(t==0) return false;
    t_ = t;
    

    //event info
    t_->Branch("run",   &evSummary_.run,   "run/I");
    t_->Branch("lumi",  &evSummary_.lumi,  "lumi/I");
    t_->Branch("event", &evSummary_.event, "event/I");
    

    // ==================
    // Gen Muons
    // ==================
    t_->Branch("numGenMuons", &evSummary_.numGenMuons, "numGenMuons/I");
    
    t_->Branch("gen_eta",  &evSummary_.gen_eta);
    t_->Branch("gen_phi",  &evSummary_.gen_phi);
    t_->Branch("gen_id",   &evSummary_.gen_id);
    t_->Branch("gen_pt",   &evSummary_.gen_pt);

    
    // ==================
    // RECO GLobal Muons
    // ==================
    
    // ==================
    t_->Branch("numGblRecoMuons", &evSummary_.numGblRecoMuons, "numGblRecoMuons/I");

    t_->Branch("gmrEta",  &evSummary_.gmrEta);
    t_->Branch("gmrPhi",  &evSummary_.gmrPhi);
    t_->Branch("gmrPt",   &evSummary_.gmrPt);
    t_->Branch("gmrValHits",   &evSummary_.gmrValHits);
    t_->Branch("gmrD0",   &evSummary_.gmrD0);
    t_->Branch("gmrChi2Norm",   &evSummary_.gmrChi2Norm);

    // Muon Segments
    t_->Branch("muonNsegs", &evSummary_.muonNsegs);
    t_->Branch("muon_cscsegs_gbl_x"      ,  evSummary_.muon_cscsegs_gbl_x      ,"muon_cscsegs_gbl_x[numGblRecoMuons][16]/F");
    t_->Branch("muon_cscsegs_gbl_y"      ,  evSummary_.muon_cscsegs_gbl_y      ,"muon_cscsegs_gbl_y[numGblRecoMuons][16]/F");
    t_->Branch("muon_cscsegs_gbl_eta"    ,  evSummary_.muon_cscsegs_gbl_eta    ,"muon_cscsegs_gbl_eta[numGblRecoMuons][16]/F");
    t_->Branch("muon_cscsegs_gbl_phi"    ,  evSummary_.muon_cscsegs_gbl_phi    ,"muon_cscsegs_gbl_phi[numGblRecoMuons][16]/F");
    
    t_->Branch("muon_cscsegs_endcap" ,  evSummary_.muon_cscsegs_endcap ,"muon_cscsegs_endcap[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_station",  evSummary_.muon_cscsegs_station,"muon_cscsegs_station[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_ring"   ,  evSummary_.muon_cscsegs_ring   ,"muon_cscsegs_ring[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_chamber", evSummary_.muon_cscsegs_chamber,"muon_cscsegs_chamber[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_nhits"  , evSummary_.muon_cscsegs_nhits  ,"muon_cscsegs_nhits[numGblRecoMuons][16]/I");
    
    t_->Branch("muon_cscsegs_islctable", evSummary_.muon_cscsegs_islctable,"muon_cscsegs_islctable[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_ismatched"   , evSummary_.muon_cscsegs_ismatched,   "muon_cscsegs_ismatched[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_lctId"       , evSummary_.muon_cscsegs_lctId    ,   "muon_cscsegs_lctId[numGblRecoMuons][16]/I");
    t_->Branch("muon_cscsegs_sector"   , evSummary_.muon_cscsegs_sector,    "muon_cscsegs_sector[numGblRecoMuons][16]/I");
    

    // ==================
    // CSC LCTS
    // ==================
    t_->Branch("numLCTs",         &evSummary_.numLCTs,    "numLCTs/I");
    t_->Branch("lctGlobalPhi",    &evSummary_.lctGlobalPhi);
    t_->Branch("lctGlobalEta",    &evSummary_.lctGlobalEta);
    t_->Branch("lctEndcap",       &evSummary_.lctEndcap);
    t_->Branch("lctStation",      &evSummary_.lctStation);
    t_->Branch("lctSector",       &evSummary_.lctSector);
    t_->Branch("lctSubSector",    &evSummary_.lctSubSector);
    t_->Branch("lctRing",         &evSummary_.lctRing);
    t_->Branch("lctChamber",      &evSummary_.lctChamber);
    t_->Branch("lctTriggerCSCID", &evSummary_.lctTriggerCSCID);
    t_->Branch("lctBx",           &evSummary_.lctBx);
    t_->Branch("lctBx0",          &evSummary_.lctBx0);
    t_->Branch("lctWire",         &evSummary_.lctWire);
    t_->Branch("lctStrip",        &evSummary_.lctStrip);

    // ==================
    // RPC LCTS
    // ==================
    
    // cluster variables
    t_->Branch("numRPC_clusters",    &evSummary_.numRPC_clusters,    "numRPC_clusters/I");
    t_->Branch("rpc_cluster_Endcap",        &evSummary_.rpc_cluster_Endcap);
    t_->Branch("rpc_cluster_Station",        &evSummary_.rpc_cluster_Station);
    t_->Branch("rpc_cluster_Sector",        &evSummary_.rpc_cluster_Sector);
    t_->Branch("rpc_cluster_SubSector",        &evSummary_.rpc_cluster_SubSector);
    t_->Branch("rpc_cluster_globalPhi",        &evSummary_.rpc_cluster_globalPhi);
    t_->Branch("rpc_cluster_globalEta",        &evSummary_.rpc_cluster_globalEta);
    t_->Branch("rpc_cluster_Chamber",        &evSummary_.rpc_cluster_Chamber);
    t_->Branch("rpc_cluster_Wire",        &evSummary_.rpc_cluster_Wire);
    t_->Branch("rpc_cluster_Strip",        &evSummary_.rpc_cluster_Strip);
    t_->Branch("rpc_cluster_Ring",        &evSummary_.rpc_cluster_Ring);
    t_->Branch("rpc_cluster_CSCId",        &evSummary_.rpc_cluster_CSCId);

    // ====================
    // CSC Tracks and LCTs
    // ====================
    t_->Branch("numTrks", &evSummary_.numTrks,    "numTrks/I");
    t_->Branch("trkPt",  &evSummary_.trkPt);
    t_->Branch("trkEta", &evSummary_.trkEta);
    t_->Branch("trkPhi", &evSummary_.trkPhi);
    t_->Branch("trkMode",&evSummary_.trkMode);
    t_->Branch("numTrkLCTs", &evSummary_.numTrkLCTs);

    t_->Branch("trkLctEndcap",    &evSummary_.trkLctEndcap,    "trkLctEndcap[4][4]/I");
    t_->Branch("trkLctChamber",    &evSummary_.trkLctChamber,    "trkLctChamber[4][4]/I");
    t_->Branch("trkLctStation",    &evSummary_.trkLctStation,    "trkLctStation[4][4]/I");
    t_->Branch("trkLctSector",    &evSummary_.trkLctSector,    "trkLctSector[4][4]/I");
    t_->Branch("trkLctRing",    &evSummary_.trkLctRing,    "trkLctRing[4][4]/I");
    t_->Branch("trkLctWire",    &evSummary_.trkLctWire,    "trkLctWire[4][4]/I");
    t_->Branch("trkLctStrip",    &evSummary_.trkLctStrip,    "trkLctStrip[4][4]/I");
    t_->Branch("trkLctCSCID",    &evSummary_.trkLctCSCID,    "trkLctCSCID[4][4]/I");
    t_->Branch("trkLctGblPhi",    &evSummary_.trkLctGblPhi,    "trkLctGblPhi[4][4]/F");
    t_->Branch("trkLctGblEta",    &evSummary_.trkLctGblEta,    "trkLctGblEta[4][4]/F");


    // RPC Tracks
    // ====================
    t_->Branch("numTrks_rpc",    &evSummary_.numTrks_rpc,    "numTrks_rpc/I");
    t_->Branch("numTrkLCTs_rpc", &evSummary_.numTrkLCTs_rpc,    "numTrkLCTs_rpc/I");

    t_->Branch("trkPt_rpc",  &evSummary_.trkPt_rpc);
    t_->Branch("trkEta_rpc", &evSummary_.trkEta_rpc);
    t_->Branch("trkPhi_rpc", &evSummary_.trkPhi_rpc);
    t_->Branch("trkMode_rpc",&evSummary_.trkMode_rpc);
    t_->Branch("isRPC_cand",&evSummary_.isRPC_cand);
    
    // ====================
    // Legacy Tracks
    // ====================
    t_->Branch("numLegTrks",    &evSummary_.numLegTrks,    "numLegTrks/I");
    t_->Branch("leg_trkPt",  &evSummary_.leg_trkPt);
    t_->Branch("leg_trkEta", &evSummary_.leg_trkEta);
    t_->Branch("leg_trkPhi", &evSummary_.leg_trkPhi);
    t_->Branch("leg_trkMode",&evSummary_.leg_trkMode);


    return true;
}



void DataEvtSummaryHandler::initStruct() {

  
  evSummary_.run   = 0;
  evSummary_.lumi  = 0;
  evSummary_.event = 0;


  // ==================
  // Gen Muons
  // ==================
  evSummary_.numGenMuons = 0;
  evSummary_.gen_eta = new vector<float>;
  evSummary_.gen_phi = new vector<float>;
  evSummary_.gen_pt  = new vector<float>;
  evSummary_.gen_id  = new vector<int>;

  // ==================
  // RECO Muons
  // ==================
  evSummary_.numGblRecoMuons = 0;
  evSummary_.gmrEta = new vector<float>;
  evSummary_.gmrPhi = new vector<float>;
  evSummary_.gmrPt  = new vector<float>;
  evSummary_.gmrD0  = new vector<float>;
  evSummary_.gmrChi2Norm  = new vector<float>;
  evSummary_.gmrValHits  = new vector<int>;
  
  
  // Segments
  evSummary_.muonNsegs = new std::vector<int>;

  for (int row=0; row < MAX_MUONS; row++)
    for (int col=0; col < MAX_SEGS_STD; col++) {
      
      evSummary_.muon_cscsegs_gbl_x[row][col] = -999;
      evSummary_.muon_cscsegs_gbl_y[row][col] = -999;
      evSummary_.muon_cscsegs_gbl_eta[row][col] = -999;
      evSummary_.muon_cscsegs_gbl_phi[row][col] = -999;
      
      evSummary_.muon_cscsegs_endcap[row][col] = -999;
      evSummary_.muon_cscsegs_station[row][col] = -999;
      evSummary_.muon_cscsegs_ring[row][col] = -999;
      evSummary_.muon_cscsegs_chamber[row][col] = -999;
      evSummary_.muon_cscsegs_nhits[row][col] = -999;
      evSummary_.muon_cscsegs_sector[row][col] = -999;

      evSummary_.muon_cscsegs_islctable[row][col] = -999;
      evSummary_.muon_cscsegs_ismatched[row][col] = -999;
      evSummary_.muon_cscsegs_lctId[row][col] = -999;
      //evSummary_.muon_cscsegs_nmatched[row][col] = -999;
      
    }


  // ==================
  // CSC LCTS
  // ==================
  evSummary_.numLCTs = 0;
  evSummary_.lctGlobalPhi    = new vector<float>;
  evSummary_.lctGlobalEta    = new vector<float>;
  evSummary_.lctEndcap       = new vector<int>;
  evSummary_.lctSector       = new vector<int>;
  evSummary_.lctSubSector    = new vector<int>;
  evSummary_.lctBx           = new vector<int>;
  evSummary_.lctBx0          = new vector<int>;
  evSummary_.lctStation      = new vector<int>;
  evSummary_.lctRing         = new vector<int>;
  evSummary_.lctChamber      = new vector<int>;
  evSummary_.lctTriggerCSCID = new vector<int>;
  evSummary_.lctStrip        = new vector<int>;
  evSummary_.lctWire         = new vector<int>;
  evSummary_.lctRing         = new vector<int>;


  // ====================
  // CSC Tracks and LCTs
  // ====================

  evSummary_.numTrks    = 0;

  evSummary_.trkPt   = new vector<float>;
  evSummary_.trkEta  = new vector<float>;
  evSummary_.trkPhi  = new vector<float>;
  evSummary_.trkMode = new vector<Int_t>;
  evSummary_.numTrkLCTs = new vector<Int_t>;

  // RPC Clusters
  evSummary_.numRPC_clusters = 0;
  evSummary_.rpc_cluster_globalPhi = new vector<float>;
  evSummary_.rpc_cluster_globalEta = new vector<float>;
  evSummary_.rpc_cluster_Station   = new vector<int>;
  evSummary_.rpc_cluster_Sector    = new vector<int>;
  evSummary_.rpc_cluster_SubSector = new vector<int>;
  evSummary_.rpc_cluster_Endcap    = new vector<int>;
  evSummary_.rpc_cluster_Chamber    = new vector<int>;
  evSummary_.rpc_cluster_Wire    = new vector<int>;
  evSummary_.rpc_cluster_Strip    = new vector<int>;
  evSummary_.rpc_cluster_Ring    = new vector<int>;
  evSummary_.rpc_cluster_CSCId    = new vector<int>;
  

  // RPC Tracks
  evSummary_.numTrkLCTs_rpc = 0;
  evSummary_.numTrks_rpc    = 0;

  evSummary_.trkPt_rpc   = new vector<float>;
  evSummary_.trkEta_rpc  = new vector<float>;
  evSummary_.trkPhi_rpc  = new vector<float>;
  evSummary_.trkMode_rpc = new vector<Int_t>;
  evSummary_.isRPC_cand = new vector<Int_t>;

  // Track LCTs
  for (int i=0; i < MAXTRK; i++) {
    for (int j=0; j < MAXTRKLCTS; j++) {
    
      evSummary_.trkLctEndcap[i][j]  = -999;
      evSummary_.trkLctStation[i][j] = -999;
      evSummary_.trkLctSector[i][j]  = -999;
      evSummary_.trkLctRing[i][j]    = -999;
      evSummary_.trkLctChamber[i][j] = -999;
      evSummary_.trkLctWire[i][j]    = -999;
      evSummary_.trkLctStrip[i][j]   = -999;
      evSummary_.trkLctCSCID[i][j]   = -999;
      evSummary_.trkLctGblPhi[i][j]  = -999;
      evSummary_.trkLctGblEta[i][j]  = -999;

    }
  }
  
  // ====================
  // Legacy CSC Tracks
  // ====================
  evSummary_.numLegTrks = 0;

  evSummary_.leg_trkPt   = new vector<float>;
  evSummary_.leg_trkEta  = new vector<float>;
  evSummary_.leg_trkPhi  = new vector<float>;
  evSummary_.leg_trkMode = new vector<Int_t>;
  


}


//
void DataEvtSummaryHandler::resetStruct() {


  // ==================
  // Gen Muons
  // ==================
  vector<float>().swap(*evSummary_.gen_eta);
  vector<float>().swap(*evSummary_.gen_phi);
  vector<float>().swap(*evSummary_.gen_pt);
  vector<int>().swap(*evSummary_.gen_id);


  // ==================
  // RECO Muons
  // ==================
  vector<float>().swap(*evSummary_.gmrEta);
  vector<float>().swap(*evSummary_.gmrPhi);
  vector<float>().swap(*evSummary_.gmrPt);
  vector<float>().swap(*evSummary_.gmrChi2Norm);
  vector<float>().swap(*evSummary_.gmrD0);
  vector<int>().swap(*evSummary_.gmrValHits);
  vector<int>().swap(*evSummary_.muonNsegs);

  // ==================
  // CSC LCTS
  // ==================
  vector<float>().swap(*evSummary_.lctGlobalPhi);
  vector<float>().swap(*evSummary_.lctGlobalEta);
  vector<int>().swap(*evSummary_.lctEndcap);
  vector<int>().swap(*evSummary_.lctSector);
  vector<int>().swap(*evSummary_.lctSubSector);
  vector<int>().swap(*evSummary_.lctBx);
  vector<int>().swap(*evSummary_.lctBx0);
  vector<int>().swap(*evSummary_.lctStation);
  vector<int>().swap(*evSummary_.lctRing);
  vector<int>().swap(*evSummary_.lctChamber);
  vector<int>().swap(*evSummary_.lctTriggerCSCID);
  vector<int>().swap(*evSummary_.lctStrip);
  vector<int>().swap(*evSummary_.lctWire);
  
  
  // ====================
  // CSC Tracks and LCTs
  // ====================
  vector<float>().swap(*evSummary_.trkPt);
  vector<float>().swap(*evSummary_.trkEta);
  vector<float>().swap(*evSummary_.trkPhi);
  vector<Int_t>().swap(*evSummary_.trkMode);
  vector<Int_t>().swap(*evSummary_.numTrkLCTs);

  // RPC CLusters
  vector<float>().swap(*evSummary_.rpc_cluster_globalPhi);
  vector<float>().swap(*evSummary_.rpc_cluster_globalEta);
  vector<int>().swap(*evSummary_.rpc_cluster_Station);
  vector<int>().swap(*evSummary_.rpc_cluster_Sector);
  vector<int>().swap(*evSummary_.rpc_cluster_SubSector);
  vector<int>().swap(*evSummary_.rpc_cluster_Endcap);
  vector<int>().swap(*evSummary_.rpc_cluster_Chamber);
  vector<int>().swap(*evSummary_.rpc_cluster_Wire);
  vector<int>().swap(*evSummary_.rpc_cluster_Strip);
  vector<int>().swap(*evSummary_.rpc_cluster_Ring);
  vector<int>().swap(*evSummary_.rpc_cluster_CSCId);

  // RPC tracks
  vector<float>().swap(*evSummary_.trkPt_rpc);
  vector<float>().swap(*evSummary_.trkEta_rpc);
  vector<float>().swap(*evSummary_.trkPhi_rpc);
  vector<Int_t>().swap(*evSummary_.trkMode_rpc);
  vector<Int_t>().swap(*evSummary_.isRPC_cand);
  
  // Track LCTs
  //vector<vector<int>>().swap(*evSummary_.trkLctEndcap);

  // ====================
  // Legacy CSC Tracks
  // ====================
  vector<float>().swap(*evSummary_.leg_trkPt);
  vector<float>().swap(*evSummary_.leg_trkEta);
  vector<float>().swap(*evSummary_.leg_trkPhi);
  vector<Int_t>().swap(*evSummary_.leg_trkMode);

}

//
void DataEvtSummaryHandler::fillTree()
{
    if(t_) t_->Fill();
}

//
DataEvtSummaryHandler::~DataEvtSummaryHandler()
{
}
