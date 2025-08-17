import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, TableStyle
from reportlab.platypus import Table
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.flowables import Spacer

from apps.remuneracion.models.remuneracion import Remuneracion
from apps.remuneracion.models.trabajador import Trabajador


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
                    fontSize=14,
                    fontName="Times-Roman")

sp_subtitle = ParagraphStyle('parrafos',
                             alignment=TA_CENTER,
                             fontSize=8,
                             fontName="Times-Roman")

sp_justifi_title_table = ParagraphStyle('parrafos',
                                        alignment=TA_JUSTIFY,
                                        fontSize=10,
                                        fontName="Times-Roman")

sp_justifi_title_table_center = ParagraphStyle('parrafos',
                                               alignment=TA_CENTER,
                                               fontSize=10,
                                               fontName="Times-Roman")

sp_justifi_title_header = ParagraphStyle('parrafos',
                                         alignment=TA_CENTER,
                                         fontSize=7,
                                         # leading=10,
                                         fontName="Times-Roman")

sp_justifi_title_body = ParagraphStyle('parrafos',
                                       alignment=TA_RIGHT,
                                       fontSize=7,
                                       # leading=10,
                                       fontName="Times-Roman")


class ReportSimulator():
    # tea = Tea.objects.get(pk=1)

    def __init__(self, pagesize, trabajador, remuneraciones):

        self.trabajador = trabajador
        self.remuneraciones = remuneraciones

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
                                 fontSize=10,
                                 fontName="Times-Roman",
                                 )
        # sp = ParagraphStyle('parrafos',
        #                     alignment=TA_CENTER,
        #                     fontSize=16,
        #                     fontName="Times-Roman",
        #                     )
        try:
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/logo_remuneracion.png")
            archivo_diris = os.path.join(settings.STATIC_LOCAL_ROOT, "img/logo_remuneracion.png")
            imagen = Image(archivo_imagen, width=220, height=40)
            # imagen_canchis = Image(archivo_diris, width=100, height=100, hAlign='RIGHT')
        except:
            imagen = Paragraph(u"LOGO", sp)

            imagen_canchis = Paragraph(u"LOGO_CANCHIS", sp)

        # nro = Paragraph(
        #     u"APOLINAR <br/> CONSTRUCTORA S.A.C <br/><br/>Cotización de Lote<br/>",
        #     sp)
        date_ = Paragraph(
            u"" + now.strftime("%d/%m/%Y") + " <br/> " + now.strftime("%H:%M:%S") + "<br/> <br/> <br/> ", sp_date)
        encabezado = [[imagen, "", date_]]
        tabla_encabezado = Table(encabezado)

        tabla_encabezado.setStyle(TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                # ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.1, colors.black),

                # ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                # ('VALIGN', (0, 0), (2, 0), 'CENTER'),
                # ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
            ]
        ))
        return tabla_encabezado

    def tabla_titulo_main(self, styles):

        titulo = Paragraph(u"MINISTERIO DE SALUD", sp)
        titulo_oficina = Paragraph(u"Ofic. Gral. de Recursos Humanos", sp_subtitle)
        encabezado = [[titulo], [titulo_oficina]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_sub_titulo_main(self, styles):

        titulo = Paragraph(u"CONSTANCIA DE REMUNERACIONES Y RETENCIONES EFECTUADOS <br/>"
                           u"POR IMPUESTO A LA 5TA. CATEGORIA PERIODO DEL 2020 <br/>"
                           u"D.S. N° 179-2004-EF Art° 71  ", sp_justifi_title_table_center)
        encabezado = [[titulo]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_trabajador(self, styles):

        data = [
            [Paragraph(u"APELLIDOS Y NOMBRES", sp_justifi_title_table),
             Paragraph(u": " + self.trabajador.apellidos_nombres, sp_justifi_title_table)],
            [Paragraph(u"NUMERO DE PLAZA", sp_justifi_title_table),
             Paragraph(u": " + str(self.trabajador.plaza), sp_justifi_title_table)],
            [Paragraph(u"CARGO", sp_justifi_title_table),
             Paragraph(u": " + self.trabajador.cargo, sp_justifi_title_table)],
            [Paragraph(u"ENTIDAD EJECUTORA", sp_justifi_title_table),
             Paragraph(u": " + self.trabajador.depedencia.entidad_ejecutora.nombre, sp_justifi_title_table)],
            [Paragraph(u"DEPENDENCIA", sp_justifi_title_table),
             Paragraph(u": " + self.trabajador.depedencia.nombre, sp_justifi_title_table)],
            [Paragraph(u"TIPO DE TRABAJADOR", sp_justifi_title_table),
             Paragraph(u": " + self.trabajador.get_tipo_display(), sp_justifi_title_table)],
        ]

        tabla = Table(data, colWidths=[5 * cm, 12 * cm])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_remuneraciones(self, styles):

        data_title = [
            [
                Paragraph(u"MESES", sp_justifi_title_header),
                Paragraph(u"INGRESOS", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u"RETENCION <br/> X EFECTUAR", sp_justifi_title_header),
                Paragraph(u"RETENCIONES", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u"TOTAL  A PAGAR <br/> O DEVOLVER", sp_justifi_title_header)
            ],
            [
                Paragraph(u" ", sp_justifi_title_header),
                Paragraph(u"REMU/V.P.", sp_justifi_title_header),
                Paragraph(u"OTRAS UE", sp_justifi_title_header),
                Paragraph(u"OTROS", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
                Paragraph(u"", sp_justifi_title_header),
                Paragraph(u"REMU/V.P.", sp_justifi_title_header),
                Paragraph(u"ADICIONAL", sp_justifi_title_header),
                Paragraph(u"OTROS", sp_justifi_title_header),
                Paragraph(u"TOTAL", sp_justifi_title_header),
                Paragraph(u"", sp_justifi_title_header)
            ],
        ]

        data_body = []

        for object in self.remuneraciones:
            for item in object.detalleremuneracion_set.all():
                data_body.append(
                    [
                        Paragraph(u"" + item.get_mes_display(), sp_justifi_title_header),
                        Paragraph(u"" + '{:,.2f}'.format(item.ingresos_remu_v_p), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.ingresos_otras_ue), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.ingresos_otros), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.ingresos_total), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.retencion_efectuar), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.retencion_remu_v_p), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.retencion_adicional), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.retencion_otros), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.retencion_total), sp_justifi_title_body),
                        Paragraph(u"" + '{:,.2f}'.format(item.total_pagar), sp_justifi_title_body),
                    ]
                )
            data_body.append(
                [
                    Paragraph(u"TOTAL", sp_justifi_title_header),
                    Paragraph(u"" + '{:,.2f}'.format(object.ingresos_remu_v_p), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.ingresos_otras_ue), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.ingresos_otros), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.ingresos_total), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.retencion_efectuar), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.retencion_remu_v_p), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.retencion_adicional), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.retencion_otros), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.retencion_total), sp_justifi_title_body),
                    Paragraph(u"" + '{:,.2f}'.format(object.total_pagar), sp_justifi_title_body),
                ]
            )

        tabla = Table(data_title + data_body)
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (0, 0), (0, 1)),
                ('SPAN', (1, 0), (0, 0)),
                ('SPAN', (5, 0), (5, 1)),
                ('SPAN', (6, 0), (9, 0)),
                ('SPAN', (10, 0), (10, 1)),
                ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                # ('GRID', (0, 1), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (-1, -1), 1),

                ('RIGHTPADDING', (1, 1), (-1, -1), 8),
            ]
        ))
        return tabla

    def tabla_footer(self, styles):

        data = [
            [Paragraph(u"Elaborado: Equipo de Remuneraciones-MINSA", sp_justifi_title_table)],
            [Paragraph(u" ", sp_justifi_title_table)],
            [Paragraph(
                u"PUEDEN EXISTIR DIFERENCIAS ENTRE ESTA CONSTANCIA CON LO REALMENTE PERCIBIDO, DEBIDO A LOS "
                u"AJUSTES EFECTUADOS POR LAS OFICINAS PAGADORAS DE LAS UNIDADES EJECUTORAS DEL SECTOR, QUIENES "
                u"DEBEN HACER LAS CORRECCIONES PERTINENTES ANTE LA SUNAT. ",
                sp_justifi_title_table)],
        ]

        tabla = Table(data)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_firma(self, styles):

        try:
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/firma.png")
            imagen = Image(archivo_imagen, width=200, height=120)
        except:
            imagen = Paragraph(u"LOGO", sp)

        encabezado = [[imagen]]
        tabla_encabezado = Table(encabezado)

        # tabla_encabezado.setStyle(TableStyle(
        #     [
        #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #     ]
        # ))
        return tabla_encabezado

    def imprimir(self):
        buffer = self.buffer
        lWidth, lHeight = A4

        doc = SimpleDocTemplate(buffer,
                                rightMargin=25,
                                leftMargin=25,
                                topMargin=15,
                                bottomMargin=15,
                                pagesize=(lWidth, lHeight))

        elements = []
        styles = getSampleStyleSheet()
        elements.append(self.tabla_encabezado(styles))
        elements.append(Spacer(1, 1 * cm))
        elements.append(self.tabla_titulo_main(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_sub_titulo_main(styles))
        elements.append(Spacer(1, 1 * cm))
        elements.append(self.tabla_trabajador(styles))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(self.tabla_remuneraciones(styles))
        elements.append(Spacer(1, 0.1 * cm))
        elements.append(self.tabla_footer(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_firma(styles))
        elements.append(Spacer(1, 0.25 * cm))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


def print_simulator(request):
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')

    trabajador_id = request.session['trabajador_id']

    trabajador = Trabajador.objects.get(pk=trabajador_id)
    remuneraciones = Remuneracion.objects.filter(trabajador=trabajador)

    reporte = ReportSimulator('A4', trabajador, remuneraciones)

    from datetime import date
    today = date.today()
    pdf_name = "REMUNERACION_" + str(today) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    pdf = reporte.imprimir()
    response.write(pdf)
    return response
