from datetime import datetime
from dhooks import Webhook, Embed
from creds import get_discord_url


url = get_discord_url()
hook = Webhook(url)

#gifs and images
goujo = 'https://i.imgur.com/rsWkrgB.gif'
jojo = 'https://i.imgur.com/XnzcljA.gif'
bot = 'https://i.imgur.com/RFk9hgO.gif'



def get_embed(txt, subject):
    global embed
    embed = Embed(
    description=f'Status for class of {subject}.',
    color=0xFFF,
    timestamp='now'  # sets the timestamp to current time
    )
    embed.set_author(name='MS-Teams Bot')
    embed.set_thumbnail(goujo)
    embed.set_image(bot)
    embed.add_field(name=f'Status for {subject}', value=txt)
    embed.set_footer(text='Here is my footer text', icon_url=jojo)
    return embed

#takes txt and put it into our embed template and sent it to our dicord channel
def notify(txt, sub):
    embed = get_embed(txt, sub)
    hook.send(embed=embed)

