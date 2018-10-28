#encoding=utf-8
import win32process
import win32gui
import pyHook
import pythoncom
from ctypes import *

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
PLAYER_BASE=0x635DB4#玩家对象基址
MONEY_OFFSET=0x24C#金钱偏移量
ADDRESS_CAN_DEPLOY=0x4991D0#建造函数偏移量
VIRTUAL_MEM = (0x1000 | 0x2000)
PAGE_EXECUTE_READWRITE = 0x00000040
dll = windll.LoadLibrary(u"ra2.dll")#编译好的动态库

def GetProcess():#获取游戏进程
    window = win32gui.FindWindow('Red Alert 2', 'Red Alert 2')  # 查找游戏窗体
    hid, pid = win32process.GetWindowThreadProcessId(window)  # 根据窗体得到进程编号
    process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)  # 用最高权限打开进程
    return process#返回的是进程地址

def GetValue(process, base, offset):
    data = c_int()
    kernel32.ReadProcessMemory(int(process), base + 0x400000, byref(data), 4, None)
    kernel32.ReadProcessMemory(int(process), data.value + offset, byref(data), 4, None)
    return data.value

def SetValue(process, base, offset, value):
    data =c_int()
    kernel32.ReadProcessMemory(int(process), base + 0x400000, byref(data), 4, None)
    address=data.value
    data = c_int(value)
    kernel32.WriteProcessMemory(int(process), address + offset, byref(data), 4, None)

def RemoteCall(process,function):
    address = kernel32.VirtualAllocEx(process, 0, 0x256, VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
    #首先申请256个字节的内存作为存放机器码的地方，这是我随便钦定的数字
    written = c_int(0)
    kernel32.WriteProcessMemory(process, address, function, 0x256, byref(written))
    # 把机器码写入到申请的内存地址
    thread = c_ulong(0)
    kernel32.CreateRemoteThread(process, None, 0, address, None, 0, byref(thread))
    #在申请的内存地址处创建一个远程线程，然后撒手不管
def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        GetCurrentProcess()
    elif event.Key=='F2':#任意建造
        process = GetProcess()
        kernel32.WriteProcessMemory(int(process), ADDRESS_CAN_DEPLOY, dll.CanDeploy, 12, None)
    elif event.Key=='F3':#开启全地图
        process = GetProcess()
        RemoteCall(process,dll.FullMap)
    if event.Key=='F5':#金钱+10000
        process = GetProcess()
        data = GetValue(process, PLAYER_BASE, MONEY_OFFSET)
        SetValue(process, PLAYER_BASE, MONEY_OFFSET, data + 10000)
    elif event.Key== 'F6':#选中的单位升级
        process = GetProcess()
        RemoteCall(process, dll.LevelUp)
    elif event.Key=='F7':#更改单位为自己所有
        process = GetProcess()
        RemoteCall(process,dll.ChangeOwnership)
    return True

def GetCurrentProcess():
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    executable = create_string_buffer("\x00" * 512)
    process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(process, None, byref(executable), 512)
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(process)

def main():
    hook = pyHook.HookManager()
    hook.KeyDown = KeyStroke
    hook.HookKeyboard()
    pythoncom.PumpMessages()

if __name__=="__main__":
    main()
