import wx.adv
import wx
import csv
import webbrowser
import threading
import time
import subprocess, ctypes, os, sys, queue
from queue import Queue
from subprocess import DEVNULL
from datetime import date

MLR_TOOLTIP = 'MLR Defense'
MLR_ICON = 'icon.png'
MLR_VERSION = 'v1.0'
MLR_LOG = 'mlr_log.txt'
MLR_TEST = 'matches.txt'
MLR_WEIGHT = 'Weights.csv'

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        # def panel
        panel = wx.Panel(self)

        # def status bar
        self.statusBar = self.CreateStatusBar()
        today = date.today().strftime("%B %d, %Y")
        self.statusBar.SetStatusText(str(today))

        # def menu bar
        infoMenu = wx.Menu()
        threatsMenu = wx.Menu()

        # def menu items
        menuAbout = infoMenu.Append(wx.ID_ABOUT, "&About", "This application has been developed to practically apply "
                                                           "machine learning to prevent ransomware.")
        menuVersion = infoMenu.Append(wx.ID_ANY, "&Version", "Software Version")
        menuGithub = infoMenu.Append(wx.ID_ANY, "&Github", "GitHub repo")
        menuThreats = threatsMenu.Append(wx.ID_ANY, "&Threats", "Possible active Threats")

        # creating menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(infoMenu, "&Info")
        menuBar.Append(threatsMenu, "&Threats")
        self.SetMenuBar(menuBar)

        # def menu binds
        self.Bind(wx.EVT_MENU, self.OnVersion, menuVersion)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnThreats, menuThreats)
        self.Bind(wx.EVT_MENU, self.OnGitHub, menuGithub)
        self.Bind(wx.EVT_MENU_HIGHLIGHT, self.Bypass)

        # Widgets
        about_button = wx.Button(panel, label="About")

        # def widget binds
        about_button.Bind(wx.EVT_BUTTON, self.OnAbout)

        # sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(about_button, 0, wx.ALL | wx.Bottom, 5)

        self.SetSizer(main_sizer)

        # spawning window
        self.SetIcon(wx.Icon(MLR_ICON))
        self.Show(True)

    def OnVersion(self, event):
        # opens a dialog box with information about the version
        verInfo = "MLR Defense Version " + MLR_VERSION
        versiondlg = wx.MessageDialog(self, verInfo, caption="Version")
        versiondlg.ShowModal()
        versiondlg.Destroy()

    def OnAbout(self, event):
        # opens a dialog box with information about the application
        aboutdlg = wx.MessageDialog(self,
                                    "This application has been developed to apply machine learning to ransomware prevention. Developed by Bradley Silva and Justin Crozier.",
                                    caption="About")
        aboutdlg.ShowModal()
        aboutdlg.Destroy()

    def OnThreats(self, event):
        # opens a new frame to show threat overview
        title = 'Threat Overview'
        frame = ThreatFrame(title=title)

    def OnGitHub(self, event):
        # opens a browser tab to github repo
        webbrowser.open('https://github.com/snices/MLRansonware')

    def Bypass(self, event):
        pass


# Threat frame to display current threat list in a list format
class ThreatFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size=(400, 300))
        self.SetIcon(wx.Icon(MLR_ICON))
        self.Show()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        formatbuff = formattedq.get()
        threatList = ["ransomware.exe", "taskmanager.exe"]
        lst = wx.ListBox(panel, size=(200, 300), choices=threatList, style=wx.LB_SINGLE)
        box.Add(lst, 0, wx.EXPAND)
        box.Add(self.text, 1, wx.EXPAND)
        panel.SetSizer(box)
        panel.Fit()

        self.Bind(wx.EVT_LISTBOX, self.onSelectBox, lst)
        self.Show(True)

    def onSelectBox(self, event):
        
        self.text.AppendText(event.GetEventObject().GetStringSelection() + " currently has a score of: " + "74%" + "\n")


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        # def tray frame
        self.frame = frame
        super(TaskBarIcon, self).__init__()

        # setting tray icon
        self.set_icon(MLR_ICON)

        # setting left click bind
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        # def tray menu
        menu = wx.Menu()
        menu.AppendSeparator()

        # def tray menu items
        create_menu_item(menu, 'Open', self.on_open)
        create_menu_item(menu, 'Exit', self.on_exit)

        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, MLR_TOOLTIP)

    def on_left_down(self, event):
        app = wx.App(False)
        frame = MainWindow(None, "MLR Defense")
        app.MainLoop()

    def on_open(self, event):
        app = wx.App(False)
        frame = MainWindow(None, "MLR Defense")
        frame.show()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def checkAdmin():
    # Run the application with admin rights
    try:
        status = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        status = False
    if not status:
        print("This is not running as an admin")
    print("Running as admin")


def networkDisable():
    # produces a list of index numbers related to active NICs
    nic_list = subprocess.check_output('wmic nic get index')
    # Manipulate list to be usable with command
    nic_list = nic_list.rstrip().decode().split()
    nic_list.pop(0)
    # loop through all identified index numbers and disable them
    for index in nic_list:
        nic_command = "wmic path win32_networkadapter where index=" + index + " call disable"
        # call the command and supress errors (Virtual NICs throw errors)
        subprocess.call(nic_command, stderr=DEVNULL)
    return nic_list


def networkEnable(nic_list):
    # loop through list of NIC indexes and re-enable them
    for index in nic_list:
        nic_command = "wmic path win32_networkadapter where index=" + index + " call enable"
        subprocess.call(nic_command, stderr=DEVNULL)


def processResponse(proc_Name):
    proc_command = "taskkill /f /im " + proc_Name
    # Kill the identified malicious process
    """os.system(command)"""
    # Test command to show process getting killed
    print("Running command: " + proc_command)


def main():
    app = App(False)
    app.MainLoop()


def monitor():
    # opens the log file and jumps to the end. Continuosly reads the file
    """logFile = open(MLR_LOG, 'r')
    logFile.seek(0,2)
    print("The log file is being monitored")
    while not quit:
        line = logFile.readline()
        if not line:
            time.sleep(0.1)
            continue"""
    # Proof of concept section
    with open(MLR_TEST) as testLogFile:
        for line in testLogFile:
            log = line.strip()
            buffer = log.split(':')
            dataq.put(buffer)
    print("This is the monitor thread exiting")

def modify():
    #creating a dictionary to store column #'s and respective weight
    w_dict = {}
    with open(MLR_WEIGHT) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            w_dict[row[0]] = row[1]
    #defining temp dict to hold procname and value
    temp = {}
    #monitoring thread main loop
    while(True):
        #when there is an object in the data queue do the following
        if dataq.not_empty:
            #get the value from the data queue and split into key and value
            databuff = dataq.get()
            key = databuff[0]
            value = databuff[1]
            #convert col# into true value using weight dict
            if value in w_dict:
                value = float(w_dict[value])
            else:
                value = 0.0
            #incrementing proc value if already stored
            if key in temp:
                temp[key] += value
            #adding new proc name and its value
            else:
                temp[key] = value
        print(temp)
        formattedq.put(temp)

if __name__ == '__main__':
    checkAdmin()
    dataq = Queue()
    formattedq = Queue()
    quit = False
    GUI = threading.Thread(target=main)
    GUI.start()
    mlrProc = threading.Thread(target=monitor)
    mlrProc.start()
    modifyProc = threading.Thread(target = modify)
    modifyProc.daemon=True
    modifyProc.start()
    GUI.join()
    quit = True
    mlrProc.join()
