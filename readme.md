to create a python venv run

py -m venv venv


to activate the venv, run (on windows):

.\venv\Scripts\activate 



run this to install dependencies

pip install -r requirements.txt



to start the server, run:

uvicorn main:app --port 8001
