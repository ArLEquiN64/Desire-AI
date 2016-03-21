import http.client
cnt = http.client.HTTPConnection("danbooru.donmai.us")
dir = "data"
start = 3
num = 1
n = 100
for j in range(start, start + num):
    f = open(dir + "/index" + str(j) + ".json", "wb")
    f.write('['.encode("utf-8"))
    for i in range(j * n, (j + 1) * n):
        cnt.request("GET", "/posts/" + str(i) + ".json")
        r1 = cnt.getresponse()
        data = r1.read()
        f.write(data)
        if(i != (j + 1) * n - 1):
            f.write(",".encode("utf-8"))
    f.write("]".encode("utf-8"))
    f.close()