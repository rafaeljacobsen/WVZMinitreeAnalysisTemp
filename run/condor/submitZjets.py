#!/usr/bin/env python
"""
an example to run systematics histograms for H4l minitrees, locally or on condor
"""

import common
if __name__ == "__main__":
    common.job("../output/condorZjets",#"/eos/user/b/bkan/SWAN_projects/WVZ_analysis/output/WWZsignaltest",#"../output/WWZsignaltest", 
            short_queue = False,
            sample_list = [
                "364100",
                "364101",
                "364102",
                "364103",
                "364104",
                "364105",
                "364106",
                "364107",
                "364108",
                "364109",
                "364110",
                "364111",
                "364112",
                "364113",
                "364114",
                "364115",
                "364116",
                "364117",
                "364118",
                "364119",
                "364120",
                "364121",
                "364122",
                "364123",
                "364124",
                "364125",
                "364126",
                "364127",
                "364128",
                "364129",
                "364130",
                "364131",
                "364132",
                "364133",
                "364134",
                "364135",
                "364136",
                "364137",
                "364138",
                "364139",
                "364140",
                "364141",
                ],
            sample_veto = [
                #  "410080",
                ],
            batch_name = "WVZ_optim")
    pass
