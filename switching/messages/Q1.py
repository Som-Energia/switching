# -*- coding: utf-8 -*-
from datetime import date, datetime

from message import Message, except_f1


class Q1(Message):
    """Classe que implementa Q1."""
    
    def get_comptadors(self):
        """Retorna totes les lectures en una llista de comptadors"""
        comptadors = []
        for mesura in self.obj.Medidas:
            if mesura.CodUnificadoPuntoSuministro.text[:20] == \
                                                    self.get_codi[:20]:
                for aparell in mesura.Aparato:
                    comptadors.append(Comptador(aparell))
        return comptadors
    
    @staticmethod
    def agrupar_lectures_per_periode(lectures):
        """Comprova si hi ha lectures per igual tipus i periode
           amb dates diferents i les agrupa.
        """
        lect = {}
        for i in lectures:
            if not i.tipus in lect:
                lect[i.tipus] = {}
            if not i.periode in lect[i.tipus]:
                lect[i.tipus][i.periode] = []
            lect[i.tipus][i.periode].append(i)
        return lect

    @staticmethod
    def agrupar_lectures_per_data(lectures):
        """Retorna un diccionari de llistes en què les
           claus són les dates inicial i final de les lectures
        """
        lect = {}
        for i in lectures:
            key = '%s-%s' % (i.data_lectura_inicial, i.data_lectura_final)
            if not key in lect:
                lect[key] = []
            lect[key].append(i)
        return lect

    @staticmethod
    def obtenir_data_inici_i_final(dic):
        """Retorna la data inicial i final del diccionari retornat 
           per la funció agrupar_lectures_per_data()
        """
        ret_ini = None
        ret_fi = None
        for i in dic.keys():
            d_ini = date(int(i.split('-')[0]), int(i.split('-')[1]),
                                                        int(i.split('-')[2]))
            if not ret_ini or ret_ini > d_ini:
                ret_ini = d_ini
            d_fi = date(int(i.split('-')[3]), int(i.split('-')[4]),
                                                        int(i.split('-')[5]))
            if not ret_fi or ret_fi < d_fi:
                ret_fi = d_fi
        return datetime.strftime(ret_ini, '%Y-%m-%d'), datetime.strftime(
                                                            ret_fi, '%Y-%m-%d')


class Lectura(object):
    """Classe que implementa la Lectura"""

    def __init__(self, lect, tarifa=None):
        self.lectura = lect
        self.tarifa = tarifa
        self._cnt = 0

    @property
    def cnt(self):
        return self._cnt

    @cnt.setter
    def cnt(self, value):
        self._cnt = value

    @property
    def tipus(self):
        tipus = {'AE': 'A',
                 'R1': 'R',
                 'PM': 'M',
                 'EP': 'EP'}
        return tipus.get(self.lectura.Magnitud.text)

    @property
    def magnitud(self):
        return self.lectura.Magnitud.text

    @property
    def consum(self):
        return float(self.lectura.ConsumoCalculado.text)

    @property
    def periode(self):
        # taula 42
        relacio = {'01': 'P1',  # Punta + Llano
                   '21': 'P1',  # Punta
                   '03': 'P2',  # Valle
                   '10': 'P1',  # Totalizador
                   '61': 'P1',  # Periodo 1
                   '62': 'P2',  # Periodo 2
                   '63': 'P3',  # Periodo 3
                   '64': 'P4',  # Periodo 4
                   '65': 'P5',  # Periodo 5
                   '66': 'P6'}  # Periodo 6

        return relacio[self.lectura.CodigoPeriodo.text]

    @property
    def constant_multiplicadora(self):
        return float(self.lectura.ConstanteMultiplicadora.text)

    @property
    def data_lectura_inicial(self):
        data = self.lectura.LecturaDesde.FechaHora.text
        return data[0:data.find('T')]

    @property
    def data_lectura_final(self):
        data = self.lectura.LecturaHasta.FechaHora.text
        return data[0:data.find('T')]

    @property
    def valor_lectura_inicial(self):
        return float(self.lectura.LecturaDesde.Lectura.text)

    @property
    def valor_lectura_final(self):
        return float(self.lectura.LecturaHasta.Lectura.text)

    @property
    def origen_lectura_inicial(self):
        return self.lectura.LecturaDesde.Procedencia.text

    @property
    def origen_lectura_final(self):
        return self.lectura.LecturaHasta.Procedencia.text

    @property
    def gir_comptador(self):
        return (10 ** int(self.lectura.NumeroRuedasEnteras.text))


class Comptador(object):
    """Classe que implementa el Comptador"""
    
    def __init__(self, data):
        self.obj = data

    def get_lectures(self):
        """Retorna totes les lectures en una llista de Lectura"""
        lectures = []
        try:
            for lect in self.obj.Integrador:
                lectures.append(Lectura(lect))
        except AttributeError:
            pass
        return lectures

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.obj.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** int(self.obj.Integrador.NumeroRuedasEnteras.text))
