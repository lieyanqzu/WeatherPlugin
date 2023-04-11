from langchain.prompts import PromptTemplate

# 和风天气api key
API_KEY = ""

# 标记BOT需要提取的内容
BOT_TAG_PATTERN = r"<bot>(.*?)</bot>"

# 获取城市搜索API地址提示语模板
LOCATION_PROMPT = PromptTemplate(
    input_variables=["location", "api_key"],
    template='''待查询天气位置：{location}
帮我拼装下面这个api地址：https://geoapi.qweather.com/v2/city/lookup?location=<location>&key={api_key}
<location>替换成这个位置的所在城市
举例：
待查询天气位置：天安门
回复：https://devapi.qweather.com/s6/weather/forecast?location=北京&key={api_key}
你只需要回复用<bot></bot>包裹起来的api地址即可''',
)

# 获取3日天气API地址提示语模板
API_PROMPT = PromptTemplate(
    input_variables=["location", "api_key", "location_resp"],
    template='''下面是和风天气城市LocationID查询api返回结果，帮我拼装下面这个api地址：https://devapi.qweather.com/v7/weather/3d?location=<location>&key={api_key}
<location>替换成{location}所在城市的LocationID
你只需要回复用<bot></bot>包裹起来的api地址即可
{location_resp}''',
)

# 解读3日天气API结果提示语模板
WEATHER_PROMPT = PromptTemplate(
    input_variables=["api_resp", "today_date"],
    template='''今天日期是：{today_date}，下面是和风天气的api返回结果，帮我整理成中文自然语言可以阅读的内容，用良好的排版展示今天、明天、后天的最高最低气温、天气状况和风力状况，只需要给我表格的内容就可以了，不要回复其他解释性内容和说明性内容，不需要bot标签包裹
{api_resp}''',
)
