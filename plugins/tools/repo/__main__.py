# repo

from userge import Config, Message, userge


@userge.on_cmd("repo", about={"header": "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"• **repo** : [my repo]({Config.UPSTREAM_REPO})"
    await message.edit(output)
