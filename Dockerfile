FROM python:3.11

EXPOSE 8000

COPY ./app /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
#CMD ["/bin/bash"]
