# 2kbit Python Edition，2kbit的Python分支版本
# Copyright(C) 2022 Abjust 版权所有。

# 本程序是自由软件：你可以根据自由软件基金会发布的GNU Affero通用公共许可证的条款，即许可证的第3版或（您选择的）任何后来的版本重新发布它和/或修改它。。

# 本程序的发布是希望它能起到作用。但没有任何保证；甚至没有隐含的保证。本程序的分发是希望它是有用的，但没有任何保证，甚至没有隐含的适销对路或适合某一特定目的的保证。 参见 GNU Affero通用公共许可证了解更多细节。

# 您应该已经收到了一份GNU Affero通用公共许可证的副本。 如果没有，请参见<https://www.gnu.org/licenses/>。

# 致所有构建及修改2kbit代码片段的用户：作者（Abjust）并不承担构建2kbit代码片段（包括修改过的版本）所产生的一切风险，但是用户有权在2kbit的GitHub项目页提出issue，并有权在代码片段修复这些问题后获取这些更新，但是，作者不会对修改过的代码版本做质量保证，也没有义务修正在修改过的代码片段中存在的任何缺陷。

import random

from aiohttp import ClientSession
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent, MemberJoinRequestEvent, \
    MemberCardChangeEvent, GroupRecallEvent, MemberLeaveEventKick, MemberLeaveEventQuit, MemberJoinEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Plain, Image
from graia.ariadne.model import Group
from graia.broadcast import Broadcast
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast import ListenerSchema
from modules import globalvars

saya = Saya.current()
channel = Channel.current()
bcc = create(Broadcast)


# bot被加好友
@channel.use(ListenerSchema(listening_events=[NewFriendRequestEvent]))
async def friend_request(event: NewFriendRequestEvent):
    await event.accept()


# bot加群
@channel.use(ListenerSchema(listening_events=[BotInvitedJoinGroupRequestEvent]))
async def group_request(event: BotInvitedJoinGroupRequestEvent):
    if event.supplicant == globalvars.owner_qq:
        await event.accept()
    else:
        await event.reject()


# 侦测加群请求
@channel.use(ListenerSchema(listening_events=[MemberJoinRequestEvent]))
async def join_request(event: MemberJoinRequestEvent):
    if (globalvars.blocklist != [] and globalvars.blocklist.__contains__(
            f"{event.source_group}_{event.supplicant}")) or (
            globalvars.g_blocklist != [] and globalvars.g_blocklist.__contains__(event.supplicant)):
        await event.reject()


# 侦测改名
@channel.use(ListenerSchema(listening_events=[MemberCardChangeEvent]))
async def card_change(app: Ariadne, event: MemberCardChangeEvent, group: Group):
    if not event.current == "":
        try:
            await app.send_message(
                group,
                MessageChain(
                    f"QQ号：{event.member.id}\n原昵称：{event.origin}\n新昵称：{event.current}"),
            )
        except:
            print("群消息发送失败")


# 侦测撤回
@channel.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def recall_detect(app: Ariadne, event: GroupRecallEvent, group: Group):
    messageChain = (At(event.operator.id), Plain(" 你又撤回了什么见不得人的东西？"))
    print(event.operator.permission)
    if not event.operator.permission == "ADMINISTRATOR" and not event.operator.permission == "OWNER":
        try:
            await app.send_message(
                group,
                MessageChain(messageChain),
            )
        except:
            print("群消息发送失败")


# 侦测踢人
@channel.use(ListenerSchema(listening_events=[MemberLeaveEventKick]))
async def kick_detect(app: Ariadne, event: MemberLeaveEventKick, group: Group):
    try:
        await app.send_message(
            group,
            MessageChain(
                f"{event.member.name} ({event.member.id}) 被踢出去辣，好似，开香槟咯！"),
        )
    except:
        print("群消息发送失败")


# 侦测退群
@channel.use(ListenerSchema(listening_events=[MemberLeaveEventQuit]))
async def quit_detect(app: Ariadne, event: MemberLeaveEventQuit, group: Group):
    try:
        await app.send_message(
            group,
            MessageChain(
                f"{event.member.name} ({event.member.id}) 退群力（悲）"),
        )
    except:
        print("群消息发送失败")


# 侦测入群
@channel.use(ListenerSchema(listening_events=[MemberJoinEvent]))
async def join_detect(app: Ariadne, event: MemberJoinEvent, group: Group):
    messageChain = (At(event.member.id), Plain(" 来辣，让我们一起撅新人！（bushi"))
    try:
        await app.send_message(
            group,
            MessageChain(messageChain),
        )
    except:
        print("群消息发送失败")


# bot对接收私聊消息的处理
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def friend_message(app: Ariadne, event: FriendMessage):
    if not event.sender.id == globalvars.owner_qq:
        messageChain = (Plain(f"消息来自：{event.sender.nickname} ({event.sender.id})\n消息内容："))
        for message in event.message_chain:
            messageChain.__add__(message)
        await app.send_friend_message(globalvars.owner_qq, messageChain)
        await app.send_friend_message(
            globalvars.owner_qq,
            MessageChain(
                "你可以使用/send <目标QQ> <消息>来发送私聊消息"
            )
        )
    elif event.sender.id == globalvars.owner_qq and event.message_chain.startswith("!send"):
        result = event.message_chain.removeprefix("!send ").split(" ")
        if len(result) >= 2:
            try:
                results = ""
                for i in range (1, len(result) - 1):
                    if i == 1:
                        results = result[i]
                    else:
                        results = results + " " + result[i]
                try:
                    await app.send_friend_message(int(str(result[0])), results)
                except:
                    await app.send_friend_message(event.sender.id, "私聊消息发送失败")
            except:
                await app.send_friend_message(event.sender.id, "参数错误")


# bot对接收群消息的处理
@bcc.receiver(GroupMessage)
async def commands(app: Ariadne, group: Group, message: MessageChain):
    s = message.display
    # 随机图片
    if s == "!photo":
        chance = 3
        choice = random.randint(0, chance - 1)
        if choice == chance - 1:
            url = "https://www.dmoe.cc/random.php"
        else:
            url = "https://source.unsplash.com/random"
        try:
            await app.send_message(
                group,
                MessageChain(
                    "图片在来的路上..."),
            )
        except:
            print("群消息发送失败")
    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()

    b_msg = await app.send_group_message(group, MessageChain(Image(data_bytes=data)))
    # 版本
    if s == "版本":
        splashes = [
            "也试试HanBot罢！Also try HanBot!",
            "誓死捍卫微软苏维埃！",
            "打倒MF独裁分子！",
            "要把反革命分子的恶臭思想，扫进历史的垃圾堆！",
            "PHP是世界上最好的编程语言（雾）",
            "社会主义好，社会主义好~",
            "Minecraft很好玩，但也可以试试Terraria！",
            "So Nvidia, f**k you!",
            "战无不胜的马克思列宁主义万岁！",
            "Bug是杀不完的，你杀死了一个Bug，就会有千千万万个Bug站起来！",
            "跟张浩扬博士一起来学Jvav罢！",
            "哼哼哼，啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊",
            "你知道吗？其实你什么都不知道！",
            "Tips:这是一条烫...烫..烫知识（）",
            "你知道成功的秘诀吗？我告诉你成功的秘诀就是：我操你妈的大臭逼",
            "有时候ctmd不一定是骂人 可能是传统美德",
            "python不一定是编程语言 也可能是屁眼通红",
            "这条标语虽然没有用，但是是有用的，因为他被加上了标语",
            "使用Python编写！"
        ]
        r = random.randint(0, len(splashes) - 1)
        try:
            await app.send_message(
                group,
                MessageChain(
                    f"机器人版本：1.0.0-pe\n上次更新日期：2023/1/6\n更新内容：这是2kbot Python Edition的第一个实验版本！\n---------\n{splashes[r]}"),
            )
        except:
            print("群消息发送失败")
