########################################################
## eff_modules.py   A script to find CSCTF efficiency by segment-Lct matching
##
## By David Curry
##
########################################################


import sys
import os
import re
import numpy as np
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
from array import *

def get_Tchain(directory, num_files):

    '''
    Takes a directory of root files and gives a tchain of the desired length(numfiles)
    '''

    os.system('rm tchain')
    
    # define the tchain object
    tchain_reco  = TChain('recoMuons') 
    tchain_csctf = TChain('csctfTTree')

    # print the contents of directory to a txt file
    temp_str = "cmsLs "+directory+ " | grep root | awk '{print ""$5""}' >> tchain"
    os.system(temp_str)
    
    with open('tchain') as file:

        for i, line in enumerate(file):

            #if i is num_files: break

            print '-----> Tchain adding root://eoscms//eos/cms/', line
            
            #first add the recoMuon tree to the chain
            tchain_reco.Add('root://eoscms//eos/cms/'+line)
            
            # now add the csctf tree
            tchain_csctf.Add('root://eoscms//eos/cms/'+line)
            
            
    # end file loop
    
    chain_list = [tchain_reco, tchain_csctf]
            
    return chain_list


def whichQ(iTrk, csc):

    '''
    Checks track quality
    '''

    # first get the track mode
    trkMode = track_mode(iTrk, csc)

    trkQ = -999

    # quality 3
    if trkMode == 2 and abs(csc.EtaTrk[iTrk]) > 1.2: trkQ = 3
    if trkMode == 3 or trkMode == 4 or trkMode == 5 or trkMode == 12: trkQ = 3
    

    # quality 2
    if trkMode == 6 and abs(csc.EtaTrk[iTrk]) > 1.2: trkQ = 2
    if trkMode == 7 and abs(csc.EtaTrk[iTrk]) < 2.1: trkQ = 2 
    if trkMode == 13 and abs(csc.EtaTrk[iTrk]) > 2.1: trkQ = 2
    
    if trkQ == -999:  trkQ = 1
    
    return trkQ


def track_mode(iTrk, csc):
    
    '''
    Returns track mode
    '''

    final_mode = -999
    
    if csc.NumLCTsTrk[iTrk] < 3:
        # first look at two hit tracks
        # Possible modes are station combinations:
        # 1-2  Mode 6 : sum 3
        # 1-3  Mode 7 : sum 4
        # 1-4  Mode 13: sum 5
        # 2-3  Mode 8 : sum 5
        # 2-4  Mode 9 : sum 6
        # 3-4  Mode 10: sum 7
    
        temp_mode = 0; track_mode = 0
        isStation_1 = False; isStation_2 = False

        # loop over tracks hits to find mode
        for iCsc in range(csc.NumLCTsTrk[iTrk]):

            temp_mode += csc.trLctStation[iTrk*4 + iCsc]
        
            if csc.trLctStation[iTrk*4 + iCsc] == 1: isStation_1 = True
            if csc.trLctStation[iTrk*4 + iCsc] == 2: isStation_2 = True

        # Which mode is track
        if temp_mode == 3: final_mode = 6
        if temp_mode == 4: final_mode = 7
        if temp_mode == 6: final_mode = 9
        if temp_mode == 7: final_mode = 10

        # In the event of mode 5 we need to find which configuration
        if track_mode == 5 and isStation_1: final_mode = 13
        elif final_mode == -999: final_mode = 8
    
        # for overlap track
        if final_mode == -999: final_mode = 15

    # end 2 hit tracks

    # 3 or more hit tracks
    # Possible modes are station combinations:
    # 1-2-3-4 Mode 1 sum 10
    # 1-2-3   Mode 2 sum 6
    # 1-2-4   Mode 2 sum 7
    # 1-3-4   Mode 3 sum 8
    # 2-3-4   Mode 4 sum 9

    if csc.NumLCTsTrk[iTrk] > 2:
        
        temp_mode = 0
        isStation1 = False
        isStation2 = False
        isStation3 = False
        isStation4 = False

        for iCsc in range(csc.NumLCTsTrk[iTrk]):
            temp_mode += csc.trLctStation[iTrk*4 + iCsc]

        # Which mode is track
        if temp_mode == 10: final_mode = 2 
        if temp_mode == 6:  final_mode = 2
        if temp_mode == 7:  final_mode = 3
        if temp_mode == 8:  final_mode = 4
        if temp_mode == 9:  final_mode = 5
        
        if final_mode == -999: final_mode = 12
        
    return final_mode
        


# ============================================================================

def is_two_segs(iEvt, iReco, tree, printLevel):

    ''' Returns a list: [Bool, [Lct Ids] ]
    Bool is whether the muon has two Segs matched to event Lcts.
    Lct Id is which Lct the Seg is matched to. Minimum two Ids
    '''

    if printLevel > 0:
        print '----> Checking muon for two matched segments.'

    # create list to be returned.  [bool, list[int]]
    list = [False, []]

    # Fill with endcap values to check for halo muon
    halo_list = []
    
    for iSeg in range(tree.muonNsegs[iReco]):
        
        if printLevel > 1: print '\nLooping over Segment # ', iSeg
        
        # Check if seg is matched to Lct
        if iSeg > 15: continue

        if printLevel > 1:
            print ' segStation :', tree.muon_cscsegs_station[iReco*16 + iSeg]
            print ' segEndcap  :', tree.muon_cscsegs_endcap[iReco*16 + iSeg]


        if tree.muon_cscsegs_ismatched[iReco*16 + iSeg]:
            
            id = tree.muon_cscsegs_lctId[iReco*16 + iSeg]
            
            if id == -999: continue
            
            if printLevel > 1:
                print '\nSegment is matched to Lct', id, \
                    '\n LctStation = ', tree.lctStation.at(id), \
                    '\n LctEndcap  = ', tree.lctEndcap.at(id)

            halo_list.append(tree.lctEndcap.at(id))
                
            if id not in list[1]: list[1].append(id)
            
    # end seg loop
            

    if len(list[1]) > 1:
        
        list[0] = True 

        if printLevel > 0: print'\n-----> Muon has two segments matched to LCTs...'

        # check for halo muon.
        if halo_list.count(halo_list[0]) < len(halo_list):  list[0] = False

    return list
    

# end is two segs matched


def is_track_match(iEvt, csc, id_list, printLevel):

    '''
    Returns a list:  [Bool, track Id].
    Bool is whether a track match was found to Seg Lcts, and track id is which track was macthed
    '''

    if printLevel > 0: print '-----> Checking for Track Lct - Seg Lct Match.'

    list = [False, 999]

    is_lct_match = False
    
    # Does a track have the same Lcts that segs matched to?
    # Loop over tracks
    for iTrk in range(0, csc.numTrks):
        for iLct in range(0, csc.numTrkLCTs[iTrk]):
            
            if is_lct_match: break
            
            if printLevel > 1:
                print '\nLooping over Track #', iTrk, ', Lct #', iLct, \
                    '\n trLctStation = ', csc.trkLctStation[iTrk*4 + iLct], \
                    '\n trLctEndcap  = ', csc.trkLctEndcap[iTrk*4 + iLct], \
                    '\n trLctSector  = ', csc.trkLctSector[iTrk*4 + iLct], \
                    '\n trLctRing    = ', csc.trkLctRing[iTrk*4 + iLct], \
                    '\n trLctChamber = ', csc.trkLctChamber[iTrk*4 + iLct], \
                    '\n trLctWire    = ', csc.trkLctWire[iTrk*4 + iLct], \
                    '\n trLctStrip   = ', csc.trkLctStrip[iTrk*4 + iLct], \
                    #'\n trLctglobalEta  = ', csc.trLctglobalEta[iTrk*4 + iLct], \
                    #'\n trLctglobalPhi  = ', csc.trLctglobalPhi[iTrk*4 + iLct]
                
            # compare track Lct to seg matched Lcts.  Loop over id_list
            for x in id_list:
                
                if is_lct_match: break

                if printLevel > 1:
                    print '\n\tLooping over LCTs in id_list:', x, \
                      '\n LctStation = ', csc.lctStation.at(x), \
                      '\n LctEndcap  = ', csc.lctEndcap.at(x), \
                      '\n LctSector  = ', csc.lctSector.at(x), \
                      '\n LctRing    = ', csc.lctRing.at(x), \
                      '\n LctChamber = ', csc.lctChamber.at(x), \
                      '\n LctWire    = ', csc.lctWire.at(x), \
                      '\n LctStrip   = ', csc.lctStrip.at(x), \
                      #'\n LctglobalEta  = ', csc.lctglobalEta.at(x), \
                      #'\n LctglobalPhi  = ', csc.lctglobalPhi.at(x)
                

                if csc.trkLctStation[iTrk*4 + iLct]   != csc.lctStation.at(x):   continue
                if csc.trkLctEndcap[iTrk*4 + iLct]    != csc.lctEndcap.at(x):    continue
                if csc.trkLctSector[iTrk*4 + iLct]    != csc.lctSector.at(x):    continue
                if csc.trkLctRing[iTrk*4 + iLct]      != csc.lctRing.at(x):      continue
                if csc.trkLctChamber[iTrk*4 + iLct]   != csc.lctChamber.at(x):   continue
                if csc.trkLctWire[iTrk*4 + iLct]      != csc.lctWire.at(x):      continue
                if csc.trkLctStrip[iTrk*4 + iLct]     != csc.lctStrip.at(x):     continue
                #if csc.trLctglobalEta[iTrk*4 + iLct] != csc.lctglobalEta.at(x):   continue
                #if csc.trLctglobalPhi[iTrk*4 + iLct] != csc.lctglobalPhi.at(x):   continue
                
                is_lct_match = True
                    
                if printLevel > 1: print'\n-----> Seg Lct and Track Lct are matched.'
                    
                list[0], list[1] = True, iTrk
                        
    if printLevel > 0 and not is_lct_match: print '-----> Could not match muon to a track.'
                    
    return list
                
# end is track match


def deltaR(iEvt, iReco, reco, csc, printLevel):

    '''
    Takes in muon and track and returns a deltaR value
    '''

    if printLevel > 1: print '\n------> Calculating Delta R between muon and track'
    



    

# ==== Binning for efficiency plots ======

num_phiBins = 16
num_etaBins = 16

scale_phi_temp = [0]*num_phiBins
scale_eta_temp = [0]*num_etaBins

scale_pt_temp = [0, 2, 3, 4, 8, 15, 25, 35, 50, 75, 100]

# Initialize phi
phiMin = -np.pi

scale_phi_temp[0] = phiMin

for iphi in range(1,len(scale_phi_temp)):
    scale_phi_temp[iphi] = scale_phi_temp[iphi-1] + (2*np.pi/(num_phiBins-1))
    

etaMin = 1.2
scale_eta_temp[0] = etaMin

for ieta in range(len(scale_eta_temp)):
    scale_eta_temp[ieta] = etaMin + (1.5*ieta/(num_etaBins-1))

#print scale_eta_temp
#print scale_phi_temp

scale_pt  = array('f', scale_pt_temp)    
scale_phi = array('f', scale_phi_temp)
scale_eta = array('f', scale_eta_temp)


# ========================================

# some useful arrays
# Array of delta phi depending on eta.  v = [ eta , delta phi ]
eta_dphi_ME1toME2 = [127, 127, 127, 127, 57, 45, 41,  42,  42,  31,
                     127, 127,  29,  28, 29, 30, 35,  37,  34,  34,
                     36,  37,  37,  37, 39, 40, 52, 126, 104, 104,
                     87,  90,  93,  87, 85, 82, 80,  79,  82,  79,
                     79,  77,  75,  75, 67, 67, 69,  68,  67,  65,
                     65,  64,  60,  58, 57, 57, 57,  55,  53,  51,
                     49,  46,  36, 127]

eta_dphi_ME1toME3 = [127, 127, 127, 127, 127, 127, 40, 80, 80, 64,
                     127, 127,  62,  41,  41,  45, 47, 48, 47, 46,
                     47,  50,  52,  51,  53,  54, 55, 73, 82, 91,
                     91,  94, 100,  99,  95,  94, 95, 91, 96, 96,
                     94,  94,  88,  88,  80,  80, 84, 84, 79, 78,
                     80,  78,  75,  72,  70,  71, 69, 71, 71, 66,
                     61,  60,  43, 127]

dt_csc_dphi = [127, 127, 127, 127,  90,  78,  76,  76,  66,  65,
               59,  90,  50,  49,  37, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127]
