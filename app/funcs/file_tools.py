import os
import hashlib
import errno
from werkzeug.utils import secure_filename

upload_folder = 'files/uploaded'  # temporary path
banned_extensions = []


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() not in banned_extensions


def secure_fn(fname):
    conv = fname.encode('utf-8')
    sec = hashlib.sha224(conv)
    return sec.hexdigest()


def save_file(file, eid):
    if file.filename == "":
        return None
    if file and allowed_file(file.filename):
        fpath = '{}/{}'.format(upload_folder, eid)
        if not os.path.exists(fpath):
            try:
                os.makedirs(fpath)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        filename = secure_filename(file.filename)
        file.save(os.path.join(fpath, filename))
        return filename
    else:
        return None
