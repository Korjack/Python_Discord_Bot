# This is My Style Discord Bot.

 [In English]

  I'm not that good at coding.

  I was not good at English, so I used English through a translator.

  If you want to listen to the YouTube video through the discode bot, you can use this code.
 
  The annotation are written in Korean and English.
  
  Please note that the explanation may be slightly different between the two languages.
 
 [In Korean]
 
  저는 코딩을 잘 하는 편이 아니고, 영어 또한 잘 하는 편이 아닙니다.

  만약 디스코드 봇 중에서 YouTube로부터 노래를 재생하고 싶으시다면 이 코드를 사용하셔도 좋습니다.

  이 봇은 스트리밍으로 재생하는 것이 아닌 동영상을 받아서 재생하는 방식입니다.

  주석은 한글과 영어로 되어 있습니다.
  
  두 개의 언어 사이에서 설명은 조금 다를 수 도 있으니 참고바랍니다.

# How to use this
  
  #### I use docker, and container is anaconda3
  
  #### 저는 도커에서 아나콘다3 컨테이너를 사용해서 봇을 돌렸습니다.
  
  #### This is a docker container that I used. Follow the [link](https://registry.hub.docker.com/u/continuumio/anaconda3/)(this is container link) if you need it.
  
  #### 제가 사용한 도커 컨테이너가 궁금하시다면 [링크](https://registry.hub.docker.com/u/continuumio/anaconda3/)를 참고바랍니다.
  
  #### If it is a different operating system or does not support apt, you will have to find and do ffmpeg yourself.
  
  #### 만일에 도커가 아닌 OS에서 구동하시게 된다면 apt를 사용하지 않는 OS는 저도 어떻게 해야할지 잘 모르니, ffmpeg는 알아서 설치바랍니다.
  
  1. Install python3(version=3.7.4) or use docker
  
     파이썬을 설치 또는 도커 사용바랍니다.

  2. Use pip and install this requirements. Use this commands
  
     pip을 사용하여 필요한 모듈을 설치합니다. 아래에 적혀있는 커맨드를 사용하시면 됩니다.
     
  
    pip install -r requirements.txt


  3. Discord bots need ffmpeg to regenerate their voices.
  
     apt를 이용하여 ffmpeg를 설치합니다.
    
    sudo apt install ffmpeg
    
     
  4. If you see an error, try the following command:
    
     에러를 보게 되신다면, 아래 명령어를 사용해보세요.
    
    sudo apt update
    
    sudo apt upgrade
    
  
# RUN! 시작!
    python discord_bot.py

