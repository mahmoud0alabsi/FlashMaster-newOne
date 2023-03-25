#------------Libraries------------
from pypdf import PdfReader
from openai import *
from googletrans import Translator
from fpdf import FPDF
from base64 import b64encode
from flask import Flask,request,render_template,url_for
from werkzeug.utils import secure_filename
import os

#------------/Libraries------------



#------------HeaderText------------
temp_ar = 'اكتب اسئلة واجوبتها عن النص التالي، اطبع سطر فارغ بعد كل سؤال واطبع سطر فارغ بعد كل جواب:\n'
temp_en = 'Write questions and anwers on next text, print space after each question and print space after each answer:\n'

#------------/HeaderText------------



# #------------getResponse------------
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY
model_id = 'gpt-3.5-turbo'
def call_api(text):
    conversation = []
    conversation.append({'role': 'user', 'content': text})
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    return response.choices[0].message.content


def det_lang(txt):
    translator = Translator()
    detect_res = translator.detect(txt)
    return detect_res.lang


def final_Text(txt, lang):
    if lang == 'ar':
        final_txt = temp_ar + txt
    elif lang == 'en':
        final_txt = temp_en + txt
    return final_txt
#------------/getResponse------------



#--------------------Preapare PDF file with resp-------------------------

class PDF(FPDF):
    def chapter_title(self,label):
        # Arial 12
        self.set_font('Arial', '', 13)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 8, '%s' % (label), 0, 1, 'C', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, text):
        # Read text 
        txt = text
        # 
        self.set_font('Arial', 'b', 13)
        # Output justified text
        self.multi_cell(0, 7, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, 'Done by (Q&A)')

    def print_chapter(self,title, name):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(name)


def get_pdf_file(text):
    txt = text
    pdf = PDF()
    pdf.print_chapter('Hello in Q&A Magic', txt)
    return pdf.output()

#--------------------/Preapare PDF file with resp-------------------------




#--------------------Read PDF file-------------------------

# PDF result
def get_result_form_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    st = ""

    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page]
        st += text.extract_text()

    lang = det_lang(st)               #detect language
    allText = final_Text(st, lang)    #merge header with pdf text
    resp = call_api(allText)          #call ChatGPT and return response
    #obj = get_pdf_file(resp)          #convert response to pdf file

    ls = resp.split('\n')
    ls[:] = (value for value in ls if value != '')
    questions_list = [ls[i] for i in range(0,len(ls), 2)]  #split response (questions)
    anwers_list = [ls[i] for i in range(1,len(ls), 2)]     #split response (answers)
    #create_link(obj)                                       #create download pdf link
    return resp, questions_list, anwers_list


#--------------------/Read PDF file and get final result-------------------------



#--------------------Text and get final result-------------------------

# Text result
def get_result_form_text(txt):
    lang = det_lang(txt)             #detect language
    allText = final_Text(txt, lang)  #merge header with pdf text
    resp = call_api(allText)         #call ChatGPT and return response
    #obj = get_pdf_file(resp)         #convert response to pdf file

    ls = resp.split('\n')
    ls[:] = (value for value in ls if value != '')
    questions_list = [ls[i] for i in range(0,len(ls), 2)]
    anwers_list = [ls[i] for i in range(1,len(ls), 2)]
    #create_link(obj)

    return resp, questions_list, anwers_list

#--------------------/Text and get final result-------------------------




#--------------------Flash part-------------------------

# Flask start
app =Flask(__name__)

app.config['File_Upload'] = 'static\PDF_files'   #'/Users/medoa/Downloads/Project/FInal style and version source/FlashMaster/static/assets/PDF_files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ContactUs')
def ContactUs():
    return render_template('ContactUs.html')


@app.route('/home',methods=['GET','POST'])
def home():
    res_txt = ''
    ques, ans = ['bateee5', 'qataef'], ['byyy', 'ramadannn']

    pdf_file = request.files['myfile']
    if request.method =='POST':

        # PDF state
        if pdf_file.filename != '' : print('hyyyyyyyyy')
            # filename = secure_filename(pdf_file.filename)
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # pdf_file.save(os.path.join(basedir, app.config['File_Upload'], filename))
            # res_txt, ques, ans = get_result_form_pdf(pdf_file)
            #os.remove(os.path.join(basedir, app.config['File_Upload'], filename))

        # Text state
        elif request.form['mytextbox5'] != '': print('yeeeeeees')
            # txt=request.form['mytextbox5']
            # res_txt, ques, ans = get_result_form_text(txt)
        
        # prepare lists
        ques_list = '$%$'.join(ques)
        ans_list = '$%$'.join(ans)

    return render_template('index.html' , out_txt=res_txt, ques_list = ques_list , ans_list=ans_list)
                                        



if __name__ == '__main__':
    app.run(debug=True)