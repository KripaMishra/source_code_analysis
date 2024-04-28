

FROM python:3.9-slim-buster

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --fix-missing build-essential

RUN pip install -r requirements.txt
EXPOSE 8000
RUN export GIT_PYTHON_GIT_EXECUTABLE=/mingw64/bin/git
CMD [ "python", "app.py" ]