from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

can.setFont("Helvetica", 8)
can.drawString(0.83*inch, 9.4*inch, "Aditya Jain")
can.drawString(0.83*inch, 9.25*inch, "Spitalhofstrasse 91")
can.drawString(0.83*inch, 9.1*inch, "94032 Passau")

can.setFont("Helvetica", 10)
can.drawRightString(7.6*inch, 8.6*inch, "14.03.2022")
can.drawRightString(7.6*inch, 8.44*inch, "12072")
can.drawRightString(7.6*inch, 8.29*inch, "202200894")
can.drawRightString(7.6*inch, 8.14*inch, "1")


can.drawString(0.89*inch, 6.87*inch, "1 x")
can.drawString(1.2*inch, 6.87*inch, "Services")
can.drawString(1.2*inch, 6.7*inch, "Services rendered")
can.drawString(1.2*inch, 6.55*inch, "2022-02")

can.drawString(5.6*inch, 6.87*inch, "19%")
can.drawString(6.13*inch, 6.87*inch, "100,00 €")
can.drawString(7.1*inch, 6.87*inch, "100,00 €")

can.line(50, 437, 560, 437)
can.drawRightString(7.7*inch, 5.8*inch, "100,00 €")
can.drawRightString(6.7*inch, 5.8*inch, "Netto-Summe:")
can.drawRightString(6.7*inch, 5.6*inch, "zzgl. 19% MwSt. auf 100,00 €:")
can.drawRightString(7.7*inch, 5.6*inch, "19,00 €")
can.drawRightString(6.7*inch, 5.4*inch, "Gesamtbetrag Brutto:")
can.drawRightString(7.7*inch, 5.4*inch, "119,00 €")

can.setFont("Helvetica", 12)
can.drawString(80, 530, "Ihre Rechnung") ## Rechnung No
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("templates/pdftemplate.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("templates/rechnung.pdf", "wb")
output.write(outputStream)
outputStream.close()