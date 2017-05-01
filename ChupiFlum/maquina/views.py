# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializer import MaquinaSerializer
from .models import Maquina
from django.contrib import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class MaquinaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = Maquina
    queryset = model.objects.all()
    serializer_class = MaquinaSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search) | Q(capacidad__icontains=search) )
        else:
            queryset = super(MaquinaViewSet, self).get_queryset()

        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        request.data['unidad_medida_id'] = request.data['unidad_medida']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        request.data['unidad_medida_id'] = request.data['unidad_medida']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs[self.lookup_field]
        machine = None
        if id:
            try:
                machine = self.model.objects.get(id=id)
                machine.estado = not machine.estado
                machine.save()
            except Maquina.DoesNotExist as e:
                return Response({'message': 'La máquina no existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'El id es obligatorio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(machine)
        return Response(serializer.data, status=status.HTTP_200_OK)
"""
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
"""
