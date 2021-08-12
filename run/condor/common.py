#!/usr/bin/env python

# future
from __future__ import print_function

# system
import sys, os, shutil
import re, glob

# 3rd party
#  import ROOT as R

# local
sys.path.append("/afs/cern.ch/user/r/rowang/public/MyPythonUtilities")
from CondorJobmaker import *
import MyPythonSystemUtil as mpsu

class job(object):
    @mpsu.autoassign
    def __init__(self, 
            output_dir,
            msg_level=1,
            test_condor=False, 
            short_queue=False,
            tree_name = "SM4L_Nominal",
            l_year = {
                "1516": "r9364", 
                "17": "r10201",
                "18": "r10724",
                },
            local=False, 
            # this is the name that will show up in condor_q for monitoring purpose
            condor_script_name = "WVZProcess.sh",
            executable_name = "./run",
            input_dir = "/eos/user/r/rowang/public/WVZ_minitrees/v1.3/",

            # this is a selected subset of sample.
            # if not specify, will run all of them.
            sample_list = [ ],
            sample_veto = [ ],

            l_sys = [
                "NOMINAL",
                ],
            batch_name = ""
            ):


        print(mpsu.green("Working on {0}".format(output_dir)))

        self.cjm = CondorJobmaker(output_dir, condor_script_name, log_dir = "./", 
                batch_name = batch_name)

        self.cjm.add_global_dependency(executable_name)
        if "atustc" in os.environ["HOSTNAME"]:
            self.proxy_file = "x509up_u{0}".format(os.getuid())
            self.cjm.add_global_dependency("/tmp/" + self.proxy_file)
            self.proxy_file2 = os.environ["KRB5CCNAME"].split(":")[1] 
            self.cjm.add_global_dependency(self.proxy_file2)
            #  self.cjm.write_steer_string("use_x509userproxy = true")
            #  self.cjm.write_steer_string("requirements = ((substr(Machine,0,11) =!= \"atustc-c6-0\")")

        for self.sysname in l_sys:
            print (self.sysname)
            for self.sample in sample_list:
                self.add_sample()
                pass
            if len(sample_list) == 0:
                self.sample = "mc16_13TeV"
                self.add_sample()
            pass
        self.script_str()
        if test_condor:
            self.cjm._final_prep()
            return
        if short_queue:
            self.cjm.submit_short()
            return
        self.cjm.submit()

        pass

    def add_sample(self):
        """
        take a sample name and a systematics name, register three jobs for condor
        under <sysname>_1516/17/18
        TODO: do it differently for data! 
        """
        for year, postfix in self.l_year.items():
            self.full_sample_name = ""
            for self.full_sample_name in glob.glob(
                    self.input_dir + "*" + self.sample + "*" + postfix + "*"):
                if(self.veto_sample()): continue
                # if self.sample is a dsid, it should only run once
                self.dsid = os.path.basename(self.full_sample_name).split(".")[1]

                self.outputdir = self.sysname + "_" + year
                self.cjm.add_block(self.outputdir, 
                        self.dsid, 
                        self.script_args(),
                        # transfer the directory directly
                        transfer_output = [self.outputdir]
                        )
            pass
        pass

    def veto_sample(self):
        for veto in self.sample_veto:
            if veto in self.full_sample_name: return True
        return False

    def script_args(self, ):
        """
        this generate the arguments for the script, where $1 will be the 
        executable's argument
        """
        self.exe_args = "file.list {0} {1}".format(
                self.outputdir, 
                self.dsid)

        return '"' + ("" 
                + "' " + self.exe_args + " '"
                + " " + self.outputdir
                + " " + self.full_sample_name
                ) + '"'
        pass

    def permission_str(self):
        if os.environ["USER"] == "rowang":
            self.cjm.write_exe_string("echo $PASSWORD | kinit rowang@CERN.CH")
        else:
            raise NotImplementedError("Please look at the example here and implement your user password.")

    def script_str(self, ):
        """
        write to the condor_script for the CondorJobmaker
        """
        self.cjm.write_exe_string("#!/bin/bash")
        #  self.cjm.write_exe_string("ls")
        #  self.cjm.write_exe_string("echo")
        #  self.cjm.write_exe_string("ls /")
        #  self.cjm.write_exe_string("echo")
        #  self.cjm.write_exe_string("ls /tmp")
        #  self.cjm.write_exe_string("echo")
        # to have eos & afs access
        if "atustc" in os.environ["HOSTNAME"]:
            self.cjm.write_exe_string("rm -f /tmp/*".format(self.proxy_file))
            self.cjm.write_exe_string("cp {0} /tmp".format(self.proxy_file))
            self.cjm.write_exe_string("cp {0} /tmp".format(os.path.basename(self.proxy_file2)))

            
            #  self.cjm.write_exe_string("ls /eos")
            #  self.cjm.write_exe_string("echo 'print $X509_USER_PROXY'")
            #  self.cjm.write_exe_string("echo $X509_USER_PROXY")
            #  self.cjm.write_exe_string("ls $X509_USER_PROXY")
            #  self.cjm.write_exe_string("klist")
            #  self.cjm.write_exe_string("ls /tmp")

        self.cjm.write_exe_string("mkdir -p $2")
        self.cjm.write_exe_string("")
        self.cjm.write_exe_string("echo")
        self.cjm.write_exe_string("echo")
        self.cjm.write_exe_string("")
        # TODO: now the disk it's hardcoded!
        self.cjm.write_exe_string("echo root://eosuser.cern.ch/$3 > file.list")
        #  self.cjm.write_exe_string("echo $3 > file.list")
        self.cjm.write_exe_string("time " + self.executable_name + " $1")
        pass
