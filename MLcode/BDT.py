#!/usr/bin/env python
import pandas as pd
import xgboost as xgb
from sklearn.metrics import confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


class BDT():
    '''This class is for BDT training, testing and cross validation'''
    
    def __init__(self, _dfsig, _dfbkg):
        # read dfsig and bkg, store it into the class object.
        # nfeature is the feature number, except for label column and weight column
        self.dfsig = _dfsig
        self.dfbkg = _dfbkg
        self.nfeature = _dfsig.shape[1] - 2 
    
    def splitdata(self, sig_frac=0.7, bkg_frac=0.7):
        # try to split the whole data into training and test data
        
        # tags for training
        sig_tag = self.dfsig.index.to_series().sample(frac=sig_frac,replace=False)
        bkg_tag = self.dfbkg.index.to_series().sample(frac=bkg_frac,replace=False)
        # train and test dataframes
        sig_train = self.dfsig.iloc[sig_tag]
        sig_test = self.dfsig.drop(sig_tag)
        bkg_train = self.dfbkg.iloc[bkg_tag]
        bkg_test = self.dfbkg.drop(bkg_tag)

        # data, weight, label for train and test set
        self.data = pd.concat([sig_train.iloc[:, 0:self.nfeature], bkg_train.iloc[:, 0:self.nfeature]])
        self.wgt = pd.concat([sig_train.iloc[:, -2], bkg_train.iloc[:, -2]])
        self.label = pd.concat([sig_train.iloc[:, -1], bkg_train.iloc[:, -1]])
        self.testdata = pd.concat([sig_test.iloc[:, 0:self.nfeature], bkg_test.iloc[:, 0:self.nfeature]])
        self.testwgt = pd.concat([sig_test.iloc[:, -2], bkg_test.iloc[:, -2]])
        self.testlabel = pd.concat([sig_test.iloc[:, -1], bkg_test.iloc[:, -1]])

        # create DMatrix, used for training and testing in XGBoost
        self.dtrain = xgb.DMatrix(self.data, label=self.label, weight=abs(self.wgt))
        self.dtest = xgb.DMatrix(self.testdata, label=self.testlabel, weight=abs(self.testwgt))
        # scale factor to make the weight of background and signal the same
        self.scale_pos_weight = sum(self.wgt[self.label==0])/sum(self.wgt[self.label==1])

        return self.dtrain, self.dtest

        
    def initparams(self, nround=20, max_depth=10, num_parallel_tree=1, eta=0.3, gamma=0, lamb=1):
        # set parameters for training
        # I will add more parameters to this part for tuning
        self.params = {'max_depth': max_depth,
                      'num_parallel_tree': num_parallel_tree,
                      'eta': eta,
                      'gamma':gamma,
                      'lambda':lamb,
                      'objective': 'binary:logistic',
                      'eval_metric':'logloss',
                      'scale_pos_weight':self.scale_pos_weight,
                     }
        self.evallist = [(self.dtrain, 'train'), (self.dtest, 'test')]
        self.nround = 20
        
        
    def train(self):
        # train the model using parameters above.
        self.model = xgb.train(self.params, self.dtrain, self.nround, self.evallist)
        
        
    def score(self, saveflag=False, name='BDTperformance.png', density=True, logscale=False):
        # plot the BDT score graph
        x = self.model.predict(self.dtest)
        plt.subplots(1,1)
        plt.hist(x=x[self.testlabel==0], weights=self.testwgt[self.testlabel==0], color='blue',histtype='step', density=density)
        plt.hist(x=x[self.testlabel==1], weights=self.testwgt[self.testlabel==1], color='red',histtype='step', density=density)
        plt.xlabel('BDTscore')
        plt.title("BDT performance (density plot)")
        if logscale:
            plt.yscale('log', basey=10)
        if saveflag:
            plt.savefig("./plots/"+name)
            
    
    def confusionmatrix(self, cutpoint=0.5):
        # get the confusion matrix with specific cutpoint.
        self.ypred = self.model.predict(self.dtest) > cutpoint
        self.mat = confusion_matrix(self.testlabel, self.ypred, sample_weight=self.testwgt)
        print("######The confusion matrix is:########")
        print(self.mat)
        return self.mat
    
        
    def significance(self):
        # get the significance, must run after we calculated the confusion matrix
        self.s = self.mat[1,1]
        self.b = self.mat[0,1]
        self.n = self.s + self.b
        self.Z = np.sqrt(2*(self.n*np.log(self.n/self.b) - self.s))
        print("#######The significance is:########")
        print(self.Z)
        return self.Z
    
    
    def importance(self, saveflag=False, name='BDTimportance.png'):
        #draw the importance graph
        ax = xgb.plot_importance(self.model)
        fig = ax.figure
        fig.set_size_inches(10,8)
        if saveflag:
            fig.savefig("./plots/"+name)
        
        
    def drawtree(self, saveflag=False):
        # draw one tree. Not recommended because the tree is very large. However, you can try it.
        ax = xgb.plot_tree(self.model, num_trees=1)
        fig = ax.figure
        fig.set_size_inches(500,20)
        if saveflag:
            fig.savefig("./plots/tree.png")
        
        
    # tuning function
    # this function could cost you a lot of time with higher cv folds. I choose it to be 3 as default.
    # need to think about the output form. For now it's the default outcome of xgb.cv().
    def tune(self, varname='max_depth', tunerange=[5,7,10]):
        # varname should be a string
        # tunerange should be a list for tune parameters
        nfold = 3
        tunehistory = {}
        for var in tunerange:
            self.params[varname] = var
            tunehistory[var] = xgb.cv(self.params, self.dtrain, nfold=nfold, num_boost_round=self.nround)
        return tunehistory
        

if __name__ == "__main__":
    # read signal and background data
    _dfsig = pd.read_csv("./data/4l_signal.csv", index_col=0)
    _dfbkg = pd.read_csv("./data/4l_background.csv", index_col=0)
    # Specify one channel
    # all: all channel
    # DF: different flavor channel
    # SFinZ: same flavor inside Z region
    # SFoutZ: same flavor outside Z region
    flag = 'DF'
    if flag=='DF':
        dfsig = _dfsig[_dfsig.DF==1]
        dfbkg = _dfbkg[_dfbkg.DF==1]
    elif flag=='SFinZ':
        dfsig = _dfsig[_dfsig.SFinZ==1]
        dfbkg = _dfbkg[_dfbkg.SFinZ==1]
    elif flag=='SFoutZ':
        dfsig = _dfsig[_dfsig.SFoutZ==1]
        dfbkg = _dfbkg[_dfbkg.SFoutZ==1]
    else:
        dfsig=_dfsig
        dfbkg=_dfbkg
    dfsig.index = range(dfsig.shape[0])
    dfbkg.index = range(dfbkg.shape[0])
    myBDT = BDT(dfsig,dfbkg)
    myBDT.splitdata()
    myBDT.initparams()
    myBDT.train()
    myBDT.score(saveflag=True,name='score_'+flag+'.png', density=True, logscale=False)
    myBDT.confusionmatrix()
    myBDT.significance()
    myBDT.importance(saveflag=True,name='importance_'+flag+'.png')
    myBDT.drawtree()
    #myBDT.tune()
