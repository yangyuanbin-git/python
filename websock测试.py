import asyncio
import websockets
import json
import requests  # 新增：用于发送 HTTP 请求

# 配置信息
HTTP_URL = "http://127.0.0.1:47000/osai/serial/open?dev_name=COM2&protocol_type=DJ&async_read=1"
WS_URI = "ws://127.0.0.1:47001"

def open_serial_port():
    """首先调用 HTTP 接口打开串口"""
    print(f"[*] 正在请求打开串口: {HTTP_URL}")
    try:
        # 发送 GET 请求
        response = requests.get(HTTP_URL, timeout=5)
        # 检查 HTTP 状态码
        if response.status_code == 200:
            print(f"[+] HTTP 请求成功: {response.text}")
            return True
        else:
            print(f"[-] HTTP 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] 调用 HTTP 接口时出错: {e}")
        return False

async def listen_websocket():
    """监听 WebSocket 数据"""
    print(f"[*] 正在尝试连接 WebSocket: {WS_URI}")
    try:
        async with websockets.connect(WS_URI) as websocket:
            print("[+] WebSocket 连接成功！等待接收数据...")
            while True:
                try:
                    message = await websocket.recv()
                    # 尝试解析 JSON
                    try:
                        data = json.loads(message)
                        print(f"\n[收到 JSON]: {json.dumps(data, indent=4, ensure_ascii=False)}")
                    except json.JSONDecodeError:
                        print(f"\n[收到 文本]: {message}")
                except websockets.ConnectionClosed:
                    print("[-] WebSocket 连接已断开")
                    break
    except Exception as e:
        print(f"[-] WebSocket 无法连接: {e}")

if __name__ == "__main__":
    # 1. 先执行 HTTP 调用
    if open_serial_port():
        # 2. 如果 HTTP 调用成功（或至少没崩溃），则进入 WebSocket 监听
        try:
            asyncio.run(listen_websocket())
        except KeyboardInterrupt:
            print("\n程序已手动停止")
    else:
        print("[-] 由于串口打开失败，程序终止。")