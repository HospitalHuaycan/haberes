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
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY, TA_LEFT
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

sp_concepto = ParagraphStyle('concepto',
                            alignment=TA_LEFT,
                            fontSize=6,
                            leading=7,
                            fontName="Times-Roman",
                            splitLongWords=True,
                            breakLongWords=True,
                            wordWrap='LTR')

ROW_HEIGHT = 3.5 * mm
CABECERAS = [   Paragraph(u"CODIGO", sp_justifi_title_header),
                Paragraph(u"CONCEPTO", sp_concepto),
                Paragraph(u"ENE", sp_justifi_title_header),
                Paragraph(u"FEB", sp_justifi_title_header),
                Paragraph(u"MAR", sp_justifi_title_header),
                Paragraph(u"ABR", sp_justifi_title_header),
                Paragraph(u"MAY", sp_justifi_title_header),
                Paragraph(u"JUN", sp_justifi_title_header),
                Paragraph(u"JUL", sp_justifi_title_header),
                Paragraph(u"AGO", sp_justifi_title_header),
                Paragraph(u"SET", sp_justifi_title_header),
                Paragraph(u"OCT", sp_justifi_title_header),
                Paragraph(u"NOV", sp_justifi_title_header),
                Paragraph(u"DIC", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header)]

# Obtener el ancho total de la página
PAGE_WIDTH, PAGE_HEIGHT = A4

# Calcular el ancho total que ocupará la tabla
TABLE_WIDTH = PAGE_WIDTH - 22  # Un margen de 20 puntos en cada lado

# Definir proporciones para las columnas (ajustando la segunda columna a un tamaño mayor)
COL_WIDTHS = [TABLE_WIDTH * 0.06, TABLE_WIDTH * 0.40, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07,
            TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07,
            TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07, TABLE_WIDTH * 0.07]


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
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/LogoInforme.jpg")
            huaycan_png = os.path.join(settings.STATIC_LOCAL_ROOT, "img/huaycan.png")
            imagen = Image(archivo_imagen, width=350, height=50)
            logo_huaycan = Image(huaycan_png, width=100, height=50)
            # imagen_canchis = Image(archivo_diris, width=100, height=100, hAlign='RIGHT')
        except:
            imagen = Paragraph(u"LOGO", sp_concepto)
            logo_huaycan = Paragraph(u"LOGO HUAYCAN", sp_date)

        date_ = Paragraph(
            u"" + now.strftime("%d/%m/%Y") + " <br/> " + now.strftime("%H:%M:%S") + "<br/> <br/> <br/> ", sp_date)
        encabezado = [[imagen, "", logo_huaycan]]
        tabla_encabezado = Table(encabezado,colWidths=[TABLE_WIDTH * 0.6,TABLE_WIDTH * 0.4,TABLE_WIDTH * 0.4])

        tabla_encabezado.setStyle(TableStyle(
            [
                # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Fondo gris en la última celda (logo derecho)
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Fondo gris en la última celda (logo derecho)
                # ('BACKGROUND', (2, 0), (2, 0), colors.grey),  # Fondo gris en la última celda (logo derecho)
                # ('BACKGROUND', (1, 0), (1, 0), colors.lightblue),  # Fondo gris en la última celda (logo derecho)
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
            CABECERAS
        ]

        data_body = []
        for object in self.constancia['monto_ingreso_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0].codcon, sp_justifi_title_header),
                    Paragraph(u"" + object[0].descon, sp_concepto),
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
                data_total.append(Paragraph("", sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title+data_body, colWidths=COL_WIDTHS, rowHeights=ROW_HEIGHT)
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
            CABECERAS,
        ]

        data_body = []
        for object in self.constancia['monto_descuento_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0].codcon, sp_justifi_title_header),
                    Paragraph(u"" + object[0].descon, sp_concepto),
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
                data_total.append(Paragraph("", sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title+data_body, colWidths=COL_WIDTHS, rowHeights=ROW_HEIGHT)
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
            CABECERAS,
        ]

        data_body = []

        data_total = []

        for index, object in enumerate(self.constancia['monto_liquido_list_total']):
            if index == 0:
                data_total.append(Paragraph(u"" + object, sp_justifi_title_header))
                data_total.append(Paragraph("", sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title+data_body, colWidths=COL_WIDTHS, rowHeights=ROW_HEIGHT)
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
            CABECERAS,
        ]

        data_body = []
        for object in self.constancia['monto_aportaciones_list']:
            data_body.append(
                [
                    Paragraph(u"" + object[0].codcon, sp_justifi_title_header),
                    Paragraph(u"" + object[0].descon, sp_concepto),
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
                data_total.append(Paragraph("", sp_justifi_title_header))
            else:
                data_total.append(Paragraph(u"" + '{:,.2f}'.format(object), sp_justifi_title_body))

        data_body.append(data_total)

        tabla = Table(data_title+data_body, colWidths=COL_WIDTHS, rowHeights=ROW_HEIGHT)
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
        now = datetime.now()
        sp_date = ParagraphStyle('parrafos',
                                 alignment=TA_RIGHT,
                                 fontSize=8,
                                 fontName="Times-Roman",
                                 )
        date_ = Paragraph(u"" + now.strftime("%d/%m/%Y") + " <br/> " + now.strftime("%H:%M:%S") + "<br/> ", sp_date)

        data = [
            [Paragraph(u"Fuente: Planilla Unica de Pago de Haberes<br/>" +
                       "Los funcionarios que firman al pie del presente declaran bajo responsabilidad que la liquidacion presente es veraz y está respaldada por las planillas de pago.",
                       sp_footer),
             date_],
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
                                rightMargin=20,
                                leftMargin=20,
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

    trabajador_id = request.GET.get('trabajador_id', 1)
    anio_id = request.GET.get('anio_id', 1)
    pk = request.GET.get('pk', 1)

    constancia = generar_constancia(request, pk)
    reporte = ReportSimulator('A4', constancia, request.session["anio_bd"])

    # El método imprimir() DEBE devolver un objeto bytes (o BytesIO).
    pdf_bytes = reporte.imprimir()

    response = HttpResponse(pdf_bytes, content_type='application/pdf') # Pasar los bytes directamente aquí

    from datetime import date
    today = date.today()
    pdf_name = "CONSTANCIA_" + str(today) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    # Ya no necesitas response.write(pdf), ya que los bytes se pasaron en la inicialización
    return response