"""Remove exporter attribution and generic theme branding from authored decks."""
import sys,zipfile
from pathlib import Path
from lxml import etree as ET
for arg in sys.argv[1:]:
 p=Path(arg);tmp=p.with_suffix('.scrub.pptx')
 with zipfile.ZipFile(p) as src,zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as dst:
  for item in src.infolist():
   data=src.read(item.filename)
   if item.filename=='docProps/core.xml':
    tree=ET.fromstring(data)
    for element in tree:
     if ET.QName(element).localname in ('creator','lastModifiedBy'):element.text=''
     if ET.QName(element).localname=='title':element.text=p.stem
    data=ET.tostring(tree,xml_declaration=True,encoding='UTF-8')
   elif item.filename=='docProps/app.xml':
    tree=ET.fromstring(data)
    for element in tree.iter():
     if ET.QName(element).localname in ('Application','Company'):element.text=''
    data=ET.tostring(tree,xml_declaration=True,encoding='UTF-8')
   elif item.filename.startswith('ppt/theme/') and item.filename.endswith('.xml'):
    data=data.replace(b'ChatGPT',b'Course').replace(b'OpenAI',b'Course')
   dst.writestr(item,data)
 tmp.replace(p)
