# COVID 19

Data Collection and Monitoring Tool for COVID19.

## Run (Development)

- create change .evn.copy file to .env and fill in your info.
- Set up postgres (check .env for config variables).
- load database - `python -m covid19.db.run +`
- create virtual environment
- pip install -r requirement.txt
- pip install -r dev-requirement.txt
- `./dev.sh`

### Extras

- drop database - `python -m covid19.db.run -`
- reload database - `python -m covid19.db.run -+`

## Run (Production)