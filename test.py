# 导入所需库
import requests
import pytest
# 后续的接口基础信息、测试函数等代码...
# 定义接口基础信息（集中管理，方便修改）
BASE_URL = "http://127.0.0.1:47000"
API_details = "/osai/sys/details"
FULL_URL_details = f"{BASE_URL}{API_details}"

API_version = "/osai/sys/version"
FULL_URL_version = f"{BASE_URL}{API_version}"

# 定义请求头（根据你的接口实际需求调整，比如加Token）
HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer your_token_here"  # 如果需要认证，取消注释并替换
}

# ---------------------- 核心测试用例 ----------------------
# 测试用例正常请求获取设备详细信息接口
def test_sys_details_normal_request():
    """获取设备信息接口"""
    try:
        # 发送GET请求（如果是POST，换成requests.post，同时加data/json参数）
        response = requests.get(
            url=FULL_URL_details,
            headers=HEADERS,
            timeout=10  # 设置10秒超时，避免脚本卡死
        )

        # 1. 验证响应状态码（正常应该是200）
        assert response.status_code == 200, f"状态码异常，预期200，实际{response.status_code}"

        # 2. 解析响应体（JSON格式）
        response_json = response.json()
        print("获取设备信息接口响应结果：", response_json)
        
        # 3. 验证响应体的关键字段（根据你的接口实际返回调整）
        # 示例：假设接口返回 {"code":0, "msg":"GetDetails success", "data":{...}}
        assert "code" in response_json, "响应体缺少code字段"
        assert response_json["code"] == 1, f"接口返回错误码，预期0，实际{response_json['code']}"
        assert response_json["msg"] == "GetDetails success!", f"提示信息异常，预期GetDetails success，实际{response_json['msg']}"
        assert "deviceinfo" in response_json, "响应体缺少deviceinfo字段"

    except requests.exceptions.Timeout:
        # 捕获超时异常
        assert False, "接口请求超时（超过10秒），请检查服务是否正常运行"
    except requests.exceptions.ConnectionError:
        # 捕获连接异常（比如服务没启动）
        assert False, "接口连接失败，请检查：1.服务是否启动 2.IP/端口是否正确 3.防火墙是否拦截"
    except Exception as e:
        # 捕获其他未知异常
        assert False, f"请求过程中出现未知错误：{str(e)}"

# 测试用例正常请求获取版本详细信息接口
def test_sys_version_normal_request():
    """获取版本信息接口"""
    try:
        # 针对sys/version的请求（和原接口逻辑类似，替换URL即可）
        response = requests.get(
            url=FULL_URL_version,
            headers=HEADERS,
            timeout=10
        )
        # 验证sys/version的响应（根据该接口的实际预期调整）
        assert response.status_code == 200, f"状态码异常，预期200，实际{response.status_code}"
        response_json = response.json()
        print("获取版本信息接口接口响应结果：", response_json)

        assert response_json["msg"] == "AISdkVersion success!", f"提示信息异常，预期AISdkVersion success，实际{response_json['msg']}"
        assert "version" in response_json, "响应体缺少version字段"  # 假设该接口返回version字段
        # 其他断言...
    except requests.exceptions.Timeout:
        # 捕获超时异常
        assert False, "接口请求超时（超过10秒），请检查服务是否正常运行"
    except requests.exceptions.ConnectionError:
        # 捕获连接异常（比如服务没启动）
        assert False, "接口连接失败，请检查：1.服务是否启动 2.IP/端口是否正确 3.防火墙是否拦截"
    except Exception as e:
        # 捕获其他未知异常
        assert False, f"请求过程中出现未知错误：{str(e)}"
# ---------------------- 运行测试 ----------------------
if __name__ == "__main__":
    # 运行所有测试用例，并生成HTML报告
    pytest.main([
        __file__,  # 当前脚本文件
        "-v",      # 显示详细测试结果
        "--html=sys_details_test_report.html"  # 生成测试报告（在当前目录）
    ])