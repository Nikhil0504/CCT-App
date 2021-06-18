import discord, requests, time, os

token = os.getenv("DISCORD_TOKEN")
client = discord.Client()


@client.event
async def on_ready():
    print("\nWe have logged in as {0.user}".format(client))


data = {}
district_list = {}


def districts(message, state, api):

    if state not in district_list:
        temp = set()
        data[state] = requests.get(api).json()
        for i in data[state]:
            temp.add(i["DISTRICT"])
        district_list[state] = sorted(list(temp))

    temp = district_list[state]
    embed = discord.Embed(
        title="Select a district",
        description="Format: -data [state] [district]",
        url=discord.embeds.EmptyEmbed,
    )

    for i in temp:
        embed.add_field(
            name=i, value="-data {} {}".format(state, i.replace(" ", "").lower())
        )

    return embed


@client.event
async def on_message(message):

    if message.content.lower() == "-tamilnadu":
        await message.channel.send(
            embed=districts(
                message,
                "tamilnadu",
                "https://api.covidbedsindia.in/v1/storages/6089820e03eef3b588d05a6d/Tamil%20Nadu",
            )
        )

    elif message.content.lower() == "-andhrapradesh":
        await message.channel.send(
            embed=districts(
                message,
                "andhrapradesh",
                "https://api.covidbedsindia.in/v1/storages/608982e003eef31f34d05a71/Andhra%20Pradesh",
            )
        )

    elif message.content.lower().startswith("-data "):
        temp = message.content.split(" ")
        flag = False

        if len(temp) < 3:
            flag = True

        for i in data[temp[1]]:
            if flag == False:
                if i["DISTRICT"].replace(" ", "").lower() != temp[2].lower():
                    continue
            embed = discord.Embed(name=i["HOSPITAL_NAME"])
            for j in i:
                embed.add_field(name=j, value=i[j])
            await message.channel.send(embed=embed)


client.run("ODU0MTc4NDA4OTM3Njg1MDEz.YMgJog.LgmQavCKowier0_RBRn42Rs-SqM")

while True:
    time.sleep(7200)
    district_list = {}
    data = {}
