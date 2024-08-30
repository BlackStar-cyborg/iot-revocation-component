# FIXME: (aver) create local folder to run from, not from root!

ARG from_image=ghcr.io/hyperledger/aries-cloudagent-python:py3.9-0.10.4
FROM ${from_image}
LABEL maintainer="Armin Veres"

ADD ./requirements.docker.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy files over
ADD _updating/_new_file.py .
ADD src/updater.py .

# enable supplication of arguments
ENTRYPOINT ["bash", "-c", "python3 -m \"$@\"", "--"]
