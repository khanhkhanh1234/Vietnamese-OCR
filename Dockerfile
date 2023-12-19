FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

RUN apt-get update && apt-get install build-essential -y && apt-get install libgl1 -y && apt-get install libglib2.0-0 -y

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY src /code/src
WORKDIR /code/src

RUN chmod +x start_service.sh

CMD ["bash", "start_service.sh"]



