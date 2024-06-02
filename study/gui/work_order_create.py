import base64
import tkinter
import tkinter.ttk as ttk
from datetime import datetime
from random import random
from tkinter import messagebox
import json
import random
import requests
from pymysql import Connection




def connection() -> Connection:
    return Connection(
        host="",
        port=3306,
        user="root",
        password="",
        autocommit=True, connect_timeout=2
    )


def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # 将datetime对象转换为ISO格式的字符串

def mapping_order_type(ordertype):
    return {'2': 'faultWorkflow', '4': 'bossWorkflow', '5': 'businessOrderWorkflow', '6': 'appealWorkflow'}.get(
        ordertype)

def creat():
    """
    工单生成
    :return:
    """
    # 校验输入
    if (validate_input(order_limit_entry.get())):
        all_disabled()
        bottom_text.insert(tkinter.END, "\n\n========>初始化数据库连接中:")
        try:
            con = connection()
        except:
            bottom_text.insert(tkinter.END, "\n========>初始化数据库连接失败:请连接VPN")
            all_normal()
            return
        bottom_text.insert(tkinter.END, "\n========>初始化数据库连接成功:" + con.get_server_info())
        bottom_text.insert(tkinter.END, "\n========>获取数据中:")
        con.select_db('cmms')
        cursor = con.cursor()
        cursor.execute("select * from  work_order_info where order_source= %s order by id desc limit %s",
                       (order_source_dict[order_source_box.get()], int(order_limit_entry.get())))
        bottom_text.insert(tkinter.END,
                           f"\n========>select * from  work_order_info where order_source= {order_source_dict[order_source_box.get()]} order by id desc limit {order_limit_entry.get()}")
        data = cursor.fetchall()
        con.close()
        bottom_text.insert(tkinter.END, f"\n========>获取到{len(data)}条数据:开始数据插入")
        for getDatum in data:
            print(getDatum[6])
            workorder = WorkOrder(getDatum[9], getDatum[31], getDatum[50], getDatum[38], getDatum[37], getDatum[13],
                                  getDatum[11],
                                  getDatum[12], getDatum[44], order_source_dict[order_source_box.get()], getDatum[6],
                                  getDatum[2],
                                  getDatum[14], None if getDatum[26] is None else str(getDatum[26]),
                                  None if getDatum[27] is None else str(getDatum[27]),getDatum[45] )

            # response = requests.post('http://223.75.3.75:20034/grid/gateway/workorder/workorder/work-order/doCreate',
            #                          json=json.loads(data))
            if order_source_box.get()!='大唐':
                data = json.dumps(workorder, ensure_ascii=False, default=lambda obj: obj.__dict__)
                print(json.loads(data))
                # 调用接口
                response=requests.post('', json=json.loads(data))
            else:
                workorder.orderType=mapping_order_type(getDatum[6])
                data = json.dumps(workorder, ensure_ascii=False, default=lambda obj: obj.__dict__)
                print(json.loads(data))
                #调用接口
                response = requests.post('',
                                     json=json.loads(data))
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            print(response.json())

        bottom_text.insert(tkinter.END, f"\n========>数据生成成功")
        all_normal()
    else:
        messagebox.showerror("Error", "Please enter a valid number between 0 and 50.")
        all_normal()


def validate_input(text):
    if text.isdigit() and 0 <= int(text) <= 50:
        return True
    else:
        return False


class WorkOrder:

    def __init__(self, createoperator, custname, extra, faultremarks, faulttype, linkaddr, linkman, linkphone,
                 operatorname, ordersource, ordertype, orderinfo, custid, preStime, preEtime,accNbrType):
        self.createOperator = createoperator
        self.custname = custname + '测试'
        self.extra = extra
        self.faultRemarks = faultremarks
        self.faultType = faulttype
        self.linkaddr = linkaddr
        self.linkman = linkman
        self.linkphone = linkphone
        self.operatorName = operatorname
        self.orderSource = ordersource
        self.orderType = ordertype
        self.orderinfo = orderinfo
        self.accNbrType = accNbrType
        self.areaid = 1118
        self.callinCode = genertate_random_numbers()
        self.city = 'WH'
        self.gridid = 1118
        self.ordernoOut = 'CS-ORDERNOOUT-' + str(random.randint(100000, 999999)).zfill(6)
        self.taskId = 'CS-TASKID-' + str(random.randint(100000, 999999)).zfill(6)
        self.custid = custid
        self.preStime = preStime
        self.preEtime = preEtime

    def __str__(self):
        return str(self.__dict__)


def genertate_random_numbers() -> str:
    # 前面两位
    area_code = ["13", "14", "15", "16", "17", "18", "19"]
    # 中间三位
    middle_numer = str(random.randint(0, 9999)).zfill(4)
    # 后四位
    last_number = str(random.randint(0, 9999)).zfill(4)
    return random.choice(area_code) + middle_numer + last_number


def all_disabled():
    order_source_box.config(state=tkinter.DISABLED)
    order_type_box.config(state=tkinter.DISABLED)
    order_limit_entry.config(state=tkinter.DISABLED)


def all_normal():
    order_source_box.config(state=tkinter.NORMAL)
    order_type_box.config(state=tkinter.NORMAL)
    order_limit_entry.config(state=tkinter.NORMAL)


order_type_dict = {"维修单": 2, "营销单": 3, "安装单": 4, "业务受理单": 5, "投诉单": 6}
order_source_dict = {"营业厅": 1, "CMP": 2, "呼叫中心": 3, "大唐": 4, "营维通": 5}
root = tkinter.Tk()
root.title("制单小工具")

tmp = open('pojo.ico', 'wb')        #创建临时的文件
tmp.write(base64.b64decode("AAABAAEAFBQAAAEAGAAoBQAAFgAAACgAAAAUAAAAKAAAAAEAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD+I8T+I8T/AP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD+JMT+I8T+IsQAAAAAAAAAAAD+KLr/LcP/k9z/rOT/rOT/rOT/rOT/rOT/rOT/rOT/rOT/rOT/rOT/rOT/Lr0AAAD+KLoAAAAAAAAAAAD+K7D+LbH/AP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD+KK7/MbL+K7YAAAAAAAAAAAAAAAD+rdIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/r9QAAAAAAAAAAAAAAAAAAAD+r8sAAAAAAAAAAAAAAAAAAAD+rOD/rOL/rOL/rOL/rOL+q+EAAAAAAAD/scsAAAAAAAAAAAAAAAAAAAD+ssMAAAAAAAAAAAAAAAAAAAD+scv/scv/scv/scv/scv/scsAAAAAAAD/s8MAAAAAAAAAAAAAAAAAAAD+tLkAAAAAAAAAAAAAAAAAAAD+t7P/t7T/t7T/t7T/t7T/t7QAAAAAAAD/tbsAAAAAAAAAAAAAAAAAAAD+t7IAAAAAAAAAAAAAAAAAAAAAAAAAAAD+u5//vJz/vJz/vJwAAAAAAAD/t7MAAAAAAAAAAAAAAAAAAAD+t6oAAAAAAAD/r9X/r9X/r9X/r9X/r9UAAAD/wYX/wYX/wYUAAAAAAAD/uasAAAAAAAAAAAAAAAAAAAD+uaMAAAAAAAD/tL7/tL7/tL7/tL7/tL4AAAD+xm/+xm/+x3EAAAAAAAD/uqMAAAAAAAAAAAAAAAAAAAD+vJkAAAAAAAD/uqb/uqb/uqb/uqb/uqYAAAAAAAAAAAAAAAAAAAAAAAD/vJoAAAAAAAAAAAAAAAAAAAD+vpIAAAAAAAD/v5D/v5D/v5D/v5D/v5AAAAAAAAAAAAAAAAAAAAAAAAD/v5IAAAAAAAAAAAAAAAAAAAD+vooAAAAAAAD/xXj/xXj/xXj/xXj/xXgAAAAAAAAAAAAAAAAAAAAAAAD/wIoAAAAAAAAAAAAAAAAAAAD+wYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/woIAAAAAAAAAAAAAAAD/aS3+omIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAD/sWz/fwAAAAAAAAAAAAD+ZSv+ZC3+p1n+xm/+xm/+xm/+xm/+xm/+xm/+xm/+xm/+xm/+xm/+xm/+Zyv/aS3+ZSkAAAAAAAAAAAD+aSD+ah/+YyoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD+aiL+ax/+aiIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///AAx/8QAMAAUADH/xAA7/+wAO+BsADvgbAA74GwAO/hsADsEbAA7BGwAOwfsADsH7AA7B+wAO//sADP/xAAwAAQAMf/EAD///AA///wAA=="))    ##把这个one图片解码出来，写入文件中去。
tmp.close()
root.iconbitmap("/pojo.ico")


# 创建一个标签
hello_lable = tkinter.Label(root, text="欢迎使用CMMS工单创建小工具 \t author:pojo123")
hello_lable.grid(row=0, column=0, columnspan=4, sticky="nsew")

order_type_lable = tkinter.Label(root, text="请选择工单类型:")
order_type_lable.grid(row=2, column=0)
# 创建工单选项下拉框
order_type_var = tkinter.StringVar()
order_type_box = ttk.Combobox(root, textvariable=order_type_var)
order_type_box["value"] = ["维修单", "安装单", "业务受理单", "投诉单"]
order_type_box.current(0)
order_type_box.grid(row=3, column=0)

order_source_lable = tkinter.Label(root, text="请选择工单来源:")
order_source_lable.grid(row=2, column=2)
# 创建工单来源下拉框
order_source_var = tkinter.StringVar()
order_source_box = ttk.Combobox(root, textvariable=order_source_var)
order_source_box["value"] = ["营业厅", "CMP", "呼叫中心", "大唐", "营维通"]
order_source_box.current(0)
order_source_box.grid(row=3, column=2)

# 创建工单条数输入框

order_limit_lable = tkinter.Label(root, text="请选择工单创建条数(1-50):")
order_limit_lable.grid(row=2, column=3)
order_limit_entry = tkinter.Entry(root)
order_limit_entry.insert(0, 1)
order_limit_entry.grid(row=3, column=3, padx=5, pady=5)

# 创建一个占据整个窗口长度的文本框
bottom_text = tkinter.Text(root)
bottom_text.grid(row=4, column=2, sticky="nsew")
bottom_text.insert(tkinter.END, "应用初始化完毕！！！")  # 放置在第1行第0列，并填充整个单元格

# 创建按钮
btn_map_publishing_send_publish = tkinter.Button(root)
btn_map_publishing_send_publish["text"] = "生成"
btn_map_publishing_send_publish["command"] = creat
btn_map_publishing_send_publish.grid(row=5, column=2)

root.mainloop()
