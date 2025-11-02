"""
Updated message placeholder script that uses SQLite database for chat history
Demonstrates integration of LangChain with persistent database storage
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from chat_database import ChatDatabase
import sys

load_dotenv()

def format_messages_for_langchain(messages):
    """Convert database messages to LangChain message format"""
    formatted_messages = []

    for role, content in messages:
        if role == 'human':
            formatted_messages.append(HumanMessage(content=content))
        elif role == 'ai':
            formatted_messages.append(AIMessage(content=content))
        elif role == 'system':
            formatted_messages.append(SystemMessage(content=content))

    return formatted_messages


def chat_with_history(session_id: str, new_query: str):
    """
    Continue a conversation using history from database

    Args:
        session_id: The conversation session to continue
        new_query: The new user query to respond to
    """

    # Instantiate model
    model = ChatOpenAI()

    # Create chat template with placeholder for history
    chat_template = ChatPromptTemplate([
        ('system', 'You are a helpful customer support agent. Use the conversation history to provide context-aware responses.'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{query}')
    ])

    # Load chat history from database
    db = ChatDatabase()

    # Get messages from the specified session
    messages = db.get_conversation_messages(session_id)

    if not messages:
        print(f"No conversation found with session_id: {session_id}")
        print("Starting a new conversation...")
        # Create new conversation if it doesn't exist
        conv_id = db.create_conversation(
            session_id=session_id,
            title="New Support Conversation"
        )
    else:
        print(f"Found {len(messages)} messages in conversation history")
        # Get conversation ID for adding new messages
        db.cursor.execute('SELECT id FROM conversations WHERE session_id = ?', (session_id,))
        conv_id = db.cursor.fetchone()['id']

    # Format messages for LangChain
    chat_history = format_messages_for_langchain(messages)

    print("\n" + "="*50)
    print("CONVERSATION HISTORY:")
    print("="*50)
    for msg in chat_history:
        role = "Human" if isinstance(msg, HumanMessage) else "AI" if isinstance(msg, AIMessage) else "System"
        print(f"{role}: {msg.content}")

    print("\n" + "="*50)
    print("NEW QUERY:")
    print("="*50)
    print(f"Human: {new_query}")

    # Create prompt with history and new query
    prompt = chat_template.invoke({
        'chat_history': chat_history,
        'query': new_query
    })

    # Get response from model
    result = model.invoke(prompt)

    print("\n" + "="*50)
    print("AI RESPONSE:")
    print("="*50)
    print(result.content)

    # Save the new exchange to database
    db.add_message(conv_id, 'human', new_query)
    db.add_message(conv_id, 'ai', result.content)

    print("\n" + "="*50)
    print("Conversation updated in database!")

    db.close()

    return result.content


def demonstrate_database_features():
    """Demonstrate various database features"""

    db = ChatDatabase()

    print("\n" + "="*50)
    print("AVAILABLE CONVERSATIONS IN DATABASE:")
    print("="*50)

    conversations = db.get_recent_conversations(10)
    for conv in conversations:
        print(f"Session: {conv['session_id']}")
        print(f"  Title: {conv['title']}")
        print(f"  Last Updated: {conv['updated_at']}")
        print()

    # Search for specific messages
    print("="*50)
    print("SEARCHING FOR 'refund' IN MESSAGES:")
    print("="*50)

    search_results = db.search_messages('refund', limit=3)
    for result in search_results:
        print(f"Found in {result['session_id']}: {result['conversation_title']}")
        print(f"  {result['role']}: {result['content'][:100]}...")
        print()

    db.close()


if __name__ == "__main__":
    # Example usage
    print("CUSTOMER SUPPORT CHAT WITH DATABASE HISTORY")
    print("=" * 50)

    # Demonstrate database features
    demonstrate_database_features()

    print("\n" + "="*50)
    print("CONTINUING EXISTING CONVERSATION:")
    print("="*50)

    # Continue the refund conversation (session_001)
    response = chat_with_history(
        session_id='session_001',
        new_query='Has my refund been processed yet? It\'s been 4 days.'
    )

    print("\n" + "="*50)
    print("STARTING NEW CONVERSATION:")
    print("="*50)

    # Start a completely new conversation
    response = chat_with_history(
        session_id='session_new_001',
        new_query='I need help setting up my new smartwatch.'
    )