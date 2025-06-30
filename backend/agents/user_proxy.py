from autogen import UserProxyAgent

def create_user_proxy():
    return UserProxyAgent(
        name="User_proxy",
        system_message="You are the human admin initiating an EDA analysis task.",
        code_execution_config={
            "use_docker": False,
            "last_n_messages": 3,
            "work_dir": "groupchat"
        },
        human_input_mode="NEVER"  # Fully automated for web app
    )