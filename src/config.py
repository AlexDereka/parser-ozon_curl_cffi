HEADERS : dict[str, str] = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.6',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# First of all, you should send 1 message to your bot to allow bot to send messages to you

# Your telegram id, used to send messages to you
YOUR_ID : str = ''

# List of telegram bots' API KEYS you can define one or more
# If first fails it will try to use next until end
API_KEYS : list[str] = []
