from urllib2 import urlopen
import xml.etree.ElementTree as ET
dictUrl = 'http://services.aonaware.com/DictService/DictService.asmx/DefineInDict?dictId=gcide&word='
namespace = '{http://services.aonaware.com/webservices/}'
def getPast(verb):
    xml = urlopen(dictUrl + verb).read()
    print xml
    tree = ET.fromstring(xml)
    print tree[1]
    text = ''
    for node in tree.iter(namespace + 'WordDefinition'):
        text = node.text
        if len(node.text) > 5:  # real def, not start tag
            text = node.text
            break
    i = text.find('[imp. {')
    return text

getPast('run')
