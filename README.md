# Powtórki Online API

## Docs

Swagger at:
`/docs`

OpenApi at:
`/openapi.json`

## Installation

Create new env python 3.12+

`pip install -r requirements.txt`

## Run

To run development server from main directory type:

`uvicorn app.main:app --reload --header server:PowtorkiOnlineApi`

To run production server from main directory type:

`uvicorn app.main:app --workers 12 --header server:PowtorkiOnlineApi`