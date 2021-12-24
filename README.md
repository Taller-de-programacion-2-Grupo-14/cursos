![linter](https://github.com/Taller-de-programacion-2-Grupo-14/cursos/actions/workflows/linter.yml/badge.svg)
[![codecov](https://codecov.io/gh/Taller-de-programacion-2-Grupo-14/ubademy-cursos/branch/master/graph/badge.svg?token=0V88B63RBJ)](https://codecov.io/gh/Taller-de-programacion-2-Grupo-14/ubademy-cursos)
# Cursos
---
Repositorio encargado de contener todos los procesos asociados a los cursos, tales como crearlos, visualizarlos, inscribirse, editarlos o cancelarlos.  
Además, contiene toda la información de los cursos y su relacion con examenes y usuarios.

La documentación de los endpoints relacionados a cursos puede verse [aquí](https://ubademy-14-prod.herokuapp.com/doc?urls.primaryName=Courses#/)

## Instalacion y despliegue productivo:
### Sin Docker
Primero, es necesario crear el virtual environment
```console
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
$ source env/bin/activate
```
Una vez levantado el virtual environment, es necesario instalar las dependencias indicadas en requirements.txt de la siguiente manera
```console
$ pip install -r requirements.txt
```
Luego, para correr la aplicación:
```console
$ hypercorn main:app --reload
```
De esta forma, la aplicacion estará corriendo en http://127.0.0.1:8000

### Docker
Para el despliegue productivo de la aplicación se provee un archivo `Dockerfile`. El mismo permitirá construir una imagen productiva de Docker del servidor de la aplicación. Para construir la imagen, se utiliza el archivo MakeFile. Para compilar la imagen primero es necesario correr:
```console
$ make buildDC
```
y luego
```console
$ make runDC
```
Para levantar la aplicacion, la cual se encontrará corriendo en http://127.0.0.1:8080

## Tests
Los tests se corren en Github Actions y el coverage se sube a Codecov. En caso de querer correrlos de forma local, una vez levantado el virtual environment basta con ejecutar:
```console
$ pytest
```
## Variables de entorno necesarias para un uso completo:
- `EXAMS_HOSTNAME`: URL de donde se va a interactuar con la api de examenes.
- `USERS_HOSTNAME`: URL de donde se va a interactuar con la api de usuarios.
- `DATABASE_URL`: URL donde se va a conectar a la base de datos.

