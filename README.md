# 和风天气-QChatGPT插件

这是一个[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)的插件
通过命令在QQ对话框输入`天气 <地点>`，通过和风天气的API查询最近3天的天气情况

注意：由于我只开了ChatGPT Plus，所以目前仅支持`revLibs`插件的逆向方式
本插件只是尝试使用langchain的提示语模板功能，以及在插件中进行多轮对话实现LLM应用的实验插件
欢迎各位大佬来一起学习交流

## 使用方式

1. 安装requirements.txt中的依赖
1. 部署[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)，完成后使用管理员账号私聊机器人号发送`!plugin get https://github.com/lieyanqzu/WeatherPlugin`安装此插件
2. 前往QChatGPT插件的所在目录，修改插件顺序，让这个插件优先于其他插件
3. 修改天气插件中template.py文件中的和风天气API KEY，也可以尝试修改提示语模板
4. 重启主程序

此时即可向机器人发送`天气 <位置>`查询天气情况