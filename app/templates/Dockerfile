FROM      ubuntu:16.04
MAINTAINER Arthur Neuman "arthur.neuman@gmail.com"

RUN apt-get update
RUN apt-get install -y python3-pip git-core libffi-dev python3-dev

RUN git clone -b contacts https://github.com/zarthur/restful-todo.git /opt/contacts

RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/contacts/requirements.txt
RUN cd /opt/contacts && python3 manage.py createall

WORKDIR /opt/contacts

EXPOSE 80

ENTRYPOINT ["python3", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "80"]
