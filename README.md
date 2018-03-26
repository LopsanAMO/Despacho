# Despacho

[![Build Status](https://travis-ci.org/LopsanAMO/Despacho.svg?branch=master)](https://travis-ci.org/LopsanAMO/Despacho)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a5f325393db0eec370f2#?env%5Bdespacho_envs%5D=W3sia2V5IjoibG9jYWxfdXJsIiwidmFsdWUiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvIiwiZGVzY3JpcHRpb24iOiIiLCJ0eXBlIjoidGV4dCIsImVuYWJsZWQiOnRydWV9XQ==)


## instalacion del entorno virtual con virtuelenv
```bash
$ pip install virtualenv
````

## Creacion y Activacion del entorno virtual
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
````

## Clonar el proyecto
```bash
$ git clone https://github.com/LopsanAMO/Despacho.git
$ cd Despacho
```

# Instalación de las dependencias
```bash
$ pip install -r requirements.txt
```

# Ejecutar el proyecto
```bash
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```
