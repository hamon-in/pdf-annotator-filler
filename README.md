# PDF Annotator

## Create virtual environment

<code>
	$ virtualenv -p python3 env
</code>
<br>

## Activate virtualenv env

<code>
	$ source venv/bin/activate
</code>
<br>

## Change current working directory

<code>
	$ cd pdf-annotator-filler
</code>
<br>

## Install modules

<code>
	$ pip install -r requirements.txt
</code>
<br>
<code>
	$ cd frontend
</code>
<br>
<code>
	$ npm install
</code>
<br>
<code>
	$ npm install vue-resource
</code>
<br>

## To run frontend dev server

<code>
	$ cd frontend
</code>
<br>
<code>
	$ npm run dev
</code>
<br>

## To run backend flask server

<code>
    $ cd backend
</code>
<br>
<code>
	$ python
</code>
<br>
<code>
	$ from api import db
</code>
<br>
<code>
	$ db.create_all()
</code>
<br>
<code>
	$ exit()
</code>
<br>
<code>
	$ mkdir api/templates
</code>
<br>
<code>
	$ mkdir api/static
</code>
<br>
<code>
	$ python run.py
</code>
<br>

## To build frontend

<code>
	$ cd frontend
</code>
<br>
<code>
	$ npm build
</code>
<br>
<code>
	$ cd ..
</code>
<br>
<code>
	mv backend/api/static/index.html backend/api/templates/index.html
</code>
<br>
