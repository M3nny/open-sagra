# 🍺 open-sagra

<div align="center">
	<img src="static/assets/logo.png" width="300" alt="Logo"/>
</div>

> Here in Italy, a sagra (sàgra /'sagra/) is a local festival.

## Installation
After installing python and git, run:

``` bash
git clone https://github.com/M3nny/open-sagra
cd open-sagra
pip install -r requirements.txt
```

## Populating the database
Use `populate_db.sql` with MySQL for a default configuration.
<u>It will create a database</u> named sagra <u>and an admin user</u> with the following credentials:
- **ID**: _a00001_
- **Password**: _password_ (encrypted with sha512 into the DB)

After setting up the enviromental variables inside the `.env` file, you will be ready go, just run: `python3 app.py`, if you don't have other services running on the local port `5000` you can reach the web app via your browser at `localhost:5000`.