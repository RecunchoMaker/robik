import os,sys
try:
    import json
except ImportError:
    import simplejson as json

class Settings(dict):
    """Very simple json config file"""
    def __init__(self, path='config.json'):
        CONFIG_PATH = os.path.join(sys.path[0], path)
        dict.__init__(self)
        self.path = path

        try:
            self.load()
        except:
            print "Creando fichero de configuracion"
            self['hs_threshold1'] = 100
            self['hs_threshold2'] = 200
            self['hs_apertura'] = 1
            self['hs_blur'] = 3
            self['hs_minLineLength'] = 100
            self['hs_maxLineGap'] = 10
            self['hs_kernel_dilate'] = 3
            self['hs_kernel_erode'] = 3
            self['hs_param1'] = 3
            self['hs_param2'] = 3
            self['hs_param3'] = 3
            self['hs_dilate_iteracciones'] = 1

            self.save()

    def load(self):
        with open(self.path, "rb") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
        self.clear()
        self.update(data)

    def save(self):
        print "Grabando..."
        with open(self.path, "wb") as f:
            json.dump(self, f, indent=4)


class SettingsDialog:
    """This class is used to show wineDlg"""

    def __init__(self, dlg):
        self.dlg = dlg
        self.gladefile = "glade1.glade"
        #setup the wine that we will return
        self.settings = Settings()
        self.widgets = {}

    def showSettings():
        result = gtk.RESPONSE_CANCEL

        wTree = gtk.glade.XML(self.gladefile)
        dlg = wTree.get_widget("dialog_settings")

        #Get all of the Entry Widgets and set their text
        valores = ['hs_threshold1','hs_threshold2','hs_apertura','hs_blur']

        for w in valores:
            widget = wTree.get_widget(w)
            widget.set_value(settings[w])

        #run the dialog and store the response
        result = dlg.run()
        if (result==gtk.RESPONSE_OK):
                #get the value of the entry fields
                print "grabaria la configuracion"

        #we are done with the dialog, destroy it
        dlg.destroy()

        #return the result
        return result
    def run(self):

        #load the dialog from the glade file
        self.wTree = gtk.glade.XML(self.gladefile)

        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("dialog_settings")

        settings_list=['hs_threshold1','hs_threshold2', \
                'hs_apertura','hs_blur']
        for s in self.settings:
            self.widget[s] = self.wTree.get_widget(s)
            self.wTree.get_widget(s).set_value(5)


"""j

hs_threshold1
hs_threshold2
hs_apertura
hs_blur
"""

"""
        #run the dialog and store the response
        self.result = self.dlg.run()
        #get the value of the entry fields
        self.wine.wine = self.enWine.get_text()
        self.wine.winery = self.enWinery.get_text()
        self.wine.grape = self.enGrape.get_text()
        self.wine.year = self.enYear.get_text()

        #we are done with the dialog, destory it
        self.dlg.destroy()

        #return the result and the wine
        return self.result,self.wine

"""

