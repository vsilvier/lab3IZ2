print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf1iDQbAAAAAE0Db9GnR6uwLETTTbAZ4W0fqPGd'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf1iDQbAAAAAIMcAQGNKP5lnIqB1B4AihvtQ17K'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 #rcolor = 0
 knopka1 = StringField('Выберите значение контраста составляющей R', validators = [DataRequired()])
 knopka2 = StringField('Выберите значение контраста составляющей G', validators = [DataRequired()])
 knopka3 = StringField('Выберите значение контраста составляющей B', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

## функция для оброботки изображения 

def draw(filename,knopka1,knopka2,knopka3):
 ##открываем изображение 
 print(filename)
 img= Image.open(filename)

##рисуем первый график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()
 
 knopka1=float(knopka1)
 knopka2=float(knopka2)
 knopka3=float(knopka3)
 
 img = np.int16(img)
 img[ : , : , 0] = img[ : , : , 0] * (knopka1/127+1)
 img[ : , : , 1] = img[ : , : , 1] * (knopka2/127+1)
 img[ : , : , 2] = img[ : , : , 2] * (knopka3/127+1) 
 img = np.clip(img, 0, 255)
 img = np.uint8(img)
 img = Image.fromarray(img, 'RGB')
 output_filename = filename
 img.save(output_filename)
 
 #рисуем второй график
 fig2 = plt.figure(figsize=(6, 4))
 ax = fig2.add_subplot()
 data2 = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b2 = ax.pcolormesh(data2, edgecolors='black', cmap='plasma')
 fig2.colorbar(b2, ax=ax)
 gr_path2 = "./static/newgr2.png"
 sns.displot(data2)
 plt.savefig(gr_path2)
 plt.close()
 return output_filename, gr_path, gr_path2

from tabulate import tabulate
 value_list = [['Alex', 13,1, 'Chess', 10],
                  ['Zia',  12,2, 'Monopoly', 25]]
 column_list = ["Name", "Age", "Number of Games", "Favourite Game", "Cost of Game"]
 print tabulate(value_list, column_list, tablefmt="grid")

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 grname2=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
 
  sz1=form.knopka1.data
  sz2=form.knopka2.data
  sz3=form.knopka3.data
  
  form.upload.data.save(filename)
  newfilename, grname, grname2 = draw(filename,sz1,sz2,sz3)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,gr_name2=grname2)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
