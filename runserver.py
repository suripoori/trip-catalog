__author__ = 'Suraj'

from trip_planner import app

if __name__ == '__main__':
    app.secret_key = 'some_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)