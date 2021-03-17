import urllib.request
import re
from twisted.internet import task, reactor
from win10toast import ToastNotifier
from urllib.error import URLError, HTTPError
import wx

#Global Variables 
CWDDeclared = False
endTime = ""

# Helper Functions

def readCWDSite():
    rawSiteList = ["Empty"]
    siteList=[]
    try:
        siteReader = urllib.request.urlopen("https://www.nco.ncep.noaa.gov/status/cwd/")
    except HTTPError as e:
        #logging.error('Error code: ', e.code)
        msg = 'Error code, ', e.code
        wx.LogError(msg)
    except URLError as e:
        #logging.error('Reason: ', e.reason)
        msg = 'Reason, ', e.reason
        wx.LogError(msg)
    else:
        rawSiteList = siteReader.readlines()
        siteReader.close()

    for line in rawSiteList:
        lineStr = line.decode("UTF8").strip() # Data in siteList is byte-like and needs to be decoded to format into python string.
        siteList.append(lineStr)
    
    return siteList

def testReader():
   #file = open('cwd_negative_test.txt') 
   file = open('cwd_positive_test.txt')
   fList = file.readlines()
   file.close()
   return fList

# Searches for text indicating CWD has been declared. The function will return False if no text indicates CWD, and True if html text indicates CWD.
def searchForStatus(HTMLList):
    declaredStatusRE = ".*Critical Weather Day Has Been Declared.*"
    CWDStatus = False # False --> No Critical Weather Day Declared; True --> Declared
    for line in HTMLList:
        if (re.search(declaredStatusRE, line) != None): 
            CWDStatus = True        
    # If logic gets here, and did not find CWD has been declared (in the above if statement), then CWDStatus is by default set to False, no need set it to false again.
    return CWDStatus

# Grabs the ending time for the CWD and returns it.
def searchForEndTime(HTMLList):
    endRE = "END: .*"
    endTime_localVar = "Default"
    for line in HTMLList:
        if (re.search(endRE, line) != None): # if not none, means it matched the regex
            endTime_localVar = line
    return endTime_localVar


    
#***********************************************************************************************

# Main Logic Function
# This function calls the above helper functions to poll the website, gather the appropiate data, and
# run the logic to determine CWD status, and determine changes to ending times of CWD.
def CWDPoll():
    global CWDDeclared
    global endTime
    msg_CWDDeclared = "CWD: " + str(CWDDeclared)
    wx.LogMessage(endTime)
    wx.LogMessage(msg_CWDDeclared)
    noficationID = "5" #5 is just a default value
    siteHTMLCode = readCWDSite() # POLL WEBSITE, get HTML Code, readCWDSite() or testReader()
    #siteHTMLCode = testReader() # Test purposes
    if (siteHTMLCode[0] == "Empty"): # takes care of it site cannot be reached (error handling)
        #logging.error("No Access to Site")
        wx.LogError("No Access to Site")
    else:
        # CHECK STATUS
        CWDStatus = searchForStatus(siteHTMLCode)
        CWDEndTime = searchForEndTime(siteHTMLCode) # Current poll of website's end time.
        
        # CWDDelcared --> Global variable, keeps track of previous status
        # CWDStatus --> status of current poll of the website 
        if (CWDDeclared == True): # CWD IS ACTIVE

            # check to see if CWD has ended 
            if (CWDStatus == False):
                CWDDeclared = False
                #logging.info("CWD Has Ended")
                wx.LogMessage("CWD Has Ended")
                noficationID = "1" #sys message
            
            # If CWD is still active, check the end times to see if it has been extended.
            elif (CWDStatus == True):
                # check for changes
                if (CWDEndTime != endTime):
                    noficationID = "2"
                    #logging.info("CWD End Time Has Changed! Check Website!!")
                    wx.LogMessage("CWD End Time Has Changed! Check Website!!")
                    endTime = CWDEndTime
                else:
                    # no changes, just print a status to shell to make sure it is still running
                    #logging.info("CWD Still Active")
                    wx.LogMessage("CWD Still Active")
                
        elif (CWDDeclared == False): # CWD IS NOT ACTIVE

            if (CWDStatus == False):
                #logging.info("No CWD Declared")
                wx.LogMessage("No CWD Declared")

            elif (CWDStatus == True):
                CWDDeclared = True
                 #sys Message
                #logging.info("CWD Just Declared")
                wx.LogMessage("CWD Just Declared")
                endTime = CWDEndTime
                noficationID = "0"
        return CWDDeclared, noficationID



#************************************************************************************************    
# Use event drive/timing to run CWDPoll with the GUI portion.
# None-GUI Engine of Application 
def mainApp():
    timeout = 60.0 # (600) 10 minutes in seconds
    l = task.LoopingCall(CWDPoll)
    l.start(timeout)
    reactor.run()
    
#mainApp()

#CWDPoll()


