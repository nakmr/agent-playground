import os

from plugins.WebSearchPlugin.web_search import WebSearchPlugin
from plugins.SlackPlugin.slack_plugin import SlackPlugin

from typing import Dict
from semantic_kernel.plugin_definition.kernel_plugin import KernelPlugin

import guidance
from guidance import system, user, assistant, gen

from semantic_kernel.planning.basic_planner import BasicPlanner

from app.config.sk_config import SKModuleConfiguration
from app.plugin.sk_add_plugin import SKPluginConfiguration


kernel = SKModuleConfiguration.add_azure_ai_to_kernel()


"""

"""
def add_plugins() -> Dict[str, KernelPlugin]:

    functions = {}

    plugins_directory = "plugins"

    funPlugin = kernel.import_semantic_plugin_from_directory(plugins_directory, "FunPlugin")
    functions["Joke"] = funPlugin["Joke"]

    messagePlugin = kernel.import_semantic_plugin_from_directory(plugins_directory, "MessagePlugin")
    functions["GenerateMessageJa"] = messagePlugin["GenerateMessageJa"]

    googlePlugin = kernel.import_plugin(WebSearchPlugin(), "WebSearchPlugin")
    functions["GoogleSearch"] = googlePlugin["GoogleSearch"]

    slackPlugin = kernel.import_plugin(SlackPlugin(), "SlackPlugin")
    functions["SendMessage"] = slackPlugin["SendMessage"]


    return functions

"""

"""
async def execute_plugins():

    functions = add_plugins()

    input = "Bitcoin price"

    # Google検索を実行
    result = await functions["GoogleSearch"].invoke(input)
    print(result)


@guidance
def conversation_with_experts(lm, input, skills, previous_input="", previous_output=""):
    with system():
        lm += f"""\
        # 前提条件
            - あなたはユーザの入力に基づいて「実行計画」を作成する優秀なプランナーです。
            - 実行計画はユーザの入力を達成するために必要な作業内容を分解および順序づけしたものです。
            - 実行計画には関数の利用を含みます。
            - 実行計画で利用できる関数は「使用可能な関数」で定義された関数のみです。
        """

    with user():
        lm += f"""
        # ゴール
            - ユーザの入力から実行計画を作成する
            - 出力形式は以下のようなJSONフォーマットであること
                ```
                {{
                    "user": "すべてのユーザ入力を統合した文章",
                    "best_plan": [実行する関数名のリスト],
                    "input_description": "実行する関数名とその関数を利用する目的の説明"
                }}
                ```
        # 実行のプロセス
            1. ユーザの入力を受け取り、実行計画を3つ作成する
            2. 最も有効な実行計画が1位となるようにランク付けする
            3. 1位の実行計画をJSONフォーマットに変換する
            4. JSONフォーマットに変数した実行計画のみを出力する
        # 使用可能な関数
        """

        for i in range(len(skills)):
            lm += f"""
                - {skills[i]["name"]}: {skills[i]["description"]}
            """

    with assistant():
        lm += f"""\
            はい。ユーザの入力に基づいて実行計画を作成し、JSONのみを出力します。
            また、実行計画の作成には使用可能な関数のみを使用します。
        """

    with user():
        if previous_output == None:
            lm += f"""\
                ユーザの入力:{input}
                必ずJSON形式の部分のみを出力してください。
            """
        else:
            lm += f"""\
                新しいユーザの入力:{input}
                前回のユーザの入力:{previous_input}
                前回のユーザの入力および新しいユーザの入力に基づいて、新しい実行計画を作成してください。
                また、必ずJSON形式の部分のみを出力してください。
            """

    with assistant():
        lm += gen(name='answer', max_tokens=1000)

    return lm

"""

"""
def generate_plan_by_agent():

    buddy = guidance.models.AzureOpenAIChat(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

    # Agentに渡す関数を定義
    skills = [
        {"name": "GenerateMessageJa", "description": "Compose a short message in Japanese based on the input subject. Execute this function before sending a message anywhere."},
        {"name": "SendMessage", "description": "Send formatted messages to Slack."},
        {"name": "GoogleSearch", "description": "Performs a web search for a given query with Google."},
        {"name": "Joke", "description": "Get a random joke."},
    ]

    result = None

    user_input = input("なにを依頼したいですか？ 特に依頼がなければ何も入力しないでください:")

    if user_input != "":
        result = buddy + conversation_with_experts(input=user_input, skills=skills)
        print(f"======実行計画======")
        print(result['answer'])
        print(f"\n")

        while True:
            user_next_input = input("実行計画を更新する場合は、何か入力してください。特に更新しない場合は何も入力せずにEnterを押してください:")
            if user_next_input == "":
                break
            else:
                result = buddy + conversation_with_experts(input=user_next_input, skills=skills, previous_input=user_input, previous_output=result['answer'])
                print(f"======再作成した実行計画======")
                print(result['answer'])
                print(f"\n")

    return result

async def execute_plan_by_agent(plan_base: str):
    # KernelにPluginを追加
    add_plugins()

    # 実行計画を作成する
    basic_planner = BasicPlanner()
    basic_plan = await basic_planner.create_plan(plan_base, kernel)
    print(f"### Plan ###\n{basic_plan.generated_plan}")

    # 実行計画を実行する
    results = await basic_planner.execute_plan(basic_plan, kernel)
    print(results)



import asyncio
# Plugin利用を実行する
# asyncio.run(execute_plugins())

# 実行計画を作成する
result = generate_plan_by_agent()

# Agentに実行計画をInputする
asyncio.run(execute_plan_by_agent(result['answer']))




