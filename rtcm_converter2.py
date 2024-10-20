import pyrtcm

# MSM7 -> MSM5
def convert_msm7_to_msm5(msg):
    if isinstance(msg, pyrtcm.MSM7):
        msm5 = pyrtcm.MSM5()
        msm5.header = msg.header  # ヘッダ情報をコピー
        msm5.sat_data = msg.sat_data  # 衛星データをコピー
        msm5.sig_data = msg.sig_data[:2]  # MSM5はMSM7のうち主要な2つの信号データを使用
        return msm5
    return msg

# MSM7 -> MSM4
def convert_msm7_to_msm4(msg):
    if isinstance(msg, pyrtcm.MSM7):
        msm4 = pyrtcm.MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        msm4.sig_data = msg.sig_data[:1]  # MSM4は1つの信号データのみを保持
        return msm4
    return msg

# MSM6 -> MSM5
def convert_msm6_to_msm5(msg):
    if isinstance(msg, pyrtcm.MSM6):
        msm5 = pyrtcm.MSM5()
        msm5.header = msg.header  # ヘッダ情報をコピー
        msm5.sat_data = msg.sat_data  # 衛星データをコピー
        msm5.sig_data = msg.sig_data[:2]  # MSM5に適合する信号データをコピー
        return msm5
    return msg

# MSM6 -> MSM4
def convert_msm6_to_msm4(msg):
    if isinstance(msg, pyrtcm.MSM6):
        msm4 = pyrtcm.MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        msm4.sig_data = msg.sig_data[:1]  # MSM4は1つの信号データのみを保持
        return msm4
    return msg

# MSM5 -> MSM4
def convert_msm5_to_msm4(msg):
    if isinstance(msg, pyrtcm.MSM5):
        msm4 = pyrtcm.MSM4()
        msm4.header = msg.header  # ヘッダ情報をコピー
        msm4.sat_data = msg.sat_data  # 衛星データをコピー
        msm4.sig_data = msg.sig_data[:1]  # MSM4は1つの信号データのみを保持
        return msm4
    return msg

# 入力されたデータを処理して変換する共通処理
def process_rtcm_data(input_data, convert_func):
    decoder = pyrtcm.RTCMDecoder(input_data)
    encoder = pyrtcm.RTCMEncoder()

    output_data = b''
    for msg in decoder:
        # 指定の変換関数でメッセージを変換
        converted_msg = convert_func(msg)
        output_data += encoder.encode(converted_msg)
    return output_data

# RTCMデータの読み込み（例としてバイナリ形式のデータ）
input_rtcm_data = b'...'  # 実際のRTCMバイナリデータをここに入力

# 実行例: MSM7 -> MSM5の変換
converted_msm5_data = process_rtcm_data(input_rtcm_data, convert_msm7_to_msm5)

# 実行例: MSM6 -> MSM4の変換
converted_msm4_data = process_rtcm_data(input_rtcm_data, convert_msm6_to_msm4)

# 変換されたデータをファイルに保存
with open("output_msm5.rtcm", "wb") as f:
    f.write(converted_msm5_data)

with open("output_msm4.rtcm", "wb") as f:
    f.write(converted_msm4_data)
