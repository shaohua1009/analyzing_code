#!/bin/env python
import os, sys
import numpy as np
import cPickle as cp
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.font_manager as ftman
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.colorbar as cb

#matplotlib.rcParams['axes.unicode_minus'] = False

INP = sys.argv[1]
OUT=sys.argv[2]
X = 57.2957795
FesMax=0.00016

#******************************************************************************#
#                                                                              #
# Generate the color map used to for creating 2D density distribution.         #
#                                                                              #
#******************************************************************************#
def genColorMap(cmap):
# Creat new colormap with white for 1.0
#  cvals = [(cmap(i)) for i in xrange(0,255)] + [('white')]
  cvals = [('white')] + [(cmap(i)) for i in xrange(1,256)] 
#  cvals = [(cmap(i)) for i in xrange(1,256)] 
  new_map = colors.LinearSegmentedColormap.from_list('new_map',cvals, N=256)
  return new_map

#******************************************************************************#
#                                                                              #
# Calculate the free energy surface from the 2D density distribution.          #
#                                                                              #
#******************************************************************************#
def calcFELandscape(density2D, temperature):
  kb = 0.008314            # Boltzmann constant in unit kJ/mol/K
  factor = -kb*temperature 
  freeEnergy2D = []
  for density1D in density2D:
    freeEnergy1D = []
    for density in density1D:
      if density <= 0: freeEnergy1D.append(1000.0)
      else: freeEnergy1D.append(factor*np.log(density))

    freeEnergy2D.append(freeEnergy1D) 
  fes = np.array(freeEnergy2D,dtype=np.float64)
  return fes-np.amin(fes)


def calcDensity2D (Xs, Ys, Ws=None):
  Bins = np.linspace(start=-180, stop=180, num=101)
  #print np.shape(Xs)
  #print np.shape(Ys)
  #print np.shape(Ws)
  hist2D, xedges, yedges = np.histogram2d(Xs,Ys,bins=Bins,weights=Ws,density=True)
  #density2D = hist2D/np.sum(hist2D)
  density2D = hist2D
  print np.amax(density2D)
  xstep = xedges[1] - xedges[0]
  xmidps = xedges[1:] - 0.5*xstep
  ystep = yedges[1] - yedges[0]
  ymidps = yedges[1:] - 0.5*ystep

  return xmidps, ymidps, density2D


################################################################################
def MakeFigure(FigW,FigH, inp, out):

  TitleFP  = ftman.FontProperties(size=18)
  LegendFP = ftman.FontProperties(size=18)
  LabelFP  = ftman.FontProperties(size=20)
  #print "Loading data ..."
  cvvals = np.loadtxt(inp,dtype=np.float32,usecols=(0,1),unpack=True,comments=['#', '@'])

  #xx0s = np.loadtxt("phipsi_CHA15.txt",dtype=np.float32,unpack=True)
  #xx0s = np.loadtxt("betaIp.txt",dtype=np.float32,unpack=True)
  #xx0s = np.loadtxt("betaII.txt",dtype=np.float32,unpack=True)
  #xx0s = np.loadtxt("betaIIp.txt",dtype=np.float32,unpack=True)
  #xx1s = np.loadtxt("betaI.txt",dtype=np.float32,unpack=True)
  #xx1s = np.loadtxt("betaIp.txt",dtype=np.float32,unpack=True)
  #xx1s = np.loadtxt("betaII.txt",dtype=np.float32,unpack=True)
  #xx1s = np.loadtxt("betaIIp.txt",dtype=np.float32,unpack=True)

  nRes = len(cvvals)/2
  #print cvvals 
  ResNames = ['GLY']
  ResIDs = [1]

  NPX = nRes
  NPY = 1

  Fig = plt.figure(figsize = (FigW,FigH),dpi=300)

  #left,bot,right,top = (0.08,0.25,0.90,0.95)
  left,bot,right,top = (0.23,0.30,0.73,0.80)

  HSpace = 0.05*(top-bot)/NPY
  WSpace = 0.10*(right-left)/NPX

  SubPlotH = (top - bot - (NPY-1)*HSpace)/NPY
  SubPlotW = (right - left - (NPX-1)*WSpace)/NPX

  for ires in range(nRes):
    #print "Makeing the %dth plot ..."%ires
    x0 = left + (ires%NPX)*(SubPlotW+WSpace)
    y0 = bot + (ires/NPX)*(SubPlotH + HSpace)
    ax = Fig.add_axes([x0,y0,SubPlotW,SubPlotH])
    ax.set_xlabel("$\phi$", fontsize=9)
    #ax.set_xlabel(" ")
    if ires == 0: ax.set_ylabel("$\psi$", fontsize=9)
    else: ax.set_ylabel(" ")
    phi = cvvals[ires*2]
    psi = cvvals[ires*2+1]
    xmidps,ymidps,dens2d = calcDensity2D (phi, psi)
    #fes = calcFELandscape(dens2d,300)
    #print dens2d
    yvals,xvals = np.meshgrid(xmidps,ymidps)

    if ires/NPX == 0: 
      xtlv=True
    else:
      xtlv=False


    if ires%NPX == 0:
      ytlv=True
    else:
      ytlv=False

    pc = MakeSubPlot(ax,xvals,yvals,dens2d,xtlv, ytlv, 0, FesMax)

    # NMR
    #xx = xx0s[ires*2]
    #yy = xx0s[ires*2+1]
    #ax.plot(xx,yy,linestyle='None',linewidth=0,color='black',marker='o',
    #        markeredgecolor='black', markeredgewidth=0,
    #        markerfacecolor='black', markersize=8, label='...')

    #xx = xx1s[ires*2]
    #yy = xx1s[ires*2+1]
    #ax.plot(xx,yy,linestyle='None',linewidth=0,color='g',marker='o',
    #        markeredgecolor='g', markeredgewidth=0,
    #        markerfacecolor='g', markersize=8, label='...')

    # Y-axis label
#    x0 = 0.2 * left
#    y0 = y0 + 0.5*SubPlotH
#    Fig.text(x0,y0,"%s-%d"%(ResNames[ires],ires+1),verticalalignment='center',
#             horizontalalignment='center',rotation='vertical',fontproperties=LabelFP)

  cbl,cbb,cbw,cbh = left+NPX*(WSpace+SubPlotW), 0.5*(top+bot)-0.5*SubPlotH, 0.02, SubPlotH
  cax = Fig.add_axes([cbl,cbb,cbw,cbh])
  cb = Fig.colorbar(pc,cax=cax,orientation='vertical')
  cbticks = np.arange(0,FesMax+0.00001,0.00004)
  cb.set_ticks(ticks=cbticks)
  cb.set_ticklabels(ticklabels=[str(i) for i in cbticks])
  cb.ax.tick_params(labelsize=5)
  cb.ax.set_yticklabels(["{:.1e}".format(i) for i in cbticks])

  Fig.savefig(out)


################################################################################
def MakeSubPlot(Axes,XVals,YVals,ColVals,XTLVisible=False,YTLVisible=False, vmin=0, vmax=30):
  """ Make a subplot.
"""
  TickFP  = ftman.FontProperties(size=5)
  MTickFP = ftman.FontProperties(size=0)

  #XTicks = np.arange(-180,360, 180)
 # XTicks = np.arange(-150,360, 50)
 # MXTicks = np.arange(-180,360, 45)
 # YTicks = np.arange(-150,360, 50)
  #YTicks = np.arange(-180,360, 180)
  XTicks = np.array([-180,-90,0,90,180]) #np.arange(-90,360, 90)
  YTicks = np.array([-180,-90,0,90,180]) #np.arange(-90,360, 90)
  MXTicks = None
  MYTicks = None
  #MYTicks = np.arange(-180,360, 45)

  AxesPropWrapper(Axes,XTicks=XTicks,YTicks=YTicks, MXTicks=MXTicks, MYTicks=MYTicks,
    XTLVisible=XTLVisible,YTLVisible=YTLVisible,XYRange=[-180,-180,180,180],
    TickFP=TickFP,MTickFP=MTickFP)

  SpinceWidth=1.5
  [i.set_linewidth(SpinceWidth) for i in Axes.spines.itervalues()]

  TickLineWidth=1.5
  for l in Axes.get_xticklines() + Axes.get_yticklines():
    l.set_markeredgewidth(TickLineWidth)

  pc = Axes.pcolormesh(XVals,YVals,ColVals,cmap=genColorMap(cmx.jet),vmin=vmin,vmax=vmax)
#  pc = Axes.pcolormesh(XVals,YVals,ColVals,cmap=genColorMap(cmx.autumn),vmin=vmin,vmax=vmax)
  return pc
     

################################################################################
def SetXTicks(Axes,Ticks=None,Minor=False, FP=20, Decimals=0, Visible=False):
  if Ticks is not None:
    Axes.set_xticks(ticks=Ticks,minor=Minor)
    TLabels = [str(x)+"$\degree$" for x in np.around(Ticks,decimals=Decimals)]
    Axes.set_xticklabels(labels=TLabels,minor=Minor,visible=Visible,fontproperties=FP)


################################################################################
def SetYTicks(Axes,Ticks=None,Minor=False, FP=20, Decimals=0, Visible=False):
  if Ticks is not None:
    Axes.set_yticks(ticks=Ticks,minor=Minor)
    TLabels = [str(x)+"$\degree$" for x in np.around(Ticks,decimals=Decimals)]
    Axes.set_yticklabels(labels=TLabels,minor=Minor,visible=Visible,fontproperties=FP)


################################################################################
def AxesPropWrapper(Axes,XTicks=None,YTicks=None,MXTicks=None,MYTicks=None,
                    XTLDecimals=0,MXTLDecimals=0,XTLVisible=True,MXTLVisible=False,
                    YTLDecimals=0,MYTLDecimals=0,YTLVisible=True,MYTLVisible=False,
                    XYRange=[0,0,1,1], TickFP=None, MTickFP=None):
  """Axes properties wrapper.
"""
  if TickFP is None:  TickFP  = ftman.FontProperties(18)
  if MTickFP is None: MTickFP = ftman.FontProperties(10)

  SetXTicks(Axes,XTicks, Minor=False,FP=TickFP, Decimals=XTLDecimals, Visible=XTLVisible)
  SetXTicks(Axes,MXTicks,Minor=True, FP=MTickFP,Decimals=MXTLDecimals,Visible=MXTLVisible)
  SetYTicks(Axes,YTicks, Minor=False,FP=TickFP, Decimals=YTLDecimals, Visible=YTLVisible)
  SetYTicks(Axes,MYTicks,Minor=True, FP=MTickFP,Decimals=MYTLDecimals,Visible=MYTLVisible)

  left, bot, right, top = XYRange
  Axes.set_xlim(left=left,right=right)
  Axes.set_ylim(bottom=bot,top=top)

  SpineWidth=2
  [l.set_linewidth(SpineWidth) for l in Axes.spines.itervalues()]

  TickLineWidth=2
  for l in Axes.get_xticklines() + Axes.get_yticklines():
    l.set_markeredgewidth(TickLineWidth)


if __name__ == '__main__':
  MakeFigure(2,2, INP, OUT )
