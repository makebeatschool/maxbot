from maxapi.types import InputMedia

from config import FILE_PATH_CHECKLIST
attachment = None
async def preload_file(bot):
    media = InputMedia(path=FILE_PATH_CHECKLIST)
    bot.checklist_attachment = await bot.upload_media(media)