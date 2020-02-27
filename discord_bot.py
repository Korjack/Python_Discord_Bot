#-*- coding:utf-8 -*-
# Use to Python Module -> Discord.
import asyncio
import discord

from discord.ext import commands

import os, re
import random
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# Get Youtube videos using pytube.
from pytube import YouTube


# This is thing that is needed to use the bot as a chat.
# For example, $play ...
# 봇에게 명령어를 내릴때 필요한 글자입니다.
# 예를 들면, $재생 ...
bot = commands.Bot(command_prefix='$')

# This base_path is the path you need to download YouTube videos or save the files you need.
# 이 봇을 사용하면서 저장되는 모든 임시파일 및 동영상은 여기에 있습니다.
base_path = '/discord_temp/'

# Youtube URL
source_url = 'https://www.youtube.com'
serch_url = '/results?search_query='

# This function gets 10 video information from YouTube with keyword.
# keyword : Youtube Title Searched by User.
# 사용자가 찾고 싶은 유튜브 영상 10가지 정도를 추려서 선택할 수 있게 함.
# keyword : 사용자가 찾고 싶어하는 검색어
def get_url(keyword):
	playlist = {}
	s = ''

	# This is the process of merging when there is a space between letters.
	# The reason for doing this is to search through the URL.
	# For example : My Heart Will Go On -> My+Heart+Will+Go+On.
	# Python3 에서 한글 오류로 인한 문제 해결로 urllib.parse.quote_plus를 사용했음.
	# 검색어 사이에 있는 띄어쓰기를 +로 대채함.
	for idx, i in enumerate(keyword):
		s += urllib.parse.quote_plus(i)
		if (idx+1 != len(keyword)):
			s+= '+'
	
	# Combine the URLs into one, and send the request.
	# URL을 통하여 검색함.
	url = source_url+serch_url+s
	response = urllib.request.urlopen(url)

	# It analyzes the data obtained by requesting Youtube through Beautiful soup's html.parser.
	# 검색해서 얻은 html파일을 분석
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	# It looks for video links in order of <h3>, <a> and <sapn> from tag.
	# <h3>, <a>, <span> 순으로 youtube 영상의 링크, 시간, 제목을 찾아낸다.
	h3 = soup.find_all('h3')
	for i in h3:
		tag_a = i.find_all('a')
		if tag_a:
			tag_span = i.find_all('span')
			ttime = ''
			if (len(tag_span) != 0):

				# It stores the corresponding video length in ttime.
				# 해당 영상의 시간정보를 가져옴.
				ttime = re.findall('[0-9]+:[0-9]+', str(tag_span))

				# This is changes the minute to second.
				# 시간이 시, 분으로 되어있어서 초로 바꿔줘야함
				if(len(ttime) != 0):
					ttime = ttime[0].split(':')
					ttime = (int(ttime[0])*60) + int(ttime[1])
				
			# It stores 10 kinds of video titles, links, and times in playlist.
			#playlist's type is dictionary.
			# 이제 10가지의 영상 정보를 playlist에다 저장함.
			for j in tag_a:
				playlist[j.get('title')] = [j.get('href'), ttime]

	return playlist

# It downloads the video that the user chooses.
# 사용자가 선택한 영상을 다은받음.
def get_mp4_file(url):
	yt = YouTube(url)
	yt.streams.first().download(base_path)
	os.rename(base_path+yt.streams.first().default_filename, base_path+'tmp.mp4')

# The command is designed to play YouTube videos in voice chat rooms.
# Youtube 영상을 보이스채널에서 재생하는 명령어임.
@bot.command()
async def 재생(ctx, *arg):
	
	# This identifies who used the command.
	# 누가 이 명령어를 사용했는지 확인.
	author = ctx.message.author

	search = ''
	for i in arg:
		search += i + ' '

	# This is command log.
	# 커맨드창 로그.
	print('{}님이 {}라고 검색했습니다'.format(author, search))

	playlist = get_url(arg)

	# This message comes when there are no unexpected errors or search results.
	# 예상치 못한 에러, 검색결과가 없을 경우 사용자에게 알려줌.
	if len(playlist) == 0:
		return await ctx.send(':warning: Something is wrong...  :confused:')
	
	# This is a message form that users create for ease of viewing.
	# 사용자에게 편하게 보여주기 위해 메세지 폼을 만듬
	content = ':mag_right: 검색결과 :mag:\n```'
	for idx, i in enumerate(playlist):
		if(idx<10):
			content += '{}. {}\n'.format(idx+1, i)
			
	# 커맨드창 로그.
	# This is command log.
	print('\n%%검색결과%%\n\n')
	print(content)
	print('='*80)

	content += '```\n\n:information_source: 30초 내로 선택해주세요...\n'
	await ctx.send(content)

	try:

		# It waits about 30 seconds for the user to choose the video they want.
		# 30초 정도 사용자의 선택을 기다린다.
		def check(m):
			return m.content in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
		msg = await bot.wait_for('message', check=check, timeout=30)

		for idx, i in enumerate(playlist):
			if (str(idx+1) == msg.content):

				# If the user who entered the command did not enter the voice channel, the user will be notified by message.
				# 사용자가 보이스 채널에 입장 안되어있으면 알림메시지를 날림.
				try:
					channel = author.voice.channel
				except:
					return await ctx.send(':warning: 보이스 채널에 입장해주세요...')
				
				# If the image is not a playable video, it informs the user with a message.
				# 동영상 파일이 문제 있거나 볼 수 없는 영상이라면 다음과 같은 알림을 보여줌.
				try:
					get_mp4_file(source_url+playlist[i][0])
				except:
					return await ctx.send(':warning: 영상에 문제가 있습니다...')
				
				# After the bot enters the voice channel where the user is located, it plays the video received at 0.10 volume.
				# 봇이 보이스채널에 입장하고, 선택한 영상을 볼륨 0.10으로 틀어준다.
				vc = await channel.connect()
				video = discord.FFmpegPCMAudio(base_path+'tmp.mp4')
				souce = discord.PCMVolumeTransformer(video, 0.10)
				await ctx.send(':notes: 뮤직 스타튜!')
				vc.play(souce)

				# The bot waits until the end of the video time, then exits the voice channel and deletes the video.
				# 영상이 끝날때까지 기다린 후에 봇은 퇴장하고, 영상을 삭제한다.
				await asyncio.sleep(playlist[i][1])
				await vc.disconnect()
				os.unlink(base_path+'tmp.mp4')
	
	# If not selected for the specified seconds in the day, the user is notified that the time is exceeded.
	# 사용자가 30초 동안 선택을 안했을 경우 시간 초과 메시지를 보낸다.
	except asyncio.TimeoutError:
		await ctx.send(':warning: 선택시간이 초과 되었습니다!')


# This is a command used to end the music that is currently playing.
# 봇이 재생중일 때, 멈추게 하는 명령어다.
@bot.command()
async def 그만(ctx, *arg):
	author = str(ctx.message.author)
	if(len(bot.voice_clients) != 0):
		for x in bot.voice_clients:
			await ctx.send(':information_source: {}님이 음악재생을 종료하셨습니다.'.format(author.split('#')[0]))
			await x.disconnect()
			try:
				os.unlink(base_path+'tmp.mp4')
			except:
				pass
	# If the bot is not on the voice channel, it informs the user that it is not on the channel.
	# 봇이 아무것도 하지 않는 상태에서 명령했을 때.
	else:
		await ctx.send(':information_source: 저는 아무것도 하고 있지 않아요...')


# This is a dice. Sends a number between 0 and 100 as a message.
# 주사위 명령어. 0 ~ 100 사이의 숫자를 보여줌.
@bot.command()
async def 주사위(ctx, *arg):
	await ctx.send(':game_die: 주사위 굴려서 나온 숫자는 {} 입니다!'.format(random.randint(0,100)))

# This is help that user use commands.
# 도움말이다.
@bot.command()
async def 도움말(ctx, *arg):
	content = """
:notebook: 명령어들 : [$재생, $그만, $주사위]
:book: $도움말 [궁금한 명령어]
"""
	if (len(arg)==0):
		await ctx.send(content)
	elif arg[0] == '재생':
		content = ':loudspeaker: $재생 [듣고싶은 YouTube영상 제목]\n:hash: 노래리스트가 나옵니다. 거기서 숫자로 골라주세요.'
	elif arg[0] == '그만':
		content = ':loudspeaker: $그만\n:hash: 봇이 음성채널에서 꺼져줍니다.'
	elif arg[0] == '주사위':
		content = ':loudspeaker: $주사위\n:hash: 0 ~ 100사이의 숫자가 나옵니다.'
		await ctx.send(content)

# Main bot start.
# 메인 시작점.
@bot.event
async def on_ready():
	print('가동준비 완료!')
	game = discord.Game("궁금하면 [$도움말]")
	await bot.change_presence(activity=game)
	

bot.run("Your Bot Token")