def get_flash_messages(request):
    flash = request.session.get('flash')
    print(flash)
    if 'flash' in request.session:
        del request.session['flash']
    request.session['flash'] = {}
    return flash

def error_for_get_to_post_url(request):
    request.session['flash']['warning'] = "Sorry, but that URL is for internal use only."

def set_flash_message(request, message_type, message):
    if 'flash' not in request.session:
        request.session['flash'] = {}
    request.session['flash'][message_type] = message
    request.session.modified = True
