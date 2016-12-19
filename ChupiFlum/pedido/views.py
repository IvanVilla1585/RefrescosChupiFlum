# -*- coding: utf-8 -*-
from django.shortcuts import render
import json
from django.core import serializers
from reportlab.lib.pagesizes import letter, A4

#Workbook nos permite crear libros en excel
from openpyxl import Workbook
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import (
    PedidoForm,
    PedidoMateriaFormSet,
)
from .models import (
    Pedido,
    Detalle_Pedido,
)
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from estado_orden.models import EstadosOrdenes
from materiaprima.models import MateriaPrima
from proveedores.models import Proveedore
from dal import autocomplete
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin
from decimal import Decimal
import ast
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class PedidoView(LoginRequiredMixin, TemplateView):
    template_name = 'pedido/pedido_form.html'

    def get_context_data(self, **kwargs):
        context = super(PedidoView, self).get_context_data(**kwargs)
        form = PedidoForm()
        detalle_form = PedidoMateriaFormSet()
        context.update({'form': form, 'detalle_form': detalle_form,})
        return context

class CrearPedido(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pedido
    success_url = reverse_lazy('pedidos:pedidosForm')
    form_class = PedidoForm
    success_message = 'El pedido numero %(id)s al proveedor fue registrado'

    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form = PedidoMateriaFormSet()
        return self.render_to_response(self.get_context_data(form=form, detalle_form=detalle_form,))

    def post(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form = PedidoMateriaFormSet(self.request.POST)
        if (form.is_valid() and detalle_form.is_valid()):
            return self.form_valid(form, detalle_form)
        else:
            return self.form_invalid(form, detalle_form)

    def form_valid(self, form, detalle_form):

        self.object = form.save(commit=False)
        estado = EstadosOrdenes.objects.get(id=1)
        self.object.id_estado = estado
        self.object.usuario = self.request.user
        self.object.save()
        detalle_form.instance = self.object
        detalle_form.save()
        detalles = Detalle_Pedido.objects.filter(id_pedido=self.object.id)

        for detalle in detalles:
            materia = MateriaPrima.objects.get(id=detalle.id_materia_prima.id)
            materia.cantidad = materia.cantidad + (detalle.cantidad * detalle.id_materia_prima.unidad_medida.equivalencia)
            materia.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_form):

        return self.render_to_response(self.get_context_data(form=form, detalle_form=detalle_form))

class ListarPedido(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Pedido
    template_name = 'pedido_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': pedido.id,
            'value': '%s %s' % (pedido.fecha, pedido.proveedor.empresa),
        } for pedido in self.object_list]
        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(proveedor__empresa__icontains=nom)
        else:
            queryset = super(ListarPedido, self).get_queryset()

        return queryset

class ModificarPedido(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_url = reverse_lazy('pedidos:pedidosForm')
    success_message = u'El pedido número %(id)s al proveedor fue registrado'

    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form = PedidoMateriaFormSet()
        return self.render_to_response(self.get_context_data(form=form, detalle_form=detalle_form,))

    def post(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form = PedidoMateriaFormSet(self.request.POST)
        if (form.is_valid() and detalle_form.is_valid()):
            return self.form_valid(form, detalle_form)
        else:
            return self.form_invalid(form, detalle_form)

    def form_valid(self, form, detalle_form):

        self.object = form.save(commit=False)
        estado = EstadosOrdenes.objects.get(id=1)
        import ipdb; ipdb.set_trace()
        self.object.id_estado = estado
        self.object.usuario = self.request.user
        self.object.save()
        detalle_form.instance = self.object
        detalle_form.save()
        detalles = Detalle_Pedido.objects.filter(id_pedido=self.object.id)

        for detalle in detalles:
            materia = MateriaPrima.objects.get(id=detalle.id_materia_prima.id)
            materia.cantidad = materia.cantidad + detalle.cantidad
            materia.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_form):

        return self.render_to_response(self.get_context_data(form=form, detalle_form=detalle_form))

class EliminarPedido(LoginRequiredMixin, DeleteView):
    model = Pedido
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    success_url = reverse_lazy('productos:listar')

class ConsultarPedido(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Pedido
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):

        if self.object is not None:

            detalle_pedido = Detalle_Pedido.objects.filter(id_pedido=self.object.id)

            data = {
                'status': 200,
                'pedido':{
                    'id': self.object.id,
                    'descripcion': self.object.descripcion,
                    'fecha': self.object.fecha,
                    'proveedor': self.object.proveedor.id,
                    'total': self.object.total ,
                    'estado': self.object.id_estado.id,
                    'productos': [{
                        'id': producto.id_materia_prima.id,
                        'cantidad': producto.cantidad,
                        'valor': producto.valor_unitario,
                    } for producto in detalle_pedido]
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'No se encuentra ninguna maquina asociada a la busqueda'
            }

        return data

class ConsultarValorMateria(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Pedido
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):

        if self.object is not None:

            detalle_pedido = Detalle_Pedido.objects.filter(id_materia_prima=self.object.id)[1]
            data = {
                'status': 200,
                'pedido':{
                    'producto': detalle_pedido.id_materia_prima.nombre,
                    'valor': detalle_pedido.valor_unitario / detalle_pedido.cantidad,
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'No se encuentra ninguna maquina asociada a la busqueda'
            }

        return data


class MateriaPrimaAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = MateriaPrima.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs

class ReportePedidosPDF(View):
    model = Pedido

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
        pdf.drawString(250, 770, u"REPORTE DE PEDIDOS")

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('DESCRIPCIÓN', 'FECHA', 'PROVEEDOR', 'USUARIO', 'TOTAL', )
        #Creamos una lista de tuplas que van a contener a las personas
        cm = 40
        detalles = [(
            pedido.descripcion,
            pedido.fecha,
            pedido.proveedor.empresa,
            pedido.usuario.username,
            pedido.total
        ) for pedido in self.model.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[3 * cm, 5 * cm, 2 * cm, 2 * cm])
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
