# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.14

# Fix python printing
ENV PYTHONUNBUFFERED 1
ENV PIP_INDEX_URL=https://mirror.cdn.ir/repository/pypi/simple


# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/local.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/





ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app/

RUN pip install --upgrade pip --index-url=${PIP_INDEX_URL}
RUN pip install --no-cache-dir -r ./requirements/production.txt --index-url=${PIP_INDEX_URL}

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
