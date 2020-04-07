import xml.dom.minidom

def parse_xmp_for_lightroom_tags(xmp_string):
    data = {}
    data['rating'] = 0
    data['tags'] = []
    xmlDocument = xml.dom.minidom.parseString(xmp_string)
    xmp = xmlDocument.documentElement
    if xmp.hasAttribute('xmlns:x'):
        if xmp.getAttribute('xmlns:x') == 'adobe:ns:meta/':
            # this is adobe meta data so continue
            try:
                rdf = xmp.getElementsByTagName('rdf:RDF')[0]
                descArray = rdf.getElementsByTagName('rdf:Description')
                for desc in descArray:
                    ratingElement = desc.getElementsByTagName('xmp:Rating')
                    if len(ratingElement) > 0:
                        rating = ratingElement[0].firstChild.nodeValue
                        data['rating'] = int(rating)
                
                    subjects = desc.getElementsByTagName('dc:subject')
                    if len(subjects) > 0:
                        bags = subjects[0].getElementsByTagName('rdf:Bag')
                        if len(bags) > 0:
                            lightroomTags = bags[0].getElementsByTagName('rdf:li')
                            tagsCombinedArray = []
                            for tags in lightroomTags:
                                tag = tags.firstChild.nodeValue
                                #print(tag)
                                tagsCombinedArray.append(tag)
                            if len(tagsCombinedArray):
                                data['tags'] = tagsCombinedArray
            except:
                # no description
                # print("the image has no valid ligthroom tags")
                pass

    return data