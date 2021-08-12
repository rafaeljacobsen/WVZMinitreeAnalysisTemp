#!/usr/bin/env python
"""

A general class for 1d plotting

You can take a look at the examples at the bottom.

FlatPlot: regular overlapping all histograms added
FlatPlotRatio: add ratio to compare with the first histogram added
FlatPlotRatioAlt: the ratio becomes w.r.t. the previous histogram added

StackPlot: just the stack plot you can think of
StackPlotRatio: add the ratio pad between data and mc
StackPlotCustomize: ratio pad will be between sig and bkg
    use add_sig, add_bkg separately
    use set_func for the actual function. commonly used are S/B, significance.
    Those are provided in SoverB(), sig_complex(), etc...
StackPlotFraction: quick purity/composition plot. (each bin will be normalized to 1)


PluginSecondAxis: plot second column on the right
    it support a secondary axis on the right hand side, for linear case
    for example, you want to overlap yield(cut efficiency) vs value(cut value) on the same plot

MultiPadPlot: arbitrary number of rows and columns of pads
    you can put any objects to this combined pad to create matrix of pads in a canvas
    NOTED: you need to save the individual canvas Plot Objects for now. Related to TODO
    NOTED: you might need to tune a little bit the margins of each pads

Adding more plot objects:
    one common example is to add ATLAS label yourself
    use cd_canvas(), cd_main(), cd_sec() to "cd" to those pad/canvas

AtlasLabel: check out AtlasLumi(), should suffice for most cases

Cosmetics:
    For non-ratio plots:
        set_frame() and set corresponding format
    For ratio plots: 
        set_frame1() and set corresponding format for main pad, 
        set_frame2() for corresponding format for ratio pad
    To look at options for frames, please look at _set_frame() function implementation.
    To change default color/marker: look at _define_scheme()

    The blank space and ratio is kind of tuned for best demonstration with minimal effort
    However it's not the most rigirous, you can always manually set them as implied in _set_frame

    Automatized tuning algorithm is below:
    for non-log in y-direction, the default minimum is 0, maximum is blank factor * y maximum(leave space for legends)
    to change blank factor for main pad, use SetUpperBlankFactor()
    for ratio pad, use SetLowerBlankFactor()

Need more than one legend? (i.e. multi-column legend):
    first call AddLegend(), use ileg arg in add()

Multi-page print:
    Print("XXX.pdf(", "pdf") for first
    Print("XXX.pdf",  "pdf") for middle ones
    Print("XXX.pdf)", "pdf") for last
    more in 
    https://root.cern.ch/doc/master/classTPad.html#a649899aa030f537517022a5d51ec152f

Small tools:
    Automatically normalize histogram to area = 1:
        call SetDoShape()

    Automatically divide content/error by bin width:
        call SetDivBinWidth()


"""

# note to developer
# TODO: 
#   1. MultiPad Plot automatically caching with class object?
#   2. Test plugin todo one

import math
import ctypes
try:
    import ROOT as R
    R.gROOT.SetBatch()
    R.gStyle.SetOptStat(0)
except:
    print("warning, ROOT not imported")

##############################################
############# Helper Functions ###############
##############################################

def DoForEachBin(h_signal, h_bkg, func):
    for i in xrange(h_signal.GetNbinsX()):
        con, err = func(
                h_signal.GetBinContent(i+1),
                h_signal.GetBinError(i+1),
                h_bkg.GetBinContent(i+1),
                h_bkg.GetBinError(i+1),
                )
        h_signal.SetBinContent(i+1, con)
        h_signal.SetBinError(i+1, err)

def Chi2Calculator(l_h1, l_h2):
    """
    use error from h1
    """
    h1 = l_h1[0].Clone()
    h1.Reset()
    h2 = l_h2[0].Clone()
    h2.Reset()
    for hist in l_h1:
        h1.Add(hist)
    for hist in l_h2:
        h2.Add(hist)

    nbins = h1.GetNbinsX()
    chi2 = 0.
    for i in xrange(nbins):
        val = h1.GetBinContent(i+1) - h2.GetBinContent(i+1)
        err = h1.GetBinError(i+1)
        #  prlnt h1.GetBinContent(i+1), h1.GetBinError(i+1)
        #  print h2.GetBinContent(i+1)
        if err == 0:
            continue
        chi2 += val * val / err

    return chi2, nbins

def SoverB(S, Serr, B, Berr):
    if B == 0 and S==0:
        return 0, 0
    elif B == 0 and S != 0:
        return 100, 100
    elif B != 0 and S == 0:
        return 0, 0
    else:
        #  print S, B
        return S / B, S / B * ((Serr / S) ** 2 + (Berr / B) ** 2) ** 0.5

def sig_simple(s, serr,  b, berr):
    if s+b == 0:
        return 0., 0.
    return s / math.sqrt(s + b), 0.

def sig_complex(s, serr, b, berr):
    if b == 0:
        return 0., 0.
    if s/b < -1.:
        exit("s = {}, b = {}, domain error".format(s, b))
    return math.sqrt( 2 * ( s + b ) * math.log(1 + s / b) - 2 * s  ), 0.

def sig_complex_bkgsigma(s, b, berr):
    if b == 0:
        return 0., 0.
    if s/b < -1.:
        print("s = {}, b = {}, domain error".format(s, b))
        return 0., 0.
    return math.sqrt( 2 * ( s + b ) * math.log( ( (s + b) * (b + berr**2)   ) / (b**2 + (s+b) * berr ** 2)  ) -\
            2 * b**2 / berr**2 * math.log(1 + berr**2 * s / (b * (b+berr**2)) )  ), 0.

##############################################
############# Helper Classes #################
##############################################

class hist_content():
    """
    save style for histogram/graph
    """
    def __init__(self, h1, drawop, lco, ls, mco, ms, lab_name, lab_op, fco, ileg):
        self.h1 = h1.Clone()
        if h1.__class__.__name__ == "TObject":
            exit("ERROR =====>  Not a TH1D passed in, are you specifying the correct name of histogram?")
        # this is a perfect example showing that 
        # python pass things as pointer!
        self.rtp = "hist"
        if not h1.__class__.__name__ == "TGraph" and\
                not h1.__class__.__name__ == "TGraphErrors" and\
                not h1.__class__.__name__ == "TGraphAsymmErrors":
            self.h1.SetDirectory(0)
        else:
            self.rtp = "gr"
        self.drawop = drawop
        self.lco = lco
        self.fco = fco
        self.ls = ls
        self.mco = mco
        self.ms = ms
        self.lab_name = lab_name
        self.lab_op = lab_op
        self.ileg = ileg
        self.is_fill_color = False
        self.falpha = 1
        self.fs = 1001

        #  self.axisRight = False
        pass

    #  def set_axis_right(val = True):
        #  self.axisRight = val

    def auto_draw(self, 
            is_draw=True, is_fill_color=False, 
            is_line_color = True):
        """
        automatically set all the styles and draw
        is_line_color: also set line to be same with 
        """
        if is_fill_color or self.is_fill_color:
            self.h1.SetFillColorAlpha(self.fco, self.falpha)
            self.h1.SetFillStyle(self.fs)
            self.h1.SetLineColor(1)
        if is_line_color:
            self.h1.SetLineColor(self.lco)
        if self.rtp == "gr":
            self.h1.SetFillColor(self.fco)
        self.h1.SetLineStyle(self.ls)
        self.h1.SetMarkerColor(self.mco)
        self.h1.SetMarkerStyle(self.ms)
        if is_draw:
            #  if self.rtp == "gr":
                #  self.h1.Draw(self.drawop)
            #  elif self.rtp == "hist":

            #  if self.axisRight:
                #  self.h1.Draw("sameY+" + self.drawop)
            #  else:
            self.h1.Draw("same" + self.drawop)
        pass
    pass # end of class hist_content

class _BasePlot:
    """
    a base class for saving colorscheme, 
    """
    def __init__(self, cn, ct="", canx = 600, cany = 600, **kwargs):
        """
        """
        self._canvas = R.TCanvas(cn, ct, canx, cany)
        self.l_leg = []
        self.l_add_leg = []
        self._define_scheme()
        self._current_lco = 0
        self._l_hist = []
        self._upper_blank_factor = 1.5
        self._is_do_shape = False
        self._is_div_bin_width = False
        self.remove_mc_stat = False
        pass

    def RemoveMCStat(self, ):
        self.remove_mc_stat = True

    def AddLegend(self, labx1, laby1, labx2, laby2):
        self.l_add_leg.append(R.TLegend(R.TLegend(labx1, laby1, labx2, laby2)))

    def SetDoShape(self, val=True):
        self._is_do_shape = val
        return self

    def SetDivBinWidth(self):
        """
        will be carried before set frames!
        """
        self._is_div_bin_width = True

    def SetUpperBlankFactor(self, val):
        self._upper_blank_factor = val

    def SetLowerBlankFactor(self, val):
        self._lower_blank_factor = val

    def _define_scheme(self,):
        """
        user can specify favorite colorscheme, dash scheme
        """
        self._l_color = [
            R.TColor.GetColor("#e41a1c"), #red
            R.TColor.GetColor("#92c5de"), #blue
            R.TColor.GetColor("#4daf4a"), #green
            R.TColor.GetColor("#984ea3"), #purple
            R.TColor.GetColor("#ff7f00"), #orange
            R.TColor.GetColor("#a65628"), #brown
            R.TColor.GetColor("#f781bf"), #pink
            R.TColor.GetColor("#ffff33"), #yellow
            #  R.TColor.GetColor("#d73027"), #dark red too similar to red
            R.TColor.GetColor("#2166ac"), #dark blue
            R.TColor.GetColor("#006837"), #dark green
            R.TColor.GetColor("#999999"), #grey
            R.TColor.GetColor("#000000"), #black
            R.TColor.GetColorTransparent(R.kWhite, 0), #transparent
                ]
        self._line_style = [
                1, 2, 3, 4,
                5, 6, 7, 8,
                9, 10, 11, 12,
            ]
        #  self._marker_style = [
                #  1, 2, 3, 4, 5,
            #  ]
        self._marker_style = [1] + range(1, 50)
        pass

    def set_color_scheme(self,l_color):
        self._l_color = l_color

    def _find_hist_max(self, l_h):
        """
        quickly find the maximum of a list of hists
        """
        bmax = 0.
        for _ in l_h:
            x, y = ctypes.c_double(), ctypes.c_double() 
            if _.__class__.__name__ == "TGraph":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    if y > bmax:
                        bmax = y.value
            elif _.__class__.__name__ == "TGraphErrors":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    yhi = _.GetErrorY(i) 
                    if y + yhi > bmax and y > 0:
                        bmax = y.value + yhi
            elif _.__class__.__name__ == "TGraphAsymmErrors":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    yhi = _.GetErrorYhigh(i) 
                    if y + yhi > bmax and y > 0:
                        bmax = y.value + yhi
                pass
            else:
                for b in xrange(_.GetNbinsX()):
                    val = _.GetBinContent(b+1) + _.GetBinError(b+1)
                    if val > bmax and _.GetBinContent(b+1) > 0:
                        bmax = val
        #  print "max is", bmax
        return bmax

    def _find_hist_min(self, l_h):
        """
        quickly find the maximum of a list of hists
        """
        #  bmin = math.inf
        bmin = float('inf')
        for _ in l_h:
            x, y = ctypes.c_double(), ctypes.c_double() 
            if _.__class__.__name__ == "TGraph":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    if y < bmin:
                        bmin = y.value
            elif _.__class__.__name__ == "TGraphErrors":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    ylo = _.GetErrorY(i) 
                    if y - ylo < bmin and y - ylo > 0:
                        bmin = y.value - ylo
            elif _.__class__.__name__ == "TGraphAsymmErrors":
                for i in xrange(_.GetN()):
                    _.GetPoint(i, x, y) 
                    ylo = _.GetErrorYlow(i) 
                    if y - ylo < bmin and y - ylo > 0:
                        bmin = y.value - ylo
                pass
            else:
                for b in xrange(_.GetNbinsX()):
                    val = _.GetBinContent(b+1) - _.GetBinError(b+1)
                    if val < bmin and val > 0:
                        bmin = val
        #  print "min is", bmin
        return bmin

    def cd_canvas(self, ):
        return self.cd_main()

    def cd_main(self, ):
        """
        go to the main canvas for legend, frame
        can be override in later plots, to cd to TPads, etc..
        """
        return self._canvas.cd() 

    def _prepare_canvas(self, x1, y1, x2, y2):
        """
        prepare the canvas, draw the frame
        """
        self.l_leg.append(R.TLegend(x1, y1, x2, y2))
        for leg in self.l_add_leg:
            self.l_leg.append(leg)
        for leg in self.l_leg:
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)
        if not hasattr(self, "_hframe1"):
            self.set_frame()
        self.cd_main()
        opt = ""
        if self._hframe1.rightAxis:
            opt += "Y+"
        self._hframe1.Draw(opt)

    def addg(self, h1, fs = -1, msize=1, **kwargs):
        h1.SetMarkerSize(msize)
        if not fs == -1:
            h1.SetFillStyle(fs)
        self.add(h1, **kwargs)

    def add(self, h1, drawop = "", lco = -999, ls = 0, mco = -1, ms = 0, lab_name = "", lab_op = "l", fco = -1, falpha = 1, fs = 1001, ileg=0, div_bin_width = False, mul_bin_width=False, is_fill_color = False):
        """
        add a most usual histogram
        """

        if lco == -999:
            lco = self._current_lco
            self._current_lco += 1
        _lco = self._l_color[lco]
        _ls  = self._line_style[ls]
        _fco = 0
        if fco == -1:
            _fco = _lco
        else:
            _fco = fco
        _mco = 0
        if mco == -1:
            _mco = _fco
        else:
            _mco = mco
        _ms  = self._marker_style[ms]
        h1 = h1.Clone()
        if self._is_do_shape and h1.Integral() != 0:
            h1.Scale( 1. / h1.Integral() )
        if self._is_div_bin_width or div_bin_width:
            for i in xrange(h1.GetNbinsX()):
                wid = h1.GetBinWidth(i+1)
                h1.SetBinContent(i+1, h1.GetBinContent(i+1) / wid)
                h1.SetBinError(i+1, h1.GetBinError(i+1) / wid)
        if mul_bin_width:
            for i in xrange(h1.GetNbinsX()):
                wid = h1.GetBinWidth(i+1)
                h1.SetBinContent(i+1, h1.GetBinContent(i+1) * wid)
                h1.SetBinError(i+1, h1.GetBinError(i+1) * wid)
        self._l_hist.append(hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, _fco, ileg))

        self._l_hist[-1].is_fill_color = is_fill_color
        self._l_hist[-1].falpha = falpha
        self._l_hist[-1].fs = fs
        pass

    def RedrawAxis(self):
        if hasattr(self, "_p1"):
            self._p1.RedrawAxis()
            self._p2.RedrawAxis()
            pass
        if hasattr(self, "_canvas"):
            self._canvas.RedrawAxis()

    def Print(self, file_name = "test.pdf", *args):
        self.RedrawAxis()
        self._canvas.Print(file_name, *args)
        pass

    def _set_frame(self, frame, canvas, Ymin, Ymax, **kwargs):
        """
        the core of all set_frame
        """
        # conveniently keep it from a closing pad
        frame.SetDirectory(0)

        blank_factor = self._upper_blank_factor
        if "blank_factor" in kwargs:
            blank_factor = kwargs["blank_factor"]


        frame.SetLineColor(0)
        frame.Reset()

        xaxis = frame.GetXaxis()
        yaxis = frame.GetYaxis()

        # make sure int/double are passed in 
        for name in [
                "xlow", "xhigh", "ylow", "yhigh",
                "LeftMargin","RightMargin",
                "TopMargin","BottomMargin"]:
            if (name in kwargs) and \
                    (type(kwargs[name]) != type(0) and\
                    type(kwargs[name]) != type(0.0)):
                        del kwargs[name]

        # user defined ones!
        if "logx" in kwargs and kwargs["logx"]:
            canvas.SetLogx()

        if "logy" in kwargs and kwargs["logy"]:
            #  print low, Ymax
            distance = ( Ymax / Ymin ) ** ((blank_factor - 1.) )
            yaxis.SetRangeUser(Ymin / distance ** 0.2, Ymax * distance ** 0.8)
            canvas.SetLogy()
        elif Ymax != None:
            yaxis.SetRangeUser(0, Ymax * blank_factor) 


        # now that it's a python object :)))
        if "rightAxis" in kwargs and kwargs["rightAxis"]:
            frame.rightAxis = True
            pass
        else:
            frame.rightAxis = False

        if "title" in kwargs:
            frame.SetTitle(kwargs["title"])
        if "xtitle" in kwargs:
            xaxis.SetTitle(kwargs["xtitle"])
        if "ytitle" in kwargs:
            yaxis.SetTitle(kwargs["ytitle"])

        if "xlow" in kwargs and "xhigh" in kwargs:
            xaxis.SetRangeUser(kwargs["xlow"], kwargs["xhigh"])
        elif "xlow" in kwargs:
            xaxis.SetRangeUser(kwargs["xlow"], xaxis.GetBinUpEdge(xaxis.GetNbins()))
        elif "xhigh" in kwargs:
            xaxis.SetRangeUser(xaxis.GetBinLowEdge(1), kwargs["xhigh"])

        # H - L = (Ymax - L) * U
        # lnH - lnL = (lnYmax - lnL) * U
        if "ylow" in kwargs and "yhigh" in kwargs:
            yaxis.SetRangeUser(kwargs["ylow"], kwargs["yhigh"])
        elif "ylow" in kwargs:
            low = kwargs["ylow"]
            if "logy" in kwargs and kwargs["logy"]:
                yaxis.SetRangeUser(low, Ymax ** blank_factor / low ** (blank_factor-1)) 
            elif Ymax != None:
                yaxis.SetRangeUser(low, low * (1 - blank_factor) + Ymax * blank_factor)
        elif "yhigh" in kwargs:
            high = kwargs["yhigh"]
            if "logy" in kwargs and kwargs["logy"]:
                yaxis.SetRangeUser((Ymax ** blank_factor / high) ** (1 - blank_factor) , high) 
            elif Ymax != None:
                yaxis.SetRangeUser((Ymax * blank_factor - high) / (blank_factor - 1), high)

        if "LeftMargin" in kwargs:
            canvas.SetLeftMargin(kwargs["LeftMargin"])
        if "RightMargin" in kwargs:
            canvas.SetRightMargin(kwargs["RightMargin"])
        if "TopMargin" in kwargs:
            canvas.SetTopMargin(kwargs["TopMargin"])
        if "BottomMargin" in kwargs:
            canvas.SetBottomMargin(kwargs["BottomMargin"])
        if "XLabelSize" in kwargs:
            xaxis.SetLabelSize(kwargs["XLabelSize"])
        if "YLabelSize" in kwargs:
            yaxis.SetLabelSize(kwargs["YLabelSize"])
        if "XTitleOffset" in kwargs:
            xaxis.SetTitleOffset(kwargs["XTitleOffset"])
        if "YTitleOffset" in kwargs:
            yaxis.SetTitleOffset(kwargs["YTitleOffset"])
        if "XTitleSize" in kwargs:
            xaxis.SetTitleSize(kwargs["XTitleSize"])
        if "YTitleSize" in kwargs:
            yaxis.SetTitleSize(kwargs["YTitleSize"])
        pass

    def set_frame(self, **kwargs):
        """
        called before draw
        """
        if "TH1" in self._l_hist[0].h1.__class__.__name__:
            self._hframe1 = self._l_hist[0].h1.Clone("hframe")
        else:
            self._hframe1 = R.TH1D("frame", "", 1, 0, 100)
        self.cd_canvas().frame = self._hframe1

        xaxis = self._hframe1.GetXaxis()
        yaxis = self._hframe1.GetYaxis()
        if xaxis.GetLabelFont() % 10 != 3:
            xaxis.SetLabelSize(xaxis.GetLabelSize() / 1.3)
            yaxis.SetLabelSize(yaxis.GetLabelSize() / 1.3)


        self.Ymin = self._find_hist_min([a.h1 for a in self._l_hist] + \
                ([self.h_mc, ] if hasattr(self, "h_mc") else [] ) +\
                ([self.h_data.h1, ] if hasattr(self, "h_data") else [] )
                )
        self.Ymax = self._find_hist_max([a.h1 for a in self._l_hist] + \
                ([self.h_mc, ] if hasattr(self, "h_mc") else [] ) +\
                ([self.h_data.h1, ] if hasattr(self, "h_data") else [] )
                )

        self._set_frame(self._hframe1, self._canvas, self.Ymin, self.Ymax, **kwargs)
        pass

    def AtlasLumi(self, lumi, tev, tp = "Internal", x=0.2, y=0.85):
        # I have ATLAS preference..
        import AtlasUtil
        self.cd_main()
        getattr(AtlasUtil, "AtlasLabel" + tp)(x, y)
        getattr(AtlasUtil, "DrawLuminosityFb")(x, y - .06, str(lumi), str(tev))

    pass # end of class _BasePlot

class _BasePlotRatio(_BasePlot):
    """
    a base class for saving colorscheme, 
    """
    def set_nan_to_1(self, setnan=True):
        """
        if denominator of the bin is 0, 
        set the divide result in that bin to 1
        """
        self._set_nan_to_1 = setnan

    def __init__(self, cn, ct="", canx = 600, cany = 600, frac = 0.4, **kwargs):
        """
        """
        self._set_nan_to_1 = False
        self._is_do_shape = False
        self._upper_blank_factor = 1.5
        self._lower_blank_factor = 1.2
        self.l_leg = []
        self.l_add_leg = []
        self._current_lco = 0
        self._frac = frac
        self._canvas = R.TCanvas(cn, ct, canx, cany)
        self._p1 = R.TPad(
                "p1","p1", 0., frac/(1+frac), 1.,            1., 0, 0)
        self._p1.Draw()
        self._p2 = R.TPad(
                "p2","p2", 0.,            0., 1., frac/(1+frac), 0, 0)
        self._p2.Draw()
        self._define_scheme()
        self._l_hist = []
        self._l_hist_ratio = []
        self._is_div_bin_width = False
        self.remove_mc_stat = False
        pass

    def cd_canvas(self, ):
        """
        memory leak?
        """
        return self._canvas.cd()

    def cd_main(self, ):
        """
        go to the main canvas for legend, frame
        can be override in later plots, to cd to TPads, etc..
        """
        return self._p1.cd()

    def cd_sec(self, ):
        """
        go to the secondary canvas for ratio
        can be override in later plots, to cd to TPads, etc..
        """
        return self._p2.cd()

    def _prepare_canvas(self, x1, y1, x2, y2):
        """
        prepare the canvas, draw the frame
        """
        self.l_leg.append(R.TLegend(x1, y1, x2, y2))
        for leg in self.l_add_leg:
            self.l_leg.append(leg)
        for leg in self.l_leg:
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)
        if not hasattr(self, "_hframe1"):
            self.set_frame1()
        if not hasattr(self, "_hframe2"):
            self.set_frame2()

        self.cd_main()
        opt = ""
        if self._hframe1.rightAxis:
            opt += "Y+"
        self._hframe1.Draw(opt)

        self.cd_sec()
        opt = ""
        if self._hframe2.rightAxis:
            opt += "Y+"
        self._hframe2.Draw(opt)

    def set_den(self, index=0):
        """
        will be operated at the beginning of set_frame2()
        """
        for hist in self._l_hist:
            hist_ratio = hist.h1.Clone()
            h_target = self._l_hist[index].h1
            # might be error from Divide, might need to improve Divide
            hist_ratio.Divide(h_target)
            # TODO: use an option here?
            for i in range(hist_ratio.GetNbinsX()):
                div = h_target.GetBinContent(i+1)
                hist_ratio.SetBinError(i+1, hist.h1.GetBinError(i+1) / div if div !=0 else 0)
            if self._set_nan_to_1:
                for i in xrange(hist_ratio.GetNbinsX()):
                    if self._l_hist[index].h1.GetBinContent(i+1) == 0:
                        hist_ratio.SetBinContent(i+1, 1)
                        hist_ratio.SetBinError(i+1, 0)
                pass
            self._l_hist_ratio.append(hist_content(hist_ratio, hist.drawop, hist.lco, hist.ls, hist.mco, hist.ms, hist.lab_name, hist.lab_op, hist.fco, hist.ileg))

    def set_frame1(self, **kwargs):
        """
        called before draw
        """
        self._hframe1 = self._l_hist[0].h1.Clone("hframe")
        self.cd_main().frame = self._hframe1

        self.Ymin = self._find_hist_min([a.h1 for a in self._l_hist] + \
                ([self.h_mc, ] if hasattr(self, "h_mc") else [] ) +\
                ([self.h_data.h1, ] if hasattr(self, "h_data") else [] )
                )
        self.Ymax = self._find_hist_max([a.h1 for a in self._l_hist] + \
                ([self.h_mc, ] if hasattr(self, "h_mc") else [] ) +\
                ([self.h_data.h1, ] if hasattr(self, "h_data") else [] )
                )

        xaxis = self._hframe1.GetXaxis()
        yaxis = self._hframe1.GetYaxis()

        # default ones!
        if "xtitle" not in kwargs:
            xaxis.SetTitle("")
        if "BottomMargin" not in kwargs:
            self._p1.SetBottomMargin(0)
        self._set_frame(self._hframe1, self._p1, self.Ymin, self.Ymax, **kwargs)
        pass

    def set_frame2(self, **kwargs):
        """
        called before draw
        """

        if not hasattr(self, "_hframe1"):
            self.set_frame1()

        if len(self._l_hist_ratio) == 0:
            self.set_den()

        self._hframe2 = self._l_hist_ratio[0].h1.Clone("hframe")
        self.cd_sec().frame = self._hframe2

        self.Ymin_ratio = self._find_hist_min(
                [a.h1 for a in self._l_hist_ratio] + \
                ([self.h_mc_ratio, ] if hasattr(self, "h_mc_ratio") else [] ) + \
                ([self.h_data_ratio, ] if hasattr(self, "h_data_ratio") else [] )
                )
        self.Ymax_ratio = self._find_hist_max(
                [a.h1 for a in self._l_hist_ratio] + \
                ([self.h_mc_ratio, ] if hasattr(self, "h_mc_ratio") else [] ) + \
                ([self.h_data_ratio, ] if hasattr(self, "h_data_ratio") else [] )
                )

        # default ones
        xaxis = self._hframe2.GetXaxis()
        yaxis = self._hframe2.GetYaxis()
        if xaxis.GetLabelFont() % 10 != 3:
            xaxis.SetLabelSize(xaxis.GetLabelSize() / self._frac)
            yaxis.SetLabelSize(yaxis.GetLabelSize() / self._frac)
            xaxis.SetTitleSize(xaxis.GetTitleSize() / self._frac)
            yaxis.SetTitleSize(yaxis.GetTitleSize() / self._frac)
        if "XTitleOffset" not in kwargs:
            xaxis.SetTitleOffset(1.0)
        if "YTitleOffset" not in kwargs:
            yaxis.SetTitleOffset(0.5)
        if "TopMargin" not in kwargs:
            self._p2.SetTopMargin(0)
        if "BottomMargin" not in kwargs:
            self._p2.SetBottomMargin(0.3)

        if "blank_factor" not in kwargs:
            kwargs["blank_factor"] = self._lower_blank_factor

        self._set_frame(self._hframe2, self._p2, self.Ymin_ratio, self.Ymax_ratio,  **kwargs)
        pass

    pass # end of class _BasePlot

##############################################
############### User Classes #################
##############################################

class FlatPlot(_BasePlot):
    """
    very simple flat plot
    """
        
    def set_frame(self, **kwargs):
        _BasePlot.set_frame(self, **kwargs)

    def draw(self, labx1=0.60, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True):
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        for _ in self._l_hist:
            _.auto_draw()
            #  _.h1.SetLineColor(_.lco)
            #  _.h1.SetLineStyle(_.ls)
            #  _.h1.SetMarkerColor(_.mco)
            #  _.h1.SetMarkerStyle(_.ms)
            #  _.h1.Draw("same" + _.drawop)
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)
            pass
        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")
        return self._canvas.cd()
    pass # end of class FlatPlot

class CompositionPlot(_BasePlot):
    """
    very simple flat plot
    """

    def __init__(self, *k):
        _BasePlot.__init__(self, *k)
        self.SetUpperBlankFactor(1)
        
    def set_frame(self, **kwargs):
        """
        called before draw
        """
        if "ylow" not in kwargs:
            kwargs["ylow"]  = 0.
        if "yhigh" not in kwargs:
            kwargs["yhigh"]  = 1.
        if "ytitle" not in kwargs:
            kwargs["ytitle"]  = "Ratio"

        h_mc = self._l_hist[0].h1.Clone()
        h_mc.Reset()
        for _ in self._l_hist:
            h_mc.Add(_.h1)

        #  self.h_mc = h_mc

        for _ in self._l_hist:
            _.h1.Divide(h_mc)



        _BasePlot.set_frame(self, **kwargs)

    def draw(self, labx1=0.60, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True):
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        for _ in self._l_hist:
            _.auto_draw()
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)
            pass

        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")
        return self._canvas.cd()
    pass # end of class FlatPlot

class FlatPlotRatio(_BasePlotRatio):
    """
    very simple flat plot with ratio pad
    """
    def draw(self, labx1=0.60, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True):
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        self.cd_main()
        for _ in self._l_hist:
            _.auto_draw()
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)
            pass
        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")
        self.cd_sec()
        for _ in self._l_hist_ratio:
            _.auto_draw()
            pass
        return self._canvas.cd()

    pass # end of class FlatPlot

class FlatPlotRatioAlt(FlatPlotRatio):
    """
    odd numbered one will divide the one befor it(index start from 0)
    """
    def set_den(self):
        """
        will be operated at the beginning of set_frame2()
        """
        #  print "set_den"
        index = 0
        for hist in self._l_hist:
            index_div = index
            if index % 2 == 1:
                index_div = index - 1
            hist_ratio = hist.h1.Clone()
            # might be error from Divide, might need to improve Divide
            hist_ratio.Divide(self._l_hist[index_div].h1)
            self._l_hist_ratio.append(hist_content(hist_ratio, hist.drawop, hist.lco, hist.ls, hist.mco, hist.ms, hist.lab_name, hist.lab_op, hist.fco, hist.ileg))
            index += 1

class StackPlot(_BasePlot):
    """
    very simple flat plot with ratio pad
    """

    def set_frame(self, **kwargs):
        """
        called before draw
        """
        h_mc = self._l_hist[0].h1.Clone()
        h_mc.Reset()
        for _ in reversed(self._l_hist):
            h_mc.Add(_.h1)

        self.h_mc = h_mc
        _BasePlot.set_frame(self, **kwargs)
        pass

    def add_data(self, h1, drawop = "", lco = -1, ls = 0, mco = -1, ms = 0, lab_name = "", lab_op = "l", fco = -1, ileg=0):
        """
        add a data histogram
        """

        _lco = 1
        _ls  = self._line_style[ls]
        _fco = 1
        if fco != -1:
            _fco = self._l_color[lco]
        _mco = 1
        #  if mco == -1:
            #  _mco = self._l_color[lco]
        #  else:
            #  _mco = self._l_color[mco]
        _ms  = self._marker_style[ms]
        #  self._l_hist.append(hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, fco))
        self.h_data = hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, _fco, ileg)
        pass

    def add(self, h1, lab_op = "F", **kwargs):
        _BasePlot.add(self, h1, lab_op = lab_op, **kwargs)


    def draw(self, labx1=0.60, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True, data_to_mc=True, is_line_color=False):
        self.hcache = []
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        self.cd_main()
        h_st = R.THStack()
        #  self.h_data.auto_draw(is_draw=False)
        #  self.hcache.append(h_mc)
        self.hcache.append(h_st)
        count = 0
        if hasattr(self, "h_data"):
            if self.h_data.ileg.ileg >= 0:
                self.l_leg[self.h_data.ileg].AddEntry(self.h_data.h1, self.h_data.lab_name, self.h_data.lab_op)
        for _ in reversed(self._l_hist):
            _.auto_draw(is_draw=False, is_fill_color=True, is_line_color=is_line_color)
            h_st.Add(_.h1)
            count += 1
            pass
        for _ in self._l_hist:
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)

        # h_st.Draw("Ehistsame")
        h_st.Draw("histsame" + _.drawop)
        graph_comberr = R.TGraphErrors(self.h_mc)
        self.hcache.append(graph_comberr)
        graph_comberr.SetLineWidth( 0 );
        graph_comberr.SetMarkerSize( 0 );
        graph_comberr.SetFillStyle( 3375 );
        graph_comberr.SetFillColor( 28 );
        graph_comberr.Draw("5same")
        if not self.remove_mc_stat:
            self.l_leg[0].AddEntry(graph_comberr, "MC Stat")
        if hasattr(self, "h_data"):
            self.h_data.h1.Draw("same")
            h_data = self.h_data.h1.Clone()
            self.hcache.append(h_data)
        h_mc_ratio = self.h_mc.Clone()
        self.hcache.append(h_mc_ratio)
        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")

        return self._canvas.cd()

    pass # end of class StackPlot

class StackPlotRatio(_BasePlotRatio):
    """
    very simple flat plot with ratio pad
    """

    def set_frame1(self, **kwargs):
        """
        called before draw
        """
        #  h_mc = self.h_data.h1.Clone()
        h_mc = self._l_hist[0].h1.Clone()
        h_mc.Reset()
        for _ in reversed(self._l_hist):
            h_mc.Add(_.h1)

        self.h_mc = h_mc
        _BasePlotRatio.set_frame1(self, **kwargs)
        pass

    def set_frame2(self, data_to_mc=True, **kwargs):
        if not hasattr(self, "_hframe1"):
            self.set_frame1()
        h_mc_ratio = self.h_mc.Clone()
        h_data = self._l_hist[0].h1.Clone()
        #  h_data = self.h_data.h1.Clone()

        if data_to_mc:
            h_data.Divide(h_mc_ratio)
            for i in xrange(h_mc_ratio.GetNbinsX()):
                if h_mc_ratio.GetBinContent(i+1) != 0:
                    h_mc_ratio.SetBinError(i+1, h_mc_ratio.GetBinError(i+1) /  h_mc_ratio.GetBinContent(i+1))
                    h_mc_ratio.SetBinContent(i+1, 1)
                else:
                    h_mc_ratio.SetBinContent(i+1, 0)
                    h_mc_ratio.SetBinError(i+1, 0)
        else:
            h_mc_ratio.Divide(h_data)
            h_data.Divide(h_data)
            #  h_data.Draw("PEsame")
            #  h_mc_ratio.Draw("histsame")

        #  self._l_hist_ratio.append(h_mc_ratio)
        #  self._l_hist_ratio.append(hist_content(h_mc_ratio, hist.drawop, hist.lco, hist.ls, hist.mco, hist.ms, hist.lab_name, hist.lab_op, hist.fco))

        hist = self._l_hist[0]
        self._l_hist_ratio.append(hist_content(h_mc_ratio, hist.drawop, hist.lco, hist.ls, hist.mco, hist.ms, hist.lab_name, hist.lab_op, hist.fco, hist.ileg))

        self.h_mc_ratio = h_mc_ratio
        self.h_data_ratio = h_data

        h_mc_ratio.SetDirectory(0)
        h_data.SetDirectory(0)

        #  for i in range(h_data.GetNbinsX()):
            #  print i, h_data.GetBinContent(i+1)
            #  print i, h_mc_ratio.GetBinContent(i+1)

        _BasePlotRatio.set_frame2(self, **kwargs)
        pass


    def add_data(self, h1, drawop = "", lco = -1, ls = 0, mco = -1, ms = 0, lab_name = "", lab_op = "l", fco = -1, ileg=0):
        """
        add a data histogram
        """

        _lco = 1
        _ls  = self._line_style[ls]
        _fco = 1
        if fco != -1:
            _fco = self._l_color[lco]
        _mco = 1
        #  if mco == -1:
            #  _mco = self._l_color[lco]
        #  else:
            #  _mco = self._l_color[mco]
        _ms  = self._marker_style[ms]
        #  self._l_hist.append(hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, fco))
        self.h_data = hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, _fco, ileg)
        pass

    def draw(self, labx1=0.6, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True,  is_line_color=False):
        self.hcache = []
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        self.cd_main()
        h_st = R.THStack()
        #  self.h_data.auto_draw(is_draw=False)
        #  self.hcache.append(h_mc)
        self.hcache.append(h_st)
        count = 0
        if self.h_data.ileg >= 0:
            self.l_leg[self.h_data.ileg].AddEntry(self.h_data.h1, self.h_data.lab_name, self.h_data.lab_op)
        for _ in reversed(self._l_hist):
            _.auto_draw(is_draw=False, is_fill_color=True, is_line_color=is_line_color)
            h_st.Add(_.h1)
            count += 1
            pass
        for _ in self._l_hist:
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)

        # h_st.Draw("Ehistsame")
        h_st.Draw("histsame" + _.drawop)
        graph_comberr = R.TGraphErrors(self.h_mc)
        self.hcache.append(graph_comberr)
        graph_comberr.SetLineWidth( 0 );
        graph_comberr.SetMarkerSize( 0 );
        graph_comberr.SetFillStyle( 3375 );
        graph_comberr.SetFillColor( 28 );
        graph_comberr.Draw("5same")
        if not self.remove_mc_stat:
            self.l_leg[0].AddEntry(graph_comberr, "MC Stat")
        self.h_data.h1.Draw("same")

        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")

        self.cd_sec()

        self.h_mc_ratio.Draw("histsame")
        self.h_data_ratio.Draw("PEsame")


        graph_comberr_ratio = R.TGraphErrors(self.h_mc_ratio)
        self.hcache.append(graph_comberr_ratio)
        graph_comberr_ratio.SetLineWidth( 0 );
        graph_comberr_ratio.SetMarkerSize( 0 );
        graph_comberr_ratio.SetFillStyle( 3375 );
        graph_comberr_ratio.SetFillColor( 28 );
        graph_comberr_ratio.Draw("5same")
        return self._canvas.cd()

    pass # end of class FlatPlot

class StackPlotFraction(StackPlotRatio):
    """
    stack plot with a second pad plotting 
    the fraction of each MC component.
    data can be plotted on the first pad as well.
    """
    def set_frame2(self, **kwargs):
        if "ylow" not in kwargs:
            kwargs["ylow"]   = 0.
        if "yhigh" not in kwargs:
            kwargs["yhigh"]  = 1.

        StackPlotRatio.set_frame2(self, data_to_mc = True, **kwargs)
        pass

    def draw(self, labx1=0.6, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True,  is_line_color=False):
        self.hcache = []
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        self.cd_main()
        h_st = R.THStack()
        #  self.h_data.auto_draw(is_draw=False)
        #  self.hcache.append(h_mc)
        self.hcache.append(h_st)
        count = 0
        if hasattr(self, "h_data"):
            if self.h_data.ileg >= 0:
                self.l_leg[self.h_data.ileg].AddEntry(self.h_data.h1, self.h_data.lab_name, self.h_data.lab_op)
        for _ in reversed(self._l_hist):
            _.auto_draw(is_draw=False, is_fill_color=True, is_line_color=is_line_color)
            h_st.Add(_.h1)
            count += 1
            pass
        for _ in self._l_hist:
            if _.ileg >= 0:
                self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)

        # h_st.Draw("Ehistsame")
        h_st.Draw("histsame" + _.drawop)
        graph_comberr = R.TGraphErrors(self.h_mc)
        self.hcache.append(graph_comberr)
        graph_comberr.SetLineWidth( 0 );
        graph_comberr.SetMarkerSize( 0 );
        graph_comberr.SetFillStyle( 3375 );
        graph_comberr.SetFillColor( 28 );
        graph_comberr.Draw("5same")
        if not self.remove_mc_stat:
            self.l_leg[0].AddEntry(graph_comberr, "MC Stat")
        if hasattr(self, "h_data"):
            self.h_data.h1.Draw("same")

        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")

        # second pad
        self.cd_sec()

        h_st2 = R.THStack()
        self.hcache.append(h_st2)
        for _ in reversed(self._l_hist):
            h = _.h1.Clone()
            h.Divide( self.h_mc )
            h_st2.Add(h)
        h_st2.Draw("histsame" + _.drawop)

        return self._canvas.cd()

    pass # end of class StackPlotFraction

class StackPlotCustomize(_BasePlotRatio):
    """
    stack plot with a second pad plotting 
    histogram where each bin is a function of signal and bkg
    for example, significance, S/B ratio
    """

    def __init__(self, cn, ct="", canx = 600, cany = 600, frac = 0.4, **kwargs):
        _BasePlotRatio.__init__(self, cn, ct, canx, cany, frac, **kwargs)
        self.l_signal_index = set([])
        self.l_bkg_index = set([])
        self._func = SoverB

    def set_func(self, func):
        self._func = func

    def set_frame1(self, **kwargs):
        """
        called before draw
        """
        h_mc = self._l_hist[0].h1.Clone()
        h_mc.Reset()
        for _ in reversed(self._l_hist):
            h_mc.Add(_.h1)

        self.h_mc = h_mc
        _BasePlotRatio.set_frame1(self, **kwargs)
        pass

    def add_sig(self, h1, drawop = "", lco = -1, ls = 0, mco = -1, ms = 0, lab_name = "", lab_op = "l", fco = -1, ileg=0):
        """
        add a most usual histogram
        """

        if lco == -1:
            lco = self._current_lco
            self._current_lco += 1
        _lco = self._l_color[lco]
        _ls  = self._line_style[ls]
        _fco = 0
        if fco == -1:
            _fco = _lco
        _mco = 0
        if mco == -1:
            _mco = _lco
        else:
            _mco = self._l_color[mco]
        _ms  = self._marker_style[ms]
        self.l_signal_index.add( len(self._l_hist) )
        self._l_hist.append(hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, _fco, ileg))
        pass

    def add_bkg(self, h1, drawop = "", lco = -1, ls = 0, mco = -1, ms = 0, lab_name = "", lab_op = "l", fco = -1, ileg=0, div_bin_width = False):
        """
        add a most usual histogram
        """

        if lco == -1:
            lco = self._current_lco
            self._current_lco += 1
        _lco = self._l_color[lco]
        _ls  = self._line_style[ls]
        _fco = 0
        if fco == -1:
            _fco = _lco
        _mco = 0
        if mco == -1:
            _mco = _lco
        else:
            _mco = self._l_color[mco]
        _ms  = self._marker_style[ms]
        self.l_bkg_index.add( len(self._l_hist) )
        self._l_hist.append(hist_content(h1, drawop, _lco, _ls, _mco, _ms, lab_name, lab_op, _fco, ileg))
        pass

    def set_frame2(self, **kwargs):
        """
        called before draw
        """
        if not hasattr(self, "_hframe1"):
            self.set_frame1()

        if len(self._l_hist_ratio) == 0:
            h_signal = self.h_mc.Clone()
            h_bkg = self.h_mc.Clone()
            h_signal.Reset()
            h_bkg.Reset()
            for _ in xrange(len(self._l_hist)):
                if _ in self.l_signal_index:
                    h_signal.Add(self._l_hist[_].h1)
                elif _ in self.l_bkg_index:
                    h_bkg.Add(self._l_hist[_].h1)

            for i in xrange(h_signal.GetNbinsX()):
                con, err = self._func(
                        h_signal.GetBinContent(i+1),
                        h_signal.GetBinError(i+1),
                        h_bkg.GetBinContent(i+1),
                        h_bkg.GetBinError(i+1),
                        )
                h_signal.SetBinContent(i+1, con)
                h_signal.SetBinError(i+1, err)
                pass

            #  self._l_hist_ratio.append(hist_content(h_signal, "PE", R.kBlack, _ls, _mco, _ms, lab_name, lab_op, _fco, 0))
            self._l_hist_ratio.append(hist_content(h_signal, "histE", R.kBlack, 1, 1, 1, "", "", 0, 0))
            pass

        self._hframe2 = self._l_hist_ratio[0].h1.Clone("hframe")
        self._hframe2.Reset()
        self.Ymin_ratio = self._find_hist_min([a.h1 for a in self._l_hist_ratio])
        self.Ymax_ratio = self._find_hist_max([a.h1 for a in self._l_hist_ratio])

        # default ones
        xaxis = self._hframe2.GetXaxis()
        yaxis = self._hframe2.GetYaxis()
        if xaxis.GetLabelFont() % 10 != 3:
            xaxis.SetLabelSize(xaxis.GetLabelSize() / self._frac)
            yaxis.SetLabelSize(yaxis.GetLabelSize() / self._frac)
            xaxis.SetTitleSize(xaxis.GetTitleSize() / self._frac)
            yaxis.SetTitleSize(yaxis.GetTitleSize() / self._frac)
        if "XTitleOffset" not in kwargs:
            xaxis.SetTitleOffset(1.0)
        if "YTitleOffset" not in kwargs:
            yaxis.SetTitleOffset(0.5)
        if "TopMargin" not in kwargs:
            self._p2.SetTopMargin(0)
        if "BottomMargin" not in kwargs:
            self._p2.SetBottomMargin(0.3)
        if "blank_factor" not in kwargs:
            kwargs["blank_factor"] = self._lower_blank_factor
        self._set_frame(self._hframe2, self._p2, self.Ymin_ratio, self.Ymax_ratio,  **kwargs)
        return h_signal
        pass

    def draw(self, labx1=0.6, laby1=0.65, labx2=0.9, laby2=0.9, draw_lab=True, data_to_mc=True, is_line_color=False, ):
        self.hcache = []
        self._prepare_canvas(labx1, laby1, labx2, laby2)
        self.cd_main()
        h_st = R.THStack()
        #  self.h_data.auto_draw(is_draw=False)
        #  self.hcache.append(h_mc)
        self.hcache.append(h_st)
        count = 0
        #  self._leg.AddEntry(self.h_data.h1, self.h_data.lab_name, self.h_data.lab_op)
        for _ in reversed(self._l_hist):
            _.auto_draw(is_draw=False, is_fill_color=True, is_line_color=is_line_color)
            h_st.Add(_.h1)
            count += 1
            pass
        for _ in self._l_hist:
            self.l_leg[_.ileg].AddEntry(_.h1, _.lab_name, _.lab_op)


        h_st.Draw("histsame" + _.drawop)
        graph_comberr = R.TGraphErrors(self.h_mc)
        self.hcache.append(graph_comberr)
        graph_comberr.SetLineWidth( 0 );
        graph_comberr.SetMarkerSize( 0 );
        graph_comberr.SetFillStyle( 3375 );
        graph_comberr.SetFillColor( 28 );
        graph_comberr.Draw("5same")
        if not self.remove_mc_stat:
            self.l_leg[0].AddEntry(graph_comberr, "MC Stat")
        #  self.h_data.h1.Draw("same")
        h_mc_ratio = self.h_mc.Clone()
        self.hcache.append(h_mc_ratio)
        if draw_lab:
            for leg in self.l_leg:
                leg.Draw("same")

        self.cd_sec()

        for _ in self._l_hist_ratio:
            _.auto_draw()

        return self._canvas
    pass # end of class FlatPlot

class MultiPadPlot(_BasePlot):
    def add_fp(self, fp):
        self.l_fp.append(fp)

    def __init__(self, cn, ct, canx, cany):
        self._canvas = R.TCanvas(cn, ct, canx, cany)
        self._upper_blank_factor = 1.5
        self.l_pads = []
        self.l_fp = []
        #  self.l_srcpads = []
        pass

    def Print(self, file_name = "test.pdf", *args):
        if len(self.l_pads):
            for p in self.l_pads:
                p.RedrawAxis()
                pass
        else:
            # todo: this canvas could contain 
            self._canvas.RedrawAxis()
            pass

        self._canvas.Print(file_name, *args)
        pass

    def add_pad(self, x0, y0, x1, y1, source_pad, **kwargs):
        print "MultiPadPlot: added pad"
        # x0 left, y0 bottom
        # x1 right, y1 top
        # in ratio

        #  self.l_srcpads.append(source_pad)
        if type(source_pad) == type(R.TCanvas()):
            self._canvas.cd()
            pad = R.TPad("np", "np", x0, y0, x1, y1, 0, 0)
            pad.Draw()
            pad.cd()
            #  source_pad.SetPad("p", "p", x0, y0, x1, y1, 0, 0)
            #  R.gROOT.SetSelectedPad(pad)
            source_pad.DrawClonePad()
            self.l_pads.append(pad)
        else:
            tm = source_pad.GetTopMargin()
            bm = source_pad.GetBottomMargin()
            lm = source_pad.GetLeftMargin()
            rm = source_pad.GetRightMargin()

            self.l_pads.append(source_pad)
            selected_pad = self.l_pads[-1]
            
            selected_pad.SetPad("p", "p", x0, y0, x1, y1, 0, 0)
            #  source_pad.SetMargin(lm, rm, bm, tm)

        selected_pad = self.l_pads[-1]
        area = selected_pad.GetWNDC() * selected_pad.GetHNDC()
        #  hframe = selected_pad.FindObject("hframe") 
        if hasattr(selected_pad, "frame"):
            hframe = selected_pad.frame 
            if hframe.GetXaxis().GetLabelFont() % 10 != 3:
                #  fs = .05 / 1.5 * area
                #  fs = .05 * area
                fs = .05
                kwargs["XLabelSize"] = fs
                kwargs["YLabelSize"] = fs
                kwargs["XTitleSize"] = fs
                kwargs["YTitleSize"] = fs

            self._set_frame(hframe, selected_pad, None, None, **kwargs)
        self._canvas.cd()
        selected_pad.Draw()
        #  selected_pad.Update()
        pass
    pass

class PluginSecondAxis(_BasePlot):
    def __init__(self, plot, pad = 1, **kwargs):
        """
        1 is main pad
        2 is second pad
        """
        _BasePlot.__init__(self, "pg_2ndAxis", **kwargs)
        self._l_color = [R.kBlack, R.kBlue]

        self._plot = plot
        if pad == 1:
            self._pad = plot.cd_main()
            self._hframe_parent = plot._hframe1
        elif pad == 2:
            self._pad = plot.cd_sec()
            self._hframe_parent = plot._hframe2

        # correct way to get min and max
        # print self._hframe_parent.GetXaxis().GetXmin(), self._hframe_parent.GetXaxis().GetXmax()
        # print self._hframe_parent.GetMinimum(), self._hframe_parent.GetMaximum()

        self._xmax = self._hframe_parent.GetXaxis().GetXmax()
        self._ymin = self._hframe_parent.GetMinimum()
        self._ymax = self._hframe_parent.GetMaximum()
        pass


    def _setup_second_axis(self):
        if not hasattr(self, "_hframe1"):
            self.set_frame()
        self._pad.cd()
        self._raxis = R.TGaxis(
                self._xmax, self._ymin, self._xmax, self._ymax,
                self._hframe1.GetMinimum(), self._hframe1.GetMaximum(),
                510, "-=L"
                )
        self._raxis.SetLabelFont(42)
        for _f1, _f2 in [
                ("SetLabelSize", "GetLabelSize"),
                ("SetLabelOffset", "GetLabelOffset"),
                ("SetTitleSize", "GetTitleSize"),
                ("SetTitleOffset", "GetTitleOffset"),
                ]:
            getattr(self._raxis, _f1)( getattr(self._hframe_parent.GetYaxis(), _f2)() )
        self._raxis.Draw()

        slope = (self._ymax - self._ymin) / \
                (self._hframe1.GetMaximum() - self._hframe1.GetMinimum())
        interp = self._ymax - slope * self._hframe1.GetMaximum()
        for _ in self._l_hist:
            _.h1.Scale(slope)
            for ibin in range(0, _.h1.GetNbinsX()+2):
                _.h1.SetBinContent(ibin, 
                        _.h1.GetBinContent(ibin) + interp)



    def draw(self, labx1=0.6, laby1=0.6, labx2=0.9, laby2=0.75, draw_lab=True):
        self._leg = R.TLegend(labx1, laby1, labx2, laby2)
        self._setup_second_axis()

        self._pad.cd()
        for _ in self._l_hist:
            _.auto_draw()
            self._leg.AddEntry(_.h1, _.lab_name, _.lab_op)
            pass
        if draw_lab:
            self._leg.Draw("same")
        return self._canvas
    pass # end of class PluginSecondAxis


##############################################
################# Examples ###################
##############################################

def test_FlatPlot1():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    fp = FlatPlot("c1","c1")
    #  fp.SetDivBinWidth()
    fp.SetDoShape()
    fp.add(ha, lco = 0, lab_name = "a histogram", drawop="EFhist", lab_op="fl", is_fill_color = True, fco=R.kRed, falpha = 0.35)
    #  fp.addg(R.TGraph(ha), lco = 0, lab_name = "a histogram", drawop="F", is_fill_color = True, fco=R.kRed, ileg=-1)
    fp.add(hb, lco = -1, ls = 1, lab_name = "b histogram", lab_op="f", drawop="Fhist", is_fill_color = True, fco=R.kBlue, falpha=0.35)
    #  fp.set_frame(ylow = 0, yhigh = 50, xlow = 0, xhigh = 5)
    fp.draw()
    fp.Print("test_FlatPlot1.pdf")

def test_FlatPlotRatio1():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    fp = FlatPlotRatio("c1","c1")
    # normalize the histogram to 1
    #  fp.SetDoShape()
    fp.add(ha,lco = 0, lab_name = "a histogram", drawop="hist")
    fp.add(hb,lco = 1, ls = 1, lab_name = "b histogram", drawop="hist")
    fp.set_frame2(ylow = 0, yhigh = 3)
    fp.draw()
    fp.Print("test_FlatPlotRatio1.pdf")

def test_StackPlotRatio1():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)
    hc = R.TH1D("hc", "hc", 2, 0, 2)

    hb.Sumw2()
    hc.Sumw2()
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    hc.Fill(0, 4)
    hc.Fill(0, 1)
    hc.Fill(1, 2)

    fp = StackPlotRatio("c1", "c1")
    fp.add_data(ha, lab_name = "data", drawop="hist", lab_op = "PLE")
    fp.add(hb,lco = 0, lab_name = "b histogram", drawop="", lab_op = "F")
    fp.add(hc,lco = 1, lab_name = "c histogram", drawop="", lab_op = "F")
    fp.set_frame2(ylow = 0, yhigh = 3, data_to_mc = False)
    fp.draw(is_line_color = True)
    fp.Print("test_StackPlotRatio1.pdf")

def test_StackPlotFraction():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)
    hc = R.TH1D("hc", "hc", 2, 0, 2)

    hb.Sumw2()
    hc.Sumw2()
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    hc.Fill(0, 4)
    hc.Fill(0, 1)
    hc.Fill(1, 2)

    fp = StackPlotFraction("c1", "c1")
    fp.add(ha, lab_name = "data", drawop="", lab_op = "F")
    fp.add(hb, lab_name = "b histogram", drawop="", lab_op = "F")
    fp.add(hc, lab_name = "c histogram", drawop="", lab_op = "F")
    fp.draw(is_line_color = True)
    fp.Print("test_StackPlotFraction.pdf")
    return fp

def test_StackPlotCustomize1():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)
    hc = R.TH1D("hc", "hc", 2, 0, 2)

    hb.Sumw2()
    hc.Sumw2()
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    hc.Fill(0, 4)
    hc.Fill(0, 1)
    hc.Fill(1, 2)

    fp = StackPlotCustomize("c1", "c1")
    fp.add_sig(ha, lab_name = "data", drawop="", lab_op = "F")
    fp.add_bkg(hb, lab_name = "b histogram", drawop="", lab_op = "F")
    fp.add_bkg(hc, lab_name = "c histogram", drawop="", lab_op = "F")
    fp.set_frame1(RightMargin = 0.1, ytitle="haha")
    fp.set_frame2(ylow = 0, yhigh = 3, RightMargin = 0.1, xtitle="eta", ytitle="ha?")
    fp.draw(is_line_color = True, data_to_mc = False)
    fp.Print("test_StackPlotCustomize1.pdf")
    return fp

def testPluginSecondAxis():
    fp = test_StackPlotCustomize1()
    pg2a = PluginSecondAxis(fp)
    pg2a._marker_style = [20]

    hc = R.TH1D("hd", "hc", 2, 0, 2)
    hc.SetBinContent(1, 0.4)
    hc.SetBinError(1, 0.04)
    hc.SetBinContent(2, 0.6)
    hc.SetBinError(2, 0.06)
    pg2a.add(hc, lab_name = "Eff", drawop = "EP", lab_op = "PLE")
    # pg2a.set_frame(ylow = 0.3, yhigh = 1.5)
    pg2a.draw(labx1=0.6, laby1=0.7, labx2=0.9, laby2=0.75)
    fp.Print("testPlugin.pdf")

def testPlotWithTGraph():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)
    b = R.TGraphErrors()
    b.SetPoint(0, 0.5, 3)
    b.SetPoint(1, 1.5, 13)
    b.SetPointError(0, 0, 2)
    b.SetPointError(1, 1, 3)

    fp = FlatPlot("c1","c1")
    fp.add(ha,lco = 0, lab_name = "a histogram", drawop="hist")
    fp.addg(b, fco = 6, fs = 3005, msize = 1.2, ms=20, lco = 12, lab_name = "b graph", drawop="3P", lab_op="PF")
    #  fp.set_frame(ylow = 0, yhigh = 50, xlow = 0, xhigh = 5)
    fp.draw()
    fp.Print("test_graph.pdf")

def testMultiPad():
    ha = R.TH1D("ha","ha", 2, 0, 2)
    hb = R.TH1D("hb", "hb", 2, 0, 2)

    ha.Sumw2()
    ha.Fill(0, 2)
    ha.Fill(0, 5)
    ha.Fill(1, 2)

    hb.Fill(0, 6)
    hb.Fill(1, 3)
    hb.Fill(1, 2)

    mpp = MultiPadPlot("name", "title", 600, 800)


    fp = FlatPlotRatio("c1","c1")
    fp.add(ha,lco = 0, lab_name = "a histogram", drawop="hist")
    fp.add(hb,lco = 1, ls = 1, lab_name = "b histogram", drawop="hist")
    fp.set_frame2(ylow = 0, yhigh = 3)
    fp.draw()
    fp.Print("test_multi_flatratio.pdf")

    cp = CompositionPlot("c3", "c3")
    # setting upper blank factor so that 
    cp.SetUpperBlankFactor(1)
    cp.add(ha,lco = 0, lab_name = "a histogram", drawop="hist")
    cp.add(hb,lco = 1, ls = 1, lab_name = "b histogram", drawop="hist")
    cp.draw(draw_lab=False)
    cp.Print("test_multi_compo.pdf")


    mpp.add_pad(0, 0.5, 1, 1,     fp.cd_main())
    mpp.add_pad(0, 0.26, 1, 0.48, fp.cd_sec(), BottomMargin=0)
    mpp.add_pad(0, 0.0, 1, 0.24,  cp.cd_main(), TopMargin=0, BottomMargin = 0.3)
    mpp.Print("test_MultiPadPlot.pdf")

if __name__ == "__main__":
    import AtlasStyle
    test_FlatPlot1()
    #  test_FlatPlotRatio1()
    #test_StackPlotRatio1()
    test_StackPlotCustomize1()
    #test_StackPlotFraction()
    #  testPlotWithTGraph()
    #  testMultiPad()
