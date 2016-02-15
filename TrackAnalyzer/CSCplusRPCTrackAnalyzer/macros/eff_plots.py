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

title = 'test'


# ====== Track matching efficiency ======
pt  = file.Get('hpt')
eta = file.Get('heta')
phi = file.Get('hphi')

pt_tr  = file.Get('hpt_trigger')
eta_tr = file.Get('heta_trigger')
phi_tr = file.Get('hphi_trigger')

'''
pt_tr_gmt  = file.Get('h_pt_trigger_gmt')
eta_tr_gmt = file.Get('h_eta_trigger_gmt')
phi_tr_gmt = file.Get('h_phi_trigger_gmt')
'''

tg_pt   = TGraphAsymmErrors(pt_tr, pt, '')
tg_eta  = TGraphAsymmErrors(eta_tr, eta, '')
tg_phi  = TGraphAsymmErrors(phi_tr, phi, '')

'''
tg_pt_gmt   = TGraphAsymmErrors(pt_tr_gmt, pt, '')
tg_eta_gmt  = TGraphAsymmErrors(eta_tr_gmt, eta, '')
tg_phi_gmt  = TGraphAsymmErrors(phi_tr_gmt, phi, '')
'''

cEta = TCanvas('cEta')
cPt  = TCanvas('cPt')
cPhi = TCanvas('cPhi')

# Start making the Canvas
cEta.cd()
tg_eta.SetLineColor(kBlue)
tg_eta.SetLineWidth(2)
tg_eta.SetMarkerStyle(23)
tg_eta.SetMarkerSize(0.8)
tg_eta.GetXaxis().SetTitle("|#eta(gen #mu)|")
tg_eta.GetYaxis().SetTitle("Efficiency")
tg_eta.GetYaxis().SetTitleOffset(1.35)
tg_eta.GetXaxis().SetNdivisions(509)
tg_eta.GetYaxis().SetNdivisions(514)
cEta.SetGridx()
cEta.SetGridy()
tg_eta.SetMinimum(0.0)
tg_eta.SetMaximum(1.02)
tg_eta.Draw('AP')
cEta.Modified()
cEta.Update()

cEta.SaveAs('plots/efficiency_alleta_'+title+'.pdf')


# Phi
cPhi.cd()
tg_phi.SetLineColor(kBlue)
tg_phi.SetLineWidth(2)
tg_phi.SetMarkerStyle(23)
tg_phi.SetMarkerSize(0.8)
tg_phi.GetXaxis().SetTitle("|#phi(#mu)|")
tg_phi.GetYaxis().SetTitle("Efficiency")
tg_phi.GetYaxis().SetTitleOffset(1.35)
tg_phi.GetXaxis().SetNdivisions(509)
tg_phi.GetYaxis().SetNdivisions(514)
cPhi.SetGridx()
cPhi.SetGridy()
tg_phi.SetMinimum(0.0)
tg_phi.SetMaximum(1.02)
tg_phi.Draw('AP')
cPhi.Modified()
cPhi.Update()

cPhi.SaveAs('plots/efficiency_phi_'+title+'.pdf')

# Pt
cPt.cd()
tg_pt.SetLineColor(kBlue)
tg_pt.SetLineWidth(2)
tg_pt.SetMarkerStyle(23)
tg_pt.SetMarkerSize(0.8)
tg_pt.GetXaxis().SetTitle("p_{T}(gen #mu)")
tg_pt.GetYaxis().SetTitle("Efficiency")
tg_pt.GetYaxis().SetTitleOffset(1.35)
tg_pt.GetXaxis().SetNdivisions(509)
tg_pt.GetYaxis().SetNdivisions(514)
cPt.SetGridx()
cPt.SetGridy()
tg_pt.SetMinimum(0.0)
tg_pt.SetMaximum(1.02)
tg_pt.Draw('AP')
cPt.Modified()
cPt.Update()

cPt.SaveAs('plots/efficiency_pt_'+title+'.pdf')



# Quick plotting
# List of variables to plot:  var name, # of bins, x-axis range, x axis
variable_list = [ 
    #['hdpt', 'Gen p_{T} - EMTF p_{T}', 50, -10, 10],
    #['hdpt_rpc', 'Gen p_{T} - EMTF+RPC p_{T}', 50, -10, 10],
    #['h_mode_trigger', 'tr EMTF Mode', 16, 0, 15],
    #['h_RPC_mode_trigger', 'tr EMTF Mode(+RPC)', 16, 0, 15],
    #['h_mode', 'EMTF Mode', 16, 0, 15],
    #['h_RPC_mode', 'EMTF Mode(+RPC)', 16, 0, 15],
    #['h_trkPt', 'CSCTF p_{T} [GeV]', 50, 0, 150],
    #['h_trkEta', 'CSCTF #eta', 50, 0, 2.4],
    #['h_trkPhi', 'CSCTF #phi', 50, -3.2, 3.2],
    #['h_trkPt_rpc', 'CSCTF+RPC p_{T} [GeV]', 50,0, 150],
    #['h_trkEta_rpc', 'CSCTF+RPC #eta', 50, 0, 2.4],
    #['h_trkPhi_rpc', 'CSCTF+RPC #phi', 50, -3.2, 3.2],
    #['h_GenPt', 'Gen p_{T} [GeV]', 50,0, 150],
    #['h_GenEta', 'Gen #eta', 50, 0, 2.4],
    #['h_GenPhi', 'Gen #phi', 50, -3.2, 3.2]
    #['hdEta', 'Delta #eta (RPC Cluster-CSC)', 50, -0.2, 0.2],
    #['hdPhi', 'Delta #phi (RPC Cluster-CSC)', 50, -0.1, 0.1],
    #['hdEta1', 'Delta #eta (RPC Cluster1-CSC1)', 50, -0.2, 0.2],
    #['hdPhi1', 'Delta #phi (RPC Cluster1-CSC1)', 50, -0.1, 0.1],
    #['hdEta2', 'Delta #eta (RPC Cluster2-CSC2)', 50, -0.2, 0.2],
    #['hdPhi2', 'Delta #phi (RPC Cluster2-CSC2)', 50, -0.1, 0.1],
    #['hdEta3', 'Delta #eta (RPC Cluster3-CSC3)', 50, -0.2, 0.2],
    #['hdPhi3', 'Delta #phi (RPC Cluster3-CSC3)', 50, -0.1, 0.1],
    #['hdEta4', 'Delta #eta (RPC Cluster4-CSC4)', 50, -0.2, 0.2],
    #['hdPhi4', 'Delta #phi (RPC Cluster4-CSC4)', 50, -0.3, 0.3]
    ]

def doPlot(variable, xaxis, nbins, bin_low, bin_high):

    canvas = TCanvas('canvas')
    hist = file.Get(variable) 
    hist.GetXaxis().SetLimits(bin_low, bin_high)
    hist.GetXaxis().SetTitle(xaxis)
    #if variable == 'hdPhi' or variable== 'hdEta':

    hist.SetFillColor(kYellow)
    hist.SetStats(0)
    hist.Draw()

    #raw_input('Press return to continue...')
    
    canvas.SaveAs('plots/'+variable+'_'+title+'.pdf')

    canvas.IsA().Destructor(canvas)
    hist.IsA().Destructor(hist)


# end do plot

for variable in variable_list:

    doPlot(variable[0], variable[1], variable[2], variable[3], variable[4])

raw_input('Press return to continue...')
