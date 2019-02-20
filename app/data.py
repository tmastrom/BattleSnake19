data = {"turn": 0, 
        "game": {"id": "1be5fdb7-9a78-4ac7-b84a-eba3403f364d"}, 
        "board": {
            "food": [{"y": 14, "x": 13}, {"y": 3, "x": 10}, 
                    {"y": 10, "x": 8}, {"y": 12, "x": 2}, 
                    {"y": 7, "x": 13}, {"y": 7, "x": 5}, 
                    {"y": 0, "x": 10}, {"y": 3, "x": 2}, 
                    {"y": 2, "x": 8}, {"y": 8, "x": 10}], 
            "width": 15, 
            "snakes": [{
                "body": [
                    {"y": 9, "x": 3}, 
                    {"y": 8, "x": 3},
                    {"y": 8, "x": 4}, 
                    {"y": 7, "x": 4}], 
                "health": 100, 
                "id": "fd26ec2c-b06d-441c-ae4f-b6b400587eba", 
                "name": "me"}], 
            "height": 15}, 
        "you": 
            {"body": [
                {"y": 9, "x": 3}, 
                {"y": 9, "x": 3}, 
                {"y": 9, "x": 3}], 
            "health": 100, 
            "id": "fd26ec2c-b06d-441c-ae4f-b6b400587eba", 
            "name": "me"}
        }
xaxis = []
yaxis = []
dont = []

for x in range(data["board"]["width"]+1):
    xaxis.append(x)
for x in range(data["board"]["height"]+1):
    yaxis.append(x)

for i in data["you"]["body"]:
    pos = [i['x'],i['y']]
    print pos

leftside = [[0, y] for y in yaxis]
rightside = [[data["board"]["width"], y] for y in yaxis]
top = [[x, 0] for x in xaxis]
bottom = [[x,data["board"]["height"]]for x in xaxis]

dont = top + bottom + rightside + leftside
#print dont
