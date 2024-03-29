
# -*- coding: utf-8 -*-

from message import Message, except_f1
import C1


class C2(Message):
    """Classe que implementa C2."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return C1.Sollicitud(self.obj.CambiodeComercializadoraConCambios.\
                          DatosSolicitud)

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self._header)
        return C1.Contracte(obj.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return C1.Client(self.obj.CambiodeComercializadoraConCambios.Cliente)

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self._header, False)
        if obj and hasattr(obj, 'DatosAceptacion'):
            return C1.Acceptacio(obj.DatosAceptacion)
        return False

    @property
    def rebuig(self):
        """Retorna una llista de Rebuig"""
        data = []
        for i in self.obj.RechazoATRDistribuidoras.Rechazo:
            data.append(C1.Rebuig(i))
        return data

    @property
    def rebuig_anullacio(self):
        """Retorna l'objecte Rebuig"""
        data = []
        for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
            data.append(C1.Rebuig(i))
        return data

    @property
    def header(self):
        return self._header

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Activacio(self.obj.\
                            ActivacionCambiodeComercializadoraConCambios)

    @property
    def notificacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Notificacio(self.obj.NotificacionComercializadoraSaliente)
    

    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return C1.Anullacio(self.obj.AnulacionSolicitud)

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data

    @property
    def mesura(self):
        """Retorna l'objecte mesura"""
        obj = getattr(self.obj, self._header)
        return Mesura(obj.Medida)

    @property
    def comentaris(self):
        """Retorna una llista de comentaris"""
        data = []
        obj = getattr(self.obj, self._header)
        if (hasattr(obj, 'Comentarios') and
            hasattr(obj.Comentarios, 'Comentario')):
            for i in obj.Comentarios.Comentario:
                data.append(Comentari(i))
        return data

    @property
    def incidencies(self):
        """Retorna una llista de incidencies"""
        data = []
        for i in self.obj.IncidenciasATRDistribuidoras.Incidencia:
            data.append(C1.Rebuig(i))
        return data

    @property
    def cnae(self):
        value = ''
        try:
            value = self.obj.CambiodeComercializadoraConCambios.CNAE.text
        except AttributeError:
            pass
        return value

    @property
    def vivenda(self):
        value = ''
        try:
            value = (self.obj.CambiodeComercializadoraConCambios.
                                        ViviendaHabitual.text)
        except AttributeError:
            pass
        return value

    @property
    def canvi_titular(self):
        value = ''
        try:
            value = (self.obj.CambiodeComercializadoraConCambios.
                                        TipoCambioTitular.text)
        except AttributeError:
            pass
        return value


class Comentari(object):

    def __init__(self, data):
        self.comentari = data
    
    @property
    def text(self):
        value = ''
        try:
            value = self.comentari.Texto.text
        except AttributeError:
            pass
        return value

    @property
    def data(self):
        value = ''
        try:
            value = self.comentari.Fecha.text
        except AttributeError:
            pass
        return value

    @property
    def hora(self):
        value = ''
        try:
            value = self.comentari.Hora.text
        except AttributeError:
            pass
        return value

class Mesura(object):

    def __init__(self, data):
        self.mesura = data
    
    @property
    def cp_propietat(self):
        value = ''
        try:
            value = self.mesura.ControlPotenciaPropiedad.text
        except AttributeError:
            pass
        return value

    @property
    def cp_installacio(self):
        value = ''
        try:
            value = self.mesura.ControlPotenciaInstalacion.text
        except AttributeError:
            pass
        return value

    @property
    def equip_aportat_client(self):
        value = ''
        try:
            value = self.mesura.EquipoAportadoCliente.text
        except AttributeError:
            pass
        return value

    @property
    def equip_installat_client(self):
        value = ''
        try:
            value = self.mesura.EquipoInstaladoCliente.text
        except AttributeError:
            pass
        return value

    @property
    def tipus_equip_mesura(self):
        value = ''
        try:
            value = self.mesura.TipoEquipoMedida.text
        except AttributeError:
            pass
        return value
