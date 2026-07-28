# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV PIP_INDEX_URL=https://mirror.cdn.ir/repository/pypi/simple

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install --upgrade pip --index-url=${PIP_INDEX_URL}
RUN pip install --no-cache-dir -r ./requirements/production.txt --index-url=${PIP_INDEX_URL}

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


