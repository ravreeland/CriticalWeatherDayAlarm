"""
GUI application for CWD Nofitication App

Toast Notification is causing wxPython loop to end. Possible switch threads? or something.
Two options to try next: See if wxPython has some other nice notification to use, similar to the toast, or get the application to flash when CWD day is declared
Third option is potentially have app become top window if CWD is declared or stopped.
"""
import wx
import wx.adv
import Critical_Weather_Day_Alarm as CWD
#import create_cwd_notification as ccn
class CWDFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(CWDFrame, self).__init__(*args, **kwargs)
        
        # Main GUI Areas
        self.bottomPanel = wx.Panel(parent=self)
        self.topPanel = wx.Panel(parent=self)
        self.bgColour_blue = wx.Colour(65,105,225)
        self.SetBackgroundColour(self.bgColour_blue)
        
        # Sizers
        self.frameSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Other class instance variables
        self.CWDtext = wx.StaticText(parent=self.topPanel, label="Critical Weather Day", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.createCWDNotificationButton = wx.Button(parent=self.topPanel, label="Create CWD Notification")
        self.CWDLog = wx.TextCtrl(parent=self.bottomPanel, style=wx.HSCROLL | wx.TE_MULTILINE)
        self.logCtrl = wx.LogTextCtrl(self.CWDLog)
        wx.Log.SetActiveTarget(self.logCtrl)
        
        # Event --> Sent up a timer, and start it
        self.pollTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.poll, self.pollTimer)
        self.pollTimer.Start(600000)

        #Button Event
        self.Bind(wx.EVT_BUTTON, self.onNotificationButton, self.createCWDNotificationButton)
        
        self.createTopPanel()
        self.createBottomPanel()
        self.frameSizer.Add(self.topPanel, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.frameSizer.Add(self.bottomPanel, 2, wx.EXPAND)
        self.SetSizer(self.frameSizer)

    
    # Seperate altering CWDText, so don't have to repeat myself if changing wording of text changes text size and format.
    # if doing so doesn't, will remove this function.
    def alterCWDText(self):
        font = self.CWDtext.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.CWDtext.SetFont(font)
        

    # Creating separate methods just to keep things a bit more organized.
    #Really unneccessary though, as it can all just be done in __init__ as i wont be using these def functions again 
    def createTopPanel(self):  
        # Changing text
        self.alterCWDText()
        # Altering Panel
        self.topPanel.SetBackgroundColour(self.bgColour_blue)
        self.topSizer.Add(self.CWDtext, 0, wx.ALIGN_CENTER_HORIZONTAL,0)
        self.topSizer.Add(self.createCWDNotificationButton, 0, wx.ALIGN_CENTER_HORIZONTAL,0)
        self.topPanel.SetSizer(self.topSizer)
    
    def createBottomPanel(self):
        bgColour_gold = wx.Colour(255, 213, 0)
        self.CWDLog.SetBackgroundColour(bgColour_gold)
        self.bottomSizer.Add(self.CWDLog, 1, wx.EXPAND)
        self.bottomPanel.SetSizer(self.bottomSizer)

    def poll(self, event):
        CWD_Logic, notificationID = CWD.CWDPoll()

        #wx.LogMessage("Logic: "+ str(CWD_Logic))
        if (CWD_Logic == True):
            self.CWDtext.SetLabel("Critical Weather Day \nDECLARED")
            self.CWDtext.SetBackgroundColour(wx.RED)
            self.Layout()
            self.createCWDAlert(notificationID)
        else:
            self.CWDtext.SetLabel("Critical Weather Day \nNOT DECLARED")
            self.CWDtext.SetBackgroundColour(wx.GREEN)
            self.Layout()

    def onNotificationButton(self, event):
        if (self.CWDtext.GetLabel() == "Critical Weather Day \nDECLARED"):
            wx.LogMessage("Creation of notification template email functionality has been removed. Didn't want to upload template that had email to work related.")
            #ccn.createCWDNotification() #Removing functionality of creating email template.
        elif(self.CWDtext.GetLabel() == "Critical Weather Day \nNOT DECLARED"):
            wx.LogMessage("Creation of notification template email functionality has been removed. Didn't want to upload template that had email to work related.")
        else:
            wx.LogError("Other error, button not working?")

    def createCWDAlert(self, messageID):
        messageTitle = "Critical Weather Day Alarm"
        messageBody = ""
        if (messageID == "0"):
            messageBody = "Critical Weather Day Has Been Declared"
        elif (messageID == "1"):
            messageBody = "Critical Weather Day Has ENDED!"
        elif (messageID == "2"):
            messageBody = "Critical Weather Day End Time HAS CHANGED! Check Website for Details!"
        notifier = wx.adv.NotificationMessage(title=messageTitle, message=messageBody)
        notifier.SetFlags(wx.ICON_INFORMATION)
        notifier.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)

        
            
if __name__ == '__main__':
    CWDapp = wx.App()
    frm = CWDFrame(None, title='Critical Weather Day Alarm')
    frm.Show()
    frm.poll(None) #does it the first time to set everything.
    CWDapp.MainLoop()
    
