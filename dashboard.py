from flask import Flask, render_template
from views.panel import panel
from views.dashboard import dashboard
from views.dash_source import dash_source
from views.integration import integration
from views.settings import settings
import leancloud


app = Flask(__name__)
app.register_blueprint(panel)
app.register_blueprint(dashboard)
app.register_blueprint(dash_source)
app.register_blueprint(integration)
app.register_blueprint(settings)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    leancloud.init('z6fhqxvpal43l238q7xzogfdls74my214o5bapm5vkwfn4xh',
                   'rb7jufb22o15nzc9ub5b6b0lx3xt845o2ofz494oc1s9esg8')
    app.run(debug=True)







