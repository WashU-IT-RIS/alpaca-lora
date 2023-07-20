FROM python:3.10.12-bullseye

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY chatbot/ ./
RUN pip install -r requirements.txt && \
    chmod 777 -R /usr/src/app

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
