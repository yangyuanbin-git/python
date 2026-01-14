from pywinauto.application import Application
import time

def connect_app(easyconnect_path):
    try:
        # 1. 连接进程
        app = Application(backend="uia").connect(path=easyconnect_path, timeout=10)
        
        # 2. 优化：使用正则表达式匹配标题，防止因为版本号变动导致定位失败
        # 并且直接获取 handle 确保它是唯一的
        main_window = app.window(title_re=".*EasyConnect.*")
        
        # 3. 关键步骤：强制激活窗口并将其带到前台
        # 如果窗口在后台，click_input 有时会点错位置或无效
        if main_window.exists():
            main_window.set_focus() 
            print("窗口已激活")
            return main_window
        else:
            print("找不到对应的窗口")
            return None
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def click_new_button(main_window):
    if main_window is None: return
    
    try:
        # 4. 优化：如果精准 ID 不行，尝试加上 top_level_only=False 扩大搜索
        btn_new = main_window.child_window(
            auto_id="MainWidget.widget_content.stackedWidget.page_product.widget_tool_product.pushButton_add_product", 
            control_type="Button"
        )
        
        if btn_new.exists(timeout=5):
            # 尝试先让按钮可见
            btn_new.draw_outline(colour='red') # 调试用：看看红框在哪，确定定位准不准
            btn_new.click_input() 
            print("成功执行点击操作")
        else:
            print("未找到‘新建’按钮")
            
    except Exception as e:
        print(f"操作异常: {e}")

if __name__ == "__main__":
    PATH = r"D:\EasyConnect\EasyConnect.exe"
    win = connect_app(PATH)
    if win:
        click_new_button(win)