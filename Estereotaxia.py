# -*- coding: iso-8859-1 -*-
# Estereotaxia version 17.2108

import os
import logging

from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from Recursos import Maquina_Russell_Brown

class Estereotaxia(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class"""

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Estereotaxia"
        self.parent.categories = ["Estereotaxia"]
        self.parent.dependencies = []
        self.parent.contributors = ["Dr. Miguel Ibañez; Dr. Dante Lovey; Dr. Lucas Vera; Dra. Elena Zema; Dr. Jorge Beninca."]
        self.parent.helpText = """Esta es la Versión 18.2309 """
        self.parent.acknowledgementText = """
        Este módulo fue desarrollado originalmente
        por Jorge A.Beninca, durante los meses de
        Enero a Julio 2015, en el dpto de Neurocirugía
        del Hospital de Niños Dr. Orlando Alassia.-
        """


class EstereotaxiaWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class"""
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        self.Registracion_Bton = ctk.ctkCollapsibleButton()
        self.Registracion_Bton.text = "Registración del Paciente"
        self.Registracion_Bton.collapsed = False
        self.Planificacion_Bton = ctk.ctkCollapsibleButton()
        self.Planificacion_Bton.text = "Plan de la Cirugía"
        self.Planificacion_Bton.collapsed = True

        #
        # Define Butones Layout Registracion
        #
        self.Bton1 = qt.QPushButton("Inicializa")
        self.Bton1.toolTip = "Inicia todas las variables.-"
        self.Bton1.setEnabled(True)
        self.Bton2 = qt.QPushButton("abre DICOM ")
        self.Bton2.toolTip = "Carga el volumen.-"
        self.Bton2.setEnabled(True)
        self.Bton3 = qt.QPushButton("Marca Fiduciarios")
        self.Bton3.toolTip = "Marca los 9 fiduciacios f.-"
        self.Bton3.setEnabled(True)
        self.Bton4 = qt.QPushButton("Marca Target")
        self.Bton4.toolTip = "Marca el fiduciario Target y realiza los cálculos.-"
        self.Bton4.setEnabled(True)

        self.Bton5 = qt.QPushButton("Volumen")
        self.Bton5.toolTip = "Visibiliza el volumen 3D"
        self.Bton6 = qt.QPushButton("N-Locadores")
        self.Bton6.toolTip = "Visibiliza los Localizadores N"
        self.Bton7 = qt.QPushButton("Fantasma")
        self.Bton7.toolTip = "Visibiliza Marco Micromar"
        self.Bton8 = qt.QPushButton("Arco")
        self.Bton8.toolTip = "Visibiliza el Arco"
        self.mensa = qt.QLabel("Mensajes...")
        self.etiqueta_v = qt.QLabel("Visualiza :")

        #
        #  Define widgets del Layout Planificacion
        #
        self.etiqueta_x = qt.QLabel(" Target x :")
        self.Sli_x = ctk.ctkSliderWidget()
        self.Sli_x.singleStep = 0.5
        self.Sli_x.minimum = -150
        self.Sli_x.maximum = 150
        self.Sli_x.setToolTip("Establece el valor del desplazamiento en el eje X (positivo a la derecha).")
        cajita_x = qt.QHBoxLayout()
        cajita_x.addWidget(self.etiqueta_x)
        cajita_x.addWidget(self.Sli_x)

        self.etiqueta_y = qt.QLabel(" Target y :")
        self.Sli_y = ctk.ctkSliderWidget()
        self.Sli_y.singleStep = 0.5
        self.Sli_y.minimum = -150
        self.Sli_y.maximum = 150
        self.Sli_y.setToolTip("Establece el valor del desplazamiento en el eje Y (+ hacia adelante).")
        cajita_y = qt.QHBoxLayout()
        cajita_y.addWidget(self.etiqueta_y)
        cajita_y.addWidget(self.Sli_y)

        self.etiqueta_z = qt.QLabel(" Target z :")
        self.Sli_z = ctk.ctkSliderWidget()
        self.Sli_z.singleStep = 0.5
        self.Sli_z.minimum = -150
        self.Sli_z.maximum = 150
        self.Sli_z.setToolTip("Establece el valor del desplazamiento en el eje Z (+ hacia arriba).")

        cajita_z = qt.QHBoxLayout()
        cajita_z.addWidget(self.etiqueta_z)
        cajita_z.addWidget(self.Sli_z)

        cajita_Target = qt.QHBoxLayout()

        self.etiqueta_f = qt.QLabel("arco a la derecha  :  ")
        self.etiqueta_g = qt.QLabel("        ")
        self.flag_Der_Izq = qt.QCheckBox()
        self.flag_Der_Izq.setToolTip("Si esta marcada, el arco estara a la derecha, sino a la izquierda.")

        self.etiqueta_a = qt.QLabel("ángulo Alfa")
        self.spin_a = qt.QSpinBox()
        self.spin_a.setToolTip("Establece el valor del angulo Alfa.")
        self.spin_a.minimum = 0
        self.spin_a.maximum = 180
        self.spin_a.setMaximumWidth(50)
        self.dial_a = qt.QDial()
        self.dial_a.setNotchesVisible(1)
        self.dial_a.setMinimumSize(100, 100)

        self.etiqueta_b = qt.QLabel("ángulo Beta")
        self.spin_b = qt.QSpinBox()
        self.spin_b.setToolTip("Establece el valor del angulo Beta.")
        self.spin_b.setMaximumWidth(50)
        self.spin_b.minimum = 0
        self.spin_b.maximum = 110
        self.dial_b = qt.QDial()
        self.dial_b.setNotchesVisible(1)
        self.dial_b.setMinimumSize(100, 100)

        cajita_Mensa = qt.QHBoxLayout()
        #cajita_Mensa.addWidget(self.mensa)

        cajita_Grilla1 = qt.QGridLayout()
        cajita_Grilla1.addWidget(self.etiqueta_g, 0, 2)
        cajita_Grilla1.addWidget(self.etiqueta_g, 0, 3)
        cajita_Grilla1.addWidget(self.etiqueta_f, 0, 0)
        cajita_Grilla1.addWidget(self.flag_Der_Izq, 0, 1)

        cajita_Grilla = qt.QGridLayout()
        cajita_Grilla.addWidget(self.etiqueta_a, 1, 0)
        cajita_Grilla.addWidget(self.spin_a, 2, 1)
        cajita_Grilla.addWidget(self.dial_a, 2, 0)
        cajita_Grilla.addWidget(self.etiqueta_b, 1, 2)
        cajita_Grilla.addWidget(self.spin_b, 2, 3)
        cajita_Grilla.addWidget(self.dial_b, 2, 2)

        cajita_1 = qt.QGridLayout()
        cajita_1.addWidget(self.etiqueta_v, 0, 0)

        cajita_1.addWidget(self.Bton5, 1, 0)
        cajita_1.addWidget(self.Bton6, 1, 1)
        cajita_1.addWidget(self.Bton7, 1, 2)
        cajita_1.addWidget(self.Bton8, 1, 3)

        Layout1 = qt.QGridLayout(self.Registracion_Bton)
        Layout1.addWidget(self.Bton1, 0, 0)
        Layout1.addWidget(self.Bton2, 0, 1)
        Layout1.addWidget(self.Bton3, 1, 0)
        Layout1.addWidget(self.Bton4, 1, 1)

        Layout2 = qt.QVBoxLayout(self.Planificacion_Bton)
        Layout2.addLayout(cajita_Grilla1)
        Layout2.addLayout(cajita_x)
        Layout2.addLayout(cajita_y)
        Layout2.addLayout(cajita_z)
        Layout2.addLayout(cajita_Target)
        Layout2.addLayout(cajita_Grilla)
        Layout2.addLayout(cajita_1)

        self.layout.addWidget(self.Registracion_Bton)
        self.layout.addWidget(self.Planificacion_Bton)
        self.layout.addStretch(1)   # Add vertical spacer

        #
        # conexiones botones con funciones
        #
        self.Registracion_Bton.clicked.connect(lambda: self.collapse1())
        self.Planificacion_Bton.clicked.connect(lambda: self.collapse2())
        self.Bton1.clicked.connect(lambda: self.lectora_botones("inicio"))
        self.Bton2.clicked.connect(lambda: self.lectora_botones("dicom"))
        self.Bton3.clicked.connect(lambda: self.lectora_botones("9_fidu"))
        self.Bton4.clicked.connect(lambda: self.lectora_botones("target"))

        self.Bton5.clicked.connect(lambda: self.visibilidad_modelos("toggle", "Volumen"))
        self.Bton6.clicked.connect(lambda: self.visibilidad_modelos("toggle", "N_Locators",))
        self.Bton7.clicked.connect(lambda: self.visibilidad_modelos("toggle", "Fantasma_Modelo"))
        self.Bton8.clicked.connect(lambda: self.visibilidad_modelos("toggle", "Arco"))

        #
        # sliders controlando desplazamientos y ángulos
        #
        self.Sli_x.valueChanged.connect(lambda: self.onCambioSliders())
        self.Sli_y.valueChanged.connect(lambda: self.onCambioSliders())
        self.Sli_z.valueChanged.connect(lambda: self.onCambioSliders())
        self.flag_Der_Izq.stateChanged.connect(lambda: self.onCambioSliders())
        self.spin_a.valueChanged.connect(lambda: self.onCambioSliders())
        self.spin_b.valueChanged.connect(lambda: self.onCambioSliders())

        self.dial_a.valueChanged.connect(lambda: self.onCambioDialValores())
        self.dial_b.valueChanged.connect(lambda: self.onCambioDialValores())

        self.lectora_botones("inicio")
        #logic.Inicializa_Escena()

        # -------------------------------------------------------

    def lectora_botones(self, modo):
        logic = registracionLogic()
        if modo == "inicio":
            #slicer.mrmlScene.Clear(0)
            logic.Inicializa_Escena()
            self.inicializaControles()
            self.Bton2.setEnabled(True)
            self.Bton3.setEnabled(False)
            self.Bton4.setEnabled(False)
            self.Planificacion_Bton.setEnabled(False)
        elif modo == "dicom":
            logic.Abre_Dicom()
            self.Bton3.setEnabled(True)
        elif modo == "9_fidu":
            logic.Marcacion_9_Fiduciarios()
            self.mensa.text = "marcando fiduciarios ..."
            self.Planificacion_Bton.setEnabled(True)
            self.Bton4.setEnabled(True)
            self.inicializaControles()
        elif modo == "target":
            logic.Marcacion_1_Fiduciario()

    def collapse1(self):
        if not self.Planificacion_Bton.isEnabled():
            print "No esta habilitado el botón.-"
            self.Registracion_Bton.collapsed = False
            return False
        if self.Registracion_Bton.collapsed:
            self.onCambioTarget()
            self.Planificacion_Bton.collapsed = False
            self.Establece_Escena_3D(True)
        else:
            self.Planificacion_Bton.collapsed = True
            self.Establece_Escena_3D(False)

    def collapse2(self):
        if self.Planificacion_Bton.collapsed:
            self.Registracion_Bton.collapsed = False
            self.Establece_Escena_3D(False)
        else:
            self.onCambioTarget()
            self.Registracion_Bton.collapsed = True
            self.Establece_Escena_3D(True)

    def onCambioSliders(self):
        target_x = self.Sli_x.value
        target_y = self.Sli_y.value
        target_z = self.Sli_z.value
        der_izq = self.flag_Der_Izq.checked
        ang_Alfa = -self.spin_a.value + 90  # el valor del spin es el que define
        ang_Beta = -self.spin_b.value       # y no el dial
        texto = "Target =  " + \
                str(round(target_x, 1)) + ",  " +\
                str(round(target_y, 1)) + ",  " +\
                str(round(target_z, 1))
        self.Establece_Isocentro_y_Arco(target_x, target_y, target_z, der_izq, ang_Alfa, ang_Beta)
        node = slicer.util.getNode("Target")
        node.SetNthFiducialPosition(0, target_x, target_y,  target_z)
        self.anota_esquina_3D(texto)
        utilitarios().impri_layout_markup(texto)

    def inicializaControles(self):
        self.Sli_x.value = 0
        self.Sli_y.value = 0
        self.Sli_z.value = 0
        self.flag_Der_Izq.checked = 1
        self.spin_a.value = 90
        self.dial_a.value = int(self.spin_a.value * 100 / 180)
        self.spin_b.value = 45
        self.dial_b.value = int(self.spin_b.value * 100 / 110)
        # self.onCambioSliders()  # no es necesario, va por simple cambio

    def onCambioTarget(self):
        fidu_node = slicer.util.getNode("Target")
        if fidu_node.GetNumberOfFiducials() != 1:
            print "No se ha encontrado un fiduciario"
            return False
        T_coord = fidu_node.GetNthMarkupLabel(0)
        T_descri = fidu_node.GetNthMarkupDescription(0)
        print "Estas son las T coordenadas que se grafican :"
        print T_descri, T_coord
        T_coord = T_coord.lstrip("[").rstrip("]")
        self.Sli_x.value = float(T_coord.split(',')[0])
        self.Sli_y.value = float(T_coord.split(',')[1])
        self.Sli_z.value = float(T_coord.split(',')[2])
        if self.Sli_x.value < 0:
            self.flag_Der_Izq.checked = False
        else:
            self.flag_Der_Izq.checked = True
        # self.onCambioSliders()  # no es necesario, va por simple cambio

    def onCambioDialValores(self):
        self.spin_a.value = int(self.dial_a.value * 180 / 100)
        self.spin_b.value = int(self.dial_b.value * 110 / 100)

    def onCambioSpinValores(self):
        # el paso al dial se hace desde spin
        self.dial_a.value = int(self.spin_a.value * 100 / 180)
        self.spin_b.value = int(self.dial_b.value * 110 / 100)

    def Establece_Escena_3D(self, set_On):
        lay = slicer.app.layoutManager()
        volu_nombre = utilitarios().obtiene_nodo("Red").GetName()
        if not volu_nombre:
            print "Error: no hay volumen cargado"
            return False
        if set_On:
            #logic.Registracion_de_Nodo(set_On, volu_nombre)
            #logic.Registracion_de_Nodo(set_On, "f")
            #logic.Registracion_de_Nodo(set_On, "Target")
            lay.setLayout(4)  # panel 3D
        if not set_On:
            #logic.Registracion_de_Nodo(set_On, volu_nombre)
            #logic.Registracion_de_Nodo(set_On, "f")
            #logic.Registracion_de_Nodo(set_On, "Target")
            lay.setLayout(6)  # panel RED

    def Establece_Isocentro_y_Arco(self, target_x, target_y, target_z, der_izq, ang_alfa, ang_beta):
        """ modifica las transformadas de la escena 3D para el arco y la aguja de puncion.-"""
        lay = slicer.app.layoutManager()
        #lay.setLayout(4)  # abre el panel 3D

        transfo_0 = vtk.vtkTransform()
        if der_izq != 1:  # coloca el arco a la izquierda
            transfo_0.RotateZ(180)
        # print transfo_0.GetMatrix()
        node_0 = slicer.util.getNode('Transformada_Der_Izq')
        node_0.SetMatrixTransformToParent(transfo_0.GetMatrix())

        transfo_1 = vtk.vtkTransform()
        transfo_1.Translate(target_x, target_y, target_z)
        node_1 = slicer.util.getNode('Transformada_Isocentro')
        node_1.SetMatrixTransformToParent(transfo_1.GetMatrix())

        transfo_2 = vtk.vtkTransform()
        if der_izq:
            transfo_2.RotateX(ang_alfa)
        else:
            transfo_2.RotateX(-ang_alfa)
        # print transfo_2.GetMatrix()
        node_2 = slicer.util.getNode('Transformada_angulo_Alfa')
        node_2.SetMatrixTransformToParent(transfo_2.GetMatrix())

        transfo_3 = vtk.vtkTransform()
        transfo_3.RotateY(ang_beta)
        # print transfo_3.GetMatrix()
        node_3 = slicer.util.getNode('Transformada_angulo_Beta')
        node_3.SetMatrixTransformToParent(transfo_3.GetMatrix())
        print
        print "Desplazamiento X, Y, Z =", target_x, ",", target_y, ",", target_z, " mm."
        if der_izq:
            print "Arco a la derecha."
        else:
            print "Arco a la izquierda."
        print "Angulo Alfa = ",   ang_alfa - 90, ", ángulo Beta = ", - ang_beta, " grados.-"

    def visibilidad_modelos(self, modo, nombre_modelo):
        if nombre_modelo == "Volumen":
            # cambia al nombre del widget RED
            logic = registracionLogic()
            nombre_modelo= logic.obtiene_nodo_RED().GetName()
            print nombre_modelo

        modelo = slicer.util.getNode(nombre_modelo)
        modelo.SetDisplayVisibility(not modelo.GetDisplayVisibility())  # invierte visibilidad
        print "Visibilidad ", nombre_modelo, ": ", bool(modelo.GetDisplayVisibility())
               

    def anota_esquina_3D(self, texto):
        lm = slicer.app.layoutManager()
        re = lm.threeDWidget(0)
        vi = re.threeDView()
        ca = vi.cornerAnnotation()
        ca.GetTextProperty().SetColor(1, 0, 0)
        ca.SetText(1, texto)


class registracionLogic(ScriptedLoadableModuleLogic):
    """Esta clase implementa todos los computos de
    registracion que requiere el modulo"""
    def __init__(self):
        pass

    def Inicializa_Escena(self):
        print "--------------------------------------------------------"
        print "clear Scene e Inicializa"
        print "--------------------------------------------------------"
        slicer.mrmlScene.Clear(0)
        modulo = slicer.util.modulePath("Estereotaxia")
        moduloPath = os.path.split(modulo)
        moduloPath = moduloPath[0]
        print "Path del módulo en uso:", moduloPath

        lay = slicer.app.layoutManager()
        lay.setLayout(4)  # panel 3D
        slicer.util.loadScene(moduloPath + "/Espacio Marco/_Marco_Scene.mrml")
        slicer.util.resetThreeDViews()

        """
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
        """

    def Abre_Dicom(self):
        lay = slicer.app.layoutManager()
        lay.setLayout(6)  # RED panel
        dw = slicer.modules.dicom.widgetRepresentation().self()
        dw.detailsPopup.open()
        print "Carga volumen del paciente"

    def Marcacion_9_Fiduciarios(self):

        targ_node = slicer.util.getNode("Target")
        targ_node.RemoveAllMarkups()

        fidu_node = slicer.util.getNode("F")
        fidu_node.RemoveAllMarkups()

        util = utilitarios()
        volu_nombre = util.obtiene_nodo("Red").GetName()
        self.Registracion_de_Nodo(False, volu_nombre)
        self.Registracion_de_Nodo(False, "F")
        self.Registracion_de_Nodo(False, "Target")
        util.cambia_window_level("Red")
        util.centra_nodo("Red")
        #self.Callback_Main()
        #return

        gest = gestion_Fiduciarios()
        gest.nombre_Nodo = "F"
        gest.total_de_Fiduciarios = 9
        gest.Marcacion_Fiduciarios()

    def Marcacion_1_Fiduciario(self):
        """
        if slicer.util.getNode("F") is None:
            print "Error, no se han marcado los fiduciarios.-"
            return False
        """
        targ_node = slicer.util.getNode("Target")
        """
        if targ_node is None:
            print "Genera el nodo Target.-"
            targ_node = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMarkupsFiducialNode')
            targ_node.SetName("Target")
            targ_node.SetScene(slicer.mrmlScene)
            slicer.mrmlScene.AddNode(targ_node)
        """

        targ_node.RemoveAllMarkups()
        util = utilitarios()
        util.cambia_window_level("Red")
        gest = gestion_Fiduciarios()
        gest.nombre_Nodo = "Target"
        gest.total_de_Fiduciarios = 1
        gest.Marcacion_Fiduciarios()

    def Callback_Main(self):
        gest = gestion_Fiduciarios()
        reload(Maquina_Russell_Brown)
        maqui = Maquina_Russell_Brown
        util = utilitarios()

        if slicer.util.getNode("Target").GetNumberOfFiducials() == 0:
            # no ha marcado el fidu Target aún
            print "Este es el proceso de Registracion"
            gest.nombre_Nodo = "F"
            fiduciarios_TAC = gest.Lectura_Fiduciarios()
            print "fiduciarios_TAC : "
            print fiduciarios_TAC
            matriz_RB = maqui.Ecuaciones_Russell_Brown(fiduciarios_TAC)
            print "matriz_RB = ", matriz_RB
            print
            fiduciarios_3D = maqui.Multiplica_puntos(fiduciarios_TAC, matriz_RB)
            print "fiduciarios_3D :  "
            print fiduciarios_3D
            print
            print "Esta es la matriz de analisis 4, LT"
            matrix4 = maqui.Analisis_por_vtk_4(
                        fiduciarios_TAC,
                        fiduciarios_3D)
            transfo4 = vtk.vtkTransform()
            transfo4.SetMatrix(matrix4)
            #print transfo4
            print "Posicion ", transfo4.GetPosition()
            print "Orientation", transfo4.GetOrientation()
            fiduciarios_3D_rotados = maqui.Transforma_puntos(
                        fiduciarios_TAC,
                        transfo4)
            print "Calculo del traslado"
            trasla = maqui.promedio_puntos(
                        fiduciarios_3D_rotados,
                        [1, 3, 7, 9])
            centroi = maqui.promedio_puntos(
                        fiduciarios_3D,
                        [1, 3, 7, 9])
            print "trasla : ", trasla
            print "centroides : ", centroi
            print "transformada rotada y trasla:"
            matrix4.SetElement(0, 3, - trasla[0])
            matrix4.SetElement(1, 3, - trasla[1])
            matrix4.SetElement(2, 3, - trasla[2] + centroi[2])
            transfo4.SetMatrix(matrix4)
            fidu_proyec = maqui.Transforma_puntos(
                        fiduciarios_TAC,
                        transfo4)
            print "Posicion ", transfo4.GetPosition()
            print "Orientation", transfo4.GetOrientation()
            print "fiduciarios proyectados :"
            print fidu_proyec
            print "######################################"
            self.Registracion_all(transfo4)
        else:
            print "Esto es Callback Gestion Fiduciario Target.-"
            print
            gest.nombre_Nodo = "Target"
            # el segundo término se elige:
            target_TAC = gest.Lectura_Fiduciarios()[1]
            print "Punto leído raw (Target TAC) : ", target_TAC
            Target = target_TAC
            print "Target corregido (sin cambios) : ", Target
            util.impri_layout_markup(str(Target))
            util.impri_layout_2D("Red", "Target = " + str(Target))

    def Registracion_all(self, transfo):
            util = utilitarios()
            self.Registracion_Transformada(transfo)
            volu_nombre = util.obtiene_nodo("Red").GetName()
            self.Registracion_de_Nodo(True, volu_nombre)
            self.Registracion_de_Nodo(True, "F")
            util.centra_nodo("Red")
            self.Renderizacion_del_Volumen(volu_nombre)

    def Registracion_Transformada(self, transfo):
        T_node = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        T_node.SetAndObserveTransformToParent(transfo)
        print "Se ha transferido vtkMatriz a Nodo Trasformada del Volumen.-"


    def Registracion_de_Nodo(self, set_On, nombre_nodo_volu):
        node_transfo_correct = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        if set_On:
            volu = slicer.util.getNode(nombre_nodo_volu)
            volu.SetAndObserveTransformNodeID(node_transfo_correct.GetID())
            print "Se ha registrado el nodo : ",
        if not set_On:
            volu = slicer.util.getNode(nombre_nodo_volu)
            volu.SetAndObserveTransformNodeID(None)
            print "Se ha UN-registrado el nodo : ",
        print volu.GetName()

    def Renderizacion_del_Volumen(self, volu_nombre):
        volu = slicer.util.getNode(volu_nombre)
        render_logic = slicer.modules.volumerendering.logic()
        display_node = render_logic.CreateVolumeRenderingDisplayNode()
        slicer.mrmlScene.AddNode(display_node)
        display_node.UnRegister(render_logic)
        render_logic.UpdateDisplayNodeFromVolumeNode(display_node, volu)
        volu.AddAndObserveDisplayNodeID(display_node.GetID())

        # generacion de la funcion de transparencia
        property_node = display_node.GetVolumePropertyNode()
        volu_property = property_node.GetVolumeProperty()
        opaci = volu_property.GetScalarOpacity()
        opaci.RemoveAllPoints()
        opaci.AddPoint(-700, 0)
        opaci.AddPoint(-150, 0)
        opaci.AddPoint(200, 0)
        opaci.AddPoint(500, 0.1)
        volu_property.Modified()
        print "Se ha completado la renderización del : ",  volu.GetName()

    def obtiene_nodo_RED(self):
        lay = slicer.app.layoutManager()
        red_logic = lay.sliceWidget("Red").sliceLogic()
        red_cn = red_logic.GetSliceCompositeNode()
        red_volu_ID = red_cn.GetBackgroundVolumeID()
        if not red_volu_ID:
            return None
        volu_node = slicer.mrmlScene.GetNodeByID(red_volu_ID)
        return volu_node

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
        if self.nombre_Nodo == "F":
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
        """callback de evaluacion de cada fiduciario luego de marcado"""
        fidu_node = slicer.util.getNode(self.nombre_Nodo)
        fidu_nume = fidu_node.GetNumberOfFiducials()
        print "Se ha generado Fiducial # ", self.nombre_Nodo, fidu_nume
        if self.nombre_Nodo == "F":
            #corrige el fiduciario al centroide
            util = utilitarios()
            util.obtiene_Centroide(fidu_nume-1, 20)

        if fidu_node.GetNumberOfFiducials() == self.total_de_Fiduciarios:
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
        """ Cambia el color y contraste de la TAC de slice RED"""
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
        fidu_nodo = slicer.util.getNode('F')

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

