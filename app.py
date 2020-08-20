from flask import Flask, render_template, request


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=('GET','POST'))
def main_page():

	if request.method == 'GET':
	
		return	render_template('trends_on_the_map.html')

 
