import os
import time
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/uploadfile', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    print(filename)
    # content = request.files['file'].read()
    # print(request.files['file'].stream)
    validate(request.files['file'].stream)
    data_dir = '/Users/pl465j'
    fpath = os.path.join(data_dir, filename)
    # request.files['file'].seek(0)
    # print(request.files['file'].read())
    uploaded_file.save(fpath)
    print(fpath)
    with open(fpath) as f:
        print(f.read())
    return uploaded_file.filename


def validate(content):
    l1 = [
        "ORDER_TYPE_ORIG",
        "END_BUF_TIME",
        "LIVE_IND",
        "OWNER_NM",
        "STRT_BUF_TIME",
        "NTWK_CD"
    ]
    data = content.read().decode().split("\n")
    content.seek(0)
    header = data.pop(0).split(",")
    print(header)
    if len(list(set(l1) ^ (set(header)))) > 0:
        print('Mismatch ', list(set(l1) ^ (set(header))))
    print('=================')
    print(data)


if __name__ == '__main__':
    app.run(debug=True)
