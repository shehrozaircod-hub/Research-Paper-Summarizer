"""
Script to populate the chat database with dummy conversation data
Creates realistic customer support conversations
"""

from chat_database import ChatDatabase
from datetime import datetime, timedelta
import random


def create_dummy_conversations():
    """Create various dummy customer support conversations"""

    # Initialize database
    db = ChatDatabase()

    # Define dummy conversation scenarios
    conversations = [
        {
            'session_id': 'session_001',
            'title': 'Order Refund Request',
            'messages': [
                ('human', "I want to request a refund for my order #12345."),
                ('ai', "I'd be happy to help you with your refund request for order #12345. May I ask the reason for the refund?"),
                ('human', "The product arrived damaged. The packaging was torn and the item inside was broken."),
                ('ai', "I'm sorry to hear that your product arrived damaged. I've initiated a refund for order #12345. You should receive the full refund within 3-5 business days. We'll also send you a prepaid return label via email."),
                ('human', "Thank you! Do I need to return the damaged item?"),
                ('ai', "Yes, please use the prepaid label to return the damaged item within 14 days. Once we receive it, your refund will be processed immediately."),
            ]
        },
        {
            'session_id': 'session_002',
            'title': 'Shipping Inquiry',
            'messages': [
                ('human', "Where is my order? It was supposed to arrive yesterday."),
                ('ai', "I understand your concern about the delayed delivery. Could you please provide me with your order number so I can track it for you?"),
                ('human', "The order number is #67890"),
                ('ai', "Thank you! I'm checking the status of order #67890 now. I can see that your package is currently in transit and experienced a slight delay at our distribution center. The updated delivery date is tomorrow by 6 PM."),
                ('human', "Is there a tracking number I can use?"),
                ('ai', "Yes, your tracking number is TRACK123456789. You can use this on our website or the carrier's website to see real-time updates. I've also sent this information to your email."),
            ]
        },
        {
            'session_id': 'session_003',
            'title': 'Product Recommendation',
            'messages': [
                ('human', "I'm looking for a good laptop for programming. What do you recommend?"),
                ('ai', "I'd be happy to help you find the right laptop for programming! To give you the best recommendation, could you tell me your budget range and whether you have any specific requirements (like screen size or operating system preference)?"),
                ('human', "My budget is around $1500, and I prefer something with at least 16GB RAM. Screen size doesn't matter much."),
                ('ai', "Based on your requirements, I recommend the TechPro Developer 15. It comes with 16GB RAM (expandable to 32GB), Intel i7 processor, 512GB SSD, and is priced at $1,399. It's specifically optimized for development work with excellent keyboard and battery life."),
                ('human', "That sounds great! Is it available in stock?"),
                ('ai', "Yes, the TechPro Developer 15 is currently in stock! We have 5 units available for immediate shipping. Would you like me to add it to your cart or would you like to know more about its specifications?"),
                ('human', "Please add it to my cart. Also, do you offer any warranty?"),
                ('ai', "I've added the TechPro Developer 15 to your cart! Yes, it comes with a 1-year manufacturer warranty, and you can extend it to 3 years for an additional $199. The extended warranty covers accidental damage and provides priority support."),
            ]
        },
        {
            'session_id': 'session_004',
            'title': 'Account Issues',
            'messages': [
                ('human', "I can't log into my account. It says my password is incorrect but I'm sure it's right."),
                ('ai', "I'm sorry you're having trouble accessing your account. For security purposes, could you please provide the email address associated with your account?"),
                ('human', "It's john.doe@email.com"),
                ('ai', "Thank you! I can see your account in our system. I'll send a password reset link to john.doe@email.com right away. You should receive it within the next 5 minutes."),
                ('human', "I received the link and reset my password, but it's still not working."),
                ('ai', "Let me investigate this further. I see there might be a cache issue. Could you please try clearing your browser's cookies and cache, or try logging in using an incognito/private browser window?"),
                ('human', "That worked! Thank you so much!"),
                ('ai', "Excellent! I'm glad that resolved the issue. For future reference, if you experience login problems, clearing cache and cookies often helps. Is there anything else I can assist you with today?"),
            ]
        },
        {
            'session_id': 'session_005',
            'title': 'Subscription Cancellation',
            'messages': [
                ('human', "I want to cancel my premium subscription."),
                ('ai', "I understand you'd like to cancel your premium subscription. Before we proceed, may I ask if there's any specific issue or feature you're not satisfied with? Perhaps I can help address it."),
                ('human', "I'm just not using it enough to justify the cost."),
                ('ai', "I completely understand. Would you be interested in our basic plan at $4.99/month instead of canceling entirely? It still gives you access to core features at a lower cost."),
                ('human', "No thanks, I'd prefer to cancel completely for now."),
                ('ai', "No problem at all! I've processed your cancellation request. Your premium subscription will remain active until the end of your current billing period on March 15, 2024. After that, your account will revert to our free tier."),
                ('human', "Will I lose my saved data?"),
                ('ai', "No, you won't lose any data! All your saved information will remain in your account. You can always reactivate your premium subscription later if you change your mind, and everything will be just as you left it."),
            ]
        },
        {
            'session_id': 'session_006',
            'title': 'Technical Support',
            'messages': [
                ('system', "Customer connected from mobile device"),
                ('human', "The app keeps crashing whenever I try to upload a photo."),
                ('ai', "I'm sorry to hear you're experiencing crashes with photo uploads. Let me help you troubleshoot this. First, which device and app version are you using?"),
                ('human', "iPhone 12, and I think the app version is 3.2.1"),
                ('ai', "Thank you! Version 3.2.1 had a known issue with photo uploads. We've fixed this in version 3.2.3. Could you please update your app from the App Store?"),
                ('human', "Updating now... Okay, it's done."),
                ('ai', "Great! Now please try uploading a photo again. Make sure to grant the app permission to access your photos if prompted."),
                ('human', "It works perfectly now! Thanks!"),
                ('ai', "Wonderful! I'm glad the update resolved the issue. The new version also includes improved upload speeds and better image compression. If you experience any other problems, please don't hesitate to reach out!"),
            ]
        },
        {
            'session_id': 'session_007',
            'title': 'Payment Issue',
            'messages': [
                ('human', "My credit card was charged twice for the same order."),
                ('ai', "I apologize for the double charge issue. This must be concerning. Let me look into this immediately. Could you please provide your order number?"),
                ('human', "Order #11111"),
                ('ai', "Thank you. I can see order #11111 in our system for $149.99. I can confirm that there appears to be a duplicate charge. This sometimes happens due to a processing error."),
                ('human', "When will I get my money back?"),
                ('ai', "I've initiated an immediate refund for the duplicate charge of $149.99. Depending on your bank, you should see the credit within 2-5 business days. I've also added a $10 credit to your account for the inconvenience."),
                ('human', "That's very helpful, thank you!"),
                ('ai', "You're welcome! I've also sent a confirmation email with the refund details and reference number REF-2024-0307. If you don't see the refund after 5 business days, please contact us with this reference number."),
            ]
        },
        {
            'session_id': 'session_008',
            'title': 'Product Exchange',
            'messages': [
                ('human', "I ordered a size M shirt but it's too small. Can I exchange it for size L?"),
                ('ai', "Of course! I'd be happy to help you exchange your shirt for a size L. Is the item unused with tags still attached?"),
                ('human', "Yes, I only tried it on once. Tags are still on."),
                ('ai', "Perfect! I've initiated an exchange for you. You'll receive a prepaid shipping label via email within the next hour. Once we receive the size M, we'll immediately ship out the size L."),
                ('human', "How long will the whole process take?"),
                ('ai', "The typical exchange timeline is 7-10 business days from when you ship the item back. However, to expedite this for you, I've upgraded your exchange to priority processing, so you should receive your size L within 5-7 business days."),
                ('human', "That's great, thanks for the fast service!"),
                ('ai', "You're very welcome! I've also noted your size preference in your account to help with future orders. You'll receive tracking information as soon as your new shirt ships."),
            ]
        }
    ]

    # Populate the database
    print("Creating dummy conversations in database...")

    for conv_data in conversations:
        # Create conversation
        conv_id = db.create_conversation(
            session_id=conv_data['session_id'],
            title=conv_data['title'],
            metadata={'source': 'dummy_data', 'created_by': 'populate_script'}
        )

        print(f"Created conversation: {conv_data['title']} (ID: {conv_id})")

        # Add messages with slight time delays to simulate real conversation
        for role, content in conv_data['messages']:
            db.add_message(
                conversation_id=conv_id,
                role=role,
                content=content,
                metadata={'generated': True}
            )

        print(f"  - Added {len(conv_data['messages'])} messages")

    print(f"\nSuccessfully created {len(conversations)} conversations")

    # Display summary
    recent = db.get_recent_conversations(5)
    print("\nMost recent conversations:")
    for conv in recent:
        print(f"  - {conv['session_id']}: {conv['title']}")

    db.close()
    print("\nDatabase populated successfully!")


if __name__ == "__main__":
    create_dummy_conversations()