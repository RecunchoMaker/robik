DEFAULT_CAMERA=0

import cv2
import numpy as np
import colorsys
import time
import random


class Scanner(object):

    """Docstring for Scanner. """

    def __init__(self, cubo, settings):
        """TODO: to be defined1. """
        self.camera_id = DEFAULT_CAMERA
        self.cap = cv2.VideoCapture(self.camera_id)
        self.settings = settings

        self.cubo = cubo
        self.lastmov = 0
        self.lastmovtam = 1
        self.status = ""

        self.reset()

    def reset(self):
        self.activo = False

        self.escaneando = False

        self.next_frame_ready = False

        self.index = 0

        # Calculo de las coordenadas de los rois
        self.roitamano = 25
        self.rejillax = 65
        self.rejillay = 52 
        self.centrox = (320-(self.rejillax/2))/2
        self.centroy = (200-(self.rejillay/2))/2
        self.lastmov = 0
        self.roi = []
        for y in xrange(-1,2):
            for x in xrange(-1,2):
                self.roi.append([self.centrox+x*self.rejillax,self.centroy+y*self.rejillay])

        self.colors = []
        self.colorsant = []
        self.frames_buenos = 0

    def get_color_medio(self, roi, a,b,imprimir = False):
        xl,yl,ch = roi.shape
        roiyuv = cv2.cvtColor(roi,cv2.COLOR_RGB2YUV)
        roihsv = cv2.cvtColor(roi,cv2.COLOR_RGB2HSV)
        h,s,v=cv2.split(roihsv)
        mask=(h<5)
        h[mask]=200
        
        roihsv = cv2.merge((h,s,v))
        std = np.std(roiyuv.reshape(xl*yl,3),axis=0)
        media = np.mean(roihsv.reshape(xl*yl,3), axis=0)-60
        mediayuv = np.mean(roiyuv.reshape(xl*yl,3), axis=0)

        if std[0]<12 and std[1]<12 and std[2]<12:
        #if (std[0]<15 and std[2]<15) or ((media[0]>100 or media[0]<25) and (std[0]>10)):
            media = np.mean(roihsv.reshape(xl*yl,3), axis=0)
            # el amarillo tiene 65 de saturacion y sobre 200
            if media[1]<60: #and (abs(media[0]-30)>10):
                # blanco
                return [-10,0,0]
            else:
                return media
        else:
            return None

    def get_colores_cara(self):
        return self.colors

    def buscar_cubo(self):
        self.roi = []
        if self.lastmov == 0:
            self.centrox = self.centrox + self.lastmovtam
        elif self.lastmov == 1:
            self.centroy = self.centroy + self.lastmovtam
            self.lastmovtam = self.lastmovtam + 1
        elif self.lastmov == 2:
            self.centrox = self.centrox - self.lastmovtam
        elif self.lastmov == 3:
            self.centroy = self.centroy - self.lastmovtam
            self.lastmovtam = self.lastmovtam + 1

        self.lastmov = (self.lastmov + 1) % 4
        if self.lastmovtam > 35:

            self.frames_buenos = 0
            self.lastmov = 0
            self.lastmovtam = 1
            self.centrox = (320-(self.rejillax/2))/2
            self.centroy = (200-(self.rejillay/2))/2

        self.roi = []
        for y in xrange(-1,2):
            for x in xrange(-1,2):
                self.roi.append([self.centrox+x*self.rejillax,self.centroy+y*self.rejillay])

    def cara_ok(self):
        if len(self.colors)==9:
            self.frames_buenos = self.frames_buenos + 1
        else:
            # No va bien... buscar otra posicion
            self.frames_buenos = 0
        if self.frames_buenos>24:
            self.frames_buenos = 0
            return True
        return False


    def switch_camara(self):
        self.activo = not self.activo
        if self.activo:

            # Capturo el primer frame para quedarme con el tamano y el factor de resize

            ret,frame = self.cap.read(self.camera_id)

            self.activo = ret
            if ret:
                self.img_height, self.img_width, self.img_channels = frame.shape
                self.img_zoomx = 320.0/self.img_width
                self.img_zoomy = 200.0/self.img_height
                # Ya tengo los datos. Capturo la imagen final y me quedo con el frame
                self.captura_frame()
            else:
                self.status = "No puedo encontrar la camara"
                print "No encuentro la camara!!!!"

    """
    Filtra lineas horizontales de un tamano concreto
    """
    def filter_lines(self, lines):
        res = []
        if lines is not None:
            for x1,y1,x2,y2 in lines[0]:
                if abs(x2-x1)<5 or abs(y2-y1)<5:
                    res.append([x1,y1,x2,y2])
        self.lines=res

    def activar(self):
        self.status = "Escaneando..."
        self.activo = True

    def get_stream_nops(self):
        while self.activo:
            self.get_frame()

    def captura_cara(self):
        while True:
            captura_frame()


    def get_color(self, frame, color1, color2):
        mask = cv2.inRange(self.hsv, color1, color2)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        return res

    def draw_osd(self,frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        self.colors=[]
        for x,y in self.roi:
            ff = frame.copy()
            roi = ff[y:y+self.roitamano, x:x+self.roitamano]
            roi_color = self.get_color_medio(roi, x,y)
            if roi_color == None:
                cv2.rectangle(frame,(x, y),(x+self.roitamano,y+self.roitamano),(255,0,0),1)
            else:
                a,b,c=int(roi_color[0]), int(roi_color[1]), int(roi_color[2])
                cv2.putText(frame,str(a),(x,y), font, 0.3,(0,0,0),1)
                self.colors.append(a)
                cv2.rectangle(frame,(x, y),(x+self.roitamano,y+self.roitamano),(0,255,0),2)
        if len(self.colors)<9:
            self.buscar_cubo()
        self.colorsant = list(self.colors)

    def get_frame(self):

        ret,frame = self.cap.read(self.camera_id)
        self.frame = cv2.resize(frame,None,fx=self.img_zoomx, fy=self.img_zoomy, \
                interpolation = cv2.INTER_AREA)

        self.frame = cv2.blur(self.frame, (3,3))
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        self.colors = []
        if self.escaneando:
            self.draw_osd(self.frame)

        return self.frame

    def captura_frame(self):
        ret,frame = self.cap.read(self.camera_id)
        self.frame = cv2.resize(frame,None,fx=self.img_zoomx, fy=self.img_zoomy, \
                interpolation = cv2.INTER_AREA)

        # Si estoy escaneando, pillo las lineas
        if self.activo:
            self.get_frame()


    def exit(self):
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
            if s == sys.stdin:
                input = sys.stdin.readline()
                return True
        return False

