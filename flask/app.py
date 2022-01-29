from flask import Flask,render_template
import sqlite3
from gevent import pywsgi


app = Flask(__name__)


@app.route('/hdxw')
def news():
    datalist  = []
    connnect = sqlite3.connect("newsdata.db")
    cursor = connnect.cursor()
    sql = "select * from hdxw"
    data = cursor.execute(sql)
    for i in data:
        datalist.append(i)
    cursor.close()
    connnect.close()
    return render_template("hdxw.html",newsdata = datalist)




if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()