import os
import discord
import keep_alive
from discord.ext import commands
#from discord.ext import commands
#from discord import app_commands
import requests
from bs4 import BeautifulSoup
#import datetime
#import keep_alive
#import os
import json
import random
import time
import interactions
from interactions import Button, ButtonStyle, ActionRow


intents = discord.Intents().all()
intents.members = True 
client = discord.Client(intents=intents)
bot = interactions.Client(token="", 
                          default_scope=[883712814068416523,1011225863527858216, 1068488232473477271, 1112024781852790836])
@bot.event
async def on_ready():
    print('loooooogged in ØZI')

async def on_command_error(self, ctx, error):
		await ctx.reply(error)

li = [
 '將', '帥', '俥', '俥', '傌', '傌', '炮', '炮', '仕', '仕', '相', '相', '車', '車', '馬',
 '馬', '包', '包', '士', '士', '象', '象', '卒', '卒', '卒', '卒', '卒', '兵', '兵', '兵',
 '兵', '兵']
li_in = ['將', '士', '象', '帥', '仕', '相', '俥', '傌', '炮', '車', '馬', '包', '卒', '兵']
data=''
def origin_shuffle():
    player_1 = []
    player_2 = []
    coli = li
    player_1.append(coli.pop(random.randint(0, len(li) - 1)))
    for i in range(4):
        player_2.append(coli.pop(random.randint(0, len(li) - 1)))
        player_1.append(coli.pop(random.randint(0, len(li) - 1)))
    return player_1, player_2, coli

def get_deck(p1, p2, pqq, p1d, p2d):
	if pqq==p1:
		return p1d
	elif pqq==p2:
		return p2d
	else:
		return '媽的沒人要跟你玩可以不要亂按嗎'

def open_file(file):
	lis=[]
	with open(file) as f:
		for i in f.readlines():
			lis.append(i)
		return lis

def open_json(json):
    with open(json) as f:
        data=json.load(f)
        return data
    
def write_json(json, data):
    with open(json, 'w') as f:
        data=json.dump(data, f, indent=2)

def get_tai(lis):
	tai = 0
	lii = []
	for i in lis:
		lii.append(li_in.index(i))
	lii.sort()
	print(lii)
	cur = -1
	if lii[0] == lii[1] == lii[2] == lii[3] == lii[4]:
		return 7
	for j in [0, 2]:
		if (lii[j + 1] - lii[j]) == (lii[j + 2] - lii[j + 1]) == 1:
			tai += 2
			cur = j
			if lii[j] == 0 or lii[j] == 3:
				tai += 1
		if lii[j] == lii[j + 1] == lii[j + 2]:
			tai += 3
			cur = j
	if cur == 0:
		if lii[3] != lii[4]:
			return 0
	elif cur == 2:
		if lii[0] != lii[1]:
			if lii[0] == 0 and lii[1] == 3:
				tai += 2
			else:
				return 0
	else:
		return 0
	return tai
ctrl_mess=''
button_get_deck = Button(style=ButtonStyle.SUCCESS,
                            label="看你目前的牌",
                            custom_id="get_deck_but",
                            disabled=False)
button_start_turn=Button(style=ButtonStyle.SUCCESS,
                         label="開始你的回合",
                         custom_id='start_turn_but',
                         disabled=False
                         )
button_jianpai=Button(style=ButtonStyle.SUCCESS,
                     label="撿起上一張牌牌",
                     custom_id="jianpai",
                     disabled=False
                     )
button_oupai=Button(style=ButtonStyle.SUCCESS,
                    label="從那疊東西裡面摸一張牌",
                    custom_id='oupai',
                    disabled=False
                    )
button_huuuu=Button(style=ButtonStyle.SUCCESS,
                         label="胡牌",
                         custom_id='huuuu'
                         )
button_accept=Button(style=ButtonStyle.SUCCESS,
                    label="接受",
                    custom_id='accept',
                    disabled=False
                    )
button_reject=Button(style=ButtonStyle.DANGER,
                    label="拒絕",
                    custom_id='reject',
                    disabled=False
                    )
button_liou=Button(style=ButtonStyle.SUCCESS,
                    label="流局",
                    custom_id='liouju',
                    disabled=False
                    )
button_last=Button(style=ButtonStyle.SUCCESS,
                    label="撿起最後一張牌並胡牌",
                    custom_id='haidi',
                    disabled=False
                    )
@bot.command(name="start_match",
			 description="跟別人來場象棋麻將吧",
			 options=[interactions.Option(
                name="opponent",
                description="who to pk?",
                type=interactions.OptionType.USER,
                required=True
                ),interactions.Option(
				name="bet",
                description="place a bet",
				type=interactions.OptionType.STRING,
				required=True
             )])
#interactions.Choice = None
async def start_match(ctx: interactions.CommandContext,opponent: str,bet: int):
    oppo=str(opponent.id)
    with open("data.json") as f:
        data=json.load(f)
    players=data["player"]
    aut=str(ctx.author.id)
    #oppo=opponent.lstrip("<@").rstrip(">")
    if aut in players.keys():
        if int(bet)>int(players[aut]["money"]):
            await ctx.send("你自己都沒錢...")
            return
    else:
        players[aut]={"money": 0, "rank": 1000, "last_sign": 0}
        await ctx.send("你自己都沒錢...")
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)
        return
    if oppo in players.keys():
        if int(bet)>int(players[oppo]["money"]):
            await ctx.send("你對手錢不夠la 不要欺負人")
            return
    else:
        players[oppo]={"money": 0, "rank": 1000, "last_sign": 0}
        await ctx.send("你對手錢不夠la 不要欺負人")
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)
        return
    if(oppo==str(ctx.author.id)):
        await ctx.send("為什麼要跟自己玩= =", ephemeral=True)
        return
    else:
        p1 = ctx.author.id
        p2=oppo
        with open("data.json") as s:
            data=json.load(s)
        match=data['game']
        data['match'][f'{p1}{p2}']={str(p1):'', str(p2):''}
        matchn=f'{p1}{p2}'
        if matchn in match.keys():
            match[matchn]=bet
        else:
            match[matchn]=bet
        with open("data.json", 'w') as s:
            json.dump(data, s, indent=2)
        message = await ctx.send(f"<@{oppo}>\n你要接受<@{ctx.author.id}>\的挑戰嗎\n賭注為{bet}元", components=[button_accept, button_reject])
        p1 = ctx.author.id
        p2=oppo
        f=open(f"{p1}{p2}.txt", 'w')
        channel = await message.create_thread(name=f"{p1}{p2}")
        p1_deck, p2_deck, cu_li = origin_shuffle()
        f.write(f"""{p1}\n{p2}\n{p1_deck[0]}{p1_deck[1]}{p1_deck[2]}{p1_deck[3]}{p1_deck[4]}\n{p2_deck[0]}{p2_deck[1]}{p2_deck[2]}{p2_deck[3]}\n0\n""")
        for i in range(len(cu_li)):
            f.write(f"""{cu_li[i]}""")
        #f.write(f'\n{ctrl_mess.id}')
        f.close()
#p1id p2id p1deck p2deck whosturn culi huan messid
@bot.component('accept')
async def acc(ctx):
    cha_id=ctx.message.thread.id
    aut=str(ctx.author.id)
    messid=ctx.message.id
    channid=ctx.channel.id
    message = await interactions.get(bot, interactions.Message, object_id=messid, parent_id=channid)
    channel = await interactions.get(bot, interactions.Channel, object_id=cha_id)
    name=channel.name
    lit=open_file(f'{name}.txt')
    if lit[1].rstrip('\n')==aut:
        await ctx.send(f'<@{ctx.author.id}>接受了挑戰！')
        await message.edit(message.content)
        print(channel.id)
        f=open(f'{name}.txt', 'a')
        f.close()
        lit=open_file(f'{name}.txt')
        await channel.send('來看牌吧', components=button_get_deck)
        ttt=lit[0].rstrip('\n')
        ctrl_mess=await channel.send(f"現在是<@{ttt}>的回合，按下下面的按鈕開始你的回合", components=button_start_turn)
        f=open(f'{name}.txt', 'a')
        f.write(f'\n{ctrl_mess.id}')
        f.close()
    else:
        await ctx.send('不要亂戳啦', ephemeral=True)
@bot.component('get_deck_but')       
async def func(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    if lit[0].rstrip('\n')==aut or lit[1].rstrip('\n')==aut:
#    print(li)
#    print(li[0].rstrip('\n'), li[1].rstrip('\n'), f'{str(ctx.author)}', li[2].rstrip('\n'), li[3])
        p_d=get_deck(lit[0].rstrip('\n'), lit[1].rstrip('\n'), f'{str(ctx.author.id)}', lit[2].rstrip('\n'), lit[3])
        await ctx.send(p_d, ephemeral=True)
    else:
        await ctx.send('可以不要亂按嗎', ephemeral=True)        
@bot.component('start_turn_but')
async def funcc(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    kk=lit[int(lit[4].rstrip('\n'))%2].rstrip('\n')

    if kk==aut:
        p_d=get_deck(lit[0].rstrip('\n'), lit[1].rstrip('\n'), aut, lit[2].rstrip('\n'), lit[3])
        if len(lit[5].rstrip('\n'))==0:
            zzz=lit[7].lstrip('\n').rstrip('\n')
            await ctx.send(f'你的牌目前是{p_d}\n現在撿牌的話會摸到"{zzz}"，而且沒牌摸了，要撿嗎', components=[button_liou, button_last], ephemeral=True)
            return
        if lit[4].rstrip('\n')=='0':
            compo=[]
            lll=[]
            for i in range(3):
                compo.append(Button(style=ButtonStyle.SUCCESS,
                                    label=f'丟掉{p_d[i]}',
                                    custom_id=f'throw_{i}'
                                    ))
            for i in [3, 4]:
                lll.append(Button(style=ButtonStyle.SUCCESS,
                                    label=f'丟掉{p_d[i]}',
                                    custom_id=f'throw_{i}'
                                    ))
            lll.append(button_huuuu)
            compo=ActionRow(components=compo)
            row_hu=ActionRow(components=lll)
            await ctx.send(f"這是你的牌，請丟牌\n{p_d}\n",components=[compo, row_hu], ephemeral=True)
        else:
            zzz=lit[7].lstrip('\n').rstrip('\n')
            await ctx.send(f'你的牌目前是{p_d}\n現在撿牌的話會摸到"{zzz}"，要摸還是要撿呢', components=[button_oupai, button_jianpai], ephemeral=True)
    else:
        await ctx.send("可以不要亂按嗎", ephemeral=True)
        
@bot.component("throw_0")
async def lol1(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    if aut==lit[0].rstrip('\n'):
        kef=2
    else:
        kef=3
    lale=''
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
    await ctx.send(f"{lit[kef][0]}被丟掉勒", ephemeral=True)
    hum=lit[(int(lit[4])+1)%2].rstrip('\n')
    with open("data.json") as s:
        data=json.load(s)
    data['match'][name][aut]=data['match'][name][aut]+lit[kef][0]
    at1=lit[0].rstrip('\n')
    at2=lit[1].rstrip('\n')
    mess=await ctx.send(f"牌桌:\n<@{at1}>:\n{data['match'][name][at1]}\n<@{at2}>:\n{data['match'][name][at2]}\n現在是<@{hum}>的回合，按下下面的按鈕開始你的回合", components=[button_start_turn,button_get_deck])
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2)
    for i in range(8):
        if i==kef:
            for j in range(5):
                if j==0:
                    pass
                else:
                    lale+=lit[kef][j]
            f.write(f'{lale}\n')
        elif i==4:
            f.write(f"{str(int(lit[4])+1)}\n")
        elif i==7:
            ss=lit[kef][0].rstrip("\n")
            f.write(f'{ss}\n')
        elif i==6:
            f.write(f'{mess.id}\n')
        else:
            lll=lit[i].rstrip('\n')
            f.write(f"{lll}\n")
            if i==100:
                f.write('\n')
    f.close()
    
@bot.component("throw_1")
async def lol2(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    if aut==lit[0].rstrip('\n'):
        kef=2
    else:
        kef=3
    lale=''
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
    await ctx.send(f"{lit[kef][1]}被丟掉勒", ephemeral=True)
    hum = lit[(int(lit[4])+1)%2].rstrip('\n')
    with open("data.json") as s:
        data=json.load(s)
    data['match'][name][aut]=data['match'][name][aut]+lit[kef][1]
    at1=lit[0].rstrip('\n')
    at2=lit[1].rstrip('\n')
    mess=await ctx.send(f"牌桌:\n<@{at1}>:\n{data['match'][name][at1]}\n<@{at2}>:\n{data['match'][name][at2]}\n現在是<@{hum}>的回合，按下下面的按鈕開始你的回合", components=[button_start_turn,button_get_deck])
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2)
    for i in range(8):
        if i==kef:
            for j in range(5):
                if j==1:
                    pass
                else:
                    lale+=lit[kef][j]
            f.write(f'{lale}\n')
        elif i==4:
            f.write(f"{str(int(lit[4])+1)}\n")
        elif i==7:
            ss=lit[kef][1].rstrip("\n")
            f.write(f'{ss}\n')
        elif i==6:
            f.write(f'{mess.id}\n')
        else:
            lll=lit[i].rstrip('\n')
            f.write(f"{lll}\n")
            if i==100:
                f.write('\n')

    
@bot.component("throw_2")
async def lol3(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    if aut==lit[0].rstrip('\n'):
        kef=2
    else:
        kef=3
    lale=''
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
    await ctx.send(f"{lit[kef][2]}被丟掉勒", ephemeral=True)
    hum=lit[(int(lit[4])+1)%2].rstrip('\n')
    with open("data.json") as s:
        data=json.load(s)
    data['match'][name][aut]=data['match'][name][aut]+lit[kef][2]
    at1=lit[0].rstrip('\n')
    at2=lit[1].rstrip('\n')
    mess=await ctx.send(f"牌桌:\n<@{at1}>:\n{data['match'][name][at1]}\n<@{at2}>:\n{data['match'][name][at2]}\n現在是<@{hum}>的回合，按下下面的按鈕開始你的回合", components=[button_start_turn,button_get_deck])
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2) 
    for i in range(8):
        if i==kef:
            for j in range(5):
                if j==2:
                    pass
                else:
                    lale+=lit[kef][j]
            f.write(f'{lale}\n')
        elif i==4:
            f.write(f"{str(int(lit[4])+1)}\n")
        elif i==7:
            ss=lit[kef][2].rstrip("\n")
            f.write(f'{ss}\n')
        elif i==6:
            f.write(f'{mess.id}\n')
        else:
            lll=lit[i].rstrip('\n')
            f.write(f"{lll}\n")
            if i==100:
                f.write('\n')

    
@bot.component("throw_3")
async def lol4(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    if aut==lit[0].rstrip('\n'):
        kef=2
        hum=int(lit[1].rstrip('\n'))
    else:
        kef=3
        hum=int(lit[0].rstrip('\n'))
    lale=''
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
    await ctx.send(f"{lit[kef][3]}被丟掉勒", ephemeral=True)
    hum=lit[(int(lit[4])+1)%2].rstrip('\n')
    with open("data.json") as s:
        data=json.load(s)
    data['match'][name][aut]=data['match'][name][aut]+lit[kef][3]
    at1=lit[0].rstrip('\n')
    at2=lit[1].rstrip('\n')
    mess=await ctx.send(f"牌桌:\n<@{at1}>:\n{data['match'][name][at1]}\n<@{at2}>:\n{data['match'][name][at2]}\n現在是<@{hum}>的回合，按下下面的按鈕開始你的回合", components=[button_start_turn,button_get_deck])
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2)
    for i in range(8):
        if i==kef:
            for j in range(5):
                if j==3:
                    pass
                else:
                    lale+=lit[kef][j]
            f.write(f'{lale}\n')
        elif i==4:
            f.write(f"{str(int(lit[4])+1)}\n")
        elif i==7:
            ss=lit[kef][3].rstrip("\n")
            f.write(f'{ss}')
        elif i==6:
            f.write(f'{mess.id}\n')
        else:
            lll=lit[i].rstrip('\n')
            f.write(f"{lll}\n")
            if i==100:
                f.write('\n')

    
@bot.component("throw_4")
async def lol5(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    if aut==lit[0].rstrip('\n'):
        kef=2
    else:
        kef=3
    lale=''
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
    await ctx.send(f"{lit[kef][4]}被丟掉勒", ephemeral=True)
    hum=lit[(int(lit[4])+1)%2].rstrip('\n')
    with open("data.json") as s:
        data=json.load(s)
    data['match'][name][aut]=data['match'][name][aut]+lit[kef][4]
    at1=lit[0].rstrip('\n')
    at2=lit[1].rstrip('\n')
    mess=await ctx.send(f"牌桌:\n<@{at1}>:\n{data['match'][name][at1]}\n<@{at2}>:\n{data['match'][name][at2]}\n現在是<@{hum}>的回合，按下下面的按鈕開始你的回合", components=[button_start_turn,button_get_deck])
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2)
    for i in range(8):
        if i==kef:
            for j in range(5):
                if j==4:
                    pass
                else:
                    lale+=lit[kef][j]
            f.write(f'{lale}\n')
        elif i==4:
            f.write(f"{str(int(lit[4])+1)}\n")
        elif i==7:
            ss=lit[kef][4].rstrip("\n")
            f.write(f'{ss}\n')
        elif i==6:
            f.write(f'{mess.id}\n')
        else:
            lll=lit[i].rstrip('\n')
            f.write(f"{lll}\n")
            if i==100:
                f.write('\n')

    
@bot.component('jianpai')
async def kkkkk(ctx):
    with open("data.json") as s:
        data=json.load(s)
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    f=open(f'{name}.txt', 'w')
    kalala=''
    hehe=lit[7].rstrip('\n')
    aha=0
    if lit[0].rstrip('\n')==aut:
        data['match'][name][lit[1].rstrip('\n')]=data['match'][name][lit[1].rstrip('\n')]+'\*'
        kalala=lit[2].rstrip('\n')
        kalala+=hehe
        aha=2
    else:
        data['match'][name][lit[0].rstrip('\n')]=data['match'][name][lit[0].rstrip('\n')]+'\*'
        kalala=lit[3].rstrip('\n')
        kalala+=hehe
        aha=3
    with open("data.json", 'w') as s:
        json.dump(data, s, indent=2)
    for i in range(7):
        if i==aha:
            f.write(f'{kalala}\n')
        elif i==4:
            f.write(f'{int(lit[4])}\n')
        else:
            fjfj=lit[i].rstrip('\n')
            f.write(f"{fjfj}\n")
    f.close()
    f=open(f'{name}.txt', 'r')
    lit=open_file(f'{name}.txt')
    compo=[]
    p_d=lit[(int(lit[4].rstrip('\n'))%2)+2]
    lll=[]
    for i in range(3):
        compo.append(Button(style=ButtonStyle.SUCCESS,
                            label=f'丟掉{p_d[i]}',
                            custom_id=f'throw_{i}'
                            ))
    for i in [3, 4]:
        lll.append(Button(style=ButtonStyle.SUCCESS,
                            label=f'丟掉{p_d[i]}',
                            custom_id=f'throw_{i}'
                            ))
    lll.append(button_huuuu)
    compo=ActionRow(components=compo)
    row_hu=ActionRow(components=lll)
    await ctx.send(f'你撿到了{hehe}!!\n順便丟張牌',components=[compo, row_hu], ephemeral=True)
    f.close()

@bot.component('oupai')
async def kkkkkk(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    aba=''
    dddd=True
    if lit[0].rstrip('\n')==aut:
        lit[5]=lit[5].rstrip('\n')
        apai=lit[5][random.randint(0, len(lit[5])-1)]#cpppppppppppppppppppppendl
        lit[2]=lit[2].rstrip('\n')+f'{apai}'
        for i in lit[5]:
            if apai==i and dddd:
                dddd=False
                continue
            aba+=i
    else:
        lit[5]=lit[5].rstrip('\n')
        apai=lit[5][random.randint(0, len(lit[5])-1)]#cpppppppppppppppppppppendl
        lit[3]=lit[3].rstrip('\n')+f'{apai}'
        for i in lit[5]:
            if apai==i and dddd:
                dddd=False
                continue
            aba+=i
    f=open(f'{name}.txt', 'w')
    for i in range(8):
        if i==5:
            rrr=aba.rstrip('\n')
            f.write(f'{rrr}\n')
        elif i==4:
            f.write(str(int(lit[4].rstrip('\n'))))
            f.write('\n')
        else:
            sajfh=lit[i].rstrip('\n')
            f.write(f'{sajfh}\n')
    f.close()
    f=open(f'{name}.txt', 'r')
    lit=open_file(f'{name}.txt')
    compo=[]
    p_d=lit[(int(lit[4])%2)+2]
    lll=[]
    for i in range(3):
        compo.append(Button(style=ButtonStyle.SUCCESS,
                            label=f'丟掉{p_d[i]}',
                            custom_id=f'throw_{i}'
                            ))
    for i in [3, 4]:
        lll.append(Button(style=ButtonStyle.SUCCESS,
                            label=f'丟掉{p_d[i]}',
                            custom_id=f'throw_{i}'
                            ))
    lll.append(button_huuuu)
    compo=ActionRow(components=compo)
    row_hu=ActionRow(components=lll)
    await ctx.send(f'你撿到了{apai}!!\n順便丟張牌',components=[compo, row_hu], ephemeral=True)
    f.close()
@bot.component('huuuu')
async def really(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    pai=''
    winner=''
    loser=''
    if lit[0].rstrip('\n')==aut:
        tai=get_tai(lit[2].rstrip('\n'))
        pai=lit[2].rstrip('\n')
        winner=lit[0].rstrip('\n')
        loser=lit[1].rstrip('\n')
    else:
        tai=get_tai(lit[3].rstrip('\n'))
        pai=lit[3].rstrip('\n')
        winner=lit[1].rstrip('\n')
        loser=lit[0].rstrip('\n')
    if tai==0:
        await ctx.send('顯然你做不到', ephemeral=True)
    else:
        with open("data.json") as s:
            data=json.load(s)
        amount=int(data['game'][name])
        winp=int(data['player'][winner]['money'])
        lop=int(data['player'][loser]['money'])
        winr=int(data['player'][winner]['rank'])
        lor=int(data['player'][loser]['rank'])
        change=max((max(winr, lor)-min(winr, lor))//10,  10)
        data['player'][winner]['money']=winp+amount*int(tai)
        data['player'][loser]['money']=lop-amount*int(tai)
        data['player'][winner]['rank']=winr+change
        data['player'][loser]['rank']=lor-change
        data['game'][name]='0'
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send(f'恭喜<@{aut}>胡了{tai}台\n{pai}！！！')
@bot.component('liouju')
async def lioule(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    await ctx.send('流局勒')
    lit=open_file(f'{name}.txt')
    channa=await ctx.get_channel()
    messa=await channa.get_message(int(lit[6].rstrip('\n')))
    await messa.delete()
@bot.component('haidi')
async def jule(ctx):
    channel=ctx.channel
    name=channel.name
    aut=str(ctx.author.id)
    lit=open_file(f'{name}.txt')
    pai=''
    winner=''
    loser=''
    if lit[0].rstrip('\n')==aut:
        lit[2]=lit[2].rstrip('\n')+lit[7]
        tai=get_tai(lit[2].rstrip('\n'))
        pai=lit[2].rstrip('\n')
        winner=lit[0].rstrip('\n')
        loser=lit[1].rstrip('\n')
    else:
        lit[3]=lit[3].rstrip('\n')+lit[7]
        tai=get_tai(lit[3].rstrip('\n'))
        pai=lit[3].rstrip('\n')
        winner=lit[1].rstrip('\n')
        loser=lit[0].rstrip('\n')
    if tai==0:
        await ctx.send('顯然你做不到', ephemeral=True)
    else:
        with open("data.json") as s:
            data=json.load(s)
        amount=int(data['game'][name])
        winp=int(data['player'][winner]['money'])
        lop=int(data['player'][loser]['money'])
        winr=int(data['player'][winner]['rank'])
        lor=int(data['player'][loser]['rank'])
        change=max((max(winr, lor)-min(winr, lor))//10,  10)
        data['player'][winner]['money']=winp+amount*int(tai)
        data['player'][loser]['money']=lop-amount*int(tai)
        data['player'][winner]['rank']=winr+change
        data['player'][loser]['rank']=lor-change
        data['game'][name]='0'
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send(f'恭喜<@{aut}>胡了{tai}台\n{pai}！！！')
@bot.command(name="atm",
			 description="太窮就來刷一下ㄅ")     
async def daily(ctx: interactions.CommandContext):
    with open("data.json") as f:
        data=json.load(f)
    players=data["player"]
    aut=str(ctx.author.id)
    mount=random.randint(1, 15)
    mount=2**mount+random.randint(1, 200)
    if aut in players.keys():
        cur=int(players[aut]["money"])+mount
        players[aut]["money"]=cur
        await ctx.send(f"你領到了{mount}元\n現在你有{cur}元")
    else:
        players[aut]={"money": mount, "rank": 1000, "last_sign": 0}
        await ctx.send(f"你領到了{mount}元\n現在你有{mount}元")
    with open("data.json", 'w') as f:
        json.dump(data, f, indent=2)
        
@bot.command(name="money",
			 description="get ur current wealth")     
async def money(ctx: interactions.CommandContext):
    with open("data.json") as f:
        data=json.load(f)
    players=data["player"]
    aut=str(ctx.author.id)
    if aut in players.keys():
        cur=int(players[aut]["money"])
        await ctx.send(f"你現在有{cur}元")
    else:
        players[aut]={"money": 0, "rank": 1000, "last_sign": 0}
        await ctx.send("你現在有0元")
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)

@bot.command(name="pay",
			 description="救濟貧困從你我做起",
			 options=[interactions.Option(
                name="who",
                description="who to pay?",
                type=interactions.OptionType.USER,
                required=True
                ),interactions.Option(
				name="amount",
                description="how much do you want to give him/her?",
				type=interactions.OptionType.INTEGER,
				required=True
             )])
#interactions.Choice = None
async def pay(ctx: interactions.CommandContext,who: str,amount: int):
    with open("data.json") as f:
        data=json.load(f)
    players=data["player"]
    aut=str(ctx.author.id)
    tar=who.lstrip('<@').rstrip('>')
    amount=int(amount)
    if amount<0:
        await ctx.send("這是搶劫欸")
        return
    if aut in players.keys():
        if tar in players.keys():
            if amount<=int(players[aut]["money"]):
                cur=int(players[aut]["money"])-amount
                players[aut]["money"]=cur
                cur=int(players[tar]["money"])+amount
                players[tar]["money"]=cur
                await ctx.send(f"you paid {who} {amount} dollar")
            else:
                await ctx.send('你錢不夠啦')
        else:
            if amount<=int(players[aut]["money"]):
                players[tar]={"money": amount, "rank": 1000, "last_sign": 0}
                cur=int(players[aut]["money"])-amount
                players[aut]["money"]=cur
            else:
                await ctx.send('你錢不夠啦')
    else:
        players[tar]={"money": 0, "rank": 1000, "last_sign": 0}
        await ctx.send('你錢不夠啦')
    with open("data.json", 'w') as f:
        json.dump(data, f, indent=2)

@bot.command(name="rank",
			 description="get ur current rank")     
async def rank(ctx: interactions.CommandContext):
    with open("data.json") as f:
        data=json.load(f)
    players=data["player"]
    aut=str(ctx.author.id)
    if aut in players.keys():
        cur=int(players[aut]["rank"])
        await ctx.send(f"你現在有{cur}分")
    else:
        players[aut]={"money": 0, "rank": 1000, "last_sign": 0}
        await ctx.send("你現在有1000分")
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)
            
@bot.command(name="rule",
			 description="查看象棋麻將的規則")     
async def rule(ctx: interactions.CommandContext):
    await ctx.send("""||~~偷~~||參考自CKEFGISC2023寒訓講義
基本胡牌方式為3+2
```
1. 手上的五張牌中 要配成三張加兩張才能胡牌
2. 三張：帥仕相、將士象、車馬包、俥傌炮、兵兵兵、卒卒卒
3. 二張：將帥或其他兩張一樣的(顏色也要一樣喔
```
計分方式：
```
採累加制 你贏的錢就是本金乘上台數喔 當然賠錢也是囉
一般3+2(底)：二台
三兵入列：二台
五兵合縱：五台
帥仕相：一台
將士象：一台
將帥對：一台
```
玩法
```
就跟麻將一樣摸一張或吃一張然後打出一張
但是不用組成特殊牌才能吃喔
別人丟的都可 吃了也不用亮出來
```""")
keep_alive.keep_alive()
bot.start()