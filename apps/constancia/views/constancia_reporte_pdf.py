import os
import sys

from reportlab.lib import colors

from apps.constancia.views.constancia import generar_constancia, get_establecimiento, get_cargo

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass
    # django.setup()

from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, TableStyle
from reportlab.platypus import Table
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.flowables import Spacer


class verticalText(Flowable):
    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text

    def draw(self):
        canvas = self.canv
        canvas.setFont("Times-Roman", 8)
        canvas.rotate(90)
        fs = canvas._fontsize
        canvas.translate(1, -fs / 1.2)  # canvas._leading?

        canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        canv.setFont("Times-Roman", 8)
        fn, fs = canv._fontname, canv._fontsize
        return canv._leading, 1 + canv.stringWidth(self.text, fn, fs)


sp = ParagraphStyle('parrafos',
                    alignment=TA_CENTER,
                    fontSize=12,
                    leading=10,
                    fontName="Times-Roman")


sp_justifi_title_table_2 = ParagraphStyle('parrafos',
                                        alignment=TA_JUSTIFY,
                                        fontSize=8,
                                        leading=10,
                                        fontName="Times-Roman" 
)

sp_subtitle = ParagraphStyle('parrafos',
                             alignment=TA_CENTER,
                             fontSize=8,
                             leading=10,
                             fontName="Times-Roman")

sp_justifi_title_table = ParagraphStyle('parrafos',
                                        alignment=TA_JUSTIFY,
                                        fontSize=8,
                                        leading=10,
                                        fontName="Times-Roman")

sp_justifi_title_table_center = ParagraphStyle('parrafos',
                                               alignment=TA_CENTER,
                                               fontSize=10,
                                               leading=10,
                                               fontName="Times-Roman")

sp_justifi_title_header = ParagraphStyle('parrafos',
                                         alignment=TA_CENTER,
                                         fontSize=7,
                                         # leading=10,
                                         splitLongWords=True,
                                         spaceShrinkage=2,
                                         leading=8,
                                         fontName="Times-Roman")

sp_justifi_title_body = ParagraphStyle('parrafos',
                                       alignment=TA_RIGHT,
                                       fontSize=7,
                                       # leading=10,
                                       leading=8,
                                       fontName="Times-Roman")

sp_footer = ParagraphStyle('parrafos',
                           alignment=TA_JUSTIFY,
                           fontSize=7,
                           leading=10,
                           fontName="Times-Roman")

ROW_HEIGHT = 3.5 * mm


class ReportSimulator():
    # tea = Tea.objects.get(pk=1)

    def __init__(self, pagesize, constancia, anio_bd):

        self.constancia = constancia
        self.anio_bd = anio_bd
        self.buffer = BytesIO()
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.height, self.width = self.pagesize

    def listToString(self, s):
        str1 = ""
        for ele in s:
            str1 += ele[2:]
        return str1

    def tabla_encabezado(self, styles):
        now = datetime.now()
        sp = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=16,
                            fontName="Times-Roman",
                            leading=20
                            )
        sp_date = ParagraphStyle('parrafos',
                                 alignment=TA_RIGHT,
                                 fontSize=8,
                                 fontName="Times-Roman",
                                 )
        # sp = ParagraphStyle('parrafos',
        #                     alignment=TA_CENTER,
        #                     fontSize=16,
        #                     fontName="Times-Roman",
        #                     )
        try:
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/Logo-01.jpg")
            archivo_diris = os.path.join(settings.STATIC_LOCAL_ROOT, "img/logo_remuneracion.png")
            imagen = Image(archivo_imagen, width=310, height=50)
            # imagen_canchis = Image(archivo_diris, width=100, height=100, hAlign='RIGHT')
        except:
            imagen = Paragraph(u"LOGO", sp)

        date_ = Paragraph(
            u"" + now.strftime("%d/%m/%Y") + " <br/> " + now.strftime("%H:%M:%S") + "<br/> <br/> <br/> ", sp_date)
        encabezado = [[imagen, "", date_]]
        tabla_encabezado = Table(encabezado)

        tabla_encabezado.setStyle(TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]
        ))
        return tabla_encabezado

    def tabla_titulo_main(self, styles):

        titulo = Paragraph(u"CONSTANCIA DE PAGO DE HABERES Y DESCUENTOS DE LEY", sp)
        espacio = Spacer(1, 12)
        encabezado = [[titulo], [espacio]]
        tabla_encabezado = Table(encabezado, rowHeights=ROW_HEIGHT)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_trabajador(self, styles):

        trabajador = self.constancia['trabajador']
        anio = self.constancia['anio']

        nivel = " -- "
        if self.constancia['constancia'].nivel:
            nivel = self.constancia['constancia'].nivel

        plaza = " -- "
        if self.constancia['constancia'].plaza:
            plaza = self.constancia['constancia'].plaza

        data = [
            [Paragraph(u"APELLIDOS Y NOMBRES", sp_justifi_title_table),
             Paragraph(u": " + trabajador.nombre_completo, sp_justifi_title_table),
             Paragraph(u"NIVEL", sp_justifi_title_table_2 ),
             Paragraph(u": " + nivel, sp_justifi_title_table)],
            [Paragraph(u"ESTABLECIMIENTO", sp_justifi_title_table),
             Paragraph(u": " + get_establecimiento(self.anio_bd, trabajador.id, anio.id), sp_justifi_title_table), "",
             ""],
            [Paragraph(u"CARGO", sp_justifi_title_table),
             Paragraph(u": " + get_cargo(self.anio_bd, trabajador.id, anio.id), sp_justifi_title_table),
             Paragraph(u"PLAZA", sp_justifi_title_table),
             Paragraph(u": " + plaza, sp_justifi_title_table)],
            [Paragraph(u"PERIODO", sp_justifi_title_table),
             Paragraph(u": " + str(anio.anio), sp_justifi_title_table), "", ""],
        ]

        tabla = Table(data, colWidths=[4 * cm, 12 * cm, 1.5 * cm, 10 * cm], rowHeights=ROW_HEIGHT)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_ingresos(self, styles):

        data_title = [
            [Paragraph(u"INGRESOS", sp_justifi_title_header), "", "", "", "", "", "", "", "", "", "", "", "", ""],
            [
                Paragraph(u"CONCEPTO", sp_justifi_title_header),
                Paragraph(u"ENERO", sp_justifi_title_header),
                Paragraph(u"FEBRERO", sp_justifi_title_header),
                Paragraph(u"MARZO", sp_justifi_title_header),
                Paragraph(u"ABRIL", sp_justifi_title_header),
                Paragraph(u"MAYO", sp_justifi_title_header),
                Paragraph(u"JUNIO", sp_justifi_title_header),
                Paragraph(u"JULIO", sp_justifi_title_header),
                Paragraph(u"AGOSTO", sp_justifi_title_header),
                Paragraph(u"SETIEMBRE", sp_justifi_title_header),
                Paragraph(u"OCTUBRE", sp_justifi_title_header),
                Paragraph(u"NOVIEMBRE", sp_justifi_title_header),
                Paragraph(u"DICIEMBRE", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
            ],
        ]

        data_body = []
        for object in self.constancia['monto_ingreso_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0], sp_justifi_title_header),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[1].monto) if object[1] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[2].monto) if object[2] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[3].monto) if object[3] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[4].monto) if object[4] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[5].monto) if object[5] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[6].monto) if object[6] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[7].monto) if object[7] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[8].monto) if object[8] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[9].monto) if object[9] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[10].monto) if object[10] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[11].monto) if object[11] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[12].monto) if object[12] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object[13]), sp_justifi_title_body)
                ]
            )

        data_total = []

        for index, object in enumerate(self.constancia['monto_ingreso_list_total']):
            if index == 0:
                data_total.append(Paragraph(u"" + object, sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title + data_body, rowHeights=ROW_HEIGHT)
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (0, 0), (-1, 0)),
                ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (1, 1), (-1, -1), 8),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ]
        ))
        return tabla

    def tabla_descuentos(self, styles):

        data_title = [
            [Paragraph(u"DESCUENTOS DE LEY", sp_justifi_title_header), "", "", "", "", "", "", "", "", "", "", "", "",
             ""],
            [
                Paragraph(u"CONCEPTO", sp_justifi_title_header),
                Paragraph(u"ENERO", sp_justifi_title_header),
                Paragraph(u"FEBRERO", sp_justifi_title_header),
                Paragraph(u"MARZO", sp_justifi_title_header),
                Paragraph(u"ABRIL", sp_justifi_title_header),
                Paragraph(u"MAYO", sp_justifi_title_header),
                Paragraph(u"JUNIO", sp_justifi_title_header),
                Paragraph(u"JULIO", sp_justifi_title_header),
                Paragraph(u"AGOSTO", sp_justifi_title_header),
                Paragraph(u"SETIEMBRE", sp_justifi_title_header),
                Paragraph(u"OCTUBRE", sp_justifi_title_header),
                Paragraph(u"NOVIEMBRE", sp_justifi_title_header),
                Paragraph(u"DICIEMBRE", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
            ],
        ]

        data_body = []
        for object in self.constancia['monto_descuento_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0], sp_justifi_title_header),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[1].monto) if object[1] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[2].monto) if object[2] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[3].monto) if object[3] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[4].monto) if object[4] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[5].monto) if object[5] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[6].monto) if object[6] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[7].monto) if object[7] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[8].monto) if object[8] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[9].monto) if object[9] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[10].monto) if object[10] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[11].monto) if object[11] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[12].monto) if object[12] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object[13]), sp_justifi_title_body)
                ]
            )

        data_total = []

        for index, object in enumerate(self.constancia['monto_descuento_list_total']):
            if index == 0:
                data_total.append(Paragraph(u"" + object, sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title + data_body, rowHeights=ROW_HEIGHT)
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (0, 0), (-1, 0)),
                ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (1, 1), (-1, -1), 8),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
            ]
        ))
        return tabla

    def tabla_liquido(self, styles):

        data_title = [
            [Paragraph(u"LIQUIDO", sp_justifi_title_header), "", "", "", "", "", "", "", "", "", "", "", "",
             ""],
            [
                Paragraph(u"CONCEPTO", sp_justifi_title_header),
                Paragraph(u"ENERO", sp_justifi_title_header),
                Paragraph(u"FEBRERO", sp_justifi_title_header),
                Paragraph(u"MARZO", sp_justifi_title_header),
                Paragraph(u"ABRIL", sp_justifi_title_header),
                Paragraph(u"MAYO", sp_justifi_title_header),
                Paragraph(u"JUNIO", sp_justifi_title_header),
                Paragraph(u"JULIO", sp_justifi_title_header),
                Paragraph(u"AGOSTO", sp_justifi_title_header),
                Paragraph(u"SETIEMBRE", sp_justifi_title_header),
                Paragraph(u"OCTUBRE", sp_justifi_title_header),
                Paragraph(u"NOVIEMBRE", sp_justifi_title_header),
                Paragraph(u"DICIEMBRE", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
            ],
        ]

        data_body = []

        data_total = []

        for index, object in enumerate(self.constancia['monto_liquido_list_total']):
            if index == 0:
                data_total.append(Paragraph(u"" + object, sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title + data_body, rowHeights=ROW_HEIGHT)
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (0, 0), (-1, 0)),
                ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (1, 1), (-1, -1), 8),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
            ]
        ))
        return tabla

    def tabla_aportaciones(self, styles):

        data_title = [
            [Paragraph(u"APORTACIONES", sp_justifi_title_header), "", "", "", "", "", "", "", "", "", "", "", "",
             ""],
            [
                Paragraph(u"CONCEPTO", sp_justifi_title_header),
                Paragraph(u"ENERO", sp_justifi_title_header),
                Paragraph(u"FEBRERO", sp_justifi_title_header),
                Paragraph(u"MARZO", sp_justifi_title_header),
                Paragraph(u"ABRIL", sp_justifi_title_header),
                Paragraph(u"MAYO", sp_justifi_title_header),
                Paragraph(u"JUNIO", sp_justifi_title_header),
                Paragraph(u"JULIO", sp_justifi_title_header),
                Paragraph(u"AGOSTO", sp_justifi_title_header),
                Paragraph(u"SETIEMBRE", sp_justifi_title_header),
                Paragraph(u"OCTUBRE", sp_justifi_title_header),
                Paragraph(u"NOVIEMBRE", sp_justifi_title_header),
                Paragraph(u"DICIEMBRE", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
            ],
        ]

        data_body = []
        for object in self.constancia['monto_aportaciones_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0], sp_justifi_title_header),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[1].monto) if object[1] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[2].monto) if object[2] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[3].monto) if object[3] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[4].monto) if object[4] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[5].monto) if object[5] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[6].monto) if object[6] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[7].monto) if object[7] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[8].monto) if object[8] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[9].monto) if object[9] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[10].monto) if object[10] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[11].monto) if object[11] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" +
                              '{:,.2f}'.format(object[12].monto) if object[12] != " " else " ", sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object[13]), sp_justifi_title_body)
                ]
            )

        data_total = []

        for index, object in enumerate(self.constancia['monto_aportaciones_list_total']):
            if index == 0:
                data_total.append(Paragraph(u"" + object, sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title + data_body, rowHeights=ROW_HEIGHT)
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (0, 0), (-1, 0)),
                ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (1, 1), (-1, -1), 8),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
            ]
        ))
        return tabla

    def tabla_footer(self, styles):

        data = [
            [Paragraph(u"CCG-LIQUIDACIONES, OFICINA DE TESORERÍA", sp_footer)],
        ]

        tabla = Table(data)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def imprimir(self):
        buffer = self.buffer
        lWidth, lHeight = A4

        doc = SimpleDocTemplate(buffer,
                                rightMargin=25,
                                leftMargin=25,
                                topMargin=0,
                                bottomMargin=15,
                                pagesize=(lHeight, lWidth))

        doc.title = "HABERES: " + self.constancia['trabajador'].nombre_completo

        elements = []
        styles = getSampleStyleSheet()
        elements.append(self.tabla_encabezado(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_titulo_main(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_trabajador(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_ingresos(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_descuentos(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_liquido(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_aportaciones(styles))
        elements.append(Spacer(1, 0 * cm))
        elements.append(self.tabla_footer(styles))
        elements.append(Spacer(1, 0.15 * cm))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


def print_constancia_pdf(request):
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')

    trabajador_id = request.GET.get('trabajador_id', 1)
    anio_id = request.GET.get('anio_id', 1)
    pk = request.GET.get('pk', 1)

    constancia = generar_constancia(request, pk)
    reporte = ReportSimulator('A4', constancia, request.session["anio_bd"])

    from datetime import date
    today = date.today()
    pdf_name = "CONSTANCIA_" + str(today) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    pdf = reporte.imprimir()
    response.write(pdf)
    return response
