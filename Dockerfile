FROM python:3
ENV FLASK_APP "./manage.py"
ENV FLASK_ENV "development"
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run --host=0.0.0.0