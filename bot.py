# 使用するライブラリのインポート
import discord  #discord.py
import re       #正規表現
import random   #ランダム
import ffmpeg   #音楽再生
import os
import subprocess
import glob     #条件に一致するファイルを取得
import time
import asyncio
from discord.ext import commands,tasks

from pydub import AudioSegment

playbot=1011929691566903306


#音楽の長さを取得する関数
def getTime(musicpath):
    sound = AudioSegment.from_file(musicpath, "m4a")
    # 情報の取得
    time = sound.duration_seconds # 再生時間(秒)
    # 情報の表示
    return time


# よくわからん。おまじない。
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



#メッセージを送る関数
async def sendMessage():
    print("send")
    botRoom = client.get_channel(playbot)   # botが投稿するチャンネルのID
    await botRoom.send("!play")




#無限再生用
endless=False

async def playmusic(message):
    if message.guild.voice_client is None:
        await message.channel.send("接続していません。")
    elif message.guild.voice_client.is_playing():
        await message.channel.send("再生中です。")
    else:
        #再生する曲をランダムで選択
        musiclist = glob.glob('../million/*.m4a')
        music = random.choice(musiclist)
        if(endless == True):
            print("endless is True")
        else:
            print("endless is False")

        musiclength = getTime(music)

        music1 = os.path.split(music)[1]
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
        message.guild.voice_client.play(source)
        await message.channel.send("”"+music1+"”を再生します。")
        print(music1)
        print(musiclength)

        await asyncio.sleep(int(musiclength)+3)
        print("wake up")
        if(endless == True):
            await playmusic(message)






# 起動時処理
@client.event
async def on_ready():
    botRoom = client.get_channel(playbot)   # botが投稿するチャンネルのID
    await botRoom.send("BOTが起動しました!")
    #サーバーにあるチャンネル情報の取得
    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名:" + str(channel.name))
        print("チャンネルID:" + str(channel.id))
        print("----------")
    # BOT情報の出力
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

   



@client.event
async def on_message(message):# メッセージが送られた時の処理


    # 送信者がBOTの場合反応しない
    #if message.author.bot:
        #return

    # 挨拶機能
    if not message.author.bot:
        if message.content.startswith("おはよう"):  # メッセージが「おはよう」で始まるか調べる
            m = "おはようございます " + message.author.name + " さん！"  # 返信の内容
            await message.channel.send(m)# メッセージが送られてきたチャンネルへメッセージを送る
    
    
    # 猫語会話機能
    # メッセージリスト（以下のどれかを返信）
    NyanList = [
        "にゃ～～～～～ん",
        "にゃ～ん",
        "にゃ～ん？",
        "にゃん",
        "にゃん？"
        ]
    n=len(NyanList)
    # メッセージに"にゃ"が含まれているか調べる
    pattern=u'にゃ'
    content = message.content
    repattern = re.compile(pattern)
    result=repattern.search(content)
    if result != None:
        if client.user != message.author:
            nyan = NyanList[random.randint(0,n-1)]    # 返信内容をランダムで決定
            await message.channel.send(nyan)    # メッセージが送られてきたチャンネルへメッセージを送る


    # 読み上げ機能
    # BOT入退出
    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません。")
        # BOTがボイスチャンネルに接続する
        else:
            await message.author.voice.channel.connect()
            await message.channel.send("**" + message.author.voice.channel.name + "** に、*BOT*  が入室しました！")
    elif message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("BOTはボイスチャンネルに接続していません。")
        else:
            # 切断する
            await message.guild.voice_client.disconnect()
            await message.channel.send("*BOT* が退出しました！")


    # 入力を監視する対象のテキストチャンネル
    ReadingoutloudCannelIds = [1009332840120451113,1009329150928093224]
    #メッセージが送られたチャンネルを取得
    chid=message.channel.id
    if chid in ReadingoutloudCannelIds:
        print(0)


    #音楽再生
    global endless
    #再生処理
    if message.content == "!play":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")
        elif message.guild.voice_client.is_playing():
            await message.channel.send("再生中です。")
        else:
            #再生する曲をランダムで選択
            musiclist = glob.glob('../million/*.m4a')
            music = random.choice(musiclist)

            musiclength = getTime(music)

            music1 = os.path.split(music)[1]
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
            message.guild.voice_client.play(source)
            await message.channel.send("”"+music1+"”を再生します。")
            print(music1)
            print(musiclength)            

    #停止処理
    elif message.content == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")

        # 再生中ではない場合は実行しない
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("再生していません。")
        else:
            message.guild.voice_client.stop()
            endless = False
            await message.channel.send("ストップしました。")

            
    #停止処理2
    elif message.content == "!lastplay":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")

        # 再生中ではない場合は実行しない
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("再生していません。")
        else:
            endless = False
            await message.channel.send("この曲で終了します。")


        
    #無限再生処理
    if message.content == "!endlessplay":
        endless = True
        await playmusic(message)





# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after):

    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
        botRoom = client.get_channel(1009335677881696276)

        # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
        announceChannelIds = [948454275955183630, 1009119186221539328]

        # 退室通知
        if before.channel is not None and before.channel.id in announceChannelIds:
            if member.name != client.user.name:
                await botRoom.send("**" + before.channel.name + "** から、*" + member.name + "*  が現実に戻りました！")
        # 入室通知&BOT入室
        if after.channel is not None and after.channel.id in announceChannelIds:
            if member.name != client.user.name:
                await botRoom.send("**" + after.channel.name + "** に、*" + member.name + "*  が現実逃避に来ました！")
                #await member.voice.channel.connect()
            

# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run("hoge token")
