# -*- coding: iso-8859-1 -*-
# Maquina_Russell_Brown version: 17.0508

import numpy
import numpy.matlib
from __main__ import vtk

""" Ecuaciones de Russell Brown para tansformacion en 3D
    (not using vtk) -

     El objetivo de este modulo es obtener la matriz de R Brown
     que permite la registracion en coordenadas 3D de un
     marco estereotaxico (Micromar) desde una imagen de TAC.
     Luego se calcula un Target en 3D en este en el mismo plano
     (en el mismo corte) en que se ha hecho la registracion.-
     """

class Marco_Micromar():
    """Clase para encapsular datos del marco MICROMAR TM-03B"""
    def __init__(self):
        pass

    # propiedades geométricas del Marco Micromar

    P0 = (0, 0, 0)

    P1 = (130, -70, 0)
    P2 = (130, -70, 0)
    P3 = (130,  70, 140)

    P4 = ( 70, 130, 140)
    P5 = (-70, 130, 0)
    P6 = (-70, 130, 0)

    P7 = (-130,  70, 140)
    P8 = (-130, -70, 0)
    P9 = (-130, -70, 0)

    P = (P0, P1, P2, P3, P4, P5, P6, P7, P8, P9)
    Pts = P
    Pall = P
    P_all = P


def Ecuaciones_Russell_Brown(fidu_TAC):
    """Resolución algebraica (maticial) con las ecuaciones d RB.
    La entrada a esta función es una lista []
    con los 9  fiduciales leídos del corte tomográfico
    y la salida es la matriz M de transformacion de RB.
    """
    print "----------- ECUACIONES RUSSELL BROWN --------------"
    m = Marco_Micromar()
    u, v, w, fr_N = fiduciarios_a_tabla(fidu_TAC)
    x, y, z = 0, 1, 2
    # calculo de los valores Z en mm.
    print "Z segun N-Locators :"
    print "Z(P2)  = ", fr_N[1] * m.P3[z]
    print "Z(P5)  = ", fr_N[2] * m.P4[z]
    print "Z(P8)  = ", fr_N[3] * m.P7[z], " mm."
    print
    F = vtk.vtkMatrix3x3()
    F.SetElement(0, 0, fr_N[1]*m.P3[x]+(1-fr_N[1])*m.P1[x])
    F.SetElement(0, 1, fr_N[1]*m.P3[y]+(1-fr_N[1])*m.P1[y])
    F.SetElement(0, 2, fr_N[1]*m.P3[z])
    F.SetElement(1, 0, fr_N[2]*m.P4[x]+(1-fr_N[2])*m.P6[x])
    F.SetElement(1, 1, fr_N[2]*m.P4[y]+(1-fr_N[2])*m.P6[y])
    F.SetElement(1, 2, fr_N[2]*m.P4[z])
    F.SetElement(2, 0, fr_N[3]*m.P7[x]+(1-fr_N[3])*m.P9[x])
    F.SetElement(2, 1, fr_N[3]*m.P7[y]+(1-fr_N[3])*m.P9[y])
    F.SetElement(2, 2, fr_N[3]*m.P7[z])

    #print "esta es F por vtk"
    #print F

    S = vtk.vtkMatrix3x3()
    S.SetElement(0, 0, u[2])
    S.SetElement(0, 1, v[2])
    S.SetElement(0, 2, w[2])
    S.SetElement(1, 0, u[5])
    S.SetElement(1, 1, v[5])
    S.SetElement(1, 2, w[5])
    S.SetElement(2, 0, u[8])
    S.SetElement(2, 1, v[8])
    S.SetElement(2, 2, w[8])

    #print "esta es S"
    #print S

    S.Invert()
    #print "esta es Sinv"
    #print S

    M = vtk.vtkMatrix3x3()
    M.Multiply3x3(S, F, M)
    M.Transpose()
    return M


def Analisis_por_vtk(fidu_3D):
    """Calcula la rotacion y traslacion y ampliacion
    por coordenadas apareadas segun una ecuacion vtk
    que usa menor error por cuadrados medios"""
    puntos = (1, 3, 4, 6, 7, 9)  # son los 6 fidu utilizados
    x, y, z = (0, 1, 2)          # solo para visualizar las coordenadas

    marco = Marco_Micromar()
    p_Sou = vtk.vtkPoints()
    p_Sou.SetNumberOfPoints(len(puntos))
    p_Tar = vtk.vtkPoints()
    p_Tar.SetNumberOfPoints(len(puntos))
    for pu in puntos:
        p_Sou.SetPoint(puntos.index(pu), marco.P[pu][x], marco.P[pu][y], 0)
        p_Tar.SetPoint(puntos.index(pu), fidu_3D[pu][x], fidu_3D[pu][y], fidu_3D[pu][z])

    print "analisis por vtk"

    Landmark_T = vtk.vtkLandmarkTransform()
    Landmark_T.SetSourceLandmarks(p_Sou)
    Landmark_T.SetTargetLandmarks(p_Tar)
    Landmark_T.Update()

    return Landmark_T.GetMatrix()


def Analisis_por_vtk_4(fidu_TAC, fidu_3D):
    """Calcula la rotacion y traslacion y ampliacion
    por coordenadas apareadas segun una ecuacion vtk
    que usa menor error por cuadrados medios"""
    puntos = (1, 3, 4, 6, 7, 9)  # son los 6 fidu utilizados
    x, y, z = (0, 1, 2)          # solo para visualizar las coordenadas

    p_Sou = vtk.vtkPoints()
    p_Sou.SetNumberOfPoints(len(puntos))
    p_Tar = vtk.vtkPoints()
    p_Tar.SetNumberOfPoints(len(puntos))
    for pu in puntos:
        p_Sou.SetPoint(puntos.index(pu),
                       fidu_TAC[pu][x],
                       fidu_TAC[pu][y],
                       fidu_TAC[pu][z])

        p_Tar.SetPoint(puntos.index(pu),
                       fidu_3D[pu][x],
                       fidu_3D[pu][y],
                       fidu_3D[pu][z])

    print "analisis por vtk"

    Landmark_T = vtk.vtkLandmarkTransform()
    Landmark_T.SetSourceLandmarks(p_Sou)
    Landmark_T.SetTargetLandmarks(p_Tar)
    Landmark_T.Update()

    print "Matrix solo rotada"

    M = Landmark_T.GetMatrix()
    M.SetElement(0, 3, 0.0)
    M.SetElement(1, 3, 0.0)
    M.SetElement(2, 3, 0.0)

    return M


def Analisis_por_SVD(fidu_3D):
    """ calcula la rotacion por Singular Value Decomposition
    (puede usar 4 o 6 fidu )"""
    puntos = (1, 3, 4, 6, 7, 9)
    x, y, z = (0, 1, 2)
    zeros_3D = fidu_3D[0]

    B = numpy.mat([
                fidu_3D[puntos[0]],
                fidu_3D[puntos[1]],
                fidu_3D[puntos[2]],
                fidu_3D[puntos[3]],
                fidu_3D[puntos[4]],
                fidu_3D[puntos[5]]
                ])
    marco = Marco_Micromar()
    A = numpy.mat([
                [marco.P[puntos[0]][x], marco.P[puntos[0]][y], 0],
                [marco.P[puntos[1]][x], marco.P[puntos[1]][y], 0],
                [marco.P[puntos[2]][x], marco.P[puntos[2]][y], 0],
                [marco.P[puntos[3]][x], marco.P[puntos[3]][y], 0],
                [marco.P[puntos[4]][x], marco.P[puntos[4]][y], 0],
                [marco.P[puntos[5]][x], marco.P[puntos[5]][y], 0]
                ])

    assert len(A) == len(B)
    n = A.shape[0];  # total points
    print "Puntos utilizados para SVD: ", n
    centroid_A = numpy.mean(A, axis=0)
    centroid_B = numpy.mean(B, axis=0)
    print "centroides matriz problema: ", centroid_B
    #print "zeros 3D :", zeros_3D
    # centre the points
    AA = A - numpy.tile(centroid_A, (n, 1))
    BB = B - numpy.tile(centroid_B, (n, 1))

    # dot is matrix multiplication for array
    H = numpy.transpose(AA) * BB
    U, S, Vt = numpy.linalg.svd(H)
    R = Vt.T * U.T
    # special reflection case
    if numpy.linalg.det(R) < 0:
        print "Reflection detected"
        Vt[2, :] *= -1
        R = Vt.T * U.T
    vt = R * (centroid_A.T + centroid_B.T)
    trasla_1, = numpy.array(vt.T)
    trasla_1 = [trasla_1.item(0),
                trasla_1.item(1),
                trasla_1.item(2)]

    print "Decomposing R: (grados)"
    Phi = numpy.degrees(numpy.arctan(R[2, 1]/R[2, 2]))
    Theta = numpy.degrees(numpy.arcsin(R[0, 2]))
    Psi = numpy.degrees(-numpy.arctan(R[1, 0]/R[0, 0]))
    rota = [Phi, Theta, Psi]
    print "rotacion segun SVD: ", rota
    print "traslacion segun SVD: ", trasla_1

    # "Addendum para entregar formato vtk"
    M = vtk.vtkMatrix4x4()
    for a in range(3):
        for b in range(3):
            #print a, b, R.tolist()[a][b]
            M.SetElement(a, b, R.tolist()[a][b])
    #print M
    #return R, trasla_1, rota
    return M, trasla_1


def Resolucion_Matricial(punto, transfo):
    """Entrega el vector, resultado del
    producto de un vector por una matriz"""
    print numpy.size(punto),
    print numpy.shape(transfo),
    if not(numpy.size(punto) == numpy.shape(transfo)[1]):
        print "NO son compatibles las dimensiones"
        return None
    print "SON compatibles las dimensiones"
    return numpy.dot(punto, transfo)


def Multiplica_puntos(lista, M):
    list_out = []
    for f in lista:
        f_3D = [0, 0, 0]
        M.MultiplyPoint(f, f_3D)
        f_3D = redondea(f_3D, 2)
        list_out.append(f_3D)
    return list_out


def Transforma_puntos(lista, T):
    lista_out = []
    for f in lista:
        if len(f) == 3:
            f.append(1)
        f_out = [0, 0, 0, 0]
        T.MultiplyPoint(f, f_out)
        lista_out.append(f_out)
    return lista_out


def promedio_puntos(lista, sele):
    out = [0, 0, 0]
    for p in sele:
        out[0] += lista[p][0]
        out[1] += lista[p][1]
        out[2] += lista[p][2]
    return [out[0]/len(sele), out[1]/len(sele), out[2]/len(sele)]


def fiduciarios_a_tabla(fidu):
    # pasa fidus a una tabla con variables u, v, w, z """
    u, v, w = [], [], []
    fr_N = [0, 0, 0, 0]

    for i in range(len(fidu)):
        u.append(fidu[i][0])
        v.append(fidu[i][1])
        w.append(fidu[i][2])

    # fraccion de z calculado por N-Locators:
    fr_N[1] = (v[2]-v[1])/(v[3]-v[1])
    fr_N[2] = (u[5]-u[6])/(u[4]-u[6])
    fr_N[3] = (v[8]-v[9])/(v[7]-v[9])

    return u, v, w, fr_N


def redondea(lista, deci):
    lista_redond = []
    for item in lista:
        lista_redond.append(round(item, deci))
    return lista_redond
