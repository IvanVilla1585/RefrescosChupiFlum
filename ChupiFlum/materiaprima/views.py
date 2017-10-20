# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializer import MateriaPrimaSerializer
from .models import MateriaPrima
from django.contrib import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class MateriaPrimaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = MateriaPrima
    queryset = model.objects.all()
    serializer_class = MateriaPrimaSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        typelist = self.request.GET.get('typelist', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search) | Q(categoria__nombre__icontains=search) | Q(unidad_medida__nombre__icontains=search))  
        elif typelist:
            queryset = super(MateriaPrimaViewSet, self).get_queryset()
        else:
            queryset = self.model.objects.filter(estado=True)

        return queryset

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs[self.lookup_field]
        material = None
        if id:
            try:
                material = self.model.objects.get(id=id)
                material.estado = not material.estado
                material.save()
            except MateriaPrima.DoesNotExist as e:
                return Response({'message': 'La materia prima no existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'El id es obligatorio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(material)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        typelist = self.request.GET.get('typelist', None)
        queryset = self.filter_queryset(self.get_queryset())
        print typelist
        page = self.paginate_queryset(queryset)
        if typelist is not None and page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
from django.shortcuts import render
import json
from django.core import serializers
from reportlab.lib.pagesizes import letter, A4

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

from .models import MateriaPrima
from proveedores.mixins import JSONResponseMixin
from .forms import MateriaPrimaForm
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


class ListarMateriaPrima(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = MateriaPrima
    template_name = 'materiaprima_list.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': materiaprima.id,
            'value': materiaprima.nombre,
        } for materiaprima in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarMateriaPrima, self).get_queryset()
        return queryset

class CrearMateriaPrima(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MateriaPrima
    success_url = reverse_lazy('materiaprim:materiaPrimaForm')
    form_class = MateriaPrimaForm
    success_message = 'La materia prima %(nombre)s se registro en el sistema'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.cantidad = self.object.cantidad * self.object.unidad_medida.equivalencia
        self.object.stock = self.object.stock * self.object.unidad_medida.equivalencia
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

class ModificarMateriaPrima(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MateriaPrima
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = MateriaPrimaForm
    success_url = reverse_lazy('materiaprim:materiaPrimaForm')
    success_message = 'Los datos de la materia prima %(nombre)s se actualizaron'

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None

    def post(self, request):
        id = self.request.POST.get('id', None)
        materia = None
        try:
            materia = MateriaPrima.objects.get(id=id)
        except MateriaPrima.DoesNotExist as e:
            self.object = materia
        if materia is not None:
            materia.estado = False
            materia.save()
            self.object = materia
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito la materia rima',
            }
        else:
            data = {
                'message': 'Esta materia prima se encuentra asociada'
            }

        return data

class ConsultarMateriaPrima(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = MateriaPrima
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        if self.object is not None:
            data = {
                'status': 200,
                'materia':{
                    'id': self.object.id,
                    'nombre': self.object.nombre,
                    'descripcion': self.object.descripcion,
                    'unidad_medida': self.object.unidad_medida.id,
                    'categoria': self.object.categoria.id,
                    'cantidad': self.object.cantidad,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'La materia prima no se encuentra registrada'
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


class MateriaPrimaView(LoginRequiredMixin, TemplateView):
    template_name = 'materiaprima/materiaprima_form.html'

    def get_context_data(self, **kwargs):
        context = super(MateriaPrimaView, self).get_context_data(**kwargs)
        context.update({'form': MateriaPrimaForm()})

        return context


class ReporteMateriaPrimaExcel(TemplateView):
    model = MateriaPrima

    def get(self, request, *args, **kwargs):

        materias = self.model.objects.all()

        wb = Workbook()

        ws = wb.active

        ws['B1'] = 'REPORTE DE MATERIA PRIMA'

        ws.merge_cells('B1:G1')

        ws['B3'] = 'NOMBRE'
        ws['C3'] = 'DESCRIPCIÓN'
        ws['D3'] = 'UNIDAD DE MEDIDA'
        ws['E3'] = 'CATEGORIA'
        ws['F3'] = 'CANTIDAD'
        ws['G3'] = 'ESTADO'
        cont=6

        for materia in materias:
            ws.cell(row=cont,column=2).value = materia.nombre
            ws.cell(row=cont,column=3).value = materia.descripcion
            ws.cell(row=cont,column=4).value = materia.unidad_medida.nombre
            ws.cell(row=cont,column=5).value = materia.categoria.nombre
            ws.cell(row=cont,column=6).value = materia.cantidad
            if materia.estado:
                ws.cell(row=cont,column=7).value = materia.estado = 'Activo'
            else:
                ws.cell(row=cont,column=8).value = materia.estado = 'Inactivo'
            cont = cont + 1

        nombre_archivo ="ReporteMateriaPrimaExcel.xlsx"

        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response


class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def print_materia(self):
            buffer = self.buffer
            doc = SimpleDocTemplate(buffer,
                                    rightMargin=72,
                                    leftMargin=72,
                                    topMargin=72,
                                    bottomMargin=72,
                                    pagesize=self.pagesize)

            # Our container for 'Flowable' objects
            elements = []

            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            materias = MateriaPrima.objects.all()
            elements.append(Paragraph('Reporte Materia Prima', styles['Heading1']))
            for i, materia in enumerate(materias):
                elements.append(Paragraph(materia.nombre, styles['Normal']))
                elements.append(Paragraph(materia.descripcion, styles['Normal']))

            doc.build(elements)

            # Get the value of the BytesIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()
            return pdf


def print_materia(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="materiaprima.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_materia()

    response.write(pdf)
    return response

class ReporteMateriaPDF(View):
    model = MateriaPrima

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
        pdf.drawString(225, 770, u"REPORTE DE MATERIA PRIMA")

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('NOMBRE', 'DESCRIPCIÓN', 'CATEGORIA', 'CANTIDAD', 'UNIDAD MEDIDA', )
        #Creamos una lista de tuplas que van a contener a las personas
        cm = 40
        detalles = [(
            materia.nombre,
            materia.descripcion,
            materia.categoria.nombre,
            materia.cantidad,
            materia.unidad_medida.nombre
        ) for materia in self.model.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[2.5 * cm, 4 * cm, 2 * cm, 2.5 * cm])
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
        detalle_orden.wrapOn(pdf, 900, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 30,y)

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
        """
