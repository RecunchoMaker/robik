
import threading
import time
import select
import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    pass

#gtk.gdk.threads_init()

import string



class View():
    def __init__(self,controller):

        # TODO: no me mola mucho esto

        self.gladefile = "glade1.glade"
        self.wTree = gtk.glade.XML(self.gladefile)

        self.img = None
        self.done = False
        self.thrd = None

        # Widgets
        self.win = self.wTree.get_widget("mainWindow")
        self.dlg_settings = self.wTree.get_widget("dialog_settings")
        self.img_gtk = self.wTree.get_widget("imgVideo")
        self.area = self.wTree.get_widget("drwCubo")


        self.scrolledWindow = self.wTree.get_widget("scrolledSolver")
        self.txtSolver = self.wTree.get_widget("txtSolver")
        self.txtSolverBuffer = self.txtSolver.get_buffer()

        self.win.connect("delete_event",self.leave_app)
        self.img_flag=0

        #TODO: Comprobar estas senales
        senales = { "on_camara_on_off": self.on_camara_on_off,
                    "on_salir" : self.leave_app,
                    "on_cmdSettings" : self.on_cmdSettings,
                    }

        self.wTree.signal_autoconnect(senales)

        self.gobjectid = 0

        controller.set_view(self)
        self.controller = controller

    # setters de widgets

    def appendTxtSolver(self, txt):
        if txt:
            antes = self.txtSolverBuffer.get_text(self.txtSolverBuffer.get_start_iter(),self.txtSolverBuffer.get_end_iter())
            self.setTxtSolver(antes + "\n" + txt)

    def setTxtSolver(self, txt):
        self.txtSolverBuffer.set_text(txt)
        adj = self.scrolledWindow.get_vadjustment()
        adj.set_value(adj.upper - adj.page_size)

    def setImg(self, image):
        # TODO: esto solo cambia cuando cambia la imagen
        self.img_height, self.img_width, self.img_channels = image.shape

        img_pixbuf = gtk.gdk.pixbuf_new_from_data(image.tostring(),
                                                gtk.gdk.COLORSPACE_RGB,
                                                False,
                                                8,
                                                self.img_width,
                                                self.img_height,
                                                self.img_width*self.img_channels)
        self.img_gtk.set_from_pixbuf(img_pixbuf)
        # TODO: hace falta???
        self.img_gtk.show()

    # senales

    def on_cmdSettings(self, widget):
        self.controller.showSettings()

    def on_resolver(self, widget, data=None):
        self.controller.resolver()


    def on_camara_on_off(self, widget):
        self.controller.switch_camara()

  
    def show(self):
        # TODO: update los controls que sean
        self.win.show_all()
        
    def thread_gtk(self):
        self.thrd = Thread(target=gtk.main, name = "GTK thread")
        self.thrd.daemon = True
        self.thrd.start()
    
    def leave_app(self,widget=None,data=None):
        self.controller.camara_off()
        self.done = True
        self.win.destroy()
        gtk.main_quit()

    def isDone(self):
        return self.done
    
    def quit(self):
        self.done = True
        self.win.destroy()
        gtk.main_quit()


