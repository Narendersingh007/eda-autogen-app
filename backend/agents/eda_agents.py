import autogen
from autogen import (
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    config_list_from_json
)

def setup_groupchat_with_agents(df_preview_str: str, model: str = "mistral", temperature: float = 0.7, max_rounds: int = 5):
    """Setup AutoGen agents for EDA with optimized performance settings"""
    
    # Proper Ollama config for AutoGen
    llm_config = {
        "config_list": [{
            "api_type": "ollama",
            "model": model,
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "temperature": temperature,
            "request_timeout": 120,
            "max_new_tokens": 2048
        }]
    }
    
    # Optimized system messages for faster, focused responses
    user_proxy = UserProxyAgent(
        name="User", 
        system_message="You are a human who wants a quick, actionable EDA analysis. Keep responses concise and focused.",
        human_input_mode="NEVER",
        llm_config=llm_config,
        code_execution_config={"use_docker": False}
    )
    
    coder = AssistantAgent(
        name="Coder",
        system_message="""You are a Python data scientist. Write CONCISE, EXECUTABLE code for EDA.

**REQUIREMENTS:**
- Write complete, runnable Python code
- Focus on KEY insights, not exhaustive analysis
- Create 3-5 meaningful visualizations maximum
- Keep explanations brief and actionable
- Use pandas, matplotlib, seaborn
- NO verbose explanations - just code and key findings
- DO NOT reload or read the dataset from disk (e.g., do NOT use pd.read_csv).
- Assume a pandas DataFrame named `df` is ALREADY loaded and available in memory; use it directly.
- For all matplotlib/seaborn plots, ensure you call `plt.show()` so plots are displayed.

**DELIVERABLES:**
1. Data overview (shape, types, missing values)
2. Key statistics and correlations
3. 3-5 meaningful plots
4. Summary of main insights

Be FAST and FOCUSED!""",
        llm_config=llm_config
    )
    
    critic = AssistantAgent(
        name="Critic", 
        system_message="""You are a data science reviewer. Provide QUICK, CONSTRUCTIVE feedback.

**REVIEW FOCUS:**
- Code quality and execution
- Visualization effectiveness
- Insight relevance
- Actionability

**KEEP IT BRIEF:**
- 2-3 sentences maximum per feedback point
- Focus on major issues only
- Suggest quick improvements
- NO lengthy explanations

Be FAST and CONCISE!""",
        llm_config=llm_config
    )
    
    analyst = AssistantAgent(
        name="Analyst", 
        system_message="""You are a business analyst. Provide QUICK, ACTIONABLE insights.

**DELIVERABLES:**
- 3-5 key business insights
- 2-3 actionable recommendations
- Risk factors to consider
- Next steps for stakeholders

**KEEP IT BRIEF:**
- Bullet points preferred
- One sentence per insight
- Focus on business value
- NO lengthy explanations

Be FAST and ACTIONABLE!""",
        llm_config=llm_config
    )
    
    # Create group chat with performance-optimized settings
    groupchat = GroupChat(
        agents=[user_proxy, coder, critic, analyst], 
        messages=[], 
        max_round=max_rounds
    )
    
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    # Optimized prompt for faster analysis
    message = f"""Perform a QUICK, FOCUSED EDA on this dataset:

**Dataset Preview:**
{df_preview_str}

**REQUIREMENTS (KEEP IT FAST):**
1. Data overview (shape, types, missing values) - 2-3 lines max
2. Key statistics - focus on important numbers only
3. 3-5 meaningful visualizations with brief insights
4. Quick quality review
5. 3-5 actionable business insights

**IMPORTANT:**
- Be CONCISE and FOCUSED
- NO lengthy explanations
- Focus on actionable insights
- Complete analysis in {max_rounds} rounds maximum

Start immediately with the data overview and code."""

    return user_proxy, manager, message