FROM python:3.10-slim

USER root
# Install Java (required by Spark), wget and Python dependencies
RUN apt-get update \
	&& apt-get install -y default-jre-headless wget gnupg \
	&& pip install --no-cache-dir pyspark pandas \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app
USER root