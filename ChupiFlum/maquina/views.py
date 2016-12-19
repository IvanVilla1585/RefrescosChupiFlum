# -*- coding: utf-8 -*-
from django.shortcuts import render
import json
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    View
)
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Maquina
from proveedores.mixins import JSONResponseMixin
from .forms import MaquinaForm
from loginusers.mixins import LoginRequiredMixin
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ListarMaquinas(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Maquina
    template_name = 'maquina_list.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        if self.object_list is not None:
            data = [{
                'id': maquina.id,
                'value': maquina.nombre,
            } for maquina in self.object_list]
        else:
            data = [{
                'id': '0',
                'value': 'No hay maquinas',
            }]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarMaquinas, self).get_queryset()

        return queryset

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None
    def post(self, request):
        id = self.request.POST.get('id', None)
        maquina = None
        try:
            maquina = Maquina.objects.get(id=id)
        except Maquina.DoesNotExist as e:
            self.object = maquina
        if maquina is not None:
            maquina.estado = False
            maquina.save()
            self.object = maquina
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito la maquina',
            }
        else:
            data = {
                'message': 'Esta maquina se encuentra asociada a procesos'
            }

        return data

class CrearMaquina(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Maquina
    success_url = reverse_lazy('maquinas:maquinaForm')
    form_class = MaquinaForm
    success_message = "La maquina %(nombre)s se registro en el sistema"

class ModificarMaquina(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Maquina
    form_class = MaquinaForm
    success_url = reverse_lazy('maquinas:maquinaForm')
    success_message = "La maquina %(nombre)s fue actualizada"

class ConsultarMaquina(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Maquina
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):

        if self.object is not None:
            data = {
                'status': 200,
                'maquina':{
                    'id': self.object.id,
                    'nombre': self.object.nombre,
                    'descripcion': self.object.descripcion,
                    'unidad_medida': self.object.unidad_medida.id,
                    'capacidad': self.object.capacidad,
                    'tiempo': self.object.tiempo,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'No se encuentra ninguna maquina asociada a la busqueda'
            }
        return data

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = None
        return obj

class MaquinaView(LoginRequiredMixin, TemplateView):
    template_name = 'maquina/maquina_form.html'


    def get_context_data(self, **kwargs):
        context = super(MaquinaView, self).get_context_data(**kwargs)
        context.update({'form': MaquinaForm()})

        return context

class ReporteMaquinasPDF(View):
    model = Maquina

    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(230, 790, u"REFRESCOS CHUPIFLUM")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(250, 770, u"REPORTE DE MAQUINAS")

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('NOMBRE', u'DESCRIPCIÓN', 'CAPACIDAD', 'UNIDAD MEDIDA', 'TIEMPO', )
        #Creamos una lista de tuplas que van a contener a las personas
        cm = 40
        detalles = [(
            maquina.nombre,
            maquina.descripcion,
            maquina.capacidad,
            maquina.unidad_medida.nombre,
            maquina.tiempo
        ) for maquina in self.model.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[3 * cm, 4 * cm, 2 * cm, 2.5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 950, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 20,y)

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
