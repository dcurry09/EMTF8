########################################################
## eff.py   A script to find CSCTF efficiency by segment-Lct matching
##
## By David Curry
##
########################################################

print '------> Setting Environment'

import sys
from ROOT import *
import numpy as np
from array import *
from collections import Counter
from eff_modules import *


# Set the print level. Default = 0
if len(sys.argv) is 1: printLevel = 0
else: printLevel = sys.argv[1]

print '------> Importing Root File'

# SingleMuon
filename = 'root://eoscms//eos/cms/store/user/dcurry/EMTF/TEST_EMTF.root'
#filename = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_0_pre5/src/L1Trigger/L1TMuonEndCap/test/TEST_EMTF.root'

file = TFile.Open(filename)

# Histogram filename
newfile = TFile("plots/trig_eff_plots_allEta_singleMu.root","recreate")

# Set the branch address of TTree in Tfile
tree = file.Get("ntuple/tree")

# A more efficient way to count
muon_count  = Counter()
final_count = Counter() 
eta_count   = Counter() 
trk_count   = Counter()
gen_count   = Counter()

# ================ Histograms ===================

hgbl_pt   = TH1F('hgbl_pt', '', 50 , 0, 50)
hcsctf_pt = TH1F('hcsctf_pt', '', 50 , 0, 50)
hgbl_eta  = TH1F('hgbl_eta', '', 50 , -2.5, 2.5)
hgbl_phi  = TH1F('hgbl_phi', '', 50 , -3.14, 3.14)


# For matching Efficiencies
hpt  = TH1F('hpt', '', len(scale_pt_temp)-1,  scale_pt)
heta = TH1F('heta', '', len(scale_eta_temp)-1, scale_eta)
hphi = TH1F('hphi', '', len(scale_phi_temp)-1, scale_phi)

hpt_trigger  = TH1F('hpt_trigger', '', len(scale_pt_temp)-1, scale_pt)
heta_trigger = TH1F('heta_trigger', '', len(scale_eta_temp)-1, scale_eta)
hphi_trigger = TH1F('hphi_trigger', '', len(scale_phi_temp)-1, scale_phi)


# Debug Hists for high pt failures
htrk_2hitmode_fail  = TH1F('htrk_2hitmode_fail', '', 7 , 0, 7)
htrk_2hitmode_all   = TH1F('htrk_2hitmode_all', '', 7 , 0, 7)
htrk_phi_fail       = TH1F('htrk_phi_fail', '', 50 , -3.14, 3.14)
htrk_eta_fail       = TH1F('htrk_eta_fail', '', 50 , -2.5, 2.5)
htrk_dphi_2hit_fail = TH1F('htrk_dphi_2hit_fail', '', 50 , 0, 500) 

htrk_mode_fail = TH1F('htrk_mode_fail', '', 15 , 0, 15)
htrk_mode_all  = TH1F('htrk_mode_all', '', 15 , 0, 15)

htrk_Q_fail = TH1F('htrk_Q_fail', '', 4, 0, 4)
htrk_Q_all  = TH1F('htrk_Q_all', '', 4, 0, 4)

hLct_endcap_fail  = TH1F('hLct_endcap_fail', '', 2 , 0, 1)
hLct_sector_fail  = TH1F('hLct_sector_fail', '', 12 , 0, 12)
hLct_ring_fail    = TH1F('hLct_ring_fail', '', 4 , 0, 4)
hLct_chamber_fail = TH1F('hLct_chamber_fail', '', 42 , 0, 42)

# Delta Phi for Event LCTs
hdphi12 = TH1F('hdphi12', '', 50 , 0, 1.57)
hdphi13 = TH1F('hdphi13', '', 50 , 0, 1.57)
hdphi14 = TH1F('hdphi14', '', 50 , 0, 1.57)
hdphi23 = TH1F('hdphi23', '', 50 , 0, 1.57)
hdphi24 = TH1F('hdphi24', '', 50 , 0, 1.57)
hdphi34 = TH1F('hdphi34', '', 50 , 0, 1.57)

# Delta Phi for EMTF Tracks LCTs
hdphi12_trk = TH1F('hdphi12_trk', '', 50 , 0, 1.57)
hdphi13_trk = TH1F('hdphi13_trk', '', 50 , 0, 1.57)
hdphi14_trk = TH1F('hdphi14_trk', '', 50 , 0, 1.57)
hdphi23_trk = TH1F('hdphi23_trk', '', 50 , 0, 1.57)
hdphi24_trk = TH1F('hdphi24_trk', '', 50 , 0, 1.57)
hdphi34_trk = TH1F('hdphi34_trk', '', 50 , 0, 1.57)

hdphi12_trk15 = TH1F('hdphi12_trk15', '', 50 , 0, 1.57)
hdphi13_trk15 = TH1F('hdphi13_trk15', '', 50 , 0, 1.57)
hdphi14_trk15 = TH1F('hdphi14_trk15', '', 50 , 0, 1.57)
hdphi23_trk15 = TH1F('hdphi23_trk15', '', 50 , 0, 1.57)
hdphi24_trk15 = TH1F('hdphi24_trk15', '', 50 , 0, 1.57)
hdphi34_trk15 = TH1F('hdphi34_trk15', '', 50 , 0, 1.57)

h2dphi_trk15     = TH2F('h2dphi_trk15', '', 6, 1, 7, 20, 0 , 10)
h2dphi_trk15_leg = TH2F('h2dphi_trk15_leg', '', 6, 1, 7, 20, 0 , 10) 

h2deta_trk15 = TH2F('h2deta_trk15', '', 6, 1, 7, 20, 0 , 40)



# efficiency(turn on)
pt_thresh = [5., 7., 10., 12., 16.]
n_thresh = len(pt_thresh)

ptbin = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 100]
ptbin_array = array('d', ptbin)
n_ptbin = len(ptbin)

csctfPt = [0]*n_thresh
csctfPt_eta1 = [0]*n_thresh
csctfPt_eta2 = [0]*n_thresh
csctfPt_eta3 = [0]*n_thresh
csctfPt_eta4 = [0]*n_thresh

csctfPt_all = TH1F('csctfPt_all', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta1 = TH1F('csctfPt_all_eta1', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta2 = TH1F('csctfPt_all_eta2', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta3 = TH1F('csctfPt_all_eta3', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta4 = TH1F('csctfPt_all_eta4', '', n_ptbin-1, ptbin_array)


for ihist, thresh in enumerate(pt_thresh):
    csctfPt[ihist] = TH1F('csctfPt_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta1[ihist] = TH1F('csctfPt_eta1_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta2[ihist] = TH1F('csctfPt_eta2_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta3[ihist] = TH1F('csctfPt_eta3_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta4[ihist] = TH1F('csctfPt_eta4_'+str(thresh), '', n_ptbin-1, ptbin_array)
   
hist_list = [csctfPt_all, csctfPt_all_eta1, csctfPt_all_eta2, csctfPt_all_eta3, csctfPt_all_eta4, \
                 hgbl_pt, hcsctf_pt, hgbl_eta, hgbl_phi, htrk_2hitmode_fail, htrk_2hitmode_all, \
                 htrk_phi_fail, hLct_chamber_fail, hLct_sector_fail, hLct_endcap_fail, hLct_ring_fail, \
                 htrk_dphi_2hit_fail, htrk_mode_all, htrk_mode_fail, htrk_Q_all, htrk_Q_fail, \
                 hpt, heta, hphi, hpt_trigger, heta_trigger, hphi_trigger, \
                 hdphi12, hdphi13, hdphi14, hdphi23, hdphi24, hdphi34,\
                 hdphi12_trk, hdphi13_trk, hdphi14_trk, hdphi23_trk, hdphi24_trk, hdphi34_trk,\
                 hdphi12_trk15, hdphi13_trk15, hdphi14_trk15, hdphi23_trk15, hdphi24_trk15, hdphi34_trk15,\
                 h2dphi_trk15, h2deta_trk15, h2dphi_trk15_leg
             ]

# ================================================

# Loop over over events in TFile
for iEvt in range(tree.GetEntries()):

    # for testing
    if iEvt > 1000: break
    
    tree.GetEntry(iEvt)
    
    if iEvt % 1000 is 0: print 'Event #', iEvt
    
    if printLevel > 1:
        print '\n============== New Event # ', tree.event, ' =================\n'\
              '\n  Run             = ', tree.run,  \
              '\n  Muons in Event  = ', tree.numGblRecoMuons,   \
              '\n  Tracks in Event = ', tree.numTrks
        

    for iTrk in range(tree.numTrks):
        if tree.numTrkLCTs[iTrk] == 4: gen_count['4hit_tracks'] +=1        
        if tree.numTrkLCTs[iTrk] == 3 : gen_count['3hit_tracks'] +=1
        if tree.numTrkLCTs[iTrk] < 3 : gen_count['2hit_tracks'] +=1
    
    # Now check each muon individually and fill hists
    for iReco in range(0, tree.numGblRecoMuons):
        
        if printLevel > 1: print '\n===== Looping over Muon', iReco, '====='
        
        if tree.gmrPt[iReco] <= 3: continue
        
        if abs(tree.gmrEta[iReco]) > 2.4 or abs(tree.gmrEta[iReco]) < 1.2: continue
        
        # only high quality muons
        if tree.gmrValHits[iReco] < 10: continue
        if tree.gmrD0[iReco] > 0.2    : continue
        if tree.gmrChi2Norm[iReco] > 3: continue
        #if reco.gmrDXY[iReco] > 0.2 and reco.gmrDz[iReco] > 0.5: continue

        #if reco.gmrEta[iReco] >= 0: continue
        
        if printLevel > 1: print '-----> Muon is Global w/ pT > 3 and eta < 2.4 & > 1.2.  Continue on'
        
        muon_count['total_gbl_muons'] +=1
        
        # set gbl muon pt
        pt_muon  = tree.gmrPt[iReco]
        eta_muon = abs(tree.gmrEta[iReco])
        phi_muon = tree.gmrPhi[iReco]
        eta_muon_plot = tree.gmrEta[iReco]
        

        #muon_count.clear()
        
        # =============================================================================================
        # Function that takes global and gives back is Matched to two Segs. Returns list[Bool, Lct id[] ]
        match_list = is_two_segs(iEvt, iReco, tree, printLevel) 

        if not match_list[0]: continue 
        
        id_list = match_list[1]
            
        if printLevel > 0: print '\n-----> Muon has two Segs matched.  Fill denominator'
         
        muon_count['denominator'] += 1

        # efficiencies
        hpt.Fill(pt_muon)
        heta.Fill(eta_muon)
        hphi.Fill(phi_muon)

        # Match to Legeacy track with simple dR
        leg_track_list = deltaRLegTrackMuon(iEvt, tree, iReco, printLevel)
        if leg_track_list[0]: iLegcscTrk = leg_track_list[1]
        else: iLegcscTrk = -999    
        
        
        # =============================================================================================
        # Does a track have the same Lcts that segs matched to?  Returns list[Bool, track Id]
        track_list = is_track_match(iEvt, tree, id_list, printLevel)
        
        #if tree.SizeTrk == 0: continue

        # track_list[0] is True for a match
        if track_list[0]: 

            if printLevel > 0: print '\n-----> Track #', track_list[1], ' has Lct matched to Segment.  Fill numerator'
          
            icscTrk = track_list[1]
            
            '''
            #  Sanity check.  USe deltaR matching netween muon and track
            eta1 = tree.gmrEta[iReco]
            eta2 = tree.EtaTrk[icscTrk]
            deta = eta1 - eta2
            deltaR = np.sqrt(deta*deta)
            if deltaR > 0.1: continue
            '''
            # ===================================

            muon_count['numerator'] += 1

            hgbl_pt.Fill(pt_muon)
            hgbl_eta.Fill(eta_muon_plot)
            hgbl_phi.Fill(phi_muon)
            
            # efficiencies
            hpt_trigger.Fill(pt_muon)
            heta_trigger.Fill(eta_muon)
            hphi_trigger.Fill(phi_muon)

            # dPhi Plots
            dphi_plots(tree, icscTrk, iLegcscTrk)



            # ======= Turn On Curves ========
            '''
            # get track quality
            trkQ = whichQ(icscTrk, tree)
            
            # track mode
            trkMode = track_mode(icscTrk, tree)

            htrk_mode_all.Fill(trkMode)
            htrk_Q_all.Fill(trkQ)

            # choose 2 or 3 hit tracks to plot
            #if tree.NumLCTsTrk[iTREETrk] < 3:
            if trkQ == 3:
            
                # Fill histograms for turn on curves
                treetfPt_all.Fill(pt_muon)

                # Eta regions
                if eta_muon > 0.9 and eta_muon <= 1.2: csctfPt_all_eta1.Fill(pt_muon)
                if eta_muon > 1.2 and eta_muon <= 2.1: csctfPt_all_eta2.Fill(pt_muon)
                if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_all_eta3.Fill(pt_muon)
        
                for ihist, thresh in enumerate(pt_thresh):

                    if csc.PtTrk[iCSCTrk] >= thresh:
                        
                        csctfPt[ihist].Fill(pt_muon)
                        
                        # fill eta regions
                        if eta_muon > 0.9 and eta_muon <= 1.2: csctfPt_eta1[ihist].Fill(pt_muon)
                        if eta_muon > 1.2 and eta_muon <= 2.1: csctfPt_eta2[ihist].Fill(pt_muon)
                        if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_eta3[ihist].Fill(pt_muon)
            '''                    
            # ===================================
            
        # end if track is matched
        
        '''    
        # Begin failure tree for non matched tracks
        
        if not track_list[0]:
            
            if printLevel > 0: print '\n-----> Track Lcts are not matched to Segments. Find out why'
            
            muon_count['No Trigger'] += 1
            
            if printLevel > 1: print ' ======== Looping over Matched Segments ========'

            # Create local counter for segment pair failings
            local = Counter()
            
            # There is the occassional muon that has more than 2 matched segments with more than one failure reason for different seg pairs.
            # It is unclear the best way to handle this, as I'd like only one failure per muon.  For now take multiple failures in this priority:
            # Sectors, eta/phi windows, stations, edging
            # Loop over matched segments
            for iSeg in id_list:
                for jSeg in id_list:
                    if iSeg < jSeg:
                        
                        if printLevel > 1: print 'Looping over Seg', iSeg, 'and Seg', jSeg
                        
                        
                        # Exclude any seg pair from different sector, same station, different endcap
                        if csc.lctSector[iSeg] is not csc.lctSector[jSeg]:  
                            if printLevel > 1: print 'Seg', iSeg, 'and Seg', jSeg, 'are in different Sectors.  Skip further comparisons'
                            local['num_segs_diff_sectors'] += 1
                            continue
                            
                        if csc.lctStation[iSeg] is csc.lctStation[jSeg]:
                            if printLevel > 1: print 'Seg', iSeg, 'and Seg', jSeg, 'are in same Station.  Skip further comparisons.'
                            local['num_segs_same_station'] += 1
                            continue
                            
                        
                        if printLevel > 1: print 'Segments are in different stations, same sector.  Checking Dphi/eta windows.' 
                        
                        
                        in_dr_eta, in_dr_phi, in_window_too_close_edge = False, False, False
                        eta_bit = csc.lctglobalEta[jSeg] >> 1
                        
                        # First the eta windows. Different stations have different windows.
                        # Stations 1 and 2 or 1 and 3
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 3 or 4:
                            if abs(csc.lctglobalEta[iSeg] - csc.lctglobalEta[jSeg]) <= 4: in_dr_eta = True
                        
                        elif abs(csc.lctglobalEta[iSeg] - csc.lctglobalEta[jSeg]) <= 6: in_dr_eta = True
                        
                        # Phi windows depend on eta and station combination
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 3:
                            dphi_window = eta_dphi_ME1toME2[eta_bit]
                            if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True
                            
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 4:
                            dphi_window = eta_dphi_ME1toME3[eta_bit]
                            if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True

                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 5:    
                            if csc.lctStation[iSeg] is 1 or csc.lctStation[iSeg] is 4:
                                dphi_window = eta_dphi_ME1toME3[eta_bit]
                                if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True

                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 5:  
                            if csc.lctStation[iSeg] is 2 or csc.lctStation[iSeg] is 3:
                                if abs(csc.lctStation[iSeg]/4 - csc.lctStation[jSeg]/4) <= 127: in_dr_phi = True
                                
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 6 or csc.lctStation[iSeg] + csc.lctStation[jSeg] is 7:
                            if abs(csc.lctStation[iSeg]/4 - csc.lctStation[jSeg]/4) <= 127: in_dr_phi = True


                        if not in_dr_phi or not in_dr_eta:
                            if printLevel > 1: print 'Segments are not in eta/phi windows' 
                            local['num_segs_not_in_windows'] += 1

                        # if in windows we need to check of the segments would make a track to close to the sector edge.
                        # phi of potential track is taken from Lct 2,3,4, in that priority
                        # Sector edging depends on potential mode of the two segments. If mode is 5, 8, 9, 10, and too close to sector edge, cancel the track 

                        else:
                            
                            if (csc.lctStation[iSeg] is 2 or csc.lctStation[jSeg] is 2) and (csc.lctStation[iSeg] is 3 or csc.lctStation[jSeg] is 3):   pairMode = 8
                            
                            elif (csc.lctStation[iSeg] is 2 or csc.lctStation[jSeg] is 2) and (csc.lctStation[iSeg] is 4 or csc.lctStation[jSeg] is 4): pairMode = 9
                            
                            elif (csc.lctStation[iSeg] is 3 or csc.lctStation[jSeg] is 3) and (csc.lctStation[iSeg] is 4 or csc.lctStation[jSeg] is 4): pairMode = 10
                            
                            if csc.lctStation[iSeg] < csc.lctStation[jSeg] and csc.lctStation[iSeg] != 1:
                                sectorTrk_phi = csc.lctglobalPhi[iSeg]
                                
                            else: sectorTrk_phi = csc.lctglobalPhi[jSeg]
                            
                            if (sectorTrk_phi < 128 or sectorTrk_phi > (4095-128) ) and (pairMode is 10 or pairMode is 8 or pairMode is 9):
                                in_window_too_close_edge = True
                                local['num_segs_sector_edge'] += 1
                                if printLevel > 1: print 'This segment pair is in windows but track was cancelled due to track being to close to sector edge(128 phi bits)'
                                                            
                            elif printLevel > 1: print 'This segment pair was in eta/phi windows and not too close to sector edge'                            
                            

                            # If the muon made it all this way and still no reason for a failure is found, call this an unnaccounted failure.
                            if in_dr_eta and in_dr_phi and not in_window_too_close_edge:
                                if printLevel > 1: print 'This segment pair was in eta/phi windows and not too close to edge.  Should have made a track!'
                                local['num_unaccounted'] += 1
                            

            # end segment loop
            # Now find why these segments did not make a track
            if local['num_unaccounted'] > 0:
                muon_count['fail_unaccounted'] += 1
                local['num_fail'] += 1
                
            if local['num_segs_diff_sectors'] > 0 and local['num_fail'] < 1: 
                if printLevel > 1: print ' ---> Segments are in different sectors'
                muon_count['fail_diff_sector'] += 1
                local['num_fail'] += 1
       
            if local['num_segs_same_station'] > 0 and local['num_fail'] < 1:     
                if printLevel > 1: print ' ---> Segments are in same station'
                muon_count['fail_same_station'] += 1
                local['num_fail'] += 1
                                
            if local['num_segs_not_in_windows'] > 0 and local['num_fail'] < 1:
                if printLevel > 1: print ' ---> Segments are not in phi/eta windows'
                muon_count['fail_windows'] += 1
                local['num_fail'] += 1
                

            if local['num_segs_sector_edge'] > 0 and local['num_fail'] < 1:
                if printLevel > 1: print ' ---> Segments are in phi/eta windows, but too close to sector edge'
                muon_count['fail_sector_edge'] += 1
                local['num_fail'] += 1
                
                
                
            if local['num_fail'] > 1: print ' !!!!!! Overcounting Seg Failures !!!!!!'

            if local['num_fail'] < 1: print ' !!!!!! Undercounting Seg Failures !!!!!!'    


            
        # end if not track matched

        # Take all counts and split them up by eta region
        # 1 = 0.9 - 1.3
        # 2 = 1.3 - 1.7 
        # 3 = 1.7 - 2.1
        # 4 = 2.1 - 2.4
        eta = abs(reco.gmrEta[iReco])

        #print '\nBefore Count =', muon_count
        
        eta_count.clear()
        
        for name in muon_count:
            if eta >= 2.1:
                eta_count[name+'%s' % ('_2.1_2.4')] += 1
                
            if eta > 1.7 and eta < 2.1:     
                eta_count[name+'%s' % ('_1.7_2.1')] += 1

            if eta > 1.3 and eta < 1.7:
                eta_count[name+'%s' % ('_1.3_1.7')] += 1

            if eta <= 1.3:
                eta_count[name+'%s' % ('_0.9_1.3')] += 1

        # append the final count with this muons count
        for name in muon_count: final_count[name] += 1
        for name in eta_count:  final_count[name] += 1
        '''

        
    # end muon loop
        
# end event loop 

#  ======== Write Hists ==========

# Little more work for turn on curves
for ihist, thresh in enumerate(pt_thresh):

    csctfPt[ihist].Write()
    csctfPt_eta1[ihist].Write()
    csctfPt_eta2[ihist].Write()
    csctfPt_eta3[ihist].Write()
    csctfPt_eta4[ihist].Write()
    

for hist in hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

del newfile

# ================================



print '\n =========== Analysis Results ============= ' \
      '\n Denominator(Muons with 2 matched Segs)   = ', muon_count['denominator'], \
      '\n Numerator(when track has a matched Lct ) = ', muon_count['numerator'], \
      '\n Two Hit EMTF Tracks            : ', gen_count['2hit_tracks'],\
      '\n Three Hit EMTF Tracks : ', gen_count['3hit_tracks'],\
      '\n Four Hit EMTF Tracks : ', gen_count['4hit_tracks']


# ==============================================================================================
# export counter values to .csv file for latex
# The .csv is in form for latex{tabular}.  Either import the file or copy/paste contents inside tabular region

'''
# Row headers.  Change these titles as you see fit.
row = ['Denominator', 'Numerator', 'Different Sectors', 'Same Station', 'Eta/Phi Windows', 'Sector Edge', 'Unaccounted']

table = np.array([

    #first row is column headers of eta regions 
    [' ', 'All Eta', '$0.9 < \eta < 1.3$', '$1.3 < \eta < 1.7$', '$1.7 < \eta < 2.1$', '$2.1 < \eta < 2.4$'],

    [row[0], final_count['denominator'], final_count['denominator_0.9_1.3'], final_count['denominator_1.3_1.7'], final_count['denominator_1.7_2.1'], \
     final_count['denominator_2.1_2.4'] ],
    
    [row[1], final_count['numerator'], final_count['numerator_0.9_1.3'], final_count['numerator_1.3_1.7'], final_count['numerator_1.7_2.1'], \
     final_count['numerator_2.1_2.4'] ],

    [row[2], final_count['fail_diff_sector'], final_count['fail_diff_sector_0.9_1.3'], final_count['fail_diff_sector_1.3_1.7'], final_count['fail_diff_sector_1.7_2.1'], \
          final_count['fail_diff_sector_2.1_2.4'] ],

    [row[3], final_count['fail_same_station'], final_count['fail_same_station_0.9_1.3'], final_count['fail_same_station_1.3_1.7'], final_count['fail_same_station_1.7_2.1'], \
     final_count['fail_same_station_2.1_2.4'] ],

    [row[4], final_count['fail_windows'], final_count['fail_windows_0.9_1.3'], final_count['fail_windows_1.3_1.7'], final_count['fail_windows_1.7_2.1'], \
     final_count['fail_windows_2.1_2.4'] ],

    [row[5], final_count['fail_sector_edge'], final_count['fail_sector_edge_0.9_1.3'], final_count['fail_sector_edge_1.3_1.7'], final_count['fail_sector_edge_1.7_2.1'], \
          final_count['fail_sector_edge_2.1_2.4'] ],

    [row[6], final_count['fail_unaccounted'], final_count['fail_unaccounted_0.9_1.3'], final_count['fail_unaccounted_1.3_1.7'], final_count['fail_unaccounted_1.7_2.1'], \
               final_count['fail_unaccounted_2.1_2.4'] ],
        
    ])

np.savetxt("myTable.csv", table, delimiter=' & ', fmt="%s", newline=' \\\\\n')

# ==============================================================================================


# Table Debugging
# Assuming my current table is size 7 x 5 (7 rows, 5 columns).   
# Add rows and columns to make sure all final counts are conserved.
test_table = table[1:, 1:].astype(np.int)

print '\n\n Final Table:\n', test_table

for col in range(5):
    if test_table[1:, col].sum() != test_table[0,col]:  print '----> Column', col, 'has an error !!!!! '
    
for row in range(7):    
    if test_table[row, 1:].sum() != test_table[row, 0]: print '----> Row', col, 'has an error !!!!! '

'''
