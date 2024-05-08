import requests
import datetime
import RPi.GPIO as GPIO
import time

# GPIOの設定
GPIO.setmode(GPIO.BOARD)
output_pin = 18  # BCM pin 18, BOARD pin 12
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)  # 初期状態をLOWに設定

# CO2の閾値を定義
CO2_THRESHOLD = 576

def get_data_from_node(node_id):
    # ノードからデータを取得
    res = requests.get('https://proxy.cep-hd-dlp.chuden.co.jp/data-n8suh89sqhcjo5g5/data-api/latest?id=CgETViZ2&subscription-key=0e35a874f02a4887adc1ed0b2561f645') # 実験室用
    if res.status_code == 200:
        return res.json()
    else:
        print(f"ノード {node_id} からデータの取得に失敗しました。ステータスコード: {res.status_code}")
        return None

def main():
    try:
        while True:
            # R3-401のデータを取得
            node_data = get_data_from_node("Ｒ３－４０１")
            if node_data:
                co2_r3_401 = None
                for res_json in node_data:
                    co2 = res_json.get('co2')  # 'co2'がNoneの場合を処理するために.get()を使用
                    if co2 is not None:
                        co2_r3_401 = co2
                        break

                if co2_r3_401 is not None:
                    print(f"Ｒ３－４０１のCO2濃度: {co2_r3_401} ppm")

                    # CO2濃度が閾値を超えているかどうかをチェック
                    if co2_r3_401 > CO2_THRESHOLD:
                        GPIO.output(output_pin, GPIO.HIGH)
                    else:
                        GPIO.output(output_pin, GPIO.LOW)

            else:
                print("Ｒ３－４０１のデータの取得に失敗しました。")

            time.sleep(1)  # 1秒間スリープ

    except KeyboardInterrupt:
        print("\nCTRL+Cが押されました。プログラムを終了します。")

    finally:
        GPIO.cleanup()  # GPIOの後片付け

if __name__ == '__main__':
    main()

