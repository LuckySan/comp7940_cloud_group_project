FROM python:latest
WORKDIR /
COPY chatbot.py / 
COPY requirements.txt /
RUN pip install pip update 
RUN pip install -r requirements.txt
ENV REDISPORT=11024
CMD ["python", "chatbot.py"]