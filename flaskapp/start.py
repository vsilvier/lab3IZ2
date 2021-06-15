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
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcDoScbAAAAANOWBHNB3QnRTxrJvpOItbhMBKsL'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcDoScbAAAAAB2vlAIbxvkMUqoI90VBDX_Ix7M8'
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
 size = StringField('size', validators = [DataRequired()])
 rcolor = StringField('choose level of red intensity (0.0 - 1)', validators = [DataRequired()])
 gcolor = StringField('choose level of green intensity (0.0 - 1)', validators = [DataRequired()])
 bcolor = StringField('choose level of blue intensity (0.0 - 1)', validators = [DataRequired()])
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

def draw(filename,size,rcolor,gcolor,bcolor):
 ##открываем изображение 
 print(filename)
 img= Image.open(filename)

##делаем график
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


##рисуем рамки
 #int rcolor = 1
 
 size=int(size)
 rcolor = float(rcolor)
 gcolor = float(gcolor)
 bcolor = float(bcolor)
 
 height = 224
 width = 224
 img= np.array(img.resize((height,width)))/255.0
 print(size)
 print(rcolor)
 #rcolor = 0
 
 img[:size,:,:] = 0
 img[:,0:size,:] = 0
 img[:,224-size:,:] = 0
 img[224-size:,:,:] = 0
 
 img[:,0:size,0] = rcolor
 img[:,224-size:,0] = rcolor
 img[224-size:,:,0] = rcolor
 img[224-size:,:,0] = rcolor


 img[:size,:,1] = gcolor
 img[:,0:size,1] = gcolor
 img[:,224-size:,1] = gcolor
 img[224-size:,:,1] = gcolor

 img[:size,:,2] = bcolor
 img[:,0:size,2] = bcolor
 img[:,224-size:,2] = bcolor
 img[224-size:,:,2] = bcolor
##сохраняем новое изображение
 img = Image.fromarray((img * 255).astype(np.uint8))
 print(img)
 #img = Image.fromarray(img)
 new_path = "./static/new.png"
 print(img)
 img.save(new_path)
 return new_path, gr_path


# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
 
  sz=form.size.data
  sr=form.rcolor.data
  sg=form.gcolor.data
  sb=form.bcolor.data
  
 
  form.upload.data.save(filename)
  newfilename, grname = draw(filename,sz,sr,sg,sb)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
 
