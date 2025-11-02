"""
Chat History Database Module
Handles storage and retrieval of conversation history using SQLite
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class ChatDatabase:
    """Manages chat history storage in SQLite database"""

    def __init__(self, db_path: str = "chat_history.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        # Conversations table - stores conversation metadata
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT  -- JSON field for additional data
            )
        ''')

        # Messages table - stores individual messages
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('human', 'ai', 'system')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,  -- JSON field for additional message data
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        ''')

        # Create indexes for better query performance
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_messages_conversation
            ON messages(conversation_id)
        ''')

        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversations_session
            ON conversations(session_id)
        ''')

        self.conn.commit()

    def create_conversation(self, session_id: str, title: Optional[str] = None,
                          metadata: Optional[Dict] = None) -> int:
        """Create a new conversation and return its ID"""
        metadata_json = json.dumps(metadata) if metadata else None

        try:
            self.cursor.execute('''
                INSERT INTO conversations (session_id, title, metadata)
                VALUES (?, ?, ?)
            ''', (session_id, title, metadata_json))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Session already exists, return existing conversation ID
            self.cursor.execute('''
                SELECT id FROM conversations WHERE session_id = ?
            ''', (session_id,))
            return self.cursor.fetchone()['id']

    def add_message(self, conversation_id: int, role: str, content: str,
                   metadata: Optional[Dict] = None) -> int:
        """Add a message to a conversation"""
        if role not in ['human', 'ai', 'system']:
            raise ValueError(f"Invalid role: {role}. Must be 'human', 'ai', or 'system'")

        metadata_json = json.dumps(metadata) if metadata else None

        self.cursor.execute('''
            INSERT INTO messages (conversation_id, role, content, metadata)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, role, content, metadata_json))

        # Update conversation's updated_at timestamp
        self.cursor.execute('''
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_conversation_messages(self, session_id: str) -> List[Tuple[str, str]]:
        """Get all messages from a conversation by session ID"""
        self.cursor.execute('''
            SELECT m.role, m.content, m.timestamp
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.session_id = ?
            ORDER BY m.timestamp ASC
        ''', (session_id,))

        messages = []
        for row in self.cursor.fetchall():
            messages.append((row['role'], row['content']))

        return messages

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get most recent conversations"""
        self.cursor.execute('''
            SELECT id, session_id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (limit,))

        conversations = []
        for row in self.cursor.fetchall():
            conversations.append({
                'id': row['id'],
                'session_id': row['session_id'],
                'title': row['title'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })

        return conversations

    def delete_conversation(self, session_id: str):
        """Delete a conversation and all its messages"""
        self.cursor.execute('''
            DELETE FROM conversations WHERE session_id = ?
        ''', (session_id,))
        self.conn.commit()

    def search_messages(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for messages containing the query text"""
        self.cursor.execute('''
            SELECT m.*, c.session_id, c.title
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.content LIKE ?
            ORDER BY m.timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit))

        results = []
        for row in self.cursor.fetchall():
            results.append({
                'session_id': row['session_id'],
                'conversation_title': row['title'],
                'role': row['role'],
                'content': row['content'],
                'timestamp': row['timestamp']
            })

        return results

    def export_conversation(self, session_id: str) -> Dict:
        """Export a conversation in a structured format"""
        # Get conversation metadata
        self.cursor.execute('''
            SELECT * FROM conversations WHERE session_id = ?
        ''', (session_id,))

        conv_row = self.cursor.fetchone()
        if not conv_row:
            return None

        conversation = {
            'session_id': conv_row['session_id'],
            'title': conv_row['title'],
            'created_at': conv_row['created_at'],
            'updated_at': conv_row['updated_at'],
            'messages': []
        }

        # Get all messages
        messages = self.get_conversation_messages(session_id)
        for role, content in messages:
            conversation['messages'].append({
                'role': role,
                'content': content
            })

        return conversation

    def close(self):
        """Close database connection"""
        self.conn.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure connection is closed"""
        self.close()