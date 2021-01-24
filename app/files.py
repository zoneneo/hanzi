from flask import send_from_directory,abort
from flask import render_template

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=["GET"])
def download(path):
    try:
        dest = app.config.get('UPLOAD_DIR')
        if path.isdigit():
            file= Files.query.get(path)
            path=file.path
        else:
            path = os.sep+ parse.unquote_plus(path)

        if not path.startswith(dest):
            abort(406,'下载请求拒绝，只允许下载资料目录')

        if os.path.isfile(path):
            path,filename=os.path.split(path)
            return send_from_directory(path, filename, as_attachment=True)
        else:
            abort(404, '文件不存在')
    except Exception as ex:
        abort(500, str(ex))