###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT


# Root file of Histograms
#file = TFile('plots/mc_allEvents.root')
file = TFile('plots/trig_eff_plots_allEta_singleMu.root')


# Get teh Hists
dphi12_trk15  = file.Get('dphi12_trk15')
dphi13_trk15  = file.Get('dphi13_trk15')
dphi14_trk15  = file.Get('dphi14_trk15')
dphi23_trk15  = file.Get('dphi23_trk15')
dphi24_trk15  = file.Get('dphi24_trk15')
dphi23_trk15  = file.Get('dphi34_trk15')

dphi_trk15 = file.Get('h2dphi_trk15')
deta_trk15 = file.Get('h2deta_trk15')

label_list = ['1-2', '1-3', '1-4', '2-3', '2-4', '3-4']


c1 = TCanvas('c1')
dphi_trk15.SetStats(0)

for i in range(0, len(label_list)):
    dphi_trk15.GetXaxis().SetBinLabel(i+1, label_list[i])
    
dphi_trk15.GetYaxis().SetTitle('|#Delta #Phi|')
dphi_trk15.Draw('COLZ')


c2 = TCanvas('c2')
deta_trk15.SetStats(0)

for i in range(0, len(label_list)):
    deta_trk15.GetXaxis().SetBinLabel(i+1, label_list[i])

deta_trk15.GetYaxis().SetTitle('|#Delta #eta|')
deta_trk15.Draw('COLZ')

raw_input('Press return to continue...')
