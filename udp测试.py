import socket
import json
import time
import threading

# 配置信息
SEND_ADDR = ('127.0.0.1', 63036)  # 发送指令的目标地址
RECV_ADDR = ('0.0.0.0', 36063)    # 本地监听返回数据的地址

def start_receiver():
    """接收端：监听 AI 返回的识别数据"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(RECV_ADDR)
        print(f"[*] 接收端已启动，正在监听端口 {RECV_ADDR[1]}...")
        
        while True:
            data, addr = s.recvfrom(4096)
            try:
                # 解析接收到的 JSON 数据
                payload = json.loads(data.decode('utf-8'))
                print(f"\n[+] 收到来自 {addr} 的返回数据:")
                print(json.dumps(payload, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"[-] 解析数据失败: {e}")

def send_recognition_request():
    """发送端：通知 AI 进行弹窗识别"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # 构造文档中的 JSON 数据
        msg = {
            "type": "AiRecognition",
            "sjc": int(time.time() * 1000)  # 生成当前毫秒时间戳
        }
        
        json_data = json.dumps(msg).encode('utf-8')
        s.sendto(json_data, SEND_ADDR)
        print(f"[>] 已发送识别指令到 {SEND_ADDR}: {msg}")
        

if __name__ == "__main__":
    # 1. 开启异步线程监听返回数据
    recv_thread = threading.Thread(target=start_receiver, daemon=True)
    recv_thread.start()

    # 稍等片刻确保监听启动
    time.sleep(1)

    # 2. 执行发送指令
    # 在实际应用中，你可以根据业务逻辑多次调用这个函数
    send_recognition_request()
    
    # 保持主线程运行，观察接收结果
    try:
        while True:
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已退出")