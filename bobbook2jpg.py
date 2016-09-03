import sys, os.path
from bs4 import BeautifulSoup
from PIL import Image

filename = sys.argv[1]
imgFolder = sys.argv[2]
outFolder = sys.argv[3]
colorMap = {
    'Weiss,normal,': (255,255,255,255),
    'Schwarz,normal,': (0,0,0,255)
}

soup = BeautifulSoup(open(filename), 'xml')
for page in soup.find_all('page'):
    if page['type'] not in ['normalpage','emptypage']: continue

    pageNumber=int(page['pagenr'])
    pageHeight = int(page.bundlesize['height'])
    pageWidth = int(page.bundlesize['width'])
    pageColor = colorMap[page.background['templatename']]
    pageImg = Image.new('RGBA', (pageWidth, pageHeight), pageColor)
    pageIsEmpty=True
    print('Processing page {}...'.format(pageNumber))

    for area in page.find_all('area'):
        pageIsEmpty=False
        left = float(area['left'])
        top = float(area['top'])
        width = float(area['width'])
        height = float(area['height'])

        print('  Adding '+area.image['filename'])
        img = Image.open(imgFolder+'/'+area.image['filename'])
        scale = float(area.image['scale'])
        imgLeft = float(area.image['left'])*-1
        imgTop = float(area.image['top'])*-1
        imgWidth = width/scale
        imgHeight = height/scale

        img = img.crop((imgLeft, imgTop, imgLeft+imgWidth, imgTop+imgHeight))
        img = img.resize((int(width), int(height)))
        pageImg.paste(img, (int(left), int(top), int(left)+int(width), int(top)+int(height)))

    if pageIsEmpty:
        print('No images in page {}. Skipping...'.format(pageNumber))
    else:
        pageImg.save(outFolder+'/'+str(pageNumber)+'.jpg')
