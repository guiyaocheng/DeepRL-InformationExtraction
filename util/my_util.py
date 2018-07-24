# -*-coding:utf-8-*-


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print
        path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print
        path + ' 目录已存在'
        return False


to_screen = False

def myprint(str):
    if to_screen:
        print(str)

def log(str, fname = 'log.txt', to_screen = True, append = True):
    if to_screen:
        print(str)
    if append:
        with open(fname, 'a') as f:
            print(str, file=f)
    else:
        with open(fname, 'w') as f:
            print(str, file=f)

def safe_str(str):
    s = str
    s = s.replace("/",".")
    s = s.replace(":",".")
    return s
