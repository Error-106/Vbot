from typing import NoReturn
from time import sleep
from asyncio import sleep
import requests
import re

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('请输入：/create + 用户名 来注册\n\n例如通过发送"/create helloworld"来注册一个用户名为helloworld的账号')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text('chatid:' + str(chat_id) + '\n\n创建账号：/create + 用户名\ne.g：/create helloworld\n\n重置密码：/reset\n需要先绑定账号，4.29后注册的账号无需手动绑定\n\n绑定账号：/bind + 用户名\ne.g：/bind helloworld\n\n查询账号信息：/info')


def info(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    check1 = judgebind(chat_id)
    if(check1 == 1):
        update.message.reply_text('你还未绑定Emby账号，请先绑定！')
    elif(check1 == 2):
        file = open('/root/accounts.txt',"r")
        accounts = file.read().splitlines()
        file.close()
        for account in accounts:
            accountss = account.split(' ')
            if(str(chat_id) == accountss[0]):
                userid = accountss[1]
        headers = {
        'accept': 'application/json',
        }

        params = {
            'api_key': '请在此处替换你的API',
        }
        response = requests.get('请把此处替换为你的Emby网址/emby/Users/' + userid, params=params, headers=headers)
        responsejson = response.json()
        name = responsejson['Name']
        createdate = responsejson['DateCreated']
        lastlogin = responsejson['LastLoginDate']
        update.message.reply_text('Emby用户名：' + name + '\n\n注册时间：' + createdate + '\n\n上一次登录时间：' + lastlogin)
    else:
        update.message.reply_text('未知错误，请联系管理员！')

def create(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    names = text.split(' ')
    name = names[1]
    chat_id = update.message.chat_id
    judge_back = judge(chat_id)
    if(judge_back == 1):
        update.message.reply_text('你的账号已经注册过Emby了！')
    elif(judge_back == 0):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = (
                    ('api_key', '请在此处替换你的API'),
                )

        data = '{"Name":"'+name+'","HasPassword":true}'

        response = requests.post('请把此处替换为你的Emby网址/emby/Users/New', headers=headers, params=params, data=data)

        status1 = response.status_code
        if(response != '' and status1 == 200):

            id1=re.findall(r'\"(.*?)\"',response.text)
            id=id1[9]

            headers1 = {
                            'accept': '*/*',
                            'Content-Type': 'application/json',
                        }

            params1 = (
                        ('api_key', '请在此处替换你的API'),
                    )

            data1 = '{"IsAdministrator":false,"IsHidden":true,"IsHiddenRemotely":true,"IsDisabled":false,"EnableRemoteControlOfOtherUsers":false,"EnableSharedDeviceControl":false,"EnableRemoteAccess":true,"EnableLiveTvManagement":false,"EnableLiveTvAccess":true,"EnableMediaPlayback":true,"EnableAudioPlaybackTranscoding":false,"EnableVideoPlaybackTranscoding":false,"EnablePlaybackRemuxing":false,"EnableContentDeletion":false,"EnableContentDownloading":false,"EnableSubtitleDownloading":false,"EnableSubtitleManagement":false,"EnableSyncTranscoding":false,"EnableMediaConversion":false,"EnableAllDevices":true}'

            requests.post('请把此处替换为你的Emby网址/emby/Users/'+id+'/Policy', headers=headers1, params=params1, data=data1)

            update.message.reply_text('注册用户名：' + name)
            f = open('/root/accounts.txt', 'a')
            f.write(str(chat_id) + ' ' + id + '\n')
            f.close()
        elif(status1 == 400):
            update.message.reply_text(response.text)
        else:
            update.message.reply_text('未知错误，请联系TG频道管理员！')


def reset(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    check = judge(chat_id)
    if(check == 0):
        update.message.reply_text('你还未注册过Emby公益服，请先注册！')
    elif(check == 1):
        check2 = judgebind(chat_id)
        if(check2 == 1):
            update.message.reply_text('你的TG账号还未绑定Emby公益服账号，请先绑定！')
        elif(check2 == 2):
            check3 = passwd(chat_id)
            if(check3 == 1):
                update.message.reply_text('密码移除成功，现密码为空！')
            else:
                update.message.reply_text('未知错误，请联系管理人员解决！')


def bind(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('暂时关闭绑定，4.29后注册的账号无需手动绑定！')
    '''text = update.message.text
    chatid = update.message.chat_id
    check = judgebind(chatid)
    if(check == 1):
        names = text.split(' ')
        name = names[1]
        userid = nametoid(name)
        with open("/root/accounts.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
        with open("/root/accounts.txt","w",encoding="utf-8") as f_w:
            for line in lines:
                if str(chatid) in line:
                    continue
                f_w.write(line)
        file2 = open('/root/accounts.txt','a')
        file2.write(str(chatid) + ' ' + userid + '\n')     
        file2.close()
        update.message.reply_text('绑定成功！')
    elif(check == 2):
        update.message.reply_text('你已经绑定过Emby账号了！')'''


def nametoid(name):
    headers = {
    'accept': 'application/json',
    }

    params = {
        'IsHidden': 'true',
        'IsDisabled': 'false',
        'Limit': '1',
        'NameStartsWithOrGreater': name,
        'api_key': '请在此处替换你的API',
    }

    response = requests.get('请把此处替换为你的Emby网址/emby/Users/Query', params=params, headers=headers)
    responsejson = response.json()
    id = responsejson['Items'][0]['Id']
    return id

def idtoname(chatid):
    file = open('/root/accounts.txt',"r")
    accounts = file.read().splitlines()
    file.close()
    for account in accounts:
        accountss = account.split(' ')
        if(str(chatid) == accountss[0]):
            userid = accountss[1]
    headers = {
    'accept': 'application/json',
    }

    params = {
        'api_key': '请在此处替换你的API',
    }
    response = requests.get('请把此处替换为你的Emby网址/emby/Users/' + userid, params=params, headers=headers)
    responsejson = response.json()
    name = responsejson['Name']
    return name


def judge(chat_id):
    file = open('/root/accounts.txt',"r")
    kk = 0
    accounts = file.read().splitlines()
    file.close()
    for account in accounts:
        accountss = account.split(' ')
        if(str(chat_id) == accountss[0]):
            kk = 1
    return kk

def judgebind(chat_id):
    file = open('/root/accounts.txt',"r")
    kk = 0
    accounts = file.read().splitlines()
    file.close()
    for account in accounts:
        accountss = account.split(' ')
        if(str(chat_id) == accountss[0]):
            length = len(accountss)
            if(length == 1):
                kk = 1
            elif(length == 2):
                kk = 2
    return kk

def passwd(chat_id):
    check = 0
    file = open('/root/accounts.txt',"r")
    accounts = file.readlines()
    file.close()
    for account in accounts:
        accountss = account.split(' ')
        if(str(chat_id) == accountss[0]):
            userid=accountss[1]
            headers = {
                'accept': '*/*',
            }

            params = {
                'api_key': '请在此处替换你的API',
            }

            json_data = {
                'ResetPassword': True,
            }

            response = requests.post('请把此处替换为你的Emby网址/emby/Users/'+userid+'/Password', params=params, headers=headers, json=json_data)
            status2 = response.status_code
            if(status2 == 204):
                check = 1
    return check



def main() -> None:
    """Start the bot."""

    updater = Updater("Telegram BOT API")
    
    dispatcher = updater.dispatcher

    # 机器人命令
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("create", create))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("bind", bind))
    dispatcher.add_handler(CommandHandler("info", info))
    

    # 启动机器人，勿删
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()