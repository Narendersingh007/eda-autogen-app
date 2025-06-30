from autogen import AssistantAgent

def create_coder(llm_config):
    return AssistantAgent(
        name="Coder",
        system_message="You are a skilled data analyst. Generate code that performs Exploratory Data Analysis (EDA) on the dataset. Visualize insights with clean plots. Use pandas, matplotlib, and seaborn.",
        llm_config=llm_config
    )