import mysql.connector as mysql
from flask import Flask, request

app = Flask(__name__)

conn = mysql.connect(
    host="sql12.freesqldatabase.com",
    username="sql12610742",
    database="sql12610742",
    password="PP7szeFBIv",
)

# conn = mysql.connect(
#     host="basildevapi.mysql.pythonanywhere-services.com",
#     username="basildevapi",
#     database="basildevapi$test",
#     password="basilbasil",
# )

db = conn.cursor()
tn = "sample"


@app.route('/', methods=['post', 'get'])
def home():
    return 'Welcome!!! To Basil Site'


@app.route("/get", methods=["POST"])
def getUser():
    try:
        data = request.json["data"]
        if data == "all":
            pass
        else:
            return {
                "Status": f"Error", "Error": "Invalid Value"}
        sql = f"select * from {tn}"
        db.execute(sql)
        res = []
        for i in db.fetchall():
            res.append({"Name:": i[0], "Number:": i[1]})
        return res
    except KeyError as k:
        return {"Status": f"Error", "Error": f"{k} key is not Found"}


@app.route("/add", methods=["POST"])
def addUser():
    try:
        name = request.json["name"]
        num = request.json["number"]
        if type(num) == str:
            return {
                "Status": f"Error", "Error": "Number Not A String"}
        elif len(str(num)) != 10:
            return {
                "Status": f"Error", "Error": "Invalid Number"}
        sql = f"insert into {tn}(name,number) values(%s,%s)"
        val = [name, num]
        db.execute(sql, val)
        conn.commit()
        return {"Status": f"Success"}
    except KeyError as k:
        return {"Status": f"Error", "Error": f"{k} key is not Found"}
    except mysql.errors.IntegrityError as err:
        if err.errno == 1062:
            return {
                "Status": f"Error", "Error": f"{err.msg}"}
        return "Error"


@app.route("/deleteAllDatas", methods=["POST"])
def truncate():
    try:
        data = request.json["data"]
        if data == "all":
            pass
        else:
            return {
                "Status": f"Error", "Error": "Invalid Value"}
        sql = f"delete from {tn}"
        db.execute(sql)
        conn.commit()
        return {"Status": f"Success"}
    except KeyError as k:
        return {"Status": f"Error", "Error": f"{k} key is not Found"}
    except mysql.errors.IntegrityError as err:
        if err.errno == 1062:
            return {
                "Status": f"Error", "Error": f"{err.msg}"}
        return "Error"


if __name__ == '__main__':
    app.run()
