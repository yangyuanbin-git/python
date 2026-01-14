from pywinauto import Desktop

try:
    # 绕过 app 链条，直接从桌面顶层根据标题锁定
    main_window = Desktop(backend="uia").window(title="OSAI_POS_Plugin")
    
    # 打印该窗口下所有的子组件（包括 ID 和 Name）
    # 这步如果也卡住，说明权限依然被系统底层拦截了
    print("--- 正在扫描窗口组件树，请稍候 ---")
    main_window.print_control_identifiers()
    
except Exception as e:
    print(f"扫描失败: {e}")