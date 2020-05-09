# Russian stocks API
Service that returns financial information about Russian companies and their stocks in a machine-readable way. It uses `russian-stocks-crawler` project to collect and aggregate data among financial sites.

## Requirements
* python 3.8
* poetry (use `pip install poetry` if it's not installed yet)

## How to run locally?
* clone the repo from github
* run `poetry install` inside project's folder
* run `cp .env.dist .env`, after that you have to provide mongo uri inside `.env` file
* run `poetry run flask run`
* open `http://localhost:5000/`, swagger has to be there

## Public url
https://russian-stocks-api.herokuapp.com/