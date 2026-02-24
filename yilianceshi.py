from pywinauto.application import Application
import pywinauto.mouse as mouse
import time

# --- 1. 连接函数 ---
def connect_app(easyconnect_path):
    try:
        # 建立连接
        app = Application(backend="uia").connect(path=easyconnect_path, timeout=10)
        main_window = app.window(title_re=".*EasyConnect.*")
        
        if main_window.exists():
            main_window.set_focus() 
            return app, main_window # 同时返回 app 和 window 方便后续重连
        return None, None
    except Exception as e:
        print(f"连接失败: {e}")
        return None, None

# --- 2. 批量处理函数 ---
def batch_create_products(app, main_window, times, item_data, exe_path):
    if main_window is None:
        return

    # 控件 ID 定义
    btn_new_id = "MainWidget.widget_content.stackedWidget.page_product.widget_tool_product.pushButton_add_product"
    base_id = "MainWidget.PopAddProduct.widget_background.stackedWidget.page_1.widget_4."
    sku_id = base_id + "lineEdit_sku"
    price_id = base_id + "lineEdit_sale_price"
    name_id = base_id + "lineEdit_name"
    save_id = "MainWidget.PopAddProduct.widget_background.widget_tool.pushButton_save"
    confirm_id = "MainWidget.PopMessageBox.widget_background.widget.pushButton_confirm"
    
    # 优化：删除按钮不建议使用超长全路径 ID，使用相对定位或后缀匹配更稳
    delete_id_end = "pushButton_delete"

    try:
        for i in range(times):
            print(f"\n>>> 正在执行第 {i+1}/{times} 组任务...")

            # 点击新建
            main_window.child_window(auto_id=btn_new_id, control_type="Button").click_input()
            
            # 等待弹窗
            sku_input = main_window.child_window(auto_id=sku_id, control_type="Edit")
            if not sku_input.exists(timeout=5):
                print("错误：弹窗加载超时")
                break

            # 输入信息
            print(f"输入数据: {item_data['name']} / {item_data['sku']}")
            sku_input.set_text(item_data['sku'])
            main_window.child_window(auto_id=price_id, control_type="Edit").set_text(item_data['price'])
            main_window.child_window(auto_id=name_id, control_type="Edit").set_text(item_data['name'])

            # 保存
            main_window.child_window(auto_id=save_id, control_type="Button").click_input()
            
            # 确认
            confirm_btn = main_window.child_window(auto_id=confirm_id, control_type="Button")
            if confirm_btn.exists(timeout=5):
                confirm_btn.click_input()
                print("已点击确认")

            # 刷新列表
            main_window.child_window(auto_id="MainWidget.widget_top_background.widget_top.widget_top_tool.pushButton_reload").click_input()
            print("已点击刷新")
            mouse.move(coords=(1805, 394))
            time.sleep(1) 
            mouse.click(coords=(1805, 394))
            print("已完成坐标点击,删除按钮")
            time.sleep(1)
            del_confirm = main_window.child_window(auto_id=confirm_id, control_type="Button")
            if del_confirm.exists(timeout=3):
               del_confirm.click_input()
            print("已确认删除")

        print("\n所有批量任务已完成！")

    except Exception as e:
        print(f"执行中断: {e}")

# --- 3. 主程序入口 ---
if __name__ == "__main__":
    EXE_PATH = r"D:\EasyConnect\EasyConnect.exe"
    LOOP_COUNT = 1 
    test_item = {"sku": "789456", "price": "100", "name": "测试商品"}

    # 建立连接
    app_obj, win = connect_app(EXE_PATH)
    while True:  
        if win: # 对象存在即为 True
            batch_create_products(app_obj, win, LOOP_COUNT, test_item, EXE_PATH)
        else:
            print("初始连接失败，请检查程序是否启动")
