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
from .forms import ProveedoreForm
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
from django.views.generic import TemplateView

from .models import Proveedore
from .mixins import JSONResponseMixin
from django.http import JsonResponse
from loginusers.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ListarProveedores(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Proveedore
    template_name = 'proveedore_list.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': proveedor.id,
            'value': proveedor.empresa,
        } for proveedor in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(empresa__icontains=nom)
        else:
            queryset = super(ListarProveedores, self).get_queryset()

        return queryset


class EliminarProveedor(LoginRequiredMixin, JSONResponseMixin, DeleteView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:proveedor')

    def get_queryset(self):
        nit = self.request.POST.get('nit', None)
        id = self.request.POST.get('pk', None)
        if id:
            queryset = self.model.objects.get(id=id)
        else:
            queryset = super(EliminarProveedor, self).get_queryset()
        return queryset

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        return self.render_to_json_response()

    def get_data(self):

        data = {
            'message': 'Se cambio el estado del proveedor a inctivo',
        }

        return data

class ActualizarEstadoView(JSONResponseMixin, View):
  object = None
  def post(self, request):
    id = self.request.POST.get('id', None)
    nit = self.request.POST.get('nit', None)
    proveedor = None
    import ipdb; ipdb.set_trace()
    try:
        proveedor = Proveedore.objects.get(id=id)
    except Proveedore.DoesNotExist as e:
        self.object = proveedor
    if proveedor is not None:
        proveedor.estado = False
        proveedor.save()
        self.object = proveedor
    return self.render_to_json_response()

  def get_data(self):
      if self.object is not None:
          data = {
              'message': 'Se inhabilito el proveedor',
          }
      else:
          data = {
              'message': 'Este proveeedor no se encuentra registrado'
          }

      return data

class CrearProveedor(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proveedore
    form_class = ProveedoreForm
    success_url = reverse_lazy('proveedores:proveedor')
    success_message = 'El proveedor %(empresa)s fue registrado en el sistema.'


class ActualizarProveedor(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:proveedor')
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = ProveedoreForm
    success_message = u'La información del proveedor %(empresa)s fue actualizada'



class ConsultarProveedor(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Proveedore
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'status': 200,
                'proveedor':{
                    'nit': self.object.nit,
                    'nombre_empresa': self.object.empresa,
                    'direccion': self.object.direccion,
                    'telefono': self.object.telefono,
                    'fax': self.object.fax,
                    'correo_empresa': self.object.correo_empresa,
                    'nombre_contacto': self.object.nombre_contacto,
                    'apellido_contacto': self.object.apellido_contacto,
                    'telefono_contacto': self.object.telefono_contacto,
                    'correo_contacto': self.object.correo_contacto,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'El proveedor no se encuentra registrado'
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



class ProveedoresView(LoginRequiredMixin, TemplateView):
    template_name = 'proveedores/proveedore_form.html'


    def get_context_data(self, **kwargs):
        context = super(ProveedoresView, self).get_context_data(**kwargs)
        context.update({'form': ProveedoreForm()})

        return context


class ReporteProveedoresPDF(View):
    model = Proveedore

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
        pdf.drawString(200, 770, u"REPORTE DE PROVEEDORES")

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('NIT', 'EMPRESA', 'DIRECCIÓN', 'TELEFONO', 'CORREO EMPRESA', 'CONTACTO', 'CORREO CONTACTO',)
        #Creamos una lista de tuplas que van a contener a las personas
        cm = 40
        detalles = [(
            proveedor.nit,
            proveedor.empresa,
            proveedor.direccion,
            proveedor.telefono,
            proveedor.correo_empresa,
            '%s %s' % (proveedor.nombre_contacto, proveedor.apellido_contacto),
            proveedor.correo_empresa
        ) for proveedor in self.model.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm, 2 * cm, 3 * cm, 2 * cm])
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
        detalle_orden.drawOn(pdf, 10,y)

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
