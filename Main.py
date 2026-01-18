import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import random

# 0. .env 파일 불러오기
load_dotenv()

# 1. 권한 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'-----------------------------------------')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="!팀짜기 | 명령 대기 중"))
    print('봇이 온라인 상태가 되었습니다!')
    print(f'-----------------------------------------')

# --- [View 1] 결과 화면 + 다시 섞기 버튼 ---
class ResultView(View):
    # 타임아웃 600초 설정
    def __init__(self, selected_members, ctx):
        super().__init__(timeout=600) 
        self.selected_members = selected_members
        self.ctx = ctx
        self.message = None # 메시지 객체를 저장할 변수

    @discord.ui.button(label="다시 섞기", style=discord.ButtonStyle.success, emoji="🎲")
    async def reshuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 1. 로직 수행
        random.shuffle(self.selected_members)
        mid_index = len(self.selected_members) // 2
        team_a = self.selected_members[:mid_index]
        team_b = self.selected_members[mid_index:]

        # 2. Embed 생성
        embed = discord.Embed(
            title=f"🎲 팀 다시 섞기 결과 (총 {len(self.selected_members)}명)",
            description="새로운 조합입니다!",
            color=0x00ff00
        )
        
        team_a_names = "\n".join([f"👤 {m.display_name}" for m in team_a])
        embed.add_field(name=f"🔴 A팀 ({len(team_a)}명)", value=team_a_names, inline=True)

        team_b_names = "\n".join([f"👤 {m.display_name}" for m in team_b])
        embed.add_field(name=f"🔵 B팀 ({len(team_b)}명)", value=team_b_names, inline=True)

        embed.set_footer(text=f"요청자: {self.ctx.author.display_name}", icon_url=self.ctx.author.avatar.url if self.ctx.author.avatar else None)

        # 3. 새 메시지 전송 및 메시지 연결 (핵심!)
        new_view = ResultView(self.selected_members, self.ctx)
        
        # interaction으로 메시지를 보낸 후, 그 메시지 객체를 가져와서 view에 저장해야 함
        await interaction.response.send_message(embed=embed, view=new_view)
        new_view.message = await interaction.original_response()

    # 타임아웃 발생 시 실행되는 함수
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass # 메시지가 삭제되었거나 권한이 없으면 무시

# --- [Select Menu] 멤버 선택 드롭다운 ---
class MemberSelect(Select):
    def __init__(self, members, ctx):
        self.members_dict = {m.id: m for m in members}
        self.ctx = ctx
        
        options = [
            discord.SelectOption(label=member.display_name, value=str(member.id), emoji="👤")
            for member in members
        ]
        super().__init__(placeholder="참여할 멤버를 선택하세요", min_values=2, max_values=len(members), options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_members = [self.members_dict[int(user_id)] for user_id in self.values]

        random.shuffle(selected_members)
        mid_index = len(selected_members) // 2
        team_a = selected_members[:mid_index]
        team_b = selected_members[mid_index:]

        result_view = ResultView(selected_members, self.ctx)

        embed = discord.Embed(
            title=f"🎮 팀 구성 결과 (총 {len(selected_members)}명)",
            description="팀 구성 완료!",
            color=0x00ff00
        )
        embed.add_field(name=f"🔴 A팀 ({len(team_a)}명)", value="\n".join([f"👤 {m.display_name}" for m in team_a]), inline=True)
        embed.add_field(name=f"🔵 B팀 ({len(team_b)}명)", value="\n".join([f"👤 {m.display_name}" for m in team_b]), inline=True)
        embed.set_footer(text=f"요청자: {self.ctx.author.display_name}", icon_url=self.ctx.author.avatar.url)
        
        # 메시지 전송 후 객체 연결
        await interaction.response.send_message(embed=embed, view=result_view)
        result_view.message = await interaction.original_response()

# --- [View 2] 드롭다운 컨테이너 ---
class TeamView(View):
    def __init__(self, members, ctx):
        super().__init__(timeout=600) # 600초 타임아웃
        self.add_item(MemberSelect(members, ctx))
        self.ctx = ctx
        self.message = None

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass

# --- 명령어: !팀짜기 ---
@bot.command(name='팀짜기')
async def make_team(ctx):
    if ctx.author.voice is None:
        embed = discord.Embed(title="❌ 오류", description="먼저 음성 채널에 입장해주세요!", color=0xff0000)
        await ctx.send(embed=embed)
        return

    voice_channel = ctx.author.voice.channel
    members = voice_channel.members
    # 봇 필터링 적용
    members = [member for member in members if not member.bot]

    if len(members) < 2:
        embed = discord.Embed(title="⚠️ 인원 부족", description="팀을 짜려면 (봇 제외) 최소 2명이 필요해요.", color=0xffa500)
        await ctx.send(embed=embed)
        return

    view = TeamView(members, ctx)
    embed = discord.Embed(title="📋 멤버 선택", description="게임에 참여할 인원을 아래 메뉴에서 선택해주세요!", color=0x3498db)
    
    # [수정] 전송된 메시지 객체를 view.message에 저장 (이게 없으면 타임아웃 때 에러 남)
    message = await ctx.send(embed=embed, view=view)
    view.message = message

# --- 명령어: !초대 ---
@bot.command(name='초대')
async def invite_link(ctx):
    bot_id = bot.user.id
    
    # [수정] 권한 설정 적용
    # 19456 = 보기(View Channels) + 보내기(Send Messages) + 임베드(Embed Links)
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&permissions=19456&scope=bot"

    embed = discord.Embed(
        title="💌 봇 초대하기",
        description="아래 버튼을 눌러서 저를 서버에 초대해주세요!\n(필요한 권한이 자동으로 포함되어 있습니다)",
        color=0xffc0cb
    )
    
    view = discord.ui.View()
    button = discord.ui.Button(label="서버에 초대하기", url=invite_url, style=discord.ButtonStyle.link, emoji="🔗")
    view.add_item(button)
    
    await ctx.send(embed=embed, view=view)

# 봇 실행 
if __name__ == "__main__":
    # 2. 환경변수에서 토큰 가져오기
    token = os.getenv('DISCORDBOT_TOKEN')
    
    # 토큰이 제대로 있는지 확인 (실수 방지용)
    if token is None:
        print("에러: .env 파일을 찾을 수 없거나 토큰이 없습니다!")
    else:
        bot.run(token) # 여기에 직접 토큰을 넣는 게 아니라 변수를 넣음