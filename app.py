import os,sys 
from flask import Flask, request, render_template
from pypdf import PdfReader
import json
from resumeparser import ats_extractor

sys.path.insert(0,os.path.abspath(os.getcwd()))

UPLOAD_PATH=r"__DATA__"
app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/process',methods=["POST"])
def ats():
    # if request.method=="GET":
    #     return render_template("index.html")
    #doc=request.files('pdf_doc')
    # get uploaded pdf
    doc=request.files['pdf_doc']
    # save file
    doc.save(os.path.join(UPLOAD_PATH,"file.pdf"))
    doc_path=os.path.join(UPLOAD_PATH,"file.pdf")
    # extract text from pdf
    data=_read_file_from_path(doc_path)
    # send to model
    parsed_data=ats_extractor(data)
    # try:
    #     parsed_data=json.loads(data)
    # except Exception as e:
    #     parsed_data={"row_response":data,"error":str(e)}
    return render_template('index.html',data=parsed_data)

def _read_file_from_path(path):

    reader = PdfReader(path)

    data = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            data += text

    return data


# def _read_file_from_path(path):
#     reader=PdfReader(path)
#     data=""

#     for page_no in range(len(reader.pages)):
#         page=reader.pages[page_no]
#         data+=page.extract_text()
#     return data

if __name__=="__main__":
    #app.run(port=8000,debug=True)
    app.run(debug=True, use_reloader=False)