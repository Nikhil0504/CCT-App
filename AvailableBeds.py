import discord, json, time, os

token = os.getenv("DISCORD_TOKEN")
client = discord.Client()


@client.event
async def on_ready():
    print("\nWe have logged in as {0.user}".format(client))


data = {}
district_list = {}

temp = set()
data["tamilnadu"] = json.load(open("beds.json"))
for i in data["tamilnadu"]:
 	temp.add(i["District"])
district_list["tamilnadu"] = sorted(list(temp))


def districts(message, state):
    temp = district_list[state]
    embed = discord.Embed(
        title="Select a district",
        description="Format: -data [state] [district]"
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
                "tamilnadu"
            )
        )

    elif message.content.lower().startswith("-data "):
        temp = message.content.split(" ")
        flag = False

        if len(temp) < 3:
            flag = True

        for i in data[temp[1]]:
            if flag == False:
                if i["District"].replace(" ", "").lower() != temp[2].lower():
                    continue
            embed = discord.Embed(name=i["Institution"])
            for j in i:
                embed.add_field(name=j, value=i[j])
            await message.channel.send(embed=embed)


client.run(token)
