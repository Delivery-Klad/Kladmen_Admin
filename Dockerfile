FROM python:3.8

ADD requirements.txt /requirements.txt
ADD Bot_admin.py /main.py
ADD okteto-stack.yaml /okteto-stack.yaml
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]