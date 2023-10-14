import re
import csv
pattern = r'(\d+)([a-zA-Z]+)'


def findairport(icao):
    with open("文件", "r") as f:
        data = f.read()
        for i in data.split():
            try:
                i = i.split(",")
                if i[4] == icao:
                    return i[8]
            except:
                pass


def determine_direction(longitude1, longitude2):
    if longitude1 > longitude2:
        return "SO"
    elif longitude1 < longitude2:
        return "SE"
    else:
        return "在同一经度线上"

# 定义替换函数
def add_space(match):
    return match.group(1) + ' ' + match.group(2)


def routecheak():
    csvdata = [['Dep','Arr','Name','EvenOdd','AltList','MinAlt','Route','Remarks']]
    with open("文件", "r") as f:
        data = f.read().split()
        for i in data:
            try:
                i = i.split(",")
                arrairport = i[5]
                depairport = i[3]
                depairportlat = findairport(depairport).replace("N", "").replace("S", "").replace("E", "")
                arrairportlat = findairport(arrairport).replace("N", "").replace("S", "").replace("E", "")
                #把第二个数字后加个小数点
                depairportlat = depairportlat[:-1] + "." + depairportlat[2:]
                arrairportlat = arrairportlat[:-1] + "." + arrairportlat[2:]
                towards = determine_direction(float(depairportlat), float(arrairportlat))
                routes = i[9]
                transalt = i[14].split("/")[0]
                if transalt != "":
                    transalt = f"S{transalt}".replace("/","/S")
                    transalt = re.sub('[\u4e00-\u9fa5]', "",transalt)
                # 如何去掉中文字符串
                routes = re.sub('[\u4e00-\u9fa5]', '', routes)
                routes = routes.replace("VOR(", " ").replace("NDB(", " ").replace(")", "").replace("/", "").replace("、",
                                                                                                                    " ").replace(
                    "。", " ")
                routes = re.sub(pattern, add_space, routes)
                csvdata.append([depairport,arrairport,i[1],towards,transalt,"",routes,""])
            except:
                pass
        csvwrite(csvdata)
def csvwrite(data):
    # 将数据写入CSV文件
    with open('example.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
if __name__ == "__main__":
    routecheak()
