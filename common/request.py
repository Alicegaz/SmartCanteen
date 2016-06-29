
def get_image_from_request(request):
    files = request.FILES
    images = files['image']
    return images