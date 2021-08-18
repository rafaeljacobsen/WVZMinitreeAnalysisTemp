#!/usr/bin/env python
"""
an example to run systematics histograms for H4l minitrees, locally or on condor
"""

import common
if __name__ == "__main__":
    common.job("../output/condorZZ",#"/eos/user/b/bkan/SWAN_projects/WVZ_analysis/output/WWZsignaltest",#"../output/WWZsignaltest", 
            short_queue = False,
            sample_list = [
                "364250",
                "364288",
                "345705",
                "345706",
                ],
            sample_veto = [
                #  "410080",
                ],
            batch_name = "WVZ_optim")
    pass
