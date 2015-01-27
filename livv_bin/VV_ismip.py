'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

import re
import os
import sys
import glob
import subprocess

import livv
from livv import *
from livv_bin.VV_test import *
import jinja2

class Ismip(AbstractTest):
    
    #
    # Constructor
    #
    def __init__(self):
        self.ismipTestsRun = []
        self.ismipBitForBitDetails = dict()
        self.ismipTestFiles = []
        self.ismipTestDetails = []
        self.ismipFileTestDetails = []
        
        self.name = "ismip"
        self.description = "Simulates steady ice flow over a surface with periodic boundary conditions"
    
    #
    # Return the name of the test
    #
    def getName(self):
        return self.name
    
    
    #
    # Runs the dome specific test case.  Calls some shared resources and
    # some diagnostic/evolving case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        self.ismipTestsRun.append(testCase)
        
        # Map the case names to the case functions
        callDict = {'ismip-hom-a/20km' : self.runLargeA,
                    'ismip-hom-c/20km' : self.runLargeC,
                    'ismip-hom-a/80km' : self.runSmallA,
                    'ismip-hom-c/80km' : self.runSmallC }
        
        # Call the correct function
        callDict[testCase]()
         
        # More common postprocessing
        return
    
    
    #
    #  Description
    #
    #
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        templateFile = "/test.html"
        template = templateEnv.get_template( templateFile )
        
        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs/ismip"
        
        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + "ismip"
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")] )
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")] )

        # Make an iterable list of the test files and details
        self.ismipFileTestDetails = zip(self.ismipTestFiles, self.ismipTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : self.getName(),
                        "indexDir" : livv.indexDir,
                        "cssDir" : livv.cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.ismipTestsRun,
                        "bitForBitDetails" : self.ismipBitForBitDetails,
                        "testDetails" : self.ismipFileTestDetails,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/ismip.html', "w")
        page.write(outputText)
        page.close()        
    
    
    #
    # Runs the diagnostic dome specific test case code.  
    #
    #
    #    
    def runLargeA(self):
        print("  Ismip-hom-A 20km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/ismip-hom-a/20km' + livv.dataDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + '/ismip-hom-a/20km' + livv.dataDir + '/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('a','20')

        # Run bit for bit test
        self.ismipBitForBitDetails['ismip-hom-a/20km'] = self.bit4bit('/ismip-hom-a/20km')
        for key, value in self.ismipBitForBitDetails['ismip-hom-a/20km'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runLargeC(self):
        print("  Ismip-hom-C 20km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/ismip-hom-c/20km' + livv.dataDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + '/ismip-hom-c/20km' + livv.dataDir + '/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('c','20')

        # Run bit for bit test
        self.ismipBitForBitDetails['ismip-hom-c/20km'] = self.bit4bit('/ismip-hom-c/20km')
        for key, value in self.ismipBitForBitDetails['ismip-hom-c/20km'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallA(self):
        print("  Ismip-hom-A 80km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/ismip-hom-a/80km' + livv.dataDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + '/ismip-hom-a/80km' + livv.dataDir + '/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('a','80')

        # Run bit for bit test
        self.ismipBitForBitDetails['ismip-hom-a/80km'] = self.bit4bit('/ismip-hom-a/80km')
        for key, value in self.ismipBitForBitDetails['ismip-hom-a/80km'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallC(self):
        print("  Ismip-hom-C 80km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/ismip-hom-c/80km' + livv.dataDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + '/ismip-hom-c/80km' + livv.dataDir + '/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('c','80')

        # Run bit for bit test
        self.ismipBitForBitDetails['ismip-hom-c/80km'] = self.bit4bit('/ismip-hom-c/80km')
        for key, value in self.ismipBitForBitDetails['ismip-hom-c/80km'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success

    #
    # Create the plots
    #
    #
    def plot(self, aOrC, size):
        #print "    Generating ismip-hom-" + aOrC + "-" + size + "km plot...." 
        #print "    This is just a dummy method.  Updates coming soon!"
        
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "ismip"
        ishoma80u_plotfile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'ug.ncl'
        bench1  = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + livv.dataDir + '/ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        bench4  = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + livv.dataDir + '/ishom.'+aOrC+'.'+size+'km.glissade.4.out.nc\", \"r\")'
        test1    = 'VAR1 = addfile(\"'+ livv.inputDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + livv.dataDir + '/ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        test4    = 'VAR4 = addfile(\"'+ livv.inputDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + livv.dataDir + '/ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        name = 'ismip'+aOrC+size+'ug.png'
        path     = 'PNG = "' + img_path + '/' + name + '"'
        plot_ishoma80u = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                        +"'  '" + path + "' " + ishoma80u_plotfile + " >> plot_details.out"
    
        print("    Saving plot details to " + img_path + " as " + name)
    
        try:
            subprocess.check_call(plot_ishoma80u, shell=True)
            #print "creating ismip hom a 80km uvel plots"
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)    
        
        
        
        
        
        