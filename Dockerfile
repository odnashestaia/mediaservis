FROM python:3.10.11

SHELL ["/bin/bash", "-c"]

# запрещяет создавать файлы для кеша 
ENV PYTHONDONTWRITEBYTECODE 1 
# все логи сразу выводяться нигде не буверизируються 
ENV PYTHONUNBUFFERED 1 

# обновляем pip 
RUN pip install --upgrade pip

# устанавливаем нужные прграммы в докер (я здесь половину не знаю)
RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev dos2unix libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# создаем и задаем рабочию папку
WORKDIR /mediaservis

# создаем static media
RUN mkdir /mediaservis/static && mkdir /mediaservis/media

# копируются файлы из нынешней деректории во внутрению 
COPY . .
RUN pip install -r req.txt
RUN pip install gunicorn==22.0.0
RUN dos2unix manage.py

CMD ["gunicorn","-b","0.0.0.0:8000"]