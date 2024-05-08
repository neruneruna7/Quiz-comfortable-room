import requests
import datetime

def evaluate_temperature_and_humidity(month, temperature, humidity):
    if month in range(3, 6):  # March to May
        temp_score = 0
        if (temperature >= 18 or temperature <= 26) and (temperature < 20 or temperature > 24):
            temp_score += 1
        elif 20 <= temperature <= 24:
            temp_score += 2
    
        humidity_score = 0
        if (humidity >= 30 or humidity <= 70) and (humidity < 40 or humidity > 60):
            humidity_score += 1
        elif 40 <= humidity <= 60:
            humidity_score += 2

    elif month in range(6, 9):  # June to August
        temp_score = 0
        if (temperature >= 23 or temperature <= 30) and (temperature < 25 or temperature > 28):
            temp_score += 1
        elif 25 <= temperature <= 28:
            temp_score += 2

        humidity_score = 0
        if (humidity >= 40 or humidity <= 70) and (humidity < 50 or humidity > 60):
            humidity_score += 1
        elif 50 <= humidity <= 60:
            humidity_score += 2

    elif month in range(9, 12):  # September to November
        temp_score = 0
        if (temperature >= 18 or temperature <= 26) and (temperature < 20 or temperature > 24):
            temp_score += 1
        elif 20 <= temperature <= 24:
            temp_score += 2

        humidity_score = 0
        if (humidity >= 30 or humidity <= 70) and (humidity < 40 or humidity > 60):
            humidity_score += 1
        elif 40 <= humidity <= 60:
            humidity_score += 2

    else:  # December to February
        temp_score = 0
        if (temperature >= 16 or temperature <= 24) and (temperature < 18 or temperature > 22):
            temp_score += 1
        elif 18 <= temperature <= 22:
            temp_score += 2

        humidity_score = 0
        if (humidity >= 30 or humidity <= 60) and (humidity < 40 or humidity > 50):
            humidity_score += 1
        elif 40 <= humidity <= 50:
            humidity_score += 2

    return temp_score, humidity_score

def evaluate_co2(co2):
    if co2 <= 500:
        return 2
    elif 500 < co2 <= 1000:
        return 1
    elif co2 > 1000:
        return 0

def evaluate_overall_score(temp_score, humidity_score, co2_score):
    total_score = temp_score + humidity_score + co2_score
    if total_score == 6:
        return "◎"
    elif 4 <= total_score <= 5:
        return "〇"
    elif 2 <= total_score <= 3:
        return "△"
    elif 0 <= total_score <= 1:
        return "×"

res = requests.get('https://proxy.cep-hd-dlp.chuden.co.jp/data-n8suh89sqhcjo5g5/data-api/latest?id=CgETViZ2&subscription-key=0e35a874f02a4887adc1ed0b2561f645') # 実験室用
for i in range(8):
    res_json = res.json()[i]
    sensorNumber = res_json['sensorNumber']
    sensorName = res_json['sensorName']
    co2 = res_json['co2']
    if co2 == None: continue # データ無ければ次
    print(sensorNumber, sensorName)
    temperature = res_json['temperature']
    relativeHumidity = res_json['relativeHumidity']
    timestamp = res_json['timestamp']
    dt = datetime.datetime.fromtimestamp(timestamp)


    month = datetime.datetime.now().month
    temp_score, humidity_score = evaluate_temperature_and_humidity(month, temperature, relativeHumidity)
    co2_score = evaluate_co2(co2)
    overall_score = evaluate_overall_score(temp_score, humidity_score, co2_score)

    print(f'温度スコア: {temp_score}, 湿度スコア: {humidity_score}, CO2スコア: {co2_score}')
    print(f'総合評価: {overall_score}')
    print(f'CO2濃度={co2}[ppm], 気温={temperature}[deg], 相対湿度={relativeHumidity}[%], タイムスタンプ={dt}')
