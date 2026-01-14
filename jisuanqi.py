from pywinauto import Application
import time

# 启动并连接
Application(backend="uia").start("calc.exe")
time.sleep(2)

# 使用 connect 确保连接到已经运行的 UI 界面进程
app = Application(backend="uia").connect(title="计算器", timeout=10)
dlg = app.window(title="计算器")

# 执行操作
dlg.child_window(auto_id="num1Button", control_type="Button").wait('visible', timeout=5).click()
dlg.child_window(auto_id="plusButton", control_type="Button").click()
dlg.child_window(auto_id="num2Button", control_type="Button").click()
dlg.child_window(auto_id="equalButton", control_type="Button").click()

# 获取结果
result = dlg.child_window(auto_id="CalculatorResults", control_type="Text").window_text()
print(f"最终结果：{result}")

# dlg.close()