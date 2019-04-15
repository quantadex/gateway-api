FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY *.egg ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m easy_install bitshares-1.2.1-py3.7.egg
RUN pip install qrcode[pil]
COPY . .

ENV FLASK_APP=wrapper.py
CMD [ "flask", "run","--host=0.0.0.0" ]
