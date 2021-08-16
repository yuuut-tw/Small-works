import pandas as pd
import tkinter as tk

# Functions
# 點選縣市選項按鈕後處理函式
def rbCity():
	global sitelist, listradio
	sitelist.clear() # 清除原有測站串列
	for r in listradio: # 移除原有測站選項按鈕
		r.destroy()
	n = 0
	for c1 in df["county"]: # 逐一取出選取縣市的測站
		if (c1 == city.get()):
			sitelist.append(df.iloc[n, 0])
		n += 1
	sitemake() # 建立測站選項按鈕
	rbSite() # 顯示PM2.5訊息

# 點選測站選項按鈕後處理函式
def rbSite():
	n = 0
	for s in df.iloc[:, 0]: # 逐一取得測站
		if (s == site.get()): # 取得點選的測站
			pm = df.iloc[n, 2] # 取得數值
			if (pd.isnull(pm)): # 如果沒有資料
				result1.set(s + "站的pm2.5目前無資料")
			else: # 轉換成等級
				if (pm <= 35):
					grade1 = "low"
				elif (pm <= 53):
					grade1 = "Mid"
				elif (pm <= 70):
					grade1 = "High"
				else:
					grade1 = "Extreme High"
				result1.set(s + "站的pm2.5值為「{}」:「{}」等級".format(str(pm), grade1)
							+"\n更新時間{}".format(df["DataCreationDate"][0])
				            )
			break # 找到點選測站就離開迴圈
		n += 1

# 重新讀取資料
def clickRefresh():
	global df
	link = "https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=csv"
	df = pd.read_csv(link)
	rbSite() # 更新測站資料

# 建立測站選項按鈕
def sitemake():
	global sitelist, listradio
	for city in sitelist:  # 逐一建立選項按鈕
		rbtem = tk.Radiobutton(frame2, text=city, variable=site, value=city, command=rbSite)
		listradio.append(rbtem) # 加入選項按鈕串列
		if (city == sitelist[0]): # 預設為第一個項目
			rbtem.select()
		rbtem.pack(side="left")

# =================================================================================================
# 讀取檔案
link = "https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=csv"
df = pd.read_csv(link)
print(df)

# 排列縣市順序 => pd.Categorical
tw_county = ['臺北市', '新北市', '基隆市', '宜蘭縣',
			 '桃園市', '新竹市', '新竹縣', '苗栗縣',
			 '臺中市', '彰化縣', '南投縣',
			 '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
			 '臺東縣', '花蓮縣',
			 '連江縣', '金門縣', '澎湖縣']
df["county"] = pd.Categorical(df["county"], tw_county)

# =================================================================================================
# TKinter 介面配置
window = tk.Tk()
window.geometry("640x270")
window.title("PM2.5即時資料站")

# 變數設立
city = tk.StringVar() # 縣市文字變數
site = tk.StringVar() # 監測站變數
result1 = tk.StringVar() # 訊息文字變數
citylist = [] # 縣市串列
sitelist = [] # 鄉鎮串列
listradio = [] # 鄉鎮選項按鈕串列

df_city_order = df.sort_values("county")
# 建立城市串列
for c1 in df_city_order["county"]:
	if (c1 not in citylist):
		citylist.append(c1)

# 建立第一個縣市的測站串列
count = 0
for c1 in df_city_order["county"]:
	if (c1 == citylist[0]):
		sitelist.append(df_city_order.iloc[count, 0])
	count += 1


label1 = tk.Label(window, text="縣市：")
label1.pack()

frame1 = tk.Frame(window) # 縣市容器
frame1.pack()
for i in range(0, 3):
	for j in range(0, 8):
		n = i*8 + j
		if (n < len(citylist)):
			city1 = citylist[n]
			rbtem = tk.Radiobutton(frame1, text=city1, variable=city, value=city1, command= rbCity)
			rbtem.grid(row=i, column=j)
			if (n == 0):
				rbtem.select()

label2 = tk.Label(window, text="測站：", pady=6, fg="blue", font=("新細明體", 12))
label2.pack()

frame2 = tk.Frame(window)
frame2.pack()
sitemake()

btnDown = tk.Button(window, text="更新資料", command=clickRefresh)
btnDown.pack(pady=6)

lblResult = tk.Label(window, textvariable=result1, fg="green")
lblResult.pack()
rbSite()

window.mainloop()
