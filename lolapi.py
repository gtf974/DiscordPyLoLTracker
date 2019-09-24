import discord
from discord.ext import commands
import requests
import asyncio

class Lolapi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lolstat(self, ctx,* ,summonername: str=None):
        """Pour afficher vos stats de League Of Legends"""
        def requestSummonerData(name, region):
            url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name.replace(" ","%20") + "?api_key=LOLAPITOKEN"
            response = requests.get(url)
            return response.json()
        def requestRankedData(id1, region):
            url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + id1 + "?api_key=LOLAPITOKEN"
            response = requests.get(url)
            return response.json()
        def requestLeagueData(id2, region):
            url = "https://"+region+".api.riotgames.com/lol/league/v4/leagues/"+id2+"?api_key=LOLAPITOKEN"
            response = requests.get(url)
            return response.json()
        def requestChampionData(id3, region):
            url= "https://"+region+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+id3+"?api_key=LOLAPITOKEN"
            response= requests.get(url)
            return response.json()
        def requestChampionName():
            url= "http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json"
            response= requests.get(url)
            return response.json()
        def requestTenor(tags):
            url= "https://api.tenor.com/v1/search?q=league%20of%20legends%20"+tags+"&key=LIVDSRZULELA&limit=1"
            response= requests.get(url)
            return response.json()

        await ctx.send("Quelle est votre région parmi:\n``euw1`` (Europe de l'Ouest)\n``ru`` (Russie)\n``kr`` (Corée)\n``br1`` (Brésil)\n``oc1`` (Océanie)\n``jp1`` (Japon)\n``na1`` (Amérique du Nord)\n``eun1`` (Europe du Nord)\n``tr1`` (Turquie)\n``la1`` (Amérique Latine 1)\n``la2`` (Amérique Latine 2)\n(30 secondes pour répondre)")
        def pred(m):
            return m.author == ctx.author and m.channel == ctx.message.channel
        try:
            region = await self.bot.wait_for("message", check=pred, timeout=30)
            region = region.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("Vous avez mis trop de temps pour répondre. :/")
        else:
            responseJSON= requestSummonerData(summonername, region)
            id= str(responseJSON["id"])
            responseJSON2= requestRankedData(id, region)
            leagueid= str(responseJSON2[0]["leagueId"])
            responseJSON3= requestLeagueData(leagueid, region)
            responseJSON4= requestChampionData(id, region)
            responseJSON5= requestChampionName()
            championid= responseJSON4[0]["championId"]
            championname= ""
            champion_Name= ""
            responseJSON6= {}
            if not summonername:
                await ctx.send("Vous devez renseigner un nom d'invocateur.")
            else:
                for dict in responseJSON5["data"]:
                    if responseJSON5["data"][dict]["key"]== str(championid):
                        championname= dict.lower().replace(" ","%20")
                        champion_Name= dict
                        responseJSON6= requestTenor(championname)
                embedlolstat1 = discord.Embed(title=":crossed_swords: **" + summonername + "** :crossed_swords: ("+str(responseJSON["summonerLevel"])+")",colour=discord.Colour.orange())
                embedlolstat1.set_footer(text="By Idotcom")
                if "IRON" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://opgg-static.akamaized.net/images/medals/iron_1.png")
                elif "BRONZE" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/bronze.png")
                elif "SILVER" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Silver.png")
                elif "GOLD" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Gold.png")
                elif "PLATINUM" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Platinum.png")
                elif "DIAMOND" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Diamond.png")
                elif "MASTER" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="https://i.imgur.com/iTCN6wL.png")
                elif "CHALLENGER" in responseJSON2[0]["tier"]:
                    embedlolstat1.set_thumbnail(url="http://i.imgur.com/6s5eKdv.png")
                embedlolstat1.add_field(name="**Queue:**", value="`" +responseJSON2[0]["queueType"] + "`")
                embedlolstat1.add_field(name="**Rank:**",value="`" + responseJSON2[0]["tier"] + " " + responseJSON2[0]["rank"] + "`")
                embedlolstat1.add_field(name="**LP:**", value="`" + str(responseJSON2[0]["leaguePoints"]) + "`")
                embedlolstat1.add_field(name="**Nom de la division:**", value="`" + responseJSON3["name"] + "`")
                loloperate4 = responseJSON2[0]["wins"] + responseJSON2[0]["losses"]
                loloperate5 = responseJSON2[0]["wins"] / loloperate4
                loloperate6 = round(loloperate5 * 100, ndigits=1)
                embedlolstat1.add_field(name="**Winrate:**",value="`" + str(loloperate6) + "% (" + str(responseJSON2[0]["wins"]) + "W/" + str(responseJSON2[0]["losses"]) + "L)`")
                embedlolstat1.add_field(name= "**Champion le plus maîtrisé**", value="`" + champion_Name + ": " + str(responseJSON4[0]["championPoints"]) + " points (Niveau "+ str(responseJSON4[0]["championLevel"])+")`")
                embedlolstat1.set_image(url= responseJSON6["results"][0]["media"][0]["gif"]["url"])
                await ctx.send(embed= embedlolstat1)
                embedlolstat2 = discord.Embed(title=":crossed_swords: **" + summonername + "** :crossed_swords: (" + str(responseJSON["summonerLevel"]) + ")", colour=discord.Colour.orange())
                embedlolstat2.set_footer(text="By Idotcom")
                if "IRON" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://opgg-static.akamaized.net/images/medals/iron_1.png")
                elif "BRONZE" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/bronze.png")
                elif "SILVER" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Silver.png")
                elif "GOLD" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Gold.png")
                elif "PLATINUM" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Platinum.png")
                elif "DIAMOND" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Diamond.png")
                elif "MASTER" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="https://i.imgur.com/iTCN6wL.png")
                elif "CHALLENGER" in responseJSON2[1]["tier"]:
                    embedlolstat2.set_thumbnail(url="http://i.imgur.com/6s5eKdv.png")
                embedlolstat2.add_field(name="**Queue:**", value="`" + responseJSON2[1]["queueType"] + "`")
                embedlolstat2.add_field(name="**Rank:**", value="`" + responseJSON2[1]["tier"] + " " + responseJSON2[1]["rank"] + "`")
                embedlolstat2.add_field(name="**LP:**", value="`" + str(responseJSON2[1]["leaguePoints"]) + "`")
                leagueid2 = str(responseJSON2[1]["leagueId"])
                responseJSON3 = requestLeagueData(leagueid2, region)
                embedlolstat2.add_field(name="**Nom de la division:**", value="`" + responseJSON3["name"] + "`")
                loloperate1 = responseJSON2[1]["wins"] + responseJSON2[1]["losses"]
                loloperate2 = responseJSON2[1]["wins"] / loloperate1
                loloperate3 = round(loloperate2 * 100, ndigits=1)
                embedlolstat2.add_field(name="**Winrate:**", value="`" + str(loloperate3) + "% (" + str(responseJSON2[1]["wins"]) + "W/" + str(responseJSON2[1]["losses"]) + "L)`")
                embedlolstat2.add_field(name="**Champion le plus maîtrisé**",value="`" + champion_Name + ": " + str(responseJSON4[0]["championPoints"]) + " points (Niveau "+ str(responseJSON4[0]["championLevel"])+")`")
                embedlolstat2.set_image(url= responseJSON6["results"][0]["media"][0]["gif"]["url"])
                await ctx.send(embed=embedlolstat2)
                embedlolstat3 = discord.Embed(title=":crossed_swords: **" + summonername + "** :crossed_swords: ("+str(responseJSON["summonerLevel"])+")",colour=discord.Colour.orange())
                embedlolstat3.set_footer(text="By Idotcom")
                if "IRON" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://opgg-static.akamaized.net/images/medals/iron_1.png")
                elif "BRONZE" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/bronze.png")
                elif "SILVER" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Silver.png")
                elif "GOLD" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Gold.png")
                elif "PLATINUM" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Platinum.png")
                elif "DIAMOND" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://mobalytics.gg/wp-content/uploads/2016/04/Diamond.png")
                elif "MASTER" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="https://i.imgur.com/iTCN6wL.png")
                elif "CHALLENGER" in responseJSON2[2]["tier"]:
                    embedlolstat3.set_thumbnail(url="http://i.imgur.com/6s5eKdv.png")
                embedlolstat3.add_field(name="**Queue:**", value="`" + responseJSON2[2]["queueType"] + "`")
                embedlolstat3.add_field(name="**Rank:**", value="`" + responseJSON2[2]["tier"] + " " + responseJSON2[2]["rank"] + "`")
                embedlolstat3.add_field(name="**LP:**", value="`" + str(responseJSON2[2]["leaguePoints"]) + "`")
                leagueid2 = str(responseJSON2[2]["leagueId"])
                responseJSON3 = requestLeagueData(leagueid2, region)
                embedlolstat2.add_field(name="**Nom de la division:**", value="`" + responseJSON3["name"] + "`")
                loloperate1 = responseJSON2[2]["wins"] + responseJSON2[2]["losses"]
                loloperate2 = responseJSON2[2]["wins"] / loloperate1
                loloperate3 = round(loloperate2 * 100, ndigits=1)
                embedlolstat3.add_field(name="**Winrate:**", value="`" + str(loloperate3) + "% (" + str(responseJSON2[2]["wins"]) + "W/" + str(responseJSON2[2]["losses"]) + "L)`")
                embedlolstat3.add_field(name="**Champion le plus maîtrisé**",value="`" + champion_Name + ": " + str(responseJSON4[0]["championPoints"]) + " points (Niveau "+ str(responseJSON4[0]["championLevel"])+")`")
                embedlolstat3.set_image(url= responseJSON6["results"][0]["media"][0]["gif"]["url"])
                await ctx.send(embed=embedlolstat3)





def setup(bot):
    bot.add_cog(Lolapi(bot))