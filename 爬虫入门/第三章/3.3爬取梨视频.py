import requests

# 真实的地址
# https://video.pearvideo.com/mp4/short/20241214/cont-1797596-16042162-hd.mp4

# 虚假的地址
# https://video.pearvideo.com/mp4/short/20241214/1736493475895-16042162-hd.mp4

url = "https://www.pearvideo.com/video_1797596"
count = url.split("_")[-1]
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "referer":"https://www.pearvideo.com/video_1797596"
}
response = requests.get("https://www.pearvideo.com/videoStatus.jsp?contId=1797596&mrd=0.4902021990282832",headers=headers)
print(response.json())
dict = response.json()
originurl = dict["videoInfo"]["videos"]["srcUrl"]
systemTime = dict["systemTime"]
print(originurl)
realurl = originurl.replace(systemTime,f"cont-{count}")
print(realurl)
with open("a.mp4","wb") as f:
    f.write(requests.get(realurl).content)