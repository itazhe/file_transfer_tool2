#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
import sys
import os
import hashlib
import json

server_ip = input("服务器IP地址：")
server_port = int(input("服务器端口："))

sock = socket.socket()
sock.connect((server_ip, server_port))

def get_file_md5(file_path):
    m = hashlib.md5()

    with open("E:\\recv\\%s" % file_path, "rb") as f:
        while True:
            data = f.read(1024)
            if len(data) == 0:
                break    
            m.update(data)
    
    return m.hexdigest().upper()

def client_login_send():
    '''
    函数功能：用户登录请求
    '''
    myuname = input("请输入用户名：")
    mypasswd = input("请输入密码：")
    req = '{"op": 1, "args":{"uname": "myuname", "passwd": "mypasswd"}}'
    data_top="{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())

def client_login_recv():
    '''
    函数功能：用户登录响应
    '''
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)

        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("登录成功！")

            while True:
            
                file_path = sock.recv(300).decode().rstrip()
                if len(file_path) == 0:
                    break

                file_size = sock.recv(15).decode().rstrip()
                if len(file_size) == 0:
                    break
                file_size = int(file_size)

                file_md5 = sock.recv(32).decode()
                if len(file_md5) == 0:
                    break

                # 如果为空文件夹
                if file_size == -1:
                    print("\n成功接收空文件夹 %s" % file_path)
                    os.makedirs("E:\\recv\\%s" % file_path, exist_ok=True)
                    continue

                
                os.makedirs(os.path.dirname("E:\\recv\\%s" % file_path), exist_ok=True)
          
                print("\n正在接收文件 %s，请稍候......" % file_path)

                f = open("E:\\recv\\%s" % file_path, "wb")

                recv_size = 0
                while recv_size < file_size:
                    file_data = sock.recv(file_size - recv_size)
                    if len(file_data) == 0:
                        break

                    f.write(file_data)
                    recv_size += len(file_data)

                f.close()

                recv_file_md5 = get_file_md5(file_path)

                if recv_file_md5 == file_md5:
                    print("成功接收文件 %s" % file_path)
                else:
                    print("接收文件 %s 失败（MD5校验不通过）" % file_path)
                    break

            sock.close()
        else:
            print("登录失败！")

def client_reg_send():
    '''
    函数功能：用户注册请求
    '''
    myuname = input("请输入用户名：")
    mypasswd = input("请输入密码：")
    myphone = input("请输入手机号：")
    myemail = input("请输入邮箱：")
    req = '{"op": 2, "args": {"uname": "myuname", "passwd": "mypasswd", "phone": "myphone", "email": "myemail"}}'
    data_top = "{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())

def client_reg_recv():
    '''
    函数功能：用户注册响应
    '''
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)

        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("注册成功！")
        else:
            print("注册失败！")

def client_uname_send():
    '''
    函数功能：校验用户名是否存在
    '''
    myuname = input("请输入用户名:")
    req = '{"op": 3, "args": {"uname": "myuname"}}'
    data_top = "{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())

def client_uname_recv():
    '''
    函数功能：用户名是否存在响应
    '''
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)

        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("用户名不存在！")
        elif rsp["error_code"] == 1:
            print("用户名已存在！")

while True:
    print(
    '''
    1.登录
    2.注册
    3.校验用户名
    4.退出
    ''')
    n = int(input("请输入序号>"))
    if n == 1:
        client_login_send()
        client_login_recv()
        break
    elif n == 2:
        client_reg_send()
        client_reg_recv()
    elif n == 3:
        client_uname_send()
        client_uname_recv()
    elif n == 4:
        break
    else:
        print("序号输入错误，请重新输入！")
