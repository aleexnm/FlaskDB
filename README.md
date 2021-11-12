# FlaskDB

Flask project gets data from a MySQL database into an HTML file with Bootstrap.
This application was made on PyCharm and on a Xubuntu VM hosted on Microsoft Windows server running in IIS.

## How to set up Flask 

Verify Python 3 installation
```
$ python3 -V
```
Install virtual environment
```
sudo apt install python3-venv
```
Navigate to the directory on which you wish to install the virtual environment.
Create a new directory for the Flask app and move into it.
```
mkdir flask_app && cd flask_app
```

Run this command in the directory you created.
```
python3 -m venv venv
```
The command will create a directory called venv, which contains a copy of the Python binary, the Pip package manager , the standard Python library, and other supporting files. You can use any name you want for the virtual environment.

To start using the virtual environment, you need to activate it with the activate script:

```
source venv/bin/activate
```

Once activated, the virtual environment’s bin directory will be added at the beginning of the $PATH variable. Your shell’s prompt will also change and show the name of the virtual environment you’re currently using. In this example that is venv.
Now that the virtual environment is activated, use the Python package manager pip to install Flask:

```
pip install Flask
```

To verify the installation, run the following command, which prints the Flask version:

```
python -m flask --version
```

Output should state the version of flask on your machine

## Creating an app for testing

Open python IDE (pycharm used for this project) and type the following python code:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
```

Here is what the code does:

1.- That first line imports the Flask class.
2.- The second line creates a new instance of the Flask class.
3.- The route() decorator is used to register the ```hello_world``` function for ```the / route```. When this route is requested, the function is called, and the message ```“Hello World!”``` is returned to the client.
Save the file as hello.py and go back to your terminal window.

We’ll use the flask command to run the application, but before that, we need to tell the shell the application to work with by setting the FLASK_APP environment variable:

```
(venv) $ export FLASK_APP=hello.py
(venv) $ flask run
```

Output should look like this:

```
 * Serving Flask app "hello.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Open http://127.0.0.1:5000 in your web browser , and you will be presented with the ```“Hello World!”``` message (in this case) or if you are running this application it should show the main dropdown of the clinics.

To stop the development server type, CTRL-C in your terminal.

Once you are done with your work, deactivate the environment by typing deactivate, and you will return to your normal shell

```
(venv) $ deactivate
```

```NOTE: flask needs to be runnning always for the app to work```
```NOTE 2: it is important to keep every file on the respective folder in order for the app to run correctly```



