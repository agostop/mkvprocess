from flask import Flask, request,render_template,make_response,url_for,redirect

app = Flask(__name__)

@app.route('/redeee')
def red():
	param=request.args['test']
	return param

@app.route('/test')
def test():
	return redirect(url_for('red',test='methon'))


if __name__ == '__main__':
	app.run(debug=True)
