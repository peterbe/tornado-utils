try:
    from PIL import Image
except ImportError:
    Image = None
import os

def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)

def get_thumbnail(save_path, image_data, (max_width, max_height), quality=85):
    if not Image:
        raise SystemError("PIL.Image was not imported")

    if os.path.isfile(save_path):
        image = Image.open(save_path)
        #print "FOUND", save_path
        return image.size
    directory = os.path.dirname(save_path)
    _mkdir(directory)
    basename = os.path.basename(save_path)
    original_save_path = os.path.join(directory, 'original.' + basename)
    with open(original_save_path, 'wb') as f:
        f.write(image_data)
    #print "WROTE", original_save_path
    original_image = Image.open(original_save_path)
    image = scale_and_crop(original_image, (max_width, max_height))
    format = None
    try:
        image.save(save_path,
                   format=format,
                   quality=quality,
                   optimize=1)
        #print "SAVED", save_path

    except IOError:
        # Try again, without optimization (PIL can't optimize an image
        # larger than ImageFile.MAXBLOCK, which is 64k by default)
        image.save(save_path,
                   format=format,
                   quality=quality)

    os.remove(original_save_path)
    return image.size


def scale_and_crop(im, requested_size, **opts):
    x, y = [float(v) for v in im.size]
    xr, yr = [float(v) for v in requested_size]

    if 'crop' in opts or 'max' in opts:
        r = max(xr / x, yr / y)
    else:
        r = min(xr / x, yr / y)

    if r < 1.0 or (r > 1.0 and 'upscale' in opts):
        im = im.resize((int(round(x * r)), int(round(y * r))),
                       resample=Image.ANTIALIAS)

    crop = opts.get('crop') or 'crop' in opts
    if crop:
        # Difference (for x and y) between new image size and requested size.
        x, y = [float(v) for v in im.size]
        dx, dy = (x - min(x, xr)), (y - min(y, yr))
        if dx or dy:
            # Center cropping (default).
            ex, ey = dx / 2, dy / 2
            box = [ex, ey, x - ex, y - ey]
            # See if an edge cropping argument was provided.
            edge_crop = (isinstance(crop, basestring) and
                           re.match(r'(?:(-?)(\d+))?,(?:(-?)(\d+))?$', crop))
            if edge_crop and filter(None, edge_crop.groups()):
                x_right, x_crop, y_bottom, y_crop = edge_crop.groups()
                if x_crop:
                    offset = min(x * int(x_crop) / 100, dx)
                    if x_right:
                        box[0] = dx - offset
                        box[2] = x - offset
                    else:
                        box[0] = offset
                        box[2] = x - (dx - offset)
                if y_crop:
                    offset = min(y * int(y_crop) / 100, dy)
                    if y_bottom:
                        box[1] = dy - offset
                        box[3] = y - offset
                    else:
                        box[1] = offset
                        box[3] = y - (dy - offset)
            # See if the image should be "smart cropped".
            elif crop == 'smart':
                left = top = 0
                right, bottom = x, y
                while dx:
                    slice = min(dx, 10)
                    l_sl = im.crop((0, 0, slice, y))
                    r_sl = im.crop((x - slice, 0, x, y))
                    if utils.image_entropy(l_sl) >= utils.image_entropy(r_sl):
                        right -= slice
                    else:
                        left += slice
                    dx -= slice
                while dy:
                    slice = min(dy, 10)
                    t_sl = im.crop((0, 0, x, slice))
                    b_sl = im.crop((0, y - slice, x, y))
                    if utils.image_entropy(t_sl) >= utils.image_entropy(b_sl):
                        bottom -= slice
                    else:
                        top += slice
                    dy -= slice
                box = (left, top, right, bottom)
            # Finally, crop the image!
            im = im.crop([int(round(v)) for v in box])
    return im
