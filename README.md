# Hasker
____
Задание: разработать web-приложение, аналог Stack Overflow.

## Deploy.
Разворачивается в docker-контейнере (Centos 8.0):
```
  
  $ docker run -it -p 8000:80 centos:latest /bin/bash

```
Внутри контейнера:
```
  
  # dnf -y install make git
  # mkdir hasker
  # cd hasker
  # git clone https://github.com/naselin/Hasker.git .
  # make prod

```
Тестовые пользователи (пароль !G@hjkm23):
```
  
  Hermes
  Leela
  Fry
```
