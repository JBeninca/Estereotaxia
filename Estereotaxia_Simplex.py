# -*- coding: iso-8859-1 -*-
# Estereotaxia_Simplex version 16.1206

import logging
import os

from __main__ import qt, ctk, slicer, vtk
from slicer.ScriptedLoadableModule import *
from Recursos import Maquina_Russell_Brown


class Estereotaxia_Simplex(ScriptedLoadableModule):
    """ Este modulo calcula en el mismo plano de un corte
    tomografico, los 9 fiduciarios y el Target. Usa solamente
    las ecuaciones de Russel Brown para la determinación 3D de un
    sistema de localizadores N de un marco Micromar
    """


    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Estereotaxia_Simplex"
        self.parent.categories = ["Estereotaxia"]
        self.parent.dependencies = []
        self.parent.contributors = ["Dr. Miguel Ibañez; Dr. Dante Lovey; Dr. Lucas Vera; Dra. Elena Zemma; Dr. Jorge Beninca."]
        self.parent.helpText = ("    1- Inicializar cargando el espacio-marco Micromar.-"
                                "    2- Cargar la TAC con fiduciales"
                                "    3- Utilizar el corte axial en el slice Rojo.-"
                                "    4- Marcar los 9 puntos fiduciales comenzando por posterior/derecha (RAS)."
                                "    5 -Leer los datos del punto Target. El resultado, registrado para esa imagen, se leerá a la derecha del punto y en la esquina inferior a la derecha del slice"
                                "    ")
        self.parent.acknowledgementText = "Este módulo fue desarrollado por Dr. Jorge Beninca del Servicio de Neurocirugía del Hospital Alassia de Santa Fe, durante Enero/Julio de 2015.- version 18.2309"


class Estereotaxia_SimplexWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available
    """
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.Registracion_Bton = ctk.ctkCollapsibleButton()
        self.Registracion_Bton.text = "Registración y cálculo del Target"
        self.layout.addWidget(self.Registracion_Bton)
        self.Grilla1 = qt.QGridLayout(self.Registracion_Bton)

        self.Bton1 = qt.QPushButton("Inicializa")
        self.Bton1.toolTip = "Inicia todas las variables.-"
        self.Bton1.setEnabled(True)
        self.Bton2 = qt.QPushButton("abre DICOM ")
        self.Bton2.toolTip = "Carga el volumen.-"
        self.Bton3 = qt.QPushButton("Marca Fiduciarios")
        self.Bton3.toolTip = "Marca los 9 fiduciacios f.-"
        self.Bton4 = qt.QPushButton("Marca Target")
        self.Bton4.toolTip = "Marca el fiduciario Target y realiza los cálculos.-"

        self.Grilla1.addWidget(self.Bton1, 0, 0)
        self.Grilla1.addWidget(self.Bton2, 0, 1)
        self.Grilla1.addWidget(self.Bton3, 1, 0)
        self.Grilla1.addWidget(self.Bton4, 1, 1)
        self.layout.addStretch(1)   # Add vertical spacer
        #
        # conecciones con las clases lógicas
        #
        self.Bton1.clicked.connect(lambda: self.lectora_botones("inicio"))
        self.Bton2.clicked.connect(lambda: self.lectora_botones("dicom"))
        self.Bton3.clicked.connect(lambda: self.lectora_botones("9_fidu"))
        self.Bton4.clicked.connect(lambda: self.lectora_botones("target"))

        self.lectora_botones("inicio")  # inicializa

    def lectora_botones(self, modo):
        logic = registracionLogic()
        if modo == "inicio":
            logic.Inicializa_Escena()
            self.Bton2.setEnabled(True)
            self.Bton3.setEnabled(False)
            self.Bton4.setEnabled(False)
        elif modo == "dicom":
            logic.Abre_Dicom()
            self.Bton3.setEnabled(True)
        elif modo == "9_fidu":
            logic.Marcacion_9_Fiduciarios()
            self.Bton4.setEnabled(True)
        elif modo == "target":
            logic.Marcacion_1_Fiduciario()


class registracionLogic(ScriptedLoadableModuleLogic):
    """Esta clase implemtenta todos los cómputos de
    registración y cálculo que requiere el modulo"""
    def __init__(self):
        pass

    def Inicializa_Escena(self):
        print "------------------------------------------------"
        print "clear Scene e Inicializa una sesion"
        print "------------------------------------------------"
        slicer.mrmlScene.Clear(0)
        modulo = slicer.util.modulePath("Estereotaxia_Simplex")
        moduloPath = os.path.split(modulo)
        moduloPath = moduloPath[0]
        lay = slicer.app.layoutManager()
        lay.setLayout(6)  # RED panel
        print "modulo path en uso:", moduloPath

        print "Genera el nodo Target.-"
        targ_node = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMarkupsFiducialNode')
        targ_node.SetName("Target")
        targ_node.SetScene(slicer.mrmlScene)
        slicer.mrmlScene.AddNode(targ_node)

        print "Genera el nodo Fiduciarios.-"
        fidu_node = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMarkupsFiducialNode')
        fidu_node.SetName("F")
        fidu_node.SetScene(slicer.mrmlScene)
        slicer.mrmlScene.AddNode(fidu_node)

    def Abre_Dicom(self):
        lay = slicer.app.layoutManager()
        lay.setLayout(6)  # RED panel
        dw = slicer.modules.dicom.widgetRepresentation().self()
        dw.detailsPopup.open()
        print "Carga volumen del paciente"

    def Marcacion_9_Fiduciarios(self):
        print "vino a marcacion de 9 fiduciarios"
        targ_node = slicer.util.getNode("Target")
        targ_node.RemoveAllMarkups()

        fidu_node = slicer.util.getNode("F")
        fidu_node.RemoveAllMarkups()

        utilitarios().cambia_window_level("Red")
        gest = gestion_Fiduciarios()
        gest.nombre_Nodo = "F"
        gest.total_de_Fiduciarios = 9
        gest.Marcacion_Fiduciarios()

    def Marcacion_1_Fiduciario(self):
        targ_node = slicer.util.getNode("Target")
        targ_node.RemoveAllMarkups()

        utilitarios().cambia_window_level("Red")
        gest = gestion_Fiduciarios()
        gest.nombre_Nodo = "Target"
        gest.total_de_Fiduciarios = 1
        gest.Marcacion_Fiduciarios()

    def Callback_Main(self):
        gest = gestion_Fiduciarios()
        reload(Maquina_Russell_Brown)
        maqui = Maquina_Russell_Brown

        # chequea si Target no tiene fiducia entonces fue f
        if slicer.util.getNode("Target").GetNumberOfFiducials() == 0:
            print "Esto es Callback Gestion Fiduciarios f.-"
            print "Fiduciarios centrados.-"
            # nada que hacer
        else:
            print "Esto es Callback Gestion Fiduciario Target.-"
            gest.nombre_Nodo = "F"
            fiduciarios_TAC = gest.Lectura_Fiduciarios()
            matriz_RB = maqui.Ecuaciones_Russell_Brown(fiduciarios_TAC)
            print "matriz RB:"
            print matriz_RB
            print
            gest.nombre_Nodo = "Target"
            Target_TAC = gest.Lectura_Fiduciarios()  # toma el segundo término
            print "Raw target: ", utilitarios().redondea(Target_TAC[1], 2)
            print
            print "----------- RESOLUCION MATRICIAL --------------"
            Target = maqui.Multiplica_puntos(Target_TAC, matriz_RB)[1]
            print "Target corregido por R.Brown =", Target
            utilitarios().impri_layout_markup(str(Target))
            utilitarios().impri_layout_2D("Red", "Target = " + str(Target))


class gestion_Fiduciarios():
    """ Esta clase maneja la entrada y lectura de los fiduciarios"""
    def __init__(self):
        self.observadores_Tags = []
        self.nombre_Nodo = ""
        self.total_de_Fiduciarios = 1
        self.temporiza = qt.QTimer()

    def Lectura_Fiduciarios(self):
        logging.info("Lectura de los fiduciarios.-")
        fidu = slicer.util.getNode(self.nombre_Nodo)
        if fidu is None:
            print "Error! No encuentra el nodo ", self.nombre_Nodo
            return False
        fidu_n = fidu.GetNumberOfFiducials()
        logging.info("Total de fiduciarios: " + str(fidu_n))
        fiduciarios_TAC = [[0, 0, 0]]
        for i in range(fidu_n):  # toma los 9 primeros fidu
            ras = [0, 0, 0]
            fidu.GetNthFiducialPosition(i, ras)
            ras = [round(ras[0], 2), round(ras[1], 2), round(ras[2], 2)]
            fiduciarios_TAC.append(ras)
        # print (fiduciarios_TAC)
        return fiduciarios_TAC

    def Marcacion_Fiduciarios(self):
        volu_nodes = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLScalarVolumeNode")
        if volu_nodes < 1:  # chequea si ha sido cargado algun volumen
            print "error: no hay volumen cargado"
            return False
        lay = slicer.app.layoutManager()
        lay.setLayout(6)  # abre el panel rojo

        fidu_node = slicer.util.getNode(self.nombre_Nodo)
        fidu_node.SetLocked(False)
        if self.nombre_Nodo == "f":
            display_node = fidu_node.GetDisplayNode()
            display_node.SetGlyphType(16)
            display_node.SetColor(200, 0, 0)

        logi_node = slicer.modules.markups.logic()
        logi_node.SetActiveListID(fidu_node)
        sele_node = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
        sele_node.SetReferenceActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
        interac_node = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
        interac_node.SetPlaceModePersistence(1)
        interac_node.SetCurrentInteractionMode(1)
        self.agregaObservador()  # control por observers

    def agregaObservador(self):
        for fiducialLista in slicer.util.getNodes('vtkMRMLMarkupsFiducialNode*').values():
            tag = fiducialLista.AddObserver(fiducialLista.MarkupAddedEvent, self.onFiducialAgregado)
            self.observadores_Tags.append((fiducialLista, tag))

    def remueveObservador(self):
        for obj, tag in self.observadores_Tags:
            obj.RemoveObserver(tag)
        self.observadores_Tags = []

    def onFiducialAgregado(self, caller, event):
        """callback de evaluacion de cada fiduciario
        luego de marcado"""
        fidu_node = slicer.util.getNode(self.nombre_Nodo)
        fidu_nume = fidu_node.GetNumberOfFiducials()
        print "Se ha generado Fiducial # ", self.nombre_Nodo,fidu_nume
        if self.nombre_Nodo == "f":
            #corrige el fiduciario al centroide
            utilitarios().obtiene_Centroide(fidu_nume-1, 20)

        if fidu_nume == self.total_de_Fiduciarios:
            self.remueveObservador()
            fidu_node.SetLocked(True)
            selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
            selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
            interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
            interactionNode.SetPlaceModePersistence(0)
            interactionNode.SetCurrentInteractionMode(0)
            # es necesario este retardo en la marcacion
            # del ultimo fidu y esperarlo para que sea visible.
            logic = registracionLogic()
            self.temporiza.singleShot(100, logic.Callback_Main)
            print "Se termina de registrar el/los fiduciarios"

class utilitarios():
    """ Esta clase es utilitarios"""
    def __init__(self):
        pass

    def cambia_window_level(self, widget):
        # Cambia el color y contraste de la TAC de slice RED
        lay = slicer.app.layoutManager()
        red_logic = lay.sliceWidget(widget).sliceLogic()
        red_cn = red_logic.GetSliceCompositeNode()
        red_volu_ID = red_cn.GetBackgroundVolumeID()
        volu_node = slicer.util.getNode(red_volu_ID)
        display_node = volu_node.GetDisplayNode()
        display_node.AutoWindowLevelOff()
        window = 100
        level = 50
        display_node.SetWindowLevel(window, level)
        print "Establecimiento de window & level a :", window, level

    def centra_nodo(self, widget):
        node = slicer.app.layoutManager().sliceWidget(widget)
        node.sliceLogic().FitSliceToAll()
        print "Se ha centrado el nodo: ", widget

    def obtiene_nodo(self, widget):
        print "obtiene nodo", widget
        lay = slicer.app.layoutManager()
        logic = lay.sliceWidget(widget).sliceLogic()
        cn = logic.GetSliceCompositeNode()
        volu_ID = cn.GetBackgroundVolumeID()
        if not volu_ID:
            return None
        volu_node = slicer.mrmlScene.GetNodeByID(volu_ID)
        return volu_node

    def obtiene_Centroide(self, fidu_nume, roi_size):
        """ calcula con un filtro sobre la intensidad,
        el centroide de cada fiduciario"""
        volu_nodo = self.obtiene_nodo("Red")
        fidu_nodo = slicer.util.getNode('f')

        matri = vtk.vtkMatrix4x4()
        volu_nodo.GetRASToIJKMatrix(matri)
        # obtiene el fiduciario reciente y lo transforma de IJK
        RAS_fidu = [0, 0, 0]
        fidu_nodo.GetNthFiducialPosition(fidu_nume, RAS_fidu)
        IJK_fidu = matri.MultiplyPoint(tuple(RAS_fidu) + (1,))
        IJK_fidu = IJK_fidu[:3]
        print fidu_nume, RAS_fidu, IJK_fidu

        # establece un cuadrado ROI
        roi_left = int(round((IJK_fidu[0]-(roi_size/2)), 0))
        roi_up = int(round((IJK_fidu[1]-(roi_size/2)), 0))
        print "roi bordes: ", roi_left, roi_up

        # obtencion del array del volumen
        z = int(IJK_fidu[2])
        array_volumen = slicer.util.array(volu_nodo.GetName())
        array_plano = array_volumen[z]
        # print "plano roi", roi_plano
        centroid_x = 0.0
        centroid_y = 0.0
        cuenta = 0
        for x in range(roi_size):
            for y in range(roi_size):
                esca = array_plano[roi_up + y, roi_left + x]
                if esca > -200:   # filtro de intensidad
                    # print y, x, esca
                    # obtención de los centroides por promedio
                    centroid_x += roi_left + x
                    centroid_y += roi_up + y
                    cuenta += 1
        if cuenta is not 0:
            centroid_x /= cuenta
            centroid_y /= cuenta
            print "cuenta", cuenta
            print "centroides:", centroid_x, centroid_y
            #print roi_left + centroid_x, roi_up + centroid_y, z
            IJK_corregido = [centroid_x,
                             centroid_y,
                             z]
        else:
            print "error en la determinacion del fidu"
            IJK_corregido = [0, 0, 0]

        # transformacion a sistema RAS
        matri2 = vtk.vtkMatrix4x4()
        volu_nodo.GetIJKToRASMatrix(matri2)
        RAS_fidu_correg = matri2.MultiplyPoint(tuple(IJK_corregido) + (1,))
        print RAS_fidu_correg[:3]

        # modificación de la posición del fiduciario
        fidu_nodo.SetNthFiducialPosition(
                    fidu_nume,
                    RAS_fidu_correg[0],
                    RAS_fidu_correg[1],
                    RAS_fidu_correg[2])
        return RAS_fidu_correg

    def impri_layout_markup(self, texto):
        # inscribe en slice
        fidu_node = slicer.util.getNode("Target")
        fidu_node.SetNthMarkupSelected(0, False)
        fidu_node.SetNthMarkupLabel(0, texto)
        #fidu_node.SetNthMarkupDescription(0, str(arg2))

    def impri_layout_2D(self, widget, texto):
        # anotando en el modulo RED
        lm = slicer.app.layoutManager()
        re = lm.sliceWidget(widget)
        vi = re.sliceView()
        ca = vi.cornerAnnotation()
        ca.SetText(1, texto)
        vi.scheduleRender()

    def redondea(self, lista, deci):
        lista_redond = []
        for item in lista:
            lista_redond.append(round(item, deci))
        return lista_redond