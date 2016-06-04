# Copyright (c) 2015, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
import socket
import getpass
import pkgutil
import platform
import argparse
import importlib

from livvkit.util import variables
from livvkit.util import datastructures
from livvkit import bundles
from livvkit import resources

def parse(args):
    """
    Handles the parsing of options for LIVV's command line interface
    
    Args:
        args: The list of arguments, typically sys.argv[1:]
    """
    parser = argparse.ArgumentParser(description="Main script to run LIVV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@')

    parser.add_argument('-o', '--out-dir', 
            default=os.path.join(os.getcwd(), "vv_" + time.strftime("%m-%d-%Y")),
            help='Location to output the LIVV webpages.')
    
    parser.add_argument('--run-tests', action='store_true', 
            help="Run unit tests.")

    parser.add_argument('--verification',
            nargs=2,
            default=None,
            help='Specify the locations of the test and bench bundle to compare (respectively).')

    parser.add_argument('--validation',
            action='store', 
            nargs='+',            
            default=None,
            help='Specify the location of the configuration files for validation tests.')
   
    return parser.parse_args()


def init(options):
    """ Initialize some defaults """
    variables.resource_dir   = os.sep.join(resources.__path__) 
    variables.output_dir     = os.path.abspath(options.out_dir)
    variables.img_dir        = variables.output_dir + "/imgs"
    variables.index_dir      = variables.output_dir
    variables.verify = True if options.verification is not None else False
    variables.validate = True if options.validation is not None else False
    # TODO: This is a workaround to handle the case when no --verification or 
    #       --validation options are given.  Need to also fix the way that 
    #       the validation/performance handling is done in the if 
    #       options.validation != [] block.  Things currently seem to work but 
    #       this can definitely be made cleaner -- arbennett 2/21/16 
    variables.model_dir = ""
    variables.model_config = ""
    variables.bench_dir = ""
    variables.bench_config = ""
    variables.numerics_model_config = ""
    variables.verification_model_config = ""
    variables.performance_model_config = ""
    variables.performance_model_module = ""
    variables.validation_model_config = ""
    variables.validation_model_module = ""

    available_bundles = [mod for imp, mod, ispkg in pkgutil.iter_modules(bundles.__path__)]
    # rstrip accounts for trailing path separators
    if options.verification is not None:
        variables.model_dir = options.verification[0].rstrip(os.sep)
        variables.bench_dir = options.verification[1].rstrip(os.sep)
        if not os.path.isdir(variables.model_dir): 
            print("")
            print("----------------------------------------------------------")
            print("                       UH OH!")
            print("----------------------------------------------------------")
            print("    Your comparison directory does not exist; please check")
            print("    the path:")
            print("\n"+variables.model_dir+"\n\n")
            exit()
        
        if not os.path.isdir(variables.bench_dir):
            print("")
            print("----------------------------------------------------------")
            print("                       UH OH!")
            print("----------------------------------------------------------")
            print("    Your benchmark directory does not exist; please check")
            print("    the path:")
            print("\n"+variables.bench_dir+"\n\n")
            exit()
            
        
        variables.model_bundle = variables.model_dir.split(os.sep)[-1]
        variables.bench_bundle = variables.bench_dir.split(os.sep)[-1]

        if variables.model_bundle in available_bundles:
            variables.numerics_model_config = os.sep.join(
                bundles.__path__ + [variables.model_bundle, "numerics.json"])
            variables.numerics_model_module = importlib.import_module(
                ".".join(["livvkit.bundles", variables.model_bundle, "numerics"]))
            variables.verification_model_config = os.sep.join(
                 bundles.__path__ + [variables.model_bundle, "verification.json"])
            variables.verification_model_module = importlib.import_module(
                 ".".join(["livvkit.bundles", variables.model_bundle, "verification"]))
            variables.performance_model_config = os.sep.join(
                 bundles.__path__ + [variables.model_bundle, "performance.json"])
            variables.performance_model_module = importlib.import_module(
                 ".".join(["livvkit.bundles", variables.model_bundle, "performance"]))
        else:
            #TODO: Should implement some error checking here...
            variables.verify = False

    if options.validation is not None:
        variables.validation_model_config = os.sep.join(
             [variables.cwd, "bundles", variables.model_bundle, "validation.json"])
        variables.validation_model_module = importlib.import_module(
             ".".join(["bundles", variables.model_bundle, "validation"]))

    if not (variables.verify or variables.validate):
        print("")
        print("----------------------------------------------------------")
        print("                       UH OH!")
        print("----------------------------------------------------------")
        print("    No verification or validation tests found/submitted!")
        print("")
        print("    Use either one or both of the --verification and")
        print("    --validation options to run tests.  For more ")
        print("    information use the --help option, view the README")
        print("    or check https://github.com/LIVVkit/LIVVkit/wiki")
        print("----------------------------------------------------------")
        print("")
        exit()

