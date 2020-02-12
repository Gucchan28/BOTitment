import asyncio

import discord
from discord.ext import commands

class Recruitment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''ここからコマンドの作成'''
    @commands.command()
    async def rect(self, ctx, about, time: int):
        '''募集をかけるよ！ タイトル＠人数 制限時間 で入力してね'''
        cnt = int(about.split('@')[1])
        reaction_member = ['参加者一覧！']
        embed = discord.Embed(title=about.split('@')[0],color=0xff8000)
        embed.add_field(name=f'あと{cnt}人 募集中\n', value='まだ誰も参加していないよ', inline=True)
        embed.add_field(name=f'制限時間は{time}分です！\n', value=';p', inline=True)
        msg = await ctx.send(embed=embed)
        '''リアクションの欄'''
        await msg.add_reaction('⏫')
        await msg.add_reaction('✖')

        def check(reaction, user):
            emoji = str(reaction.emoji)
            if user.bot == True:
                pass
            else:
                return emoji == '⏫' or '✖'
        
        while len(reaction_member)-1 <= cnt:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=time*60, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await ctx.send('時間になりました！人は集まったかな？')
                break
            else:
                if str(reaction.emoji) == '⏫':
                    reaction_member.append(user.name)
                    cnt -= 1
                    embed = discord.Embed(title=about.split('@')[0],color=0xff8000)
                    embed.add_field(name=f'あと{cnt}人 募集中\n', value='\n'.join(reaction_member), inline=True)
                    embed.add_field(name=f'制限時間は{time}分です！\n', value=';p', inline=True)
                    await msg.edit(embed=embed)

                    if cnt == 0:
                        embed = discord.Embed(title=about.split('@')[0],color=0xff8000)
                        embed.add_field(name=f'あと{cnt}人 募集中\n', value='\n'.join(reaction_member), inline=True)
                        embed.add_field(name=f'制限時間は{time}分です！\n', value=';p', inline=True)
                        await msg.edit(embed=embed)
                        await msg.clear_reactions()
                        finish = discord.Embed(title=about.split('@')[0],color=0xff8000)
                        finish.add_field(name='人数が集まりました！', value='\n'.join(reaction_member), inline=True)
                        await ctx.send(embed=finish)
                
                elif str(reaction.emoji) == '✖':
                    if user.name in reaction_member:
                        reaction_member.remove(user.name)
                        cnt += 1
                        embed = discord.Embed(title=about.split('@')[0],color=0xff8000)
                        embed.add_field(name=f'あと{cnt}人 募集中\n', value='\n'.join(reaction_member), inline=True)
                        embed.add_field(name=f'制限時間は{time}分です！\n', value=';p', inline=True)
                        await msg.edit(embed=embed)
                    else:
                        pass

def setup(bot):
    bot.add_cog(Recruitment(bot))
