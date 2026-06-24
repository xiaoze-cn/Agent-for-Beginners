import requests

# 请自己配置以下参数
BASE_URL = "https://api.XXX.com/v1"
API_KEY = "sk-XXX"
MODEL = "XXX"


class OpenAIChat:
    def __init__(self, model, base_url, api_key):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.messages = []

    def developer(self, content):
        self.messages.append({"role": "developer", "content": content})

    def user(self, content):
        self.messages.append({"role": "user", "content": content})

    def assistant(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def build(self, **options):
        return {
            "model": self.model,
            "messages": self.messages,
            **options,
        }

    def send_request(self, **options):
        base_url = self.base_url.rstrip("/")
        if not base_url.lower().endswith("/v1"):
            base_url = f"{base_url}/v1"

        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=self.build(**options),
        )
        response.raise_for_status()
        return response.json()

    def parse_response(self, data):
        message = data["choices"][0]["message"]
        self.messages.append(message)
        return message


def main():
    chat = OpenAIChat(
        model=MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
    )

    while True:
        user_input = input("User：").strip()

        if user_input == "/exit":
            break

        if not user_input:
            continue

        chat.user(user_input)
        data = chat.send_request(temperature=0.3, max_tokens=1024)
        message = chat.parse_response(data)

        print(f"Agent：{message['content']}")


if __name__ == "__main__":
    main()
