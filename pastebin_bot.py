import time
import requests
import groq

# 🔹 Pastebin API Details
PASTEBIN_API_KEY = "RsWWfx8B9mmSbGSc5-RIs7SOfQZlSNon"  # Developer API Key
PASTEBIN_USER_KEY = "b6b0ac69c995c7740fa3a0d484f8653f"  # User API Key
PASTE_ID = "TSpaZp3v"  # Your Pastebin Paste ID

# 🔹 Groq API Details
GROQ_API_KEY = "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"
client = groq.Groq(api_key=GROQ_API_KEY)

# ✅ Store last processed content to avoid duplicate processing
last_content = None

# 🔄 Function to Get Pastebin Content
def get_pastebin_content():
    url = f"https://pastebin.com/raw/{PASTE_ID}"  # Fetch raw paste text
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

# 🤖 Function to Get Answer from Groq
def get_chatgpt_answer(question):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# ✏️ Function to Create a New Pastebin Paste (Since Editing is NOT Supported)
def create_new_pastebin(content):
    url = "https://pastebin.com/api/api_post.php"
    params = {
        "api_dev_key": PASTEBIN_API_KEY,
        "api_user_key": PASTEBIN_USER_KEY,
        "api_paste_code": content,
        "api_paste_name": "Updated Paste",
        "api_paste_private": "1",  # 1 = Unlisted
        "api_paste_expire_date": "10M",
        "api_paste_format": "text",
        "api_option": "paste",
    }
    response = requests.post(url, data=params)
    return response.text if response.status_code == 200 else None

# 🔄 Continuous Monitoring Loop
while True:
    print("🔄 Monitoring Pastebin for new questions...")

    # Fetch Pastebin content
    content = get_pastebin_content()

    if content and content != last_content:  # Check if content changed
        last_content = content.strip()  # Store the latest paste content
        print(f"📜 Current Paste Content:\n{last_content}")

        if last_content.endswith("?"):  # Check if the last line is a question
            print(f"🤖 Found a question: {last_content}")

            # Get an answer from Groq API
            answer = get_chatgpt_answer(last_content)
            print(f"💡 Answer: {answer}")

            # Append answer below the question
            updated_content = last_content + "\n\nAnswer: " + answer

            # Create a new Pastebin paste (since direct edits are NOT possible)
            new_paste_url = create_new_pastebin(updated_content)
            if new_paste_url:
                print(f"✅ New Pastebin URL: {new_paste_url}")
            else:
                print("❌ Failed to create a new Pastebin paste!")

        else:
            print("⏳ No new questions found. Checking again in 15 seconds...")

    else:
        print("⚠️ No changes detected. Skipping update.")

    time.sleep(15)  # Wait for 15 seconds before checking again
