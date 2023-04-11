import re
import datetime

import requests

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
from plugins.WeatherPlugin.template import API_KEY, BOT_TAG_PATTERN, LOCATION_PROMPT, API_PROMPT, WEATHER_PROMPT


"""
在收到私聊或群聊消息"天气 <地点>"时，通过和风天气API查询最近三天天气并返回结果"
"""


# 注册插件
@register(name="Weather", description="和风天气", version="0.1", author="lieyanqzu")
class WeatherPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        try:
            import plugins.revLibs.pkg.process.procmsg as procmsg
            self.process_message = lambda kwargs: procmsg.process_message(
                session_name=kwargs['launcher_type']+"_"+str(kwargs['launcher_id']), 
                prompt=kwargs['text_message'], **kwargs)
        except:
            self.process_message = lambda kwargs: "目前仅支持revLibs"
            # 没有token测试，也许是这样写吧
            # mgr = pkg.utils.context.get_qqbot_manager()
            # config = pkg.utils.context.get_config()
            # self.process_message = lambda kwargs: (pkg.qqbot.message.process_normal_message(
            #     kwargs['text_message'], mgr, config, kwargs['launcher_type'], kwargs['launcher_id'], kwargs['sender_id']))[0]

    # 当收到个人消息和群聊消息时触发
    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def normal_message_received(self, event: EventContext, **kwargs):
        msg = kwargs['text_message']
        # 如果消息为天气 <地点>则触发
        # 本来想让gpt判断是不是查询天气，但是没调教出来
        if "天气 " in msg:  
            # 通过GPT辅助构建城市LocationID查询接口地址
            prompt = LOCATION_PROMPT.format(location=msg[len("天气 "):], api_key=API_KEY)
            kwargs['text_message'] = prompt
            reply = self.process_message(kwargs)
            # 输出调试信息
            logging.debug(reply)
            # 通过<bot>标签提取接口地址
            match = re.search(BOT_TAG_PATTERN, reply)
            if match:
                response = requests.get(match.group(1))
                # 通过GPT辅助构建3天天气查询接口地址
                prompt = API_PROMPT.format(location=msg[len("天气 "):], api_key=API_KEY, location_resp=response.text)
                kwargs['text_message'] = prompt
                reply = self.process_message(kwargs)
                # 输出调试信息
                logging.debug(reply)
                # 通过<bot>标签提取接口地址
                match = re.search(BOT_TAG_PATTERN, reply)
                if match:
                    response = requests.get(match.group(1))
                    # 将api结果发给gpt转换成自然语言可阅读内容
                    prompt = WEATHER_PROMPT.format(api_resp=response.text, today_date=datetime.date.today())
                    kwargs['text_message'] = prompt
                    reply = self.process_message(kwargs)
                    # 输出调试信息
                    logging.debug(reply)

            # 回复消息
            event.add_return("reply", [reply])

            # 阻止该事件默认行为（向接口获取回复）
            event.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
