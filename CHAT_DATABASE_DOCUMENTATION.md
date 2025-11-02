# Chat History Database Documentation

## Overview

This documentation covers the implementation of a persistent chat history system using SQLite database for LangChain-based conversational AI applications. The system replaces the simple text file approach with a robust, scalable database solution.

## Table of Contents

1. [Architecture](#architecture)
2. [Database Schema](#database-schema)
3. [Components](#components)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Migration from Text Files](#migration-from-text-files)
9. [Best Practices](#best-practices)

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│           LangChain Application             │
│  (message_placeholder_db.py)                │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│          ChatDatabase Class                 │
│         (chat_database.py)                  │
│                                             │
│  • Connection Management                    │
│  • CRUD Operations                          │
│  • Search & Export                          │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│           SQLite Database                   │
│         (chat_history.db)                   │
│                                             │
│  Tables:                                    │
│  • conversations                            │
│  • messages                                 │
└─────────────────────────────────────────────┘
```

### Key Improvements Over Text File Approach

| Feature | Text File | Database |
|---------|-----------|----------|
| **Structure** | Unstructured lines | Relational tables with foreign keys |
| **Querying** | Manual parsing | SQL queries with indexes |
| **Scalability** | Limited | Handles millions of messages |
| **Concurrency** | File locks | Multi-user support |
| **Search** | Linear scan | Indexed search |
| **Metadata** | None | JSON fields for extensibility |
| **Performance** | O(n) reads | O(log n) with indexes |

---

## Database Schema

### Conversations Table

Stores metadata about each conversation session.

```sql
CREATE TABLE conversations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT UNIQUE NOT NULL,  -- Unique identifier for the conversation
    title           TEXT,                   -- Human-readable title
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        TEXT                    -- JSON field for additional data
);
```

### Messages Table

Stores individual messages within conversations.

```sql
CREATE TABLE messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,       -- Foreign key to conversations
    role            TEXT NOT NULL,          -- 'human', 'ai', or 'system'
    content         TEXT NOT NULL,          -- The actual message content
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        TEXT,                   -- JSON field for message metadata
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

### Indexes

For optimized query performance:

```sql
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conversations_session ON conversations(session_id);
```

---

## Components

### 1. chat_database.py

Core database interface providing:

- **Connection management** with context manager support
- **CRUD operations** for conversations and messages
- **Search functionality** across all messages
- **Export capabilities** for conversation backup
- **Automatic table creation** on first use

### 2. populate_dummy_data.py

Creates realistic customer support conversations including:

- Order refund requests
- Shipping inquiries
- Product recommendations
- Account issues
- Technical support
- Payment problems
- Product exchanges

### 3. message_placeholder_db.py

LangChain integration demonstrating:

- Loading conversation history from database
- Converting database records to LangChain message format
- Continuing existing conversations
- Saving new exchanges back to database
- Search and retrieval capabilities

---

## Installation & Setup

### Prerequisites

```bash
pip install langchain langchain-openai python-dotenv sqlite3
```

### Initial Setup

1. **Create the database and schema:**
   ```python
   from chat_database import ChatDatabase
   db = ChatDatabase()  # Automatically creates tables
   db.close()
   ```

2. **Populate with dummy data:**
   ```bash
   python3 populate_dummy_data.py
   ```

3. **Configure environment variables:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

---

## Usage Guide

### Basic Usage

```python
from chat_database import ChatDatabase

# Initialize database
db = ChatDatabase()

# Create a new conversation
conv_id = db.create_conversation(
    session_id="user_123_chat_001",
    title="Customer Support Chat",
    metadata={"channel": "web", "user_id": "123"}
)

# Add messages
db.add_message(conv_id, "human", "I need help with my order")
db.add_message(conv_id, "ai", "I'd be happy to help! What's your order number?")

# Retrieve conversation
messages = db.get_conversation_messages("user_123_chat_001")
for role, content in messages:
    print(f"{role}: {content}")

db.close()
```

### Integration with LangChain

```python
from message_placeholder_db import chat_with_history

# Continue an existing conversation
response = chat_with_history(
    session_id='session_001',
    new_query='What's the status of my refund?'
)

# Start a new conversation
response = chat_with_history(
    session_id='new_session_001',
    new_query='I want to upgrade my subscription'
)
```

---

## API Reference

### ChatDatabase Class

#### Constructor
```python
ChatDatabase(db_path: str = "chat_history.db")
```

#### Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create_conversation()` | Create new conversation | `session_id`, `title`, `metadata` | `int` (conversation ID) |
| `add_message()` | Add message to conversation | `conversation_id`, `role`, `content`, `metadata` | `int` (message ID) |
| `get_conversation_messages()` | Get all messages from a conversation | `session_id` | `List[Tuple[str, str]]` |
| `get_recent_conversations()` | Get most recent conversations | `limit` | `List[Dict]` |
| `delete_conversation()` | Delete a conversation and its messages | `session_id` | `None` |
| `search_messages()` | Search messages containing text | `query`, `limit` | `List[Dict]` |
| `export_conversation()` | Export conversation as dictionary | `session_id` | `Dict` |

---

## Examples

### Example 1: Customer Support Bot

```python
def handle_customer_query(user_id: str, query: str):
    """Handle a customer support query with context"""

    session_id = f"support_{user_id}_{datetime.now().strftime('%Y%m%d')}"

    # Continue or start conversation
    response = chat_with_history(session_id, query)

    # Log for quality assurance
    with ChatDatabase() as db:
        export = db.export_conversation(session_id)
        save_for_review(export)

    return response
```

### Example 2: Search Previous Interactions

```python
def find_similar_issues(problem_description: str):
    """Find similar issues from past conversations"""

    db = ChatDatabase()

    # Search for similar problems
    similar = db.search_messages(problem_description, limit=5)

    solutions = []
    for match in similar:
        # Get full conversation context
        conv = db.export_conversation(match['session_id'])
        solutions.append({
            'problem': match['content'],
            'solution': extract_solution(conv['messages'])
        })

    db.close()
    return solutions
```

### Example 3: Analytics and Reporting

```python
def generate_support_report():
    """Generate analytics on support conversations"""

    db = ChatDatabase()

    # Get all conversations from last 30 days
    db.cursor.execute('''
        SELECT COUNT(*) as total,
               AVG(message_count) as avg_messages,
               COUNT(DISTINCT DATE(created_at)) as active_days
        FROM (
            SELECT c.id, c.created_at, COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.created_at > datetime('now', '-30 days')
            GROUP BY c.id
        )
    ''')

    stats = db.cursor.fetchone()

    db.close()
    return stats
```

---

## Migration from Text Files

### Old Approach (text file)

```python
# Old: Reading from text file
chat_history = []
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())
```

### New Approach (database)

```python
# New: Reading from database
from chat_database import ChatDatabase

db = ChatDatabase()
messages = db.get_conversation_messages('session_001')
chat_history = format_messages_for_langchain(messages)
db.close()
```

### Migration Script

```python
def migrate_text_to_db(text_file: str, session_id: str):
    """Migrate existing text file history to database"""

    db = ChatDatabase()
    conv_id = db.create_conversation(
        session_id=session_id,
        title="Migrated Conversation"
    )

    with open(text_file) as f:
        for line in f:
            # Parse the line format (customize based on your format)
            if line.startswith('HumanMessage'):
                content = extract_content(line)
                db.add_message(conv_id, 'human', content)
            elif line.startswith('AIMessage'):
                content = extract_content(line)
                db.add_message(conv_id, 'ai', content)

    db.close()
    print(f"Migrated {text_file} to database")
```

---

## Best Practices

### 1. Session ID Management

```python
# Good: Structured session IDs
session_id = f"{user_id}_{channel}_{timestamp}"
session_id = f"support_ticket_{ticket_number}"

# Bad: Random or unclear IDs
session_id = "abc123"
session_id = str(uuid.uuid4())  # Hard to track
```

### 2. Error Handling

```python
def safe_chat_operation(session_id: str, query: str):
    """Example of proper error handling"""
    try:
        with ChatDatabase() as db:
            messages = db.get_conversation_messages(session_id)
            # Process messages
            return process_with_ai(messages, query)
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        # Fallback to in-memory conversation
        return handle_without_history(query)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "I'm having trouble accessing conversation history."
```

### 3. Performance Optimization

```python
# Use indexes for frequent queries
db.cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_messages_timestamp
    ON messages(timestamp)
''')

# Batch operations when possible
messages_to_add = [
    ('human', 'Question 1'),
    ('ai', 'Answer 1'),
    ('human', 'Question 2'),
    ('ai', 'Answer 2')
]

db.cursor.executemany('''
    INSERT INTO messages (conversation_id, role, content)
    VALUES (?, ?, ?)
''', [(conv_id, role, content) for role, content in messages_to_add])
```

### 4. Data Retention

```python
def cleanup_old_conversations(days_to_keep: int = 90):
    """Remove old conversations for GDPR compliance"""

    db = ChatDatabase()
    db.cursor.execute('''
        DELETE FROM conversations
        WHERE created_at < datetime('now', ? || ' days')
    ''', (-days_to_keep,))

    deleted = db.cursor.rowcount
    db.conn.commit()
    db.close()

    print(f"Deleted {deleted} old conversations")
```

### 5. Backup Strategy

```python
import shutil
from datetime import datetime

def backup_database():
    """Create timestamped backup of database"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"backups/chat_history_{timestamp}.db"

    shutil.copy2("chat_history.db", backup_path)
    print(f"Database backed up to {backup_path}")
```

---

## Troubleshooting

### Common Issues

1. **Database Locked Error**
   - Solution: Ensure proper connection closing
   - Use context managers (`with` statement)

2. **Missing Conversations**
   - Check session_id format and consistency
   - Verify conversation was created before adding messages

3. **Performance Issues**
   - Add appropriate indexes
   - Use LIMIT in queries
   - Consider periodic vacuuming: `VACUUM;`

4. **Character Encoding**
   - SQLite handles UTF-8 by default
   - Ensure proper encoding in Python strings

---

## Conclusion

This database-backed chat history system provides a robust, scalable solution for managing conversational AI interactions. Key benefits include:

- **Persistence**: Conversations survive application restarts
- **Searchability**: Find information across all conversations
- **Scalability**: Handle thousands of concurrent conversations
- **Analytics**: Generate insights from conversation data
- **Compliance**: Easy data management for privacy regulations

The system is designed to be easily extended with additional features like user management, conversation branching, or integration with other databases.