"""Render the editable planning guide; requires reportlab."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
root=Path(__file__).resolve().parents[1]/'Planning Guide'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodySmall',fontName='Helvetica',fontSize=9,leading=11.5,spaceAfter=4))
styles.add(ParagraphStyle(name='MonoSmall',fontName='Courier',fontSize=8,leading=10,spaceAfter=7))
styles['Heading1'].fontSize=21
styles['Heading1'].leading=25
styles['Heading2'].fontSize=12
styles['Heading2'].leading=15
styles['Heading3'].fontSize=11
story=[]
lines=(root/'how to make a code plan.md').read_text().splitlines()
i=0
while i<len(lines):
    line=lines[i];i+=1
    if not line.strip(): continue
    if line=='<!-- page -->': story.append(PageBreak());continue
    if line.startswith('```'):
        code=[]
        while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
        i+=1;story.append(Preformatted('\n'.join(code),styles['MonoSmall']));continue
    if line.startswith('|'):
        rows=[line]
        while i<len(lines) and lines[i].startswith('|'):rows.append(lines[i]);i+=1
        rows=[r for r in rows if not r.startswith('| ---')]
        data=[[Paragraph(escape(c.strip()),styles['BodySmall']) for c in r.strip('|').split('|')] for r in rows]
        table=Table(data,colWidths=[70,170,276],repeatRows=1)
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcecf4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd8df')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
        story.extend([table,Spacer(1,8)]);continue
    level=len(line)-len(line.lstrip('#'))
    style=styles['Heading'+str(min(level,3))] if level else styles['BodySmall']
    text=line.lstrip('# ').replace('\u2013','-').replace('\u2014','-')
    story.append(Paragraph(escape(text),style))
def footer(canvas,doc):
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#607485'))
    canvas.drawString(48,25,'AI BUILDER  /  PLANNING HANDOFF')
    canvas.drawRightString(564,25,str(doc.page))
SimpleDocTemplate(str(root/'how to make a code plan.pdf'),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=38,bottomMargin=40,title='How to make a code plan').build(story,onFirstPage=footer,onLaterPages=footer)
