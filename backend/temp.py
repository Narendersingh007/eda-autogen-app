from agents.eda_agents import setup_groupchat_with_agents

sample_preview = "col1,col2\n1,2\n3,4\n5,6"
user_proxy, manager, message = setup_groupchat_with_agents(sample_preview)
user_proxy.initiate_chat(manager, message=message)

for msg in manager.groupchat.messages:
    if isinstance(msg, dict):
        sender = msg.get("name", "Unknown")
        content = msg.get("content", "NO CONTENT")
        print(f"{sender}: {content}")
    else:
        # fallback for object-style messages
        print(f"{getattr(msg, 'sender', 'Unknown')}: {getattr(msg, 'content', 'NO CONTENT')}")