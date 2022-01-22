# Distributed interaction system : Sensor network

Pour paramétrer l’API formée par le microframework flask, il faut set quelques variables :

Sous windows:

set FLASK_APP=API_rest.py

set FLASK_ENV=development

Sous mac/linux:

export FLASK_APP=API_rest.py

export FLASK_ENV=development

Pour exécuter le projet, il faut lancer les cinq programmes suivants en parallèle :

flask run

python ./launch_sensors.py

python ./launch_agreg1.py

python ./launch_agreg2.py

python ./launch_client.py

