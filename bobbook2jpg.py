import sys, os.path, argparse
from bs4 import BeautifulSoup
from PIL import Image

colorMap = {
    'Weiss,normal,': (255,255,255,255),
    'Schwarz,normal,': (0,0,0,255)
}

parser = argparse.ArgumentParser(description='Convert Bob Book to JPGs')
parser.add_argument('inputFile', help='Input MCF file')
parser.add_argument('inputFolder',
    help='Input folder (typically Something_MCF-Datein)')
parser.add_argument('outputFolder', help='Output folder')
parser.add_argument('--size', default='2595x1024',
    help='Resolution of double page image', metavar='WIDTHxHEIGHT')

args=parser.parse_args()
size=args.size.split('x')
outResolution=(int(size[0]), int(size[1]))

soup = BeautifulSoup(open(args.inputFile), 'xml')
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
        img = Image.open(args.inputFolder+'/'+area.image['filename'])
        scale = float(area.image['scale'])
        imgLeft = float(area.image['left'])*-1
        imgTop = float(area.image['top'])*-1
        imgWidth = width/scale
        imgHeight = height/scale

        img = img.crop((imgLeft, imgTop, imgLeft+imgWidth, imgTop+imgHeight))
        img = img.resize((int(width), int(height)))
        pageImg.paste(img, (int(left), int(top), int(left)+int(width), int(top)+int(height)))

    if pageIsEmpty:
        print('  No images in page {}. Skipping...'.format(pageNumber))
    else:
        pageLeft = pageImg.crop((0,0,pageWidth/2,pageHeight))
        pageLeft.thumbnail(outResolution)
        pageLeft.save(args.outputFolder+'/'+str(pageNumber+2)+'.jpg')
        pageRight = pageImg.crop((pageWidth/2,0,pageWidth,pageHeight))
        pageRight.thumbnail(outResolution)
        pageRight.save(args.outputFolder+'/'+str(pageNumber+3)+'.jpg')
