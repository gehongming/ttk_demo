# -- coding: utf-8 --
"""
@Time ： 2021/12/17 15:51
@Auth ： ghm
@File ：demo3.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap import Style, tk
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import time
from datetime import datetime
from urllib.parse import quote, parse_qs
from urllib import parse
import hmac
from hashlib import sha1
import base64
from urllib.parse import urlencode
from requests import request
import user
import requests
import os
import sys



os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
    os.path.dirname(sys.argv[0]), 'cacert.pem')  # request库需要用到该文件

LOG_LINE_NUM = 0


class HandleOpenapi:
    """
    生成请求openapi的请求地址
    """

    def __init__(
            self,
            path,
            method,
            protocol,
            host,
            access_key_secret,
            access_key_id):
        # 获取时间戳并进行url转码
        timestamp = quote(HandleOpenapi.get_utc_time())
        self.path = path
        self.method = method.upper()
        self.timestamp = timestamp
        self.protocol = protocol
        self.host = host
        # self.expires = expires
        self.access_key_secret = access_key_secret
        self.access_key_id = access_key_id

    def sign(self, s=None):
        # 排序后url
        if len(self.path.split('?')) > 1:
            s = self.path.split('?')[1]
            self.path = self.path.split('?')[0]
        if s:
            s = HandleOpenapi.encoded_params(param=s)
            temp_url = self.host + "/" + self.path + "?AccessKeyId=" + self.access_key_id + "&Expires=" + '86400' + \
                       "&Timestamp=" + self.timestamp + "&" + s
        else:
            temp_url = self.host + "/" + self.path + "?AccessKeyId=" + self.access_key_id + "&Expires=" + '86400' + \
                       "&Timestamp=" + self.timestamp
        # print("排序编码后url:",temp_url)
        url_param = self.method + temp_url
        # 对签名进行url编码
        # signature = quote(HandleOpenapi.hash_hmac(url_param, self.access_key_secret, sha1))
        signature = urlencode({"Signature": HandleOpenapi.hash_hmac(url_param, self.access_key_secret, sha1)})
        # 加上签名后的url
        result = temp_url + '&' + signature
        # result = temp_url + '&Signature=' + signature
        res = self.protocol + "://" + result
        # print("加上签名后的url:", res)
        return res

    @staticmethod
    def get_utc_time():
        time1 = datetime.utcfromtimestamp(int(time.time()))
        utc_time = time1.strftime("%Y-%m-%dT%H:%M:%SZ")
        return utc_time

    @staticmethod
    def hash_hmac(code, key, sha1):
        hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
        return base64.b64encode(hmac_code).decode()

    @staticmethod
    def encoded_params(param):
        param = HandleOpenapi.sort_params(param=param)
        dic = parse_qs(param)
        for key in dic:
            s = dic[key][0]
            dic[key] = s
        encoded_data = urlencode(dic)
        return encoded_data

    @staticmethod
    def sort_params(param):
        param = param.split('&')
        param_list = []
        for i in param:
            param_list.append(i)
        param_list.sort()
        result = ''
        for i in param_list:
            result += i + '&'
        return result[:-1]


class MY_GUI():

    def __init__(self, init_window_name):

        self.init_window_name = init_window_name
        self.init_window_name.title("openapi工具v2.9.2_小明")  # 窗口名
        # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1200x760+180+10')
        self.init_window_name.maxsize(1200, 760)
        self.init_window_name.minsize(1200, 760)

    # 设置窗口排版
    def set_init_window(self):
        # 标签
        self.init_protocol_label = ttk.Label(
            self.init_window_name,
            text='选择协议：',
            bootstyle='danger'
            )
        self.init_protocol_label.grid(row=1, column=0)

        self.init_host_label = ttk.Label(
            self.init_window_name,
            text='选择环境：',
            bootstyle='danger'
            )
        self.init_host_label.grid(row=2, column=0, rowspan=1)

        self.init_env_label = ttk.Label(
            self.init_window_name,
            text='虚拟环境标：',
            bootstyle=INFO
            )
        self.init_env_label.grid(row=3, column=0, rowspan=1)

        self.init_url_label = ttk.Label(
            self.init_window_name,
            text='接口地址：',
            bootstyle='danger'
            )
        self.init_url_label.grid(row=4, column=0, rowspan=1)

        self.init_method_label = ttk.Label(
            self.init_window_name,
            text='请求方式：',
            bootstyle='danger'
            )
        self.init_method_label.grid(row=5, column=0, rowspan=1)

        self.init_data_label = ttk.Label(
            self.init_window_name,
            text="get请求数据：",
            bootstyle=INFO
            )
        self.init_data_label.grid(row=6, column=0)

        self.access_key_secret = ttk.Label(
            self.init_window_name,
            text="秘钥：",
            bootstyle='danger'
            )
        self.access_key_secret.grid(row=7, column=0)

        self.access_key_id = ttk.Label(
            self.init_window_name,
            text="秘钥ID：",
            bootstyle='danger'
            )
        self.access_key_id.grid(row=8, column=0)

        self.init_json_label = ttk.Label(
            self.init_window_name,
            text="post数据格式：",
            bootstyle=INFO
            )
        self.init_json_label.grid(row=9, column=0)

        self.init_counts_label = ttk.Label(
            self.init_window_name, text="请求次数：", bootstyle=INFO)
        self.init_counts_label.grid(row=10, column=0)

        self.init_post_label = ttk.Label(
            self.init_window_name,
            text="post入参：",
            bootstyle=INFO
            )
        self.init_post_label.grid(row=12, column=0)

        self.str_button = ttk.Button(
            self.init_window_name,
            text="选择文件",
            width=10,
            bootstyle="info",
            command= self.upload_file
            )  # 调用内部方法  加()为直接调用
        self.str_button.grid(row=11, column=0)

        self.result_data_label = ttk.Label(
            self.init_window_name, text="输出结果", bootstyle='success',font=("宋体", 15))
        self.result_data_label.grid(row=0, column=16)


        # 下拉框
        cv3 = tkinter.StringVar()
        self.init_protocol_combobox = ttk.Combobox(
            self.init_window_name,
            width=27,
            height=0,
            textvariable=cv3,
            bootstyle='outline menubutton'
        )  # 选择协议录入框
        self.init_protocol_combobox.grid(row=1, column=1)
        self.init_protocol_combobox["value"] = ('http', 'https')

        cv = tkinter.StringVar()
        self.init_host_combobox = ttk.Combobox(
            self.init_window_name,
            width=30,
            height=0,
            textvariable=cv
        )  # 选择环境录入框
        self.init_host_combobox.grid(row=2, column=1, rowspan=1,pady=7)
        self.init_host_combobox["value"] = (
            'clink2-portal-yuzhilin-poc.cticloud.cn',
            "api-bj.clink.cn",
            "api-sh.clink.cn",
            'api-bj-test0.clink.cn',
            'clink2-openapi-dev.clink.cn',
            'alb-01l5fw2u4lg0sajop3.cn-beijing.alb.aliyuncs.com',
            'servicecenter.inspur.com:10010')

        self.init_env_Text = Entry(
            self.init_window_name,
            width=33,
            )  # height=1)  # 环境标录入框
        self.init_env_Text.grid(row=3, column=1, rowspan=1)
        # self.init_env_Text.insert(0, 'dev.feizq')  # debug用

        self.init_url_Text = Entry(
            self.init_window_name,
            width=33,)  # height=1)  # 接口地址录入框
        self.init_url_Text.grid(row=4, column=1, rowspan=1,pady=7)
        # self.init_url_Text.insert(0, 'customer_params')  # debug用

        # 下拉框
        cv2 = tkinter.StringVar()
        self.init_method_combobox = ttk.Combobox(
            self.init_window_name,
            width=27,
            height=0,
            textvariable=cv2,
            style='outline menubutton'
        )  # 请求方式录入框
        self.init_method_combobox.grid(row=5, column=1, rowspan=1,pady=7)
        self.init_method_combobox["value"] = ("GET", "POST")
        self.init_method_combobox.SelectedIndex = "GET"

        self.init_data_Text = Entry(
            self.init_window_name,
            width=33,)  # get请求数据录入框
        self.init_data_Text.grid(row=6, column=1, rowspan=1,pady=7)

        self.init_aks_Text = Entry(
            self.init_window_name,
            width=33,)  # 秘钥
        self.init_aks_Text.grid(row=7, column=1, rowspan=1,pady=7)
        # self.init_aks_Text.insert(0, '5XNS2km5KIf1274Ji3Ph')  # debug用

        self.init_aki_Text = Entry(
            self.init_window_name,
            width=33,)  # 秘钥ID录入框
        self.init_aki_Text.grid(row=8, column=1, rowspan=1,pady=7)
        # self.init_aki_Text.insert( 0, '2fb070dab1937d9451fbd4cb444b444f')  # debug用

        # 下拉框
        cv2 = tkinter.StringVar()
        self.init_type_combobox = ttk.Combobox(
            self.init_window_name,
            width=27,
            height=0,
            textvariable=cv2,
            style='outline menubutton'
        )  # post数据格式录入框
        self.init_type_combobox.grid(row=9, column=1, rowspan=1,pady=7)
        self.init_type_combobox["value"] = (
            "json", "form-data", "sms", "MultipartFile")

        self.init_count_Text = ttk.Entry(
            self.init_window_name,
            width=33,)  # 请求次数录入框
        self.init_count_Text.grid(row=10, column=1, rowspan=1,pady=7)
        self.init_count_Text.insert(0, 1)

        self.init_file_Text = ttk.Entry(
            self.init_window_name,
            width=33,)  # 文件选择框
        self.init_file_Text.grid(row=11, column=1, rowspan=1,pady=7)

        self.init_json_Text = ScrolledText(
            self.init_window_name,
            width=70,
            height=15)  # post入参框
        self.init_json_Text.grid(row=13, column=0, columnspan=10, padx=10)

        # self.log_data_Text = Text(
        #     self.init_window_name,
        #     width=70,
        #     height=9)
        # self.log_data_Text.grid(row=14, column=0, columnspan=10)
        # s = 'tinet_dev--4V0779O0p6601SGe1A81--ec77c8b35b137787551bd903ca7810c0\n' \
        #      'aliyun-test0--K6RJ6j8Qy3ynk43bkt01--e18656832567bd0bd191d46a64bc0063\n' \
        #      'aliyun-test2--IM01k8uFyW1400Mzpi7f--c04c8a558a57f53da81d4d0dd5cd6d46\n' \
        #      'tinet-test3--E7w7gTE79g550EC8qmO5--f6a5bbf509d61b7f5294ef23c01a00e9\n' \
        #      'aliyun-test2--IM01k8uFyW1400Mzpi7f--c04c8a558a57f53da81d4d0dd5cd6d46\n'
        # self.log_data_Text.insert('end', s)
        # self.log_data_Text.config(state='disabled')  # 禁止编辑

        self.result_data_Text = ttk.ScrolledText(
            self.init_window_name,
            width=70,
            height=40)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=18, columnspan=10)

        # 按钮
        self.str_button = ttk.Button(
            self.init_window_name,
            text="发送请求",
            width=10,
            command=self.openapi)  # 调用内部方法  加()为直接调用

        self.str_button.grid(row=1, column=11,rowspan=1,)

        self.str_button = ttk.Button(
            self.init_window_name,
            text="生成url",
            width=10,
            style='success',
            command=self.dourl)  # 调用内部方法  加()为直接调用
        self.str_button.grid(row=2, column=11,rowspan=2)

        self.copy_button = ttk.Button(
            self.init_window_name,
            text="复制",
            width=10,
            style='info',
            command=self.copy)  # 调用内部方法  加()为直接调用
        self.copy_button.grid(row=3, column=11,rowspan=3)

        self.clean_button = ttk.Button(
            self.init_window_name,
            text="清空",
            width=10,
            style='danger',
            command=self.clean)  # 调用内部方法  加()为直接调用
        self.clean_button.grid(row=4, column=11,rowspan=4)

    # 功能函数
    def openapi(self):
        protocol = self.init_protocol_combobox.get()
        host = self.init_host_combobox.get()
        env = self.init_env_Text.get()
        url = self.init_url_Text.get()
        method = self.init_method_combobox.get()
        s = self.init_data_Text.get()
        access_key_secret = self.init_aks_Text.get()
        access_key_id = self.init_aki_Text.get()
        type = self.init_type_combobox.get()

        jsons = self.init_json_Text.get('1.0', 'end')
        files = self.init_file_Text.get()
        files_name = str(files).split('/')[-1]
        count = self.init_count_Text.get()
        if not count:
            count = 1
        else:
            count = int(count)
        # print(method,url,s,access_key_id,access_key_secret,type,count,jsons)

        api = HandleOpenapi(
            path=url,
            host=host,
            access_key_secret=access_key_secret,
            access_key_id=access_key_id,
            method=method,
            protocol=protocol)  # 参数
        if not env:
            headers = {}
            sms_headers = {"Content-Type": "application/json"}
        else:
            headers = {"X-Virtual-Env": str(env)}
            sms_headers = {"Content-Type": "application/json",
                           "X-Virtual-Env": str(env)}

        if method == 'GET':
            if s:
                ur = api.sign(s=str(s))
            else:
                ur = api.sign()
            for i in range(count):
                try:
                    self.result_data_Text.insert(
                        END, f'-------请求第{i + 1}次,很快就好等一哈--------,\n'
                             f'-------请求url--------\n{ur},\n')
                    time.sleep(0.02)
                    self.result_data_Text.update()
                    response = request(
                        method=method, url=ur, headers=headers, timeout=8)
                except Exception as e:
                    self.result_data_Text.insert(END, f'请求报错{e}\n')
                else:
                    self.result_data_Text.insert(
                        END,
                        f'-------返回状态:{response.status_code}，\n'
                        f'-------请求返回:-------\n{response.text}\n')
                    time.sleep(0.02)
                    self.result_data_Text.update()
                time.sleep(0.01)
        else:
            try:
                jsons = eval(jsons)
            except BaseException:
                Messagebox.show_error(title='请求报错', message="json格式错误,请检查", alert=True, position=[600,300])
            else:
                ur = api.sign()
                if type == 'json':
                    for i in range(int(count)):
                        try:
                            self.result_data_Text.insert(
                                END, f'-------请求第{i + 1}次,很快就好等一哈--------,\n'
                                     f'-------请求url--------\n{ur},\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                            response = request(
                                method=method, url=ur, json=jsons, headers=headers, timeout=20)

                        except Exception as e:
                            self.result_data_Text.insert(END, f'\n 请求报错{e}')
                        else:
                            self.result_data_Text.insert(
                                END,
                                f'-------返回状态:{response.status_code}，\n'
                                f'-------请求返回:-------\n{response.text}\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                        time.sleep(0.01)
                elif type == 'sms':
                    for i in range(int(count)):
                        try:
                            self.result_data_Text.insert(
                                END, f'-------请求第{i + 1}次,很快就好等一哈--------,\n'
                                     f'-------请求url--------\n{ur},\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                            response = request(
                                method=method, url=ur, json=jsons, headers=sms_headers, timeout=20)

                        except Exception as e:
                            self.result_data_Text.insert(END, f'请求报错{e}\n')
                        else:
                            self.result_data_Text.insert(
                                END,
                                f'-------返回状态:{response.status_code}，\n'
                                f'-------请求返回:-------\n{response.text}\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()

                        time.sleep(0.01)
                elif type == 'MultipartFile':
                    for i in range(count):
                        try:
                            chat_files = [
                                ('file', (files_name, open(
                                    str(files), 'rb'), 'application/octet-stream'))]
                            self.result_data_Text.insert(
                                END, f'-------请求第{i + 1}次,很快就好等一哈--------,\n'
                                     f'-------请求url--------\n{ur},\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                            response = requests.post(
                                url=ur, data=jsons, files=chat_files, headers=headers, timeout=20)
                        except Exception as e:
                            self.result_data_Text.insert(END, f'\n 请求报错{e}')
                        else:
                            self.result_data_Text.insert(
                                END,
                                f'-------返回状态:{response.status_code}，\n'
                                f'-------请求返回:-------\n{response.text}\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                        time.sleep(0.01)
                else:  # type==form_data
                    for i in range(count):
                        try:
                            self.result_data_Text.insert(
                                END, f'-------请求第{i + 1}次,很快就好等一哈--------,\n'
                                     f'-------请求url--------\n{ur},\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                            response = requests.post(
                                url=ur, files=jsons, headers=headers, timeout=20)
                        except Exception as e:
                            self.result_data_Text.insert(END, f'\n 请求报错{e}')
                        else:
                            self.result_data_Text.insert(
                                END,
                                f'-------返回状态:{response.status_code}，\n'
                                f'-------请求返回:-------\n{response.text}\n')
                            time.sleep(0.02)
                            self.result_data_Text.update()
                        time.sleep(0.01)


    def dourl(self):
        protocol = self.init_protocol_combobox.get()
        host = self.init_host_combobox.get()
        url = self.init_url_Text.get()
        method = self.init_method_combobox.get()
        s = self.init_data_Text.get()
        access_key_secret = self.init_aks_Text.get()
        access_key_id = self.init_aki_Text.get()

        jsons = self.init_json_Text.get('1.0', 'end')

        api = HandleOpenapi(
            path=url,
            host=host,
            access_key_secret=access_key_secret,
            access_key_id=access_key_id,
            method=method,
            protocol=protocol)  # 参数
        if method == 'GET':
            if s:
                ur = api.sign(s=str(s))
            else:
                ur = api.sign()
        else:
            ur = api.sign()

        self.result_data_Text.insert(END, f'生成的url：{ur}\n')

    def clean(self):
        self.result_data_Text.delete('1.0', 'end')

    def copy(self):
        self.result_data_Text.clipboard_clear()
        text = self.result_data_Text.get('1.0', 'end')
        self.result_data_Text.clipboard_append(text)
        Messagebox.ok(
            message="复制成功",
            title="复制成功",
            alert=False,  # 指定是否响铃，默认False
            position=[600,300]   # 位置
        )

    def upload_file(self):
        # askopenfilename 1次上传1个；askopenfilenames1次上传多个

        selectFile = tkinter.filedialog.askopenfilename()
        if self.init_file_Text.get():
            self.init_file_Text.delete(0, END)
        self.init_file_Text.insert(0, selectFile)  # 将地址反写到输入框


def gui_start():
    style = Style(theme='ghm2')  # 先选择主题，代替了TK()实例化
    init_window = style.master  # 必须实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 主界面
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
