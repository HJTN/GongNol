import discord
import json
from datetime import datetime

TOKEN = json.load(open('params.json'))['TOKEN']
CHANNEL_ID = json.load(open('params.json'))['CHANNEL_ID']

class ChatBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.change_presence(
            status=discord.Status.online, 
            activity=discord.Game(name='GongNol'))
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            await message.channel.send(f'pong {message.author.mention}')
        else:
            answer = self.get_answer(message.content)
            await message.channel.send(answer)
    
    def get_day_of_week(self):
        weekday_list = ['월', '화', '수', '목', '금', '토', '일']

        weekday = weekday_list[datetime.now().weekday()]
        date = datetime.today().strftime('%Y년 %m월 %d일')
        result = f'{date} {weekday}요일입니다.'
        return result
    
    def get_time(self):
        return datetime.today().strftime('%H시 %M분 %S초')
    
    def get_answer(self, txt):
        trim_txt = txt.replace(' ', '')

        answer_dict = {
            '안녕': '안녕하세요! GongNol ChatBot 입니다.',
            '요일': f': Calendar: 오늘은 {self.get_day_of_week()}입니다.',
            '시간': f': Clock: 현재 시간은 {self.get_time()}입니다.',
        }

        if trim_txt == '' or None:
            return '알 수 없는 질의입니다. 답변을 드릴 수 없습니다.'
        elif trim_txt in answer_dict.keys():
            return answer_dict[trim_txt]
        else:
            for key in answer_dict.keys():
                if key.find(trim_txt) != -1:
                    return f'연관 단어 [{key}]에 대한 답변입니다.\n {answer_dict[key]}'
            
            for key in answer_dict.keys():
                if answer_dict[key].find(txt[1:]) != -1:
                    return f'질문과 가장 유사한 질문 [{key}]에 대한 답변입니다.\n {answer_dict[key]}'
        
        return f'{txt}은(는) 알 수 없는 질의입니다. 답변을 드릴 수 없습니다.'

intents = discord.Intents.default()
intents.message_content = True

client = ChatBot(intents=intents)
client.run(TOKEN)