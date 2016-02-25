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
file = TFile('plots/trig_eff_plots_allEta_Pt16GeV.root')

title = 'test'

print '\n\n============ Making Rate Plots ============='


# ====== Get the Histograms ==========================

rate     = file.Get('hrate')
rate_leg = file.Get('hrate_leg')

rate_gmt     = file.Get('hrate_gmt')
rate_gmt_leg = file.Get('hrate_gmt_leg')

rate_15_14_13_11 = file.Get('hrate_15_14_13_11')
rate_15_14_13 = file.Get('hrate_15_14_13')
rate_15_14 = file.Get('hrate_15_14')
rate_15 = file.Get('hrate_15')

rate_15_14_13_11_leg = file.Get('hrate_15_14_13_11_leg')
rate_15_14_13_leg = file.Get('hrate_15_14_13_leg')
rate_15_14_leg = file.Get('hrate_15_14_leg')
rate_15_leg = file.Get('hrate_15_leg')


# ====================================================


cRate     = TCanvas('cRate')
cRate_leg = TCanvas('cRate_leg')

cRate_divide = TCanvas('cRate_divide')

stack      = THStack('stack', '')
stack_leg  = THStack('stack_leg', '')

cRate.cd()
cRate.SetGridx()
cRate.SetGridy()

rate.SetStats(0)
rate.SetLineColor(kBlue)
rate.SetLineWidth(2)
rate.SetMarkerStyle(23)
rate.SetMarkerSize(0.8)
rate.SetMinimum(0.0)

rate_gmt.SetLineColor(6)
rate_gmt.SetLineWidth(2)
rate_gmt.SetMarkerStyle(23)
rate_gmt.SetMarkerSize(0.8)

rate_15_14_13_11.SetLineColor(kRed)
rate_15_14_13_11.SetLineWidth(2)
rate_15_14_13_11.SetMarkerStyle(23)
rate_15_14_13_11.SetMarkerSize(0.8)

rate_15_14_13.SetLineColor(kGreen)
rate_15_14_13.SetLineWidth(2)
rate_15_14_13.SetMarkerStyle(23)
rate_15_14_13.SetMarkerSize(0.8)

rate_15_14.SetLineColor(kBlack)
rate_15_14.SetLineWidth(2)
rate_15_14.SetMarkerStyle(23)
rate_15_14.SetMarkerSize(0.8)

rate_15.SetLineColor(kOrange)
rate_15.SetLineWidth(2)
rate_15.SetMarkerStyle(23)
rate_15.SetMarkerSize(0.8)

#rate.Draw()
#rate_15_14_13_11.Draw('same')
#rate_15_14_13.Draw('same')
#rate_15_14.Draw('same')
#rate_15.Draw('same')
#rate_gmt.Draw('same')


stack.Add(rate_gmt)
stack.Add(rate_15_14_13_11)
stack.Add(rate_15_14_13)
stack.Add(rate_15_14)
stack.Add(rate_15)
stack.Add(rate)
stack.Draw('nostack')
stack.GetXaxis().SetTitle("EMTF p_{T}[GeV]")
stack.GetYaxis().SetTitle("Rate")
stack.GetYaxis().SetTitleOffset(1.35)
stack.GetXaxis().SetNdivisions(509)
stack.GetYaxis().SetNdivisions(514)


lrate = TLegend(0.85,1,1,0.6);
lrate.SetBorderSize(0)
lrate.SetFillColor(0)
lrate.AddEntry(rate, "All Modes")
lrate.AddEntry(rate_gmt, "GMT Modes")
lrate.AddEntry(rate_15_14_13_11, "uGMT Modes")
lrate.AddEntry(rate_15_14_13, "15-14-13")
lrate.AddEntry(rate_15_14, "15-14")
lrate.AddEntry(rate_15, "15")

lrate.Draw("same")

cRate.SetLogy()
cRate.Modified()
cRate.Update()
cRate.SaveAs('plots/rate_'+title+'.pdf')


# Legacy ============================================================
cRate_leg.cd()
cRate_leg.SetGridx()
cRate_leg.SetGridy()

rate_leg.SetStats(0)
rate_leg.SetLineColor(kBlue)
rate_leg.SetLineWidth(2)
rate_leg.SetMarkerStyle(23)
rate_leg.SetMarkerSize(0.8)
rate_leg.SetMinimum(0.0)

rate_gmt_leg.SetLineColor(6)
rate_gmt_leg.SetLineWidth(2)
rate_gmt_leg.SetMarkerStyle(23)
rate_gmt_leg.SetMarkerSize(0.8)

rate_15_14_13_11_leg.SetLineColor(kRed)
rate_15_14_13_11_leg.SetLineWidth(2)
rate_15_14_13_11_leg.SetMarkerStyle(23)
rate_15_14_13_11_leg.SetMarkerSize(0.8)

rate_15_14_13_leg.SetLineColor(kGreen)
rate_15_14_13_leg.SetLineWidth(2)
rate_15_14_13_leg.SetMarkerStyle(23)
rate_15_14_13_leg.SetMarkerSize(0.8)

rate_15_14_leg.SetLineColor(kBlack)
rate_15_14_leg.SetLineWidth(2)
rate_15_14_leg.SetMarkerStyle(23)
rate_15_14_leg.SetMarkerSize(0.8)

rate_15_leg.SetLineColor(kOrange)
rate_15_leg.SetLineWidth(2)
rate_15_leg.SetMarkerStyle(23)
rate_15_leg.SetMarkerSize(0.8)

#rate.Draw()
#rate_15_14_13_11.Draw('same')
#rate_15_14_13.Draw('same')
#rate_15_14.Draw('same')
#rate_15.Draw('same')
#rate_gmt.Draw('same')


stack_leg.Add(rate_gmt_leg)
stack_leg.Add(rate_15_14_13_11_leg)
stack_leg.Add(rate_15_14_13_leg)
stack_leg.Add(rate_15_14_leg)
stack_leg.Add(rate_15_leg)
stack_leg.Add(rate_leg)
stack_leg.Draw('nostack')
stack_leg.GetXaxis().SetTitle("CSCTF p_{T}[GeV]")
stack_leg.GetYaxis().SetTitle("Rate")
stack_leg.GetYaxis().SetTitleOffset(1.35)
stack_leg.GetXaxis().SetNdivisions(509)
stack_leg.GetYaxis().SetNdivisions(514)


lrate_leg = TLegend(0.85,1,1,0.6);
lrate_leg.SetBorderSize(0)
lrate_leg.SetFillColor(0)
lrate_leg.AddEntry(rate_leg, "All Modes")
lrate_leg.AddEntry(rate_gmt_leg, "GMT Modes")
lrate_leg.AddEntry(rate_15_14_13_11_leg, "uGMT Modes")
lrate_leg.AddEntry(rate_15_14_13_leg, "15-14-13")
lrate_leg.AddEntry(rate_15_14_leg, "15-14")
lrate_leg.AddEntry(rate_15_leg, "15")

lrate_leg.Draw("same")

cRate_leg.SetLogy()
cRate_leg.Modified()
cRate_leg.Update()
cRate_leg.SaveAs('plots/rate_leg'+title+'.pdf')


# =======================================
# Divide the EMTF/CSCTF

cRate_divide.cd()
cRate_divide.SetGridx()
cRate_divide.SetGridy()

rate_15_14_13_11.Divide(rate_15_14_13_11_leg)
rate_15_14_13.Divide(rate_15_14_13_leg)
rate_15_14.Divide(rate_15_14_leg)
rate_15.Divide(rate_15_leg)
rate_gmt.Divide(rate_gmt_leg)
rate.Divide(rate_leg)

rate_15_14_13_11.SetStats(0)

rate_15_14_13_11.Draw()
rate_15_14_13.Draw('same')
rate_15_14.Draw('same')
rate_15.Draw('same')
rate_gmt.Draw('same')
rate.Draw('same')


lrate_d = TLegend(0.85,1,1,0.6);
lrate_d.SetBorderSize(0)
lrate_d.SetFillColor(0)
lrate_d.AddEntry(rate, "All Modes")
lrate_d.AddEntry(rate_gmt, "GMT Modes")
lrate_d.AddEntry(rate_15_14_13_11, "uGMT Modes")
lrate_d.AddEntry(rate_15_14_13, "15-14-13")
lrate_d.AddEntry(rate_15_14, "15-14")
lrate_d.AddEntry(rate_15, "15")
lrate_d.Draw("same")


cRate_divide.Modified()
cRate_divide.Update()
cRate_divide.SaveAs('plots/rate_leg_divide_'+title+'.pdf')

raw_input('Press return to continue...')
