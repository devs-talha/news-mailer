FROM python:3.9-slim

ENV HOME=/home/usr/app

RUN apt-get update && apt-get -y install cron vim

ARG DAWN_SCRAPER_BASE_URL
ARG DAWN_SCRAPER_SECTIONS_TO_RETRIEVE
ARG MAIL_API_KEY
ARG MAIL_SENDER
ARG MAIL_RECIPIENTS
ARG STORAGE_ENDPOINT
ARG STORAGE_ACCESS_KEY
ARG STORAGE_SECRET_KEY
ARG STORAGE_BUCKET
ARG STORAGE_PATH_PREFIX
ARG GMT
ARG IMAGE_QUALITY
ARG CRON_HOUR
ARG CRON_MINUTE

ENV DAWN_SCRAPER_BASE_URL=${DAWN_SCRAPER_BASE_URL}
ENV DAWN_SCRAPER_SECTIONS_TO_RETRIEVE=${DAWN_SCRAPER_SECTIONS_TO_RETRIEVE}
ENV MAIL_API_KEY=${MAIL_API_KEY}
ENV MAIL_SENDER=${MAIL_SENDER}
ENV MAIL_RECIPIENTS=${MAIL_RECIPIENTS}
ENV STORAGE_ENDPOINT=${STORAGE_ENDPOINT}
ENV STORAGE_ACCESS_KEY=${STORAGE_ACCESS_KEY}
ENV STORAGE_SECRET_KEY=${STORAGE_SECRET_KEY}
ENV STORAGE_BUCKET=${STORAGE_BUCKET}
ENV STORAGE_PATH_PREFIX=${STORAGE_PATH_PREFIX}
ENV GMT=${GMT}
ENV IMAGE_QUALITY=${IMAGE_QUALITY}
ENV CRON_HOUR=${CRON_HOUR}
ENV CRON_MINUTE=${CRON_MINUTE}

WORKDIR $HOME

ADD . $HOME

# Make sure the script is executable
RUN chmod +x ./generate_env.sh

# Run the script to generate the .env file
RUN ./generate_env.sh

RUN pip install -r requirements.txt

RUN echo "${CRON_MINUTE} ${CRON_HOUR} * * * /usr/local/bin/python3 /home/usr/app/run.py > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]