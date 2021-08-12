# $Id: AtlasUtil.py 2320 2012-10-24 14:13:34Z krasznaa $
#
# Module providing some convenience functions for decorating ATLAS plots.
#

##
# @short Function producing the "ATLAS Preliminary" sign
#
# There is a usual format for the "ATLAS Preliminary" sign on the plots,
# this function takes care of using that. Plus, it makes it simple to
# remove/change the "Preliminary" part if/when necessary.
#
# @param x The X position of the text in the [0,1] interval
# @param y The Y position of the text in the [0,1] interval
# @param color The color of the text
def AtlasLabel( x, y, color = 1 ):
    # ROOT is needed of course:
    import ROOT
    # Draw the "ATLAS" part:
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont( 72 )
    l.SetTextColor( color )
    l.DrawLatex( x, y, "ATLAS" )
    # Draw the "Preliminary" part:
    l.SetTextFont( 42 )
    #  l.DrawLatex( x + 0.16, y, "Internal" )
    return

def AtlasLabelPreliminary( x, y, color = 1 ):
    # ROOT is needed of course:                                                                                                                                                      
    import ROOT
    # Draw the "ATLAS" part:                                                                                                                                                         
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont( 72 )
    l.SetTextColor( color )
    l.DrawLatex( x, y, "ATLAS" )
    # Draw the "Preliminary" part:                                                                                                                                                   
    l.SetTextFont( 42 )
    l.DrawLatex( x + 0.16, y, "Preliminary" )
    return

def AtlasLabelInternal( x, y, color = 1 , txtsize=0):
    # ROOT is needed of course:                                                                                                                                                      
    import ROOT
    # Draw the "ATLAS" part:                                                                                                                                                         
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont( 72 )
    l.SetTextColor( color )
    l.DrawLatex( x, y, "ATLAS" )
    # Draw the "Preliminary" part:                                                                                                                                                   
    l.SetTextFont( 42 )
    if txtsize != 0:
        l.SetTextSize(txtsize)
    l.DrawLatex( x + 0.16, y, "Internal" )
    return

##
# @short Function drawing generic text on the plots
#
# This is just to save the user a few lines of code in his/her script
# when putting some additional comments on a plot.
#
# @param x The X position of the text in the [0,1] interval
# @param y The Y position of the text in the [0,1] interval
# @param text The text to be displayed
# @param color The color of the text
def DrawTextOneLine( x, y, text, color = 1, size = 0.04, NDC = True,
                     halign = "left", valign = "bottom",
                     skipLines = 0, angle = 0.0 ):

    halignMap = {"left":1, "center":2, "right":3}
    valignMap = {"bottom":1, "center":2, "top":3}

    scaleLineHeight = 1.0
    if valign == "top": scaleLineHeight = 0.8
    if skipLines: text = "#lower[%.1f]{%s}" % (skipLines*scaleLineHeight,text)

    # Draw the text quite simply:
    import ROOT
    l = ROOT.TLatex()
    if NDC: l.SetNDC()
    l.SetTextAlign( 10*halignMap[halign] + valignMap[valign] )
    l.SetTextColor( color )
    l.SetTextSize( size )
    l.SetTextAngle( angle )
    l.DrawLatex( x, y, text )
    return l

def DrawText( x, y, text, color = 1, size = 0.04, NDC = True,
              halign = "left", valign = "bottom", angle = 0.0 ):

    objs = []
    skipLines = 0
    for line in text.split('\n'):
       objs.append( DrawTextOneLine( x, y, line, color, size, NDC, halign, valign, skipLines, angle ) )
       if NDC == True: y -= 0.05 * size/0.04
       else:
         skipLines += 1

    return objs

##
# @short Function drawing the luminosity value on the plots
#
# This is just a convenience function for putting a pretty note
# on the plots of how much luminosity was used to produce them.
#
# @param x The X position of the text in the [0,1] interval
# @param y The Y position of the text in the [0,1] interval
# @param lumi The luminosity value in 1/pb
# @param color The color of the text
def DrawLuminosity( x, y, lumi, color = 1, size=0.05):
    DrawText( x, y, "#intLdt = " + str( lumi ) + " fb^{-1}", color , size )
    return

##
# @short Function drawing the luminosity value on the plots in fb-1
#
# This is just a convenience function for putting a pretty note
# on the plots of how much luminosity was used to produce them.
#
# @param x The X position of the text in the [0,1] interval
# @param y The Y position of the text in the [0,1] interval
# @param lumi The luminosity value in 1/fb
# @param color The color of the text
def DrawLuminosityFb( x, y, lumi, energy, color = 1 , size = 0.035):
    #DrawText( x, y, "#lower[-0.2]{#scale[0.55]{#int}}Ldt = " + str( lumi ) + " fb^{-1}", color , 0.05 )
    #DrawText( x, y, "#sqrt{s} = "+str(energy)+"TeV, " + str( lumi ) + " fb^{-1}", color , 0.035 )
    DrawText( x, y, "#sqrt{s} = " + str(energy)+" TeV, " + "#intLdt = " + str( lumi ) + " fb^{-1}", color , size )
    return

##
# @short Function drawing the ECM energy on the plots
#
# This is just a convenience function for putting a pretty note
# on the plots of what centre of mass energy/energies was/were
# used to fill the histogram.
#
# @param x The X position of the text in the [0,1] interval
# @param y The Y position of the text in the [0,1] interval
# @param ecm The centre of mass energy in TeV
# @param color The color of the text
def DrawEcm( x, y, ecm, color = 1 , size = 0.05):
    DrawText( x, y, "#sqrt{s} = " + str( ecm ) + " TeV", color, size )
    return
