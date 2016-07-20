
def get_image_from_request(request):
    files = request.FILES
    try:
        images = files['image']
        return images
    except Exception:
        return False


# TODO больше защиты
