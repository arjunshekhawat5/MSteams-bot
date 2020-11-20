from datetime import datetime
from dhooks import Webhook, Embed
url = 'https://discord.com/api/webhooks/779211044815765545/qqKJIVWN8e7vQ-z8deu0XXe5WIGRjcBicrPOT6QXgpCC587D742-xijYgcjj4ZAK5ZjZ'
hook = Webhook(url)

embed = Embed(
    description='Joins the MS-teams video classes.',
    #color=0xFFF,
    timestamp='now'  # sets the timestamp to current time
    )
jojo = 'https://i.imgur.com/rsWkrgB.gif'
goujo = 'https://i.imgur.com/XnzcljA.gif'


embed.set_author(name='MS-Teams Bot')
embed.set_thumbnail(jojo)
embed.set_image(goujo)


def get_embed(txt, subject):
    global embed

    embed.add_field(name=f'Status for {subject}', value=txt)
    #embed.set_footer(text='Here is my footer text', icon_url=image1)
    return embed

def notify_status(action,subject, status = True):
    date_time = datetime.now().date()
    if action.lower() == 'join':
        if status:
            txt = f"Successfully joined the class for {subject} on {date_time}. "            
        else:
            txt = f"Failed to join the class for {subject} on {date_time}. "

    else:
        txt = f"Left class for  {subject} on {date_time}. "

        
    hook.send(embed=get_embed(txt, subject))

notify_status('Join', 'test_subject', True)