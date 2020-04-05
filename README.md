# Shop Local

Code for https://shoplocal.se/.

## Running

1. Setup App Engine runtime using instructions on https://cloud.google.com/appengine/docs/standard/python3/quickstart.


2. Create an isolated Python environment

```
python3 -m venv env
source env/bin/activate
```

3. The App Engine JSON service account config should be added to `config/shoplocalese.json`.


4. Get requirements

```
pip install  -r requirements.txt

```

5. Start the server

```
Start local devleopment environment:

```
python main.py
```
