# 2kbit Python Edition，2kbit的Python分支版本
# Copyright(C) 2022 Abjust 版权所有。

# 本程序是自由软件：你可以根据自由软件基金会发布的GNU Affero通用公共许可证的条款，即许可证的第3版或（您选择的）任何后来的版本重新发布它和/或修改它。。

# 本程序的发布是希望它能起到作用。但没有任何保证；甚至没有隐含的保证。本程序的分发是希望它是有用的，但没有任何保证，甚至没有隐含的适销对路或适合某一特定目的的保证。 参见 GNU Affero通用公共许可证了解更多细节。

# 您应该已经收到了一份GNU Affero通用公共许可证的副本。 如果没有，请参见<https://www.gnu.org/licenses/>。

# 致所有构建及修改2kbit代码片段的用户：作者（Abjust）并不承担构建2kbit代码片段（包括修改过的版本）所产生的一切风险，但是用户有权在2kbit的GitHub项目页提出issue，并有权在代码片段修复这些问题后获取这些更新，但是，作者不会对修改过的代码版本做质量保证，也没有义务修正在修改过的代码片段中存在的任何缺陷。

from creart import create
import pkgutil
from graia.saya import Saya
from graia.broadcast import Broadcast
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from modules import globalvars
import os.path
import mysql.connector

# 初始化全局变量
if not os.path.exists("globals.txt"):
    lines = ["owner_qq=", "api=", "api_key=", "bot_qq=", "verify_key=", "database_host=", "database_user=",
             "database_passwd=", "database_name="]
    f = open("globals.txt", "w")
    f.writelines(line + '\n' for line in lines)
    f.close()
    input("全局变量文件已创建！现在，你需要前往项目文件夹或者程序文件夹找到globals.txt并按照要求编辑（按回车键退出）")
    exit(0)
else:
    f = open('globals.txt', 'r')
    for line in f.readlines():
        split = line.split("=")
        if len(split) == 2:
            if split[0] == "owner_qq":
                globalvars.owner_qq = int(split[1].replace("\n", ""))
            elif split[0] == "api":
                globalvars.api = split[1].replace("\n", "")
            elif split[0] == "api_key":
                globalvars.api_key = split[1].replace("\n", "")
            elif split[0] == "bot_qq":
                globalvars.bot_qq = int(split[1].replace("\n", ""))
            elif split[0] == "verify_key":
                globalvars.verify_key = split[1].replace("\n", "")
            elif split[0] == "database_host":
                globalvars.database_host = split[1].replace("\n", "")
            elif split[0] == "database_user":
                globalvars.database_user = split[1].replace("\n", "")
            elif split[0] == "database_passwd":
                globalvars.database_passwd = split[1].replace("\n", "")
            elif split[0] == "database_name":
                globalvars.database_name = split[1].replace("\n", "")
# 启动机器人程序
saya = create(Saya)
bcc = create(Broadcast)
app = Ariadne(
    connection=config(
        globalvars.bot_qq,  # 你的机器人的 qq 号
        globalvars.verify_key,  # 填入你的 mirai-api-http 配置中的 verifyKey
        # 以下两行（不含注释）里的 host 参数的地址
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
        HttpClientConfig(host="http://localhost:8081"),
        WebsocketClientConfig(host="http://localhost:8081"),
    ),
)
# 初始化
# 连接数据库
msc = mysql.connector.connect(user=globalvars.database_user, password=globalvars.database_passwd,
                              host=globalvars.database_host,
                              database=globalvars.database_name)
cursor = msc.cursor()
# 若数据表不存在则创建
sqls = [
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`blocklist` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',`gid` VARCHAR(10) NOT NULL COMMENT 'Q群号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`ops` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',`gid` VARCHAR(10) NOT NULL COMMENT 'Q群号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`ignores` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',`gid` VARCHAR(10) NOT NULL COMMENT 'Q群号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`g_blocklist` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`g_ops` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`g_ignores` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',PRIMARY KEY (`id`));",
    f"CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`repeatctrl` (`id` INT NOT NULL AUTO_INCREMENT,`qid` VARCHAR(10) NOT NULL COMMENT 'QQ号',`gid` VARCHAR(10) NOT NULL COMMENT 'Q群号',`last_repeat` bigint NOT NULL DEFAULT '946656000' COMMENT '上次复读时间',`last_repeatctrl` bigint NOT NULL DEFAULT '946656000' COMMENT '上次复读控制时间',`repeat_count` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '复读计数',PRIMARY KEY (`id`));",
    f"""
    CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`bread` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gid` varchar(10) NOT NULL COMMENT 'Q群号',
  `factory_level` int NOT NULL DEFAULT '1' COMMENT '面包厂等级',
  `storage_upgraded` int NOT NULL DEFAULT '0' COMMENT '库存升级次数',
  `bread_diversity` tinyint NOT NULL DEFAULT '0' COMMENT '多样化生产状态',
  `factory_exp` int NOT NULL DEFAULT '0' COMMENT '面包厂经验',
  `breads` int NOT NULL DEFAULT '0' COMMENT '面包库存',
  `exp_gained_today` int NOT NULL DEFAULT '0' COMMENT '近24小时获取经验数',
  `last_expfull` bigint NOT NULL DEFAULT '946656000' COMMENT '上次达到经验上限时间',
  `last_expgain` bigint NOT NULL DEFAULT '946656000' COMMENT '近24小时首次获取经验时间',
  `last_produce` bigint NOT NULL DEFAULT '946656000' COMMENT '上次完成一轮生产周期时间',
  PRIMARY KEY (`id`));
""",
    f"""
    CREATE TABLE IF NOT EXISTS `{globalvars.database_name}`.`material` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gid` varchar(10) NOT NULL COMMENT 'Q群号',
  `flour` int NOT NULL DEFAULT 0 COMMENT '面粉数量',
  `egg` int NOT NULL DEFAULT 0 COMMENT '鸡蛋数量',
  `yeast` int NOT NULL DEFAULT 0 COMMENT '酵母数量',
  `last_produce` bigint NOT NULL DEFAULT '946656000' COMMENT '上次完成一轮生产周期时间',
  PRIMARY KEY (`id`));
""",
    f"INSERT IGNORE INTO `{globalvars.database_name}`.`material` (id, gid) SELECT id, gid FROM `{globalvars.database_name}`.`bread`"
]
for sql in sqls:
    cursor.execute(sql)
# 更新数据表
try:
    cursor.execute(f"""
    ALTER TABLE `{globalvars.database_name}`.`bread`
ADD COLUMN `speed_upgraded` INT NOT NULL DEFAULT 0 COMMENT '生产速度升级次数' AFTER `storage_upgraded`,
ADD COLUMN `output_upgraded` INT NOT NULL DEFAULT 0 COMMENT '产量升级次数' AFTER `speed_upgraded`,
CHANGE COLUMN `bread_diversity` `factory_mode` TINYINT NOT NULL DEFAULT '0' COMMENT '面包厂生产模式' ;
    """)
except:
    ...
msc.close()
# 更新列表
# 加载模块
with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")
app.launch_blocking()
