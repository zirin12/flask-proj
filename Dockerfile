FROM python:3
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD [ "./app.py" ]