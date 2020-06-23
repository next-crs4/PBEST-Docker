FROM python:3

ARG USER_ID
ARG GROUP_ID

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY ./app /app/

RUN mkdir /config
ADD /config/requirements.pip /config/

ADD /app/pbest-test.py /usr/local/bin/pbest-test.py
ADD /app/pbest.py /usr/local/bin/pbest.py
RUN chmod +x /usr/local/bin/pbest-test.py
RUN chmod +x /usr/local/bin/pbest.py
RUN ln -s /usr/local/bin/pbest-test.py /usr/local/bin/pbest-test
RUN ln -s /usr/local/bin/pbest.py /usr/local/bin/pbest


RUN apt-get -qq update && \
    apt-get install --no-install-recommends -y dialog apt-utils software-properties-common && \
    apt-get install -y octave liboctave-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install -r /config/requirements.pip && \
    rm -rf ~/.cache/ && \
    groupadd -g ${GROUP_ID} appuser && \
    useradd -m -u ${USER_ID} -g appuser appuser && \
    octave-cli --eval "pkg install -forge io"


USER appuser