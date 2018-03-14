# Despacho

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a5f325393db0eec370f2)


## instalacion del entorno virtual con virtuelenv
```bash
$ pip install virtualenv
````

## Creacion y Activacion del entorno virtual
```bash
$ virtualenv -p python3 myvenv
$ source myvenv/bin/activate
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
