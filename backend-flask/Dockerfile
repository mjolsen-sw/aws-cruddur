FROM 009160064216.dkr.ecr.us-west-1.amazonaws.com/cruddur-python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]