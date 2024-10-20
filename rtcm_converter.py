# use https://github.com/rtklibexplorer/rtklib-py
import rtcm
from rtcm.decoder import RTCMDecoder
from rtcm.encoder import RTCMEncoder
from rtcm.rtcmtypes import MSM4, MSM5, MSM6, MSM7

# MSM7 -> MSM5
def convert_msm7_to_msm5(msg):
    if isinstance(msg, MSM7):
        msm5 = MSM5()
        msm5.header = msg.header  # ヘッダ情報をコピー
        msm5.sat_data = msg.sat_data  # 衛星データをコピー
        msm5.sig_data = msg.sig_data  # 信号データをコピー（MSM5に対応する信号のみ）
        return msm5
    return msg

# MSM7 -> MSM4
def convert_msm7_to_msm4(msg):
    if isinstance(msg, MSM7):
        msm4 = MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        # MSM4には信号データが少ないため、適切なフィルタリングが必要
        msm4.sig_data = msg.sig_data[:1]  # 例えばL1信号のデータのみを含める
        return msm4
    return msg

# MSM6 -> MSM5
def convert_msm6_to_msm5(msg):
    if isinstance(msg, MSM6):
        msm5 = MSM5()
        msm5.header = msg.header  # ヘッダ情報をコピー
        msm5.sat_data = msg.sat_data  # 衛星データをコピー
        msm5.sig_data = msg.sig_data  # MSM5に対応する信号のみをコピー
        return msm5
    return msg

# MSM6 -> MSM4
def convert_msm6_to_msm4(msg):
    if isinstance(msg, MSM6):
        msm4 = MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        # MSM4は少ない信号しか含まないため、必要なフィールドだけを抽出
        msm4.sig_data = msg.sig_data[:1]  # 例えばL1信号のデータのみを含める
        return msm4
    return msg

# MSM5 -> MSM4
def convert_msm5_to_msm4(msg):
    if isinstance(msg, MSM5):
        msm4 = MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        # MSM4には限られた信号データだけが含まれる
        msm4.sig_data = msg.sig_data[:1]  # L1信号のデータを優先して含める
        return msm4
    return msg

# 入力されたデータを処理して変換する共通処理
def process_rtcm_data(input_data, convert_func):
    decoder = RTCMDecoder(input_data)
    encoder = RTCMEncoder()

    output_data = b''
    for msg in decoder:
        # 指定の変換関数でメッセージを変換
        converted_msg = convert_func(msg)
        output_data += encoder.encode(converted_msg)
    return output_data

# 実行例: MSM7 -> MSM5の変換
input_rtcm_data = b'...'  # RTCMバイナリデータを入力
converted_msm5_data = process_rtcm_data(input_rtcm_data, convert_msm7_to_msm5)

# 実行例: MSM6 -> MSM4の変換
converted_msm4_data = process_rtcm_data(input_rtcm_data, convert_msm6_to_msm4)

# 変換されたデータをファイルに保存
with open("output_msm5.rtcm", "wb") as f:
    f.write(converted_msm5_data)
    
with open("output_msm4.rtcm", "wb") as f:
    f.write(converted_msm4_data)
