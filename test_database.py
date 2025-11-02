"""
Quick test script to demonstrate the database functionality
"""

from chat_database import ChatDatabase
import json


def test_database():
    """Test and demonstrate database functionality"""

    print("="*60)
    print("TESTING CHAT HISTORY DATABASE")
    print("="*60)

    db = ChatDatabase()

    # 1. Show existing conversations
    print("\n1. EXISTING CONVERSATIONS:")
    print("-"*40)
    conversations = db.get_recent_conversations(5)
    for conv in conversations:
        print(f"  • {conv['session_id']}: {conv['title']}")

    # 2. Display a sample conversation
    print("\n2. SAMPLE CONVERSATION (session_001 - Order Refund):")
    print("-"*40)
    messages = db.get_conversation_messages('session_001')
    for i, (role, content) in enumerate(messages, 1):
        print(f"  [{i}] {role.upper()}: {content[:100]}...")

    # 3. Search functionality
    print("\n3. SEARCH RESULTS FOR 'shipping':")
    print("-"*40)
    results = db.search_messages('shipping', limit=3)
    for result in results:
        print(f"  • Found in {result['session_id']}")
        print(f"    {result['role']}: {result['content'][:80]}...")

    # 4. Database statistics
    print("\n4. DATABASE STATISTICS:")
    print("-"*40)

    # Count total conversations
    db.cursor.execute("SELECT COUNT(*) FROM conversations")
    total_convs = db.cursor.fetchone()[0]

    # Count total messages
    db.cursor.execute("SELECT COUNT(*) FROM messages")
    total_msgs = db.cursor.fetchone()[0]

    # Count messages by role
    db.cursor.execute("""
        SELECT role, COUNT(*) as count
        FROM messages
        GROUP BY role
        ORDER BY count DESC
    """)
    role_counts = db.cursor.fetchall()

    print(f"  • Total Conversations: {total_convs}")
    print(f"  • Total Messages: {total_msgs}")
    print(f"  • Messages by Role:")
    for row in role_counts:
        print(f"      - {row['role']}: {row['count']} messages")

    # 5. Export a conversation
    print("\n5. EXPORTING CONVERSATION (session_002):")
    print("-"*40)
    export = db.export_conversation('session_002')
    print(f"  • Session ID: {export['session_id']}")
    print(f"  • Title: {export['title']}")
    print(f"  • Number of messages: {len(export['messages'])}")
    print(f"  • First message: {export['messages'][0]['content'][:80]}...")

    db.close()

    print("\n" + "="*60)
    print("DATABASE TEST COMPLETED SUCCESSFULLY!")
    print("="*60)


if __name__ == "__main__":
    test_database()