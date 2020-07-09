import wx.adv
import wx
import sys
import threading
import time
import subprocess, ctypes, os, sys
from subprocess import DEVNULL

MLR_TOOLTIP = 'MLR Defense' 
MLR_ICON = 'icon.png' 
MLR_VERSION = 'v1.0'
MLR_LOG = 'mlr_log.txt'

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        #def panel
        panel = wx.Panel(self)

        #def status bar
        self.CreateStatusBar()
        
        #def menu bar
        infoMenu = wx.Menu()
        
        #def menu items
        menuAbout = infoMenu.Append(wx.ID_ABOUT, "&About", "This application has been developed to practically apply machine learning to prevent ransomware.")
        menuVersion = infoMenu.Append(wx.ID_ANY, "&Version", "Software Version")

        #creating menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(infoMenu,"&Info")
        self.SetMenuBar(menuBar)
    
        #def menu binds
        self.Bind(wx.EVT_MENU, self.OnVersion, menuVersion)
        self.Bind(wx.EVT_MENU, self.OnAbout,menuAbout)

        #Widgets
        about_button = wx.Button(panel, label = "About")

        #def widget binds
        about_button.Bind(wx.EVT_BUTTON, self.OnAbout)

        #sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(about_button, 0, wx.ALL | wx.Bottom, 5)
        
        self.SetSizer(main_sizer)

        #spawning window
        self.SetIcon(wx.Icon(MLR_ICON))
        self.Show(True)

    def OnVersion(self, event):
        #opens a dialog box with information about the version
        verInfo = "MLR Defense Version " + MLR_VERSION
        versiondlg = wx.MessageDialog(self, verInfo, caption="Version")
        versiondlg.ShowModal()
        versiondlg.Destroy()

    def OnAbout(self, event):
        #opens a dialog box with information about the application
        aboutdlg = wx.MessageDialog(self, "This application has been developed to apply machine learning to ransomware prevention. Developed by Bradley Silva and Justin Crozier.", caption="About")
        aboutdlg.ShowModal()
        aboutdlg.Destroy()

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        #def tray frame
        self.frame = frame
        super(TaskBarIcon, self).__init__()

        #setting tray icon
        self.set_icon(MLR_ICON)

        #setting left click bind
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        #def tray menu
        menu = wx.Menu()
        menu.AppendSeparator()
        
        #def tray menu items
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
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def checkAdmin():
    #Run the application with admin rights
    try:
        status = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        status = False
    if not status:
        print("This is not running as an admin")
    print("Running as admin")

def networkDisable():
    nic_list = subprocess.check_output('wmic nic get index')
    nic_list = nic_list.rstrip().decode().split()
    nic_list.pop(0)
    for index in nic_list:
        nic_command = "wmic path win32_networkadapter where index=" + index + " call disable"
        subprocess.call(nic_command, stderr=DEVNULL)
    return nic_list

def networkEnable(nic_list):
    for index in nic_list:
        nic_command = "wmic path win32_networkadapter where index=" + index + " call enable"
        subprocess.call(nic_command, stderr=DEVNULL)
		
def processResponse(proc_Name):
    proc_command = "taskkill /f /im " + proc_Name
    #os.system(command)
    print("Running command: " + proc_command)

def main():
    app = App(False)
    app.MainLoop()

def monitor():
    logFile = open(MLR_LOG, 'r')
    logFile.seek(0,2)
    print("The log file is being monitored")
    net_list = networkDisable()    
    while not quit:
        line = logFile.readline()
        if not line:
            time.sleep(0.1)
            continue
    
    networkEnable(net_list)
    print("This is the monitor thread exiting")

if __name__ == '__main__':
    checkAdmin()
    quit = False
    GUI = threading.Thread(target=main)
    GUI.start()
    mlrProc = threading.Thread(target=monitor)
    mlrProc.start()
    GUI.join()
    quit = True
    mlrProc.join()
    