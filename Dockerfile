FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY *.egg ./
#RUN useradd -u "100" nginx
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m easy_install bitshares-1.2.1-py3.7.egg
RUN pip install qrcode[pil] uwsgi
COPY . .
CMD [ "uwsgi","--ini", "wrapper.ini"]
#CMD [ "uwsgi", "--socket","0.0.0.0:5000","--protocol=http","-w","wsgi:app", "-M"]
