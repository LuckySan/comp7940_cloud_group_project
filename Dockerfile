FROM huanjason/scikit-learn:latest
WORKDIR /app
COPY . /app
RUN pip install pip update 
RUN pip install -r requirements.txt
CMD ["python", "chatbot.py"]
