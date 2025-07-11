import autogen
from autogen import (
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    config_list_from_json
)

def setup_groupchat_with_agents(df_preview_str: str):
    # Load Ollama config (local LLM)
    llm_config = {
        "config_list": [{
            "api_type": "ollama",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "model": "mistral",
            "temperature": 0.2,
            "num_predict": 2048,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "seed": 42,
            "top_k": 40,
            "top_p": 0.9
        }]
    }

    # Define the user (human) proxy
    user_proxy = UserProxyAgent(
        name="User",
        system_message="You are a human who wants an EDA analysis from AI agents.",
        human_input_mode="NEVER",
        code_execution_config={"use_docker": False}
    )

    # Coder Agent (writes code)
    coder = AssistantAgent(
        name="Coder",
        system_message="You write Python pandas/matplotlib/seaborn code to perform EDA based on user input.",
        llm_config=llm_config,
    )

    # Critic Agent (reviews code and visuals)
    critic = AssistantAgent(
        name="Critic",
        system_message="""Critic. You are highly skilled at reviewing EDA code and analysis.
Rate the code and insights across these:
- bugs
- data transformation
- goal compliance
- visualization type
- encoding
- aesthetics

Provide a score out of 10 for each and suggest improvements (no code).""",
        llm_config=llm_config,
    )

    # Analyst Agent (optional: adds high-level summaries and insights)
    analyst = AssistantAgent(
        name="Analyst",
        system_message="You summarize EDA findings, interpret visuals, and generate insights for business decision making.",
        llm_config=llm_config,
    )

    # Create group chat
    groupchat = GroupChat(
        agents=[user_proxy, coder, critic, analyst],
        messages=[],
        max_round=10
    )

    # Group chat manager
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )

    # Initial message with dataset preview
    message = f"""
Please perform an Exploratory Data Analysis (EDA) on the following dataset.
Here are the first few rows:\n{df_preview_str}
Generate insightful analysis, visualizations, and summaries.
"""

    return user_proxy, manager, message