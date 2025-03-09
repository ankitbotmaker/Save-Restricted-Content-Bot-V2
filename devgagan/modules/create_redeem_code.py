from pyrogram import Client, filters
from .create_redeem_code import generate_redeem_code
OWNER_ID = 7792539085  # Owner ID यहाँ डालो

@Client.on_message(filters.command("generate_code") & filters.user(OWNER_ID))
async def generate_code(client, message):
    print("✅ Generate Code Command Triggered")  # Debugging के लिए
    await message.reply_text("✅ Redeem Code: ABCD1234")  # Static Response