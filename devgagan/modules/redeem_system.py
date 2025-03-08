import json
import random
import string
import time

OWNER_ID = 7792539085  # आपका Owner ID

# JSON File से डेटा लोड करें
def load_data():
    try:
        with open("redeem_codes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"codes": {}}

# JSON File में डेटा सेव करें
def save_data(data):
    with open("redeem_codes.json", "w") as f:
        json.dump(data, f, indent=4)

# नया कोड जनरेट करने का फ़ंक्शन
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# कोड क्रिएट करने का कमांड
async def create_redeem_code(update, context):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return await update.message.reply_text("❌ आप इस कमांड को इस्तेमाल नहीं कर सकते!")

    args = context.args
    if len(args) < 1:
        return await update.message.reply_text("⚠ कृपया समय सीमा (जैसे 1h, 1d) प्रदान करें।")

    duration = args[0]
    if duration.endswith("h"):
        expiry_time = int(time.time()) + int(duration[:-1]) * 3600
    elif duration.endswith("d"):
        expiry_time = int(time.time()) + int(duration[:-1]) * 86400
    else:
        return await update.message.reply_text("❌ समय सीमा गलत है! सही फॉर्मेट: `1h` या `1d`")

    code = generate_code()
    
    data = load_data()
    data["codes"][code] = {
        "expiry": expiry_time,
        "used_by": []
    }
    save_data(data)

    await update.message.reply_text(f"✅ नया रिडीम कोड:\n`{code}`\n🕒 वैधता: {duration}")

# कोड रिडीम करने का कमांड
async def redeem_code(update, context):
    user_id = update.message.from_user.id
    args = context.args
    if not args:
        return await update.message.reply_text("⚠ कृपया एक वैध कोड दर्ज करें!")

    code = args[0].strip()
    data = load_data()

    if code not in data["codes"]:
        return await update.message.reply_text("❌ यह कोड अमान्य है!")

    if user_id in data["codes"][code]["used_by"]:
        return await update.message.reply_text("⚠ आप पहले ही इस कोड का उपयोग कर चुके हैं!")

    if time.time() > data["codes"][code]["expiry"]:
        del data["codes"][code]  # एक्सपायर्ड कोड डिलीट करें
        save_data(data)
        return await update.message.reply_text("❌ यह कोड एक्सपायर हो गया है!")

    # यूज़र को ऐड करें
    data["codes"][code]["used_by"].append(user_id)
    save_data(data)

    await update.message.reply_text("✅ आपका कोड सफलतापूर्वक रिडीम हो गया!")