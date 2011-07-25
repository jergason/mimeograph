from PIL import Image
import random
from bisect import bisect

#NOTE: This function was inspired heavily by Steven Kay's
# article at
# http://stevendkay.wordpress.com/2009/09/08/generating-ascii-art-from-photographs-in-python/.
# Thanks to him for the algorithm.
def convert_image(image):
    '''Creates an ASCII art image from an arbitrary image'''
    # greyscale.. the following strings represent
    # 7 tonal ranges, from lighter to darker.
    # for a given pixel tonal level, choose a character
    # at random from that range.
    greyscale = [" ", ".", ",-", "_ivc=!/|\\~", "gjez2]/()t[+T7Vf", "mdK4ZGbNDXY5P*Q", "W8KMAB", "#%$@"]

    # using the bisect class to put luminosity values
    # in various ranges.
    # these are the luminosity cut-off points for each
    # of the 7 tonal levels. At the moment, these are 7 bands
    # of even width, but they could be changed to boost
    # contrast or change gamma, for example.
    zonebounds=[36 ,72, 108, 144, 180, 216, 252]

    # resize image
    im=Image.open(image)
    im=im.resize((80, 37),Image.BILINEAR)
    # convert to black and white
    im=im.convert("L")

    # Loop over each pixel and replace with a character of
    # approximately the same brightness.
    str=""
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            lum=255-im.getpixel((x,y))
            row=bisect(zonebounds,lum)
            possibles=greyscale[row]
            str=str+possibles[random.randint(0,len(possibles)-1)]
        str=str+"\n"

    return str


def get_flash_messages(request):
    """Get all flash messages from the session object and delete the messages
    that used to be there."""
    flash = request.session.get('flash')
    print(flash)
    if 'flash' in request.session:
        del request.session['flash']
    request.session['flash'] = {}
    return flash

def error_for_get_to_post_url(request):
    """Helper function that sets a flash warning when a user tries to access an
    internal URL."""
    request.session['flash']['warning'] = "Sorry, but that URL is for internal use only."

def set_flash_message(request, message_type, message):
    """Set flash messages, and make sure the session is marked as changed so it
    gets saved."""
    if 'flash' not in request.session:
        request.session['flash'] = {}
    request.session['flash'][message_type] = message
    request.session.modified = True
