from utils.cookie import get_cookie
from utils.inputs import select_rbxmx
from utils.session import Session

auth_cookie = get_cookie()

s = Session(auth_cookie)
asset_id = s.upload(select_rbxmx())

print(asset_id)