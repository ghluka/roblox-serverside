from flask import Blueprint, request

executor = Blueprint("executor", __name__)

users = {}

@executor.route('/api/execute', methods=['POST'])
def web_execute():
    user = request.args.get("userid")
    data = request.data.decode("utf8")
    
    if users.get(user) != None:
        users[user].append(data)
        return "OK"
    return "NO CLIENT"

@executor.route('/api/ping')
def roblox_ping():
    user = users.get(request.headers["user-id"])
    
    script = ""
    if not user:
        users.update({request.headers["user-id"]: []})
    elif len(user) > 0:
        script = user[0]
        user.pop(0)

    return script

@executor.route('/api/close', methods=['POST'])
def roblox_close():
    userid = request.headers["user-id"]

    if users.get(userid) != None:
        users.pop(userid)

    return "OK"