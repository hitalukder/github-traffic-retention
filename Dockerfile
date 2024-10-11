FROM registry.access.redhat.com/ubi8/python-39:1-113.1682304667 as base

WORKDIR /app/backend

COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt

COPY app.py app.py