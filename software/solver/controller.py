from scanner import Scanner
from solver import Solver
from cubo import *
from cuboescaneado import *
from robot import *
from view import View
#from objetoredirect import ObjetoRedirect

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

import threading
import time
import cv2
import logging
from settings import *

gtk.gdk.threads_init()


class Controller(object):

    """Docstring for Controller. """

    def __init__(self, settings):
        """TODO: to be defined1. """
        self.cubo = Cubo()
        self.cuboescaneado = CuboEscaneado()
        self.settings = settings
        self.scanner = Scanner(self.cubo, self.settings)
        self.robot = Robot()
        self.solver = Solver(self.cubo)


        # camara a of (primero true y luego switch)

    def set_view(self, view):
        self.view = view
        self.view.setImg(cv2.imread('novideo.png'))
    

    def change_setting(self, widget, scroll, value):
        print "en change setting"

        print "rango ", widget.get_name()
        print "scrll ", scroll
        print "value ", value
        value = int(value)
        self.settings[widget.get_name()] = value
    def showSettings(self):
        result = gtk.RESPONSE_CANCEL
        settings = Settings()

        for w in settings:
            print w
            widget = self.view.wTree.get_widget(w)
            widget.set_value(settings[w])
            print 'on_'+w+'_change_value'
            #widget.connect('on_'+w+'_change_value', self.change_setting)            
            widget.connect('change_value', self.change_setting)            
        print "Muestro"

        #run the dialog and store the response
        result = self.view.dlg_settings.run()
        if (result==gtk.RESPONSE_OK):
            #get the value of the entry fields
            print "grabaria la configuracion"
            self.settings.save()

        elif (result==gtk.RESPONSE_CANCEL):
            print "cancelo"
            self.settings.load()
        else:
            print "Result = ",result
                

        #we are done with the dialog, destroy it
        self.view.dlg_settings.hide()

        #return the result
        return result
        

    def camara_off(self):
        self.view.setTxtSolver("Camara apagada")
        self.scanner.reset()
        time.sleep(2/24.0)   # por si esta pendiente el thread 
        self.view.setImg(cv2.imread('novideo.png'))

    def switch_camara(self):
        self.scanner.switch_camara()
        if self.scanner.activo:
            threading.Thread(target=self.scanner_thread, args=(self.scanner,)).start()
        else:
            self.camara_off()

    def resolver(self):
        if self.solver.is_running():
            logging.debug("Aguanta! Estoy en ello!")
            pass
        else:
            print self.solver
            self.solver.scramble(30)
            #obj = ObjetoRedirect(s)
            threading.Thread(target=self.resolver_thread, args=(self.solver,)).start()


    # threads
    def scanner_thread(self, scanner, data=None):
        # pillo el primer frame para no entrar en la chisma
        #self.cuboescaneado.carasescaneadas = 0
        self.robot.reset()
        scanner.reset()
        scanner.activar()

        self.view.setTxtSolver("Comienza escaneo")
        print self.scanner.activo
        while self.scanner.activo:
            self.robot.reset()
            #scanner.reset()
            print "init cubo escaneado"
            self.cuboescaneado.__init__()

            while self.cuboescaneado.carasescaneadas < 6:
                scanner.escaneando = False
                threading.Thread(target=self.robot.prepara_siguiente_cara).start()
                while not self.scanner.cara_ok():
                    scanner.escaneando = self.robot.listo
                    self.view.setImg(self.scanner.get_frame())
                    time.sleep(1/60.0) 
                    if not self.scanner.activo:
                        self.view.appendTxtSolver("Escaneo cancelado")
                        return None
                self.view.appendTxtSolver("Escaneada cara " + str(self.cuboescaneado.carasescaneadas))

                # grabar a ver que pasa:
                rgb = cv2.cvtColor(self.scanner.frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite('/tmp/cara_'+str(self.cuboescaneado.carasescaneadas)+'.jpg',rgb)

                self.cuboescaneado.anadir_colores(self.scanner.get_colores_cara())
                print self.scanner.get_colores_cara()
                time.sleep(0.1)

            self.robot.fin_escaneo()
            self.view.appendTxtSolver("Escaneo completo. Comprobando colores")
            res = self.cuboescaneado.normaliza_colores()
            self.view.appendTxtSolver(self.cuboescaneado.get_resultado())
            if res:
                break;

                time.sleep(3)

        if not self.scanner.activo:
            return None

        # Se escaneo primero la cara 2, luego la 5, luego la 4... (ver cubo.py)
        self.cubo.setColoresCara(4, self.cuboescaneado.colores_def[0],2) # right
        self.cubo.setColoresCara(5, self.cuboescaneado.colores_def[1],2) # down
        self.cubo.setColoresCara(2, self.cuboescaneado.colores_def[2],2) # left
        self.cubo.setColoresCara(1, self.cuboescaneado.colores_def[3],2) # back
        self.cubo.setColoresCara(3, self.cuboescaneado.colores_def[4],1) # front
        self.cubo.setColoresCara(0, self.cuboescaneado.colores_def[5],1) 
        self.cubo.configAdyacentes()

        print self.cubo.toStr()
        self.robot.write('init')

        #threading.Thread(target=self.resolver_thread, args=(self.solver,)).start()
        th = threading.Thread(target=self.solver.solve)
        th.start()
        while th.is_alive():
            seq = self.solver.get_secuencia()
            self.view.appendTxtSolver(self.solver.get_status())
            
            if seq:
                self.robot.write('seq ' + seq)
                print "Solver alive. Aparecio nueva sec " + seq
            time.sleep(1)
        # terminar secuencias pendientes
        print "El solver termino"

        seq = self.solver.get_secuencia()
        while seq:
            print "Quedan sequencias pendientes " + seq
            self.robot.write('seq ' + seq)
            seq = self.solver.get_secuencia()
            time.sleep(10.1)
            self.view.appendTxtSolver(self.solver.get_status())

        print "No quedan secuencias"
        self.view.appendTxtSolver("\nTerminado!\n\n")
        self.robot.write('pa')
        self.robot.write('ba 4')
        self.robot.write('pa')
        self.robot.write('ba -4')


    def resolver_thread(self, objeto, data=None):
        th = threading.Thread(target=objeto.solve)
        th.start()
        while th.is_alive():
            self.view.setTxtSolver(objeto.get_status())
            time.sleep(0.1)
        # creo que ya no existe el objeto
        self.view.setTxtSolver('Terminado')
        #self.view.setTxtSolver(objeto.get_stdout()+'Terminado')
        
if __name__ == "__main__":

    #" Fichero de configuracion
    settings = Settings("config.json")

    controller = Controller(settings)

    # Gtk.main()
    view = View(controller)
    view.show() 

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()



