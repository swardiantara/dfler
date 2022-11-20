
from fpdf import FPDF, HTMLMixin
from datetime import datetime
import pandas as pd


class CustomPDF(FPDF):
  def header(self):
    # Set up a logo
    self.image('drone-png-47009.png', 10, 8, 33)
    self.set_font('Helvetica', 'B', 15)
    # Add an address
    self.cell(100)
    self.cell(0, 5, 'Mike Driscoll', ln=1)
    self.cell(100)
    self.cell(0, 5, '123 American Way', ln=1)
    self.cell(100)
    self.cell(0, 5, 'Any Town, USA', ln=1)
    # Line break
    self.ln(20)

  def footer(self):
    date = datetime.now()
    # date_time_obj = datetime.strptime(str(date), '%Y-%m-%d, %H:%M:%S')
    date_time = 'Generated on: ' +  date.strftime("%m/%d/%Y, %H:%M:%S")
    self.set_y(-10)
    self.set_font('Helvetica', 'I', 8)
    # Add a page number
    page = 'Page ' + str(self.page_no()) + '/{nb}'
    self.cell(0, 10, date_time, 0, 0, 'L')
    self.cell(0, 10, page, 0, 0, 'C')


def create_pdf(pdf_path):
  pdf = CustomPDF()
  # Create the special value {nb}
  pdf.alias_nb_pages()
  pdf.add_page()
  pdf.set_font('Times', '', 12)
  col_width = pdf.w / 4.5
  col_width2 = pdf.w / 2.2
  row_height = pdf.font_size
  spacing = 1.5

  timeline = pd.read_csv('sample_timeline.csv', encoding='utf-8')
  for row in range(timeline.shape[0]):
    for col in range(timeline.shape[1]):
      if col == 0:
        pdf.cell(col_width, row_height*spacing, txt=timeline.iloc[row, col], border=1)
      elif col == 1:
        pdf.cell(col_width, row_height*spacing, txt=timeline.iloc[row, col], border=1)
      else:
        pdf.multi_cell(col_width2, row_height*spacing, txt=timeline.iloc[row, col], border=1)
    # pdf.ln(row_height*spacing)
  pdf.output(pdf_path)
