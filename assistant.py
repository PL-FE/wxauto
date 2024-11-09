import openai
import json

class ChatGPTClient:
    def __init__(self):
        self.model = 'gpt-4o-mini'
        # 替换成你的key，我这个是一个测试的key，请自行替换
        openai.api_key = "sk-7EzKMSSKdTlNMy2C2e88C383E15b45BfA59228FaF2Fe38B11"

        openai.base_url = "https://api.gpt.ge/v1/"
        openai.default_headers = {"x-foo": "true"}


    def get_response(self, history: list) -> str:
        """
        传入历史记录，调用 ChatGPT 并返回下一句回复的建议。

        Parameters:
            history (list): 历史记录列表，每个元素是一个字典，包含角色和内容，例如：
                            [{"role": "user", "content": "你好，ChatGPT"}, {"role": "assistant", "content": "你好！有什么可以帮您的？"}]

        Returns:
            str: ChatGPT 的回复内容
        """

        msg = [
            {
                "role": "user",
                "content": "我会输入一段聊天记录给你，请你生成下一句回复给我。回复格式为列表，每项是一句回复，列表长度为5.要求返回格式只能是列表的JSON，不能包含md格式，以下是聊天记录：",
            },
            {
                "role": "user",
                "content": json.dumps(history, ensure_ascii=False, indent=4)
            }
        ]

        response = openai.chat.completions.create(
            model=self.model,
            messages=msg,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content



# 使用示例
if __name__ == "__main__":
    client = ChatGPTClient()

    history = [
        {"role": "user", "content": "你好，ChatGPT"},
        {"role": "assistant", "content": "你好！有什么可以帮您的？"},
        {"role": "user", "content": "请告诉我今天的天气。"}
    ]

    reply = client.get_response(history)
    print("ChatGPT 回复:", reply)

