import os
import config
from flask import render_template

app = config.connex_app
app.add_api('swagger.yml')


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser default url

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

