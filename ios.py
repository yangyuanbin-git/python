import wda
# 连接到 tidevice 转发的 WDA 服务
c = wda.Client('http://127.0.0.1:60105')
print(c.status())

# 启动设置 App
bundle_id = 'com.apple.Preferences'
s = c.session(bundle_id)

# 4. 操作示例
# 查找名字为 "Wi-Fi" 的设置项并点击
s(label="Wi-Fi").click()

# 5. 回到主屏幕
c.home()