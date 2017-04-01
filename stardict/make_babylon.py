# This Python file uses the following encoding: utf-8
"""
Usage:
python make_babylon.py pathToDicts
e.g.
python make_babylon.py ../../Cologne_localcopy
"""
import re,codecs,sys
from lxml import etree
import transcoder
	
def add_tags1(x):
	global prevsutra
	m = re.search(u'^(.*)॥([१२३४५६७८९०। /-]*)॥',x)
	sutra = m.group(1).strip()
	num = m.group(2).strip()
	current_sutra = num.split(u'।')
	print current_sutra
	if len(current_sutra) != 3:
		print current_sutra
		prevsutra = current_sutra
		exit(0)
	result = '\n\n'+num+'|'+sutra+'|'+sutra+' '+num+'|'+num+' '+sutra+'\n'+sutra+' '+num+' <BR> '
	result = result.replace(u'।','.')
	return result

	
	

if __name__=="__main__":
	pathToDicts = sys.argv[1]
	dictList = ['acc','ae','ap','ap90','ben','bhs','bop','bor','bur','bur','cae','ccs','gra','gst','ieg','inm','krm','mci','md','mw','mw72','mwe','pd','pe','pgn','pui','pw','pwg','sch','shs','skd','snp','stc','vcp','vei','wil','yat']
	dictList = ['md']
	for dictId in dictList:
		inputfile = pathToDicts+'/'+dictId+'/'+dictId+'xml/xml/'+dictId+'.xml'
		tree = etree.parse(inputfile)
		hw = tree.xpath("/"+dictId+"/H1/h/key1")
		entry =  tree.xpath("/"+dictId+"/H1/body")
		outputfile = codecs.open('output/'+dictId+'.babylon','w','utf-8')
		for x in xrange(len(hw)):
			heading = etree.tostring(hw[x], method='text', encoding='utf-8')
			print heading
			heading = transcoder.transcoder_processString(heading,'slp1','deva')
			text = etree.tostring(entry[x], method='text', encoding='utf-8')
			html = etree.tostring(entry[x], method='html', encoding='utf-8')
			html = html.decode('utf-8')
			sanskrittext = re.findall('<s>([^<]*)</s>',html)
			for sans in sanskrittext:
				html = html.replace('<s>'+sans+'</s>','<s>'+transcoder.transcoder_processString(sans,'slp1','deva')+'</s>')
			#html = transcoder.transcoder_processString(html,'as','roman')
			html = re.sub('[<][^>]*[>]','',html)
			outputfile.write(heading+'\n')
			outputfile.write(html+'\n\n')
		outputfile.close()
		