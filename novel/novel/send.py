import pyautogui
from wxauto import *
class Send():
    # 获取当前微信客户端
    wx = WeChat()
    # 获取会话列表
    wx.GetSessionList()
    '''
    # 输出当前聊天窗口聊天消息
    '''
    def get_message(self):
        msgs = self.wx.GetAllMessage
        for msg in msgs:
            print('%s : %s' % (msg[0], msg[1]))
        ## 获取更多聊天记录
        self.wx.LoadMoreMessage()
        msgs = self.wx.GetAllMessage
        for msg in msgs:
            print('%s : %s' % (msg[0], msg[1]))

    '''
    # 函数功能： 单个用户 单个文件发送
    '''
    def send_file_to_single_user(self,file, message,who):
        # 向某人发送文件
        print("******************************************")
        try:
            print(f"开始向单个用户`{who}`发送文件:{file}")
            self.wx.ChatWith(who)  # 打开`文件传输助手`聊天窗口
            if message!="":
                self.wx.SendMsg(message)
            if file != "":
                self.wx.SendFiles(file)
            print("发送完毕")
        except Exception as e:
            print("发送失败，原因:", e)
        print("******************************************")
        pyautogui.hotkey('alt', 'f4')

    '''
    # 函数功能： 多个用户 多个文件发送
    '''
    def send_files_to_mul_user(self,files, users):
        print("******************************************")
        # 向某人发送文件
        for who in users:
            try:
                print(f"开始跟{who}发送文件")
                self.wx.ChatWith(who)
                for file in files:
                    print(f"向用户`{who}`发送文件:{file}")
                    self.wx.SendFiles(file)
                print("发送完毕")
            except Exception as e:
                print("发送失败，原因:", e)
        print("发送成功")
        print("******************************************")


if __name__ == '__main__':
    se = Send()
    # file1 = r'D:\book\{}.txt'.format(name)  # 文件路径
    file1 = r'E:\picture\结果2023-03-29-13-42-48.png'  # 文件路径
    who = '文件传输助手'     # 适用于中文版微信
    se.send_file_to_single_user(file=file1,message="文件到了，请查收~" ,who=who)