import streamlit as st
import pandas as pd
import os
import sys
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from backend.agents.eda_agents import setup_groupchat_with_agents
from config import (
    LLM_PROVIDER, 
    get_available_models_for_provider, 
    get_default_model_for_provider, 
    DEFAULT_TEMPERATURE, 
    DEFAULT_MAX_ROUNDS,
    is_provider_configured
)

# Page configuration
st.set_page_config(
    page_title="EDA Autogen App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #00e676;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #444;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #00e676;
    }
    
    .user-message {
        border-left-color: #2196f3;
        background: #1a1a2e;
    }
    
    .coder-message {
        border-left-color: #4caf50;
        background: #1a2e1a;
    }
    
    .critic-message {
        border-left-color: #e91e63;
        background: #2e1a1a;
    }
    
    .analyst-message {
        border-left-color: #ff9800;
        background: #2e2e1a;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00e676 0%, #00c853 100%);
        color: #000;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 230, 118, 0.3);
    }
    
    .file-uploader {
        border: 2px dashed #00e676;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
    
    .provider-info {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #444;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 EDA Autogen App</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("---")
        
        # LLM Provider Selection
        provider_options = ["ollama", "openai", "gemini"]
        selected_provider = st.selectbox(
            "🤖 LLM Provider",
            provider_options,
            index=provider_options.index(LLM_PROVIDER),
            help="Choose your LLM provider"
        )
        
        # Provider-specific configuration
        if selected_provider == "ollama":
            st.info("🖥️ **Local Ollama** - Free, offline, privacy-focused")
            if not is_provider_configured("ollama"):
                st.warning("⚠️ Make sure Ollama is running: `ollama serve`")
        
        elif selected_provider == "openai":
            st.info("☁️ **OpenAI API** - Professional, reliable, paid")
            if not is_provider_configured("openai"):
                st.error("❌ OpenAI API key not configured")
                st.markdown("Set `OPENAI_API_KEY` environment variable")
        
        elif selected_provider == "gemini":
            st.info("☁️ **Google Gemini** - Fast, cost-effective, paid")
            if not is_provider_configured("gemini"):
                st.error("❌ Gemini API key not configured")
                st.markdown("Set `GEMINI_API_KEY` environment variable")
        
        # Model selection based on provider
        available_models = get_available_models_for_provider(selected_provider)
        default_model = get_default_model_for_provider(selected_provider)
        
        if available_models:
            selected_model = st.selectbox(
                "🎯 Select Model",
                available_models,
                index=available_models.index(default_model) if default_model in available_models else 0,
                help=f"Choose the {selected_provider} model to use"
            )
        else:
            st.error(f"No models available for {selected_provider}")
            selected_model = default_model
        
        # Temperature control
        temperature = st.slider(
            "🌡️ Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
            help="Lower values = more focused, Higher values = more creative"
        )
        
        # Performance optimization section
        st.markdown("---")
        st.markdown("**🚀 Performance Settings**")
        
        # Faster defaults for better performance
        temperature = st.slider(
            "🌡️ Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = faster, more concise responses"
        )
        
        max_rounds = st.slider(
            "🔄 Max Conversation Rounds",
            min_value=5,
            max_value=20,
            value=5,
            help="Lower = faster analysis, Higher = more thorough"
        )
        
        # Performance tips
        if max_rounds > 5:
            st.warning("⚠️ High rounds may slow down analysis")
        if temperature < 0.5:
            st.info("💡 Higher temperature = faster responses")
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("- Upload CSV files for analysis")
        "- Watch AI agents collaborate"
        "- Get insights and visualizations"
        f"- Using {selected_provider.upper()} provider"
        
        st.markdown("---")
        st.markdown("**🔧 Requirements:**")
        if selected_provider == "ollama":
            st.markdown("- Ollama running locally")
            st.markdown(f"- Model: {selected_model}")
        else:
            st.markdown(f"- Model: {selected_model}")
            st.markdown(f"- {selected_provider.upper()} API configured")
        
        # Model info
        with st.expander("ℹ️ Model Information"):
            model_info = {
                # Ollama models
                "mistral": "Fast, balanced performance - recommended for most use cases",
                "llama3": "High quality, slower processing - best for complex analysis",
                "codellama": "Specialized for code generation - excellent for data science code",
                "qwen": "Good balance of speed and quality - versatile option",
                "neural-chat": "Intel's optimized model - good performance on Intel hardware",
                "phi3": "Microsoft's lightweight model - fast and efficient",
                # OpenAI models
                "gpt-3.5-turbo": "Fast, cost-effective - good for most EDA tasks",
                "gpt-4": "High quality, more expensive - best for complex analysis",
                "gpt-4-turbo": "Balanced performance - good quality at reasonable cost",
                # Gemini models
                "gemini-1.5-flash": "Fast, cost-effective - good for most use cases",
                "gemini-1.5-pro": "High quality - excellent for complex analysis",
                "gemini-2.0-flash": "Latest model - cutting-edge performance"
            }
            if selected_model in model_info:
                st.info(model_info[selected_model])
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Provider status
     
        st.subheader(f"🔌 {selected_provider.upper()} Provider Status")
        
        if is_provider_configured(selected_provider):
            st.success(f"✅ {selected_provider.upper()} is configured and ready")
        else:
            st.error(f"❌ {selected_provider.upper()} is not properly configured")
            if selected_provider == "ollama":
                st.markdown("**To fix:** Start Ollama with `ollama serve`")
            else:
                st.markdown(f"**To fix:** Set {selected_provider.upper()}_API_KEY environment variable")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # File upload section
     
        st.subheader("📁 Upload Your Dataset")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file to analyze",
            type=['csv'],
            help="Upload any CSV file for automated EDA analysis"
        )
        
        if uploaded_file is not None:
            try:
                # Read and display data preview
                df = pd.read_csv(uploaded_file)
                
                st.success(f"✅ File uploaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Data preview
                with st.expander("🔍 Data Preview", expanded=True):
                    st.dataframe(df.head(10), width='stretch')
                    
                    # Basic info
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.metric("Rows", df.shape[0])
                        st.metric("Columns", df.shape[1])
                    
                    with col_info2:
                        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                        st.metric("Data Types", len(df.dtypes.unique()))
                
                # Analysis button
                if st.button("🚀 Start AI Analysis", type="primary", use_container_width=True):
                    if is_provider_configured(selected_provider):
                        start_analysis(df, selected_model, temperature, max_rounds, selected_provider)
                    else:
                        st.error(f"❌ {selected_provider.upper()} is not configured. Please check the sidebar.")
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Status and progress
        st.subheader("📊 Analysis Status")
        
        if 'analysis_complete' not in st.session_state:
            st.info("👆 Upload a CSV file and click 'Start AI Analysis' to begin")
        
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.success(f"✅ Analysis complete! {len(st.session_state.chat_history)} messages generated")
            
            # Download results
            if st.button("💾 Download Results"):
                download_results()
            
            # Show quick stats
            with st.expander("📈 Quick Stats"):
                if st.session_state.chat_history:
                    agent_counts = {}
                    for msg in st.session_state.chat_history:
                        sender = msg['sender']
                        agent_counts[sender] = agent_counts.get(sender, 0) + 1
                    
                    st.metric("Total Messages", len(st.session_state.chat_history))
                    st.metric("Agents Involved", len(agent_counts))
                    st.metric("Most Active", max(agent_counts, key=agent_counts.get) if agent_counts else "N/A")

def start_analysis(df, model, temperature, max_rounds, provider):
    """Start the AI analysis with the uploaded dataset"""
    
    # Initialize session state
    st.session_state.chat_history = []
    if 'analysis_started' not in st.session_state:
        st.session_state.analysis_started = True
    
    # Performance tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_tracker = st.empty()
    
    # Start timing
    start_time = time.time()
    
    try:
        # Update status
        status_text.text(f"🤖 Initializing AI agents with {provider.upper()}...")
        progress_bar.progress(0.1)

        # Setup agents with custom parameters
        user_proxy, manager, message = setup_groupchat_with_agents(
            df.head().to_string(),
            model=model,
            temperature=temperature,
            max_rounds=max_rounds
        )

        progress_bar.progress(0.3)
        status_text.text("🧠 Agents are collaborating...")

        # Create chat container with live updates
        chat_container = st.container()

        # Create a placeholder for live agent conversation
        conversation_placeholder = st.empty()

        # Start the conversation with live display
        with chat_container:
            st.subheader("🧠 AI Agent Collaboration")

            # Add debugging info
            with st.expander("🔍 Debug Info", expanded=False):
                st.write(f"**Provider:** {provider}")
                st.write(f"**Model:** {model}")
                st.write(f"**Temperature:** {temperature}")
                st.write(f"**Max Rounds:** {max_rounds}")
                st.write(f"**Expected Time:** {max_rounds * 2} minutes max")

            # Live conversation display
            st.markdown("### 💬 Live Conversation")
            conversation_area = st.empty()

            # Initialize chat
            user_proxy.initiate_chat(manager, message=message)

            # Show message count for debugging
            actual_messages = len(manager.groupchat.messages)
            st.info(f"📊 Generated {actual_messages} messages from AI agents")

            # Prepare chat history (reset to avoid duplicates)
            st.session_state.chat_history = []
            # To accumulate all markdown for conversation
            conversation_markdown = ""

            # Process messages with live display and code execution
            total_messages = len(manager.groupchat.messages)
            for i, msg in enumerate(manager.groupchat.messages):
                # Check timeout (2 minutes per round max)
                elapsed_time = time.time() - start_time
                max_expected_time = max_rounds * 120  # 2 minutes per round

                if elapsed_time > max_expected_time:
                    st.warning(f"⏰ Analysis taking longer than expected ({elapsed_time/60:.1f} minutes)")
                    if elapsed_time > max_expected_time * 1.5:  # 50% over expected
                        st.error("⏰ Analysis timeout - stopping for performance")
                        break

                # Update time tracker
                time_tracker.text(f"⏱️ Elapsed: {elapsed_time/60:.1f} minutes")

                # Determine message type and styling
                if isinstance(msg, dict):
                    sender = msg.get("name") or msg.get("role") or provider.upper()
                    content = msg.get("content", "No content")
                else:
                    sender = getattr(msg, "name", None) or getattr(msg, "role", None) or provider.upper()
                    content = getattr(msg, "content", "No content")

                # Skip empty messages
                if not content or content.strip() == '':
                    continue

                # Add to session state
                st.session_state.chat_history.append({
                    'sender': sender,
                    'content': content,
                    'timestamp': time.time()
                })

                # Create a message bubble as markdown
                message_class = get_message_class(sender)
                message_md = (
                    f'<div class="chat-message {message_class}">'
                    f"<strong>{sender}</strong> (Message {i+1}/{total_messages})<br>"
                    f"{content}"
                    f"</div>\n"
                    "---\n"
                )
                conversation_markdown += message_md
                # Update the conversation area dynamically
                conversation_area.markdown(conversation_markdown, unsafe_allow_html=True)

                # Live code execution for Coder agent
                if sender == "Coder" and "```python" in content:
                    try:
                        # Extract Python code from the message
                        code_start = content.find("```python") + 9
                        code_end = content.find("```", code_start)
                        if code_end != -1:
                            python_code = content[code_start:code_end].strip()

                            # Create a code execution section
                            with st.expander(f"🚀 Executing {sender}'s Code", expanded=True):
                                st.code(python_code, language="python")

                                # Execute the code
                                try:
                                    # Create a local namespace with the dataframe
                                    local_vars = {'df': df, 'pd': pd, 'plt': plt, 'sns': sns, 'np': np}

                                    # Execute the code
                                    exec(python_code, globals(), local_vars)

                                    # Display any plots that were created
                                    if 'plt' in local_vars and local_vars['plt'].gcf().get_axes():
                                        st.pyplot(local_vars['plt'].gcf())
                                        st.success("✅ Code executed successfully! Plot displayed above.")

                                    # Show any variables that were created
                                    if 'df' in local_vars and local_vars['df'] is not df:
                                        st.write("**Modified DataFrame:**")
                                        st.dataframe(local_vars['df'].head(), width='stretch')

                                except Exception as exec_error:
                                    st.error(f"❌ Code execution failed: {str(exec_error)}")
                                    st.code(f"# Error: {str(exec_error)}", language="python")

                    except Exception as parse_error:
                        st.warning(f"⚠️ Could not parse code from {sender}'s message")

                # Update progress - ensure it stays within valid bounds
                if total_messages > 0:
                    progress = 0.3 + (i + 1) * (0.6 / total_messages)  # 0.3 to 0.9
                    progress = min(max(progress, 0.0), 1.0)  # Clamp between 0.0 and 1.0
                    progress_bar.progress(progress)

                # Reduced delay for faster processing (optionally remove or decrease)
                # time.sleep(0.2)

            # Final progress and status
            total_time = time.time() - start_time
            progress_bar.progress(1.0)
            status_text.text(f"✅ Analysis complete in {total_time/60:.1f} minutes!")
            time_tracker.text(f"⏱️ Total time: {total_time/60:.1f} minutes")
            st.session_state.analysis_complete = True

            # Performance summary
            if total_time > max_rounds * 120:  # Over 2 minutes per round
                st.warning(f"⚠️ Analysis took {total_time/60:.1f} minutes - consider reducing max rounds or temperature for faster results")
            else:
                st.success(f"🚀 Fast analysis completed in {total_time/60:.1f} minutes!")

            # Show summary
            show_analysis_summary()

    except Exception as e:
        total_time = time.time() - start_time
        st.error(f"❌ Analysis failed after {total_time/60:.1f} minutes: {str(e)}")
        status_text.text("❌ Analysis failed")
        progress_bar.progress(0)
        time_tracker.text(f"⏱️ Failed after: {total_time/60:.1f} minutes")
        # Log the full error for debugging
        st.exception(e)

def get_message_class(sender):
    """Get CSS class for message styling based on sender"""
    # Map exact agent names to their CSS classes
    if sender == "user" or sender.lower() == "user":
        return 'user-message'
    elif sender == "Coder":
        return 'coder-message'
    elif sender == "Critic":
        return 'critic-message'
    elif sender == "Analyst":
        return 'analyst-message'
    else:
        return ''

def show_analysis_summary():
    """Display a summary of the analysis results"""
    st.subheader("📋 Analysis Summary")
    
    if 'chat_history' in st.session_state:
        # Count messages by agent
        agent_counts = {}
        for msg in st.session_state.chat_history:
            sender = msg['sender']
            agent_counts[sender] = agent_counts.get(sender, 0) + 1
        
        # Display summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Messages", len(st.session_state.chat_history))
            st.metric("Agents Involved", len(agent_counts))
        
        with col2:
            st.metric("Analysis Duration", f"{len(st.session_state.chat_history) * 0.5:.1f}s")
            st.metric("Most Active Agent", max(agent_counts, key=agent_counts.get) if agent_counts else "N/A")

def download_results():
    """Download the analysis results"""
    if 'chat_history' in st.session_state:
        # Create a text file with all messages
        content = "EDA Autogen App - Analysis Results\n"
        content += "=" * 50 + "\n\n"
        
        for msg in st.session_state.chat_history:
            content += f"{msg['sender']}:\n{msg['content']}\n\n"
            content += "-" * 30 + "\n\n"
        
        # Create download button
        st.download_button(
            label="📥 Download Analysis Report",
            data=content,
            file_name="eda_analysis_report.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
