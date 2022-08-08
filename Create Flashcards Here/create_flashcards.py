#!/usr/bin/env python
"""Creates flashcards from a folder of images


    ################################################
    IF YOU ARE ON MAC PRESS 'Run' UP TOP OR PRESS F5
    ################################################

This script accepts an input of a folder name.
Make sure that folder exists and has images. This script will create flashcards based on the image names.

Example:   

    /lesson1/
    |- far.png
    |- car.jpg
    |- target.jpeg
    |- arm.png

What is the folder name?
>lesson1
Who is the author? (leave blank to skip)
>
Highlight the first letter? (yes/no/input) < this is best for letter flashcards
>input
What letters to highlight?
>ar
Found 4 images in the lesson1 folder.
generating...
lesson1_flashcards.pdf generated with 4 flashcards.

You should be able to see a new pdf file with the flashcards in the folder, and the 'ar' will be highlighted in each word.
"""

import reportlab
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import os
from datetime import datetime
import re



PAGE_HEIGHT = 8.3*inch #if you need different sized paper. This is landscape A4 paper.
PAGE_WIDTH = 11.7*inch
ACCEPTED_EXTENSIONS = ['png','jpg','jpeg','webp'] #edit this if you need more image extensions





__author__ = "Artem Nikitin"
__copyright__ = "Copyright 2022"
__credits__ = ["Artem Niktin", "whatstheword.io"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "None"
__email__ = "admin@whatstheword.io"
__status__ = "Production"





def createWord(word, canvas, creator=None, highlight_letter=False, special_case=None):
    """
        creates a pdf page with the word in the middle
    params:
        word: str of the word
        canvas: the reportlab pdf canvas
        creator: name of the author, to add a name
        highlight_letter: make the first letter green
        special_case: highlight specific letters in the special case, e.g. special_case='x' for words like box,fox, highlight the x not the first letter
    """
    font_size = 250
    text_width = stringWidth(word, 'Bahnschrift SemiBold SemiCondensed', font_size)
    while text_width>PAGE_WIDTH:
        font_size -= 10
        text_width = stringWidth(word, 'Bahnschrift SemiBold SemiCondensed', font_size)
    text_object = canvas.beginText(5.85*inch-(text_width/2),4.15*inch -0.8*inch)
    text_object.setFont("Bahnschrift SemiBold SemiCondensed", font_size)
    if highlight_letter:
        if special_case:
            if special_case in word:
                positions = [m.start() for m in re.finditer(special_case,word)]
                next_letter = -1
                for i,letter in enumerate(word):
                    if next_letter != -1 and i<next_letter:
                        continue
                    if i in positions:
                        text_object.setFillColorRGB(0.2,.8,0.5)
                        text_object.textOut(special_case)
                        next_letter = i + len(special_case)
                    else:
                        text_object.setFillColorRGB(0,0,0)
                        text_object.textOut(letter)  
            else:
                text_object.setFillColorRGB(0,0,0)
                text_object.textOut(word)
        else:
            text_object.setFillColorRGB(0.2,.8,0.5)
            text_object.textOut(word[0])
            text_object.setFillColorRGB(0,0,0)
            text_object.textOut(word[1:])
    else:
        text_object.setFillColorRGB(0,0,0)
        text_object.textOut(word)
          
    canvas.drawText(text_object)
    if creator:
        name = canvas.beginText(PAGE_WIDTH-2*inch,inch*0.8)
        name.setFont("Times-Roman",12)
        name.setFillColorRGB(0.85,0.85,0.85)
        name.textOut(f"made by {creator}")
        canvas.drawText(name)


def getWidthHeight(path):
    """
        returns:
            the optimal width and height of the image based on the constraints given by the PAGE_HEIGHT and PAGE_WIDTH
    """
    image = Image.open(path)
    h = image.height
    w = image.width
    new_height = 0
    new_width = 0
    if h>w:
        ratio = h/w
        new_height = PAGE_HEIGHT*0.8
        new_width = new_height/ratio
    else:
        ratio = w/h
        new_width = PAGE_WIDTH*0.7
        new_height = new_width/ratio
    return int(new_width), int(new_height)


def createPicture(path, canvas):
    img_w, img_h = getWidthHeight(path)
    image = canvas.drawImage(path,(PAGE_WIDTH-img_w)/2,(PAGE_HEIGHT-img_h)/2,width=img_w,height=img_h,mask='auto')




def getFolderName()->str:
    """
    returns:
        string of the input
    """
    return input('\nWhat is the folder name?\n>').strip()

def getCreatorName()->str:
    """
    returns:
        string of the input
    """
    return input('\nWho is the author?\n>').strip()

def getHighlightFirstLetter()->str:
    """
    returns:
        string of the input
    """
    return input('\nHighlight the first letter? (yes/no/input)\n>').strip().lower()

def getSpecialCase()->str:
    """
    returns:
        string of the input
    """
    return input('\nWhat should be highlighted?\n>').strip()

if __name__ == '__main__':
    folder_name = ''
    folder_name = getFolderName()
    while folder_name == '':
        print('Invalid name')
        folder_name = getFolderName()
    creator_name = getCreatorName()
    if creator_name.strip() == '':
        creator_name = None
    highlight_answer = getHighlightFirstLetter()
    highlight = False
    special_case = None
    if highlight_answer.lower().startswith('y'):
        highlight = True
    if highlight_answer.lower().startswith('i'):
        special_case = getSpecialCase()
        highlight = True
        
    file_name = f"{folder_name} Flashcards {str(datetime.now().strftime('%Y-%m-%d-%H%M'))}.pdf"
    folder_path = f'./{folder_name}/'
    canvas = Canvas(file_name, pagesize=(PAGE_WIDTH,PAGE_HEIGHT))
    reportlab.rl_config.TTFSearchPath.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../Fonts for flashcards/'))
    pdfmetrics.registerFont(TTFont('Times New Roman', 'times-ro.ttf'))
    pdfmetrics.registerFont(TTFont('Bahnschrift SemiBold SemiCondensed', 'bahnschrift_font.ttf'))

    
    try:
        picfiles = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.split('.')[1] in ACCEPTED_EXTENSIONS]
    except Exception:
        print(f'Unable to get files from the folder ./{folder_name}/ Are you sure it exists?')
        exit()

    print(f'Found {len(picfiles)} images in the {folder_name} folder.')
    print('Generating...')
    for file in picfiles:
        word = file.split('.')[0]
        createPicture(f'./{folder_name}/'+file, canvas)
        canvas.showPage()
        createWord(word, canvas, creator_name, highlight, special_case)
        canvas.showPage()


    canvas.save()

    print(f"{file_name} generated with {len(picfiles)} flashcards.")






