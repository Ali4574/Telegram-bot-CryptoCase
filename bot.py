from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import re

# Define states - expanded to match PDF questions
(NAME, EMAIL, PHONE, LOCATION, INCIDENT_TYPE, INCIDENT_DESCRIPTION, 
 EXCHANGE, CRYPTO_TYPE, NETWORK, NETWORK_OTHER, WALLET_ADDRESSES, DATE_TIME, 
 AMOUNT_LOST, HOW_OCCURRED, HOW_OCCURRED_OTHER, PROOF_OWNERSHIP, TRANSACTION_IDS, 
 EVIDENCE, POLICE_REPORT, OTHER_SERVICES, ADDITIONAL_INFO) = range(21)

def is_valid_email(email):
    """Check if email is valid using regex pattern"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask for name."""
    keyboard = [['Start Recovery Process']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "🛡 Welcome to Crypto Recovery Desk! 🚀\n\n"
        "We specialize in tracing, investigating, and recovering stolen or lost cryptocurrencies.\n\n"
        "Before we can assist you, we need to gather detailed information about your case.\n"
        "All information is kept strictly confidential and used only for investigation purposes.\n\n"
        "Press 'Start Recovery Process' to begin, or use /cancel at any time to stop.",
        reply_markup=reply_markup
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store name and ask for email."""
    if update.message.text == 'Start Recovery Process':
        await update.message.reply_text(
            "📋 Section A – Basic Contact Information\n\n"
            "1. Please enter your Full Name (for official records):",
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME
    
    if len(update.message.text) < 3:
        await update.message.reply_text(
            "⚠️ Please enter a valid name (at least 3 characters long).\n"
            "What is your full name?"
        )
        return NAME
    
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "2. Please enter your Email Address (for investigation updates):\n"
        "Make sure to enter a valid email address where we can contact you."
    )
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate email and ask for phone."""
    email = update.message.text
    
    if not is_valid_email(email):
        await update.message.reply_text(
            "⚠️ Please enter a valid email address.\n"
            "For example: name@example.com"
        )
        return EMAIL
    
    context.user_data["email"] = email
    await update.message.reply_text(
        "3. Please enter your Phone / WhatsApp number (optional):\n"
        "You can type 'Skip' if you don't want to provide this."
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store phone and ask for location."""
    if update.message.text.lower() == 'skip':
        context.user_data["phone"] = "Not provided"
    else:
        context.user_data["phone"] = update.message.text
    
    await update.message.reply_text(
        "4. Please enter your Location / Country:\n"
        "This helps determine jurisdiction & applicable laws."
    )
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store location and ask for incident type."""
    context.user_data["location"] = update.message.text
    
    keyboard = [
        ['Scam', 'Hacked Wallet'],
        ['Fraudulent Investment', 'Lost Access'],
        ['Other']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📋 Section B – Incident Overview\n\n"
        "5. What happened? Please choose one:",
        reply_markup=reply_markup
    )
    return INCIDENT_TYPE

async def get_incident_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store incident type and ask for description."""
    context.user_data["incident_type"] = update.message.text
    
    await update.message.reply_text(
        "6. Please briefly describe the incident in your own words:",
        reply_markup=ReplyKeyboardRemove()
    )
    return INCIDENT_DESCRIPTION

async def get_incident_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store description and ask for exchange."""
    context.user_data["incident_description"] = update.message.text
    
    await update.message.reply_text(
        "📋 Section C – Case Details\n\n"
        "7. Exchange or Platform Name (if applicable):\n"
        "Enter the name or type 'N/A' if not applicable."
    )
    return EXCHANGE

async def get_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store exchange and ask for crypto type."""
    context.user_data["exchange"] = update.message.text
    
    await update.message.reply_text(
        "8. Type of Cryptocurrency involved:\n"
        "For example: USDT, BTC, ETH, etc."
    )
    return CRYPTO_TYPE

async def get_crypto_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store crypto type and ask for network."""
    context.user_data["crypto_type"] = update.message.text
    
    keyboard = [
        ['Ethereum', 'TRON'],
        ['Binance Smart Chain', 'Bitcoin'],
        ['Polygon', 'Avalanche'],
        ['Other']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "9. Network / Blockchain:",
        reply_markup=reply_markup
    )
    return NETWORK

async def get_network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store network and ask for wallet addresses."""
    if update.message.text == 'Other':
        await update.message.reply_text(
            "Please specify the Network / Blockchain:",
            reply_markup=ReplyKeyboardRemove()
        )
        return NETWORK_OTHER
    
    context.user_data["network"] = update.message.text
    
    await update.message.reply_text(
        "10. Wallet Address(es) involved:\n"
        "Please provide your wallet address and the suspected scammer/hacker's address if known.\n"
        "Separate multiple addresses with new lines."
    )
    return WALLET_ADDRESSES

async def get_network_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store custom network and ask for wallet addresses."""
    context.user_data["network"] = update.message.text
    
    await update.message.reply_text(
        "10. Wallet Address(es) involved:\n"
        "Please provide your wallet address and the suspected scammer/hacker's address if known.\n"
        "Separate multiple addresses with new lines."
    )
    return WALLET_ADDRESSES

async def get_wallet_addresses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store wallet addresses and ask for date/time."""
    context.user_data["wallet_addresses"] = update.message.text
    
    await update.message.reply_text(
        "11. Date & Time of Incident:\n"
        "Please provide the approximate date and time when the incident occurred."
    )
    return DATE_TIME

async def get_date_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store date/time and ask for amount lost."""
    context.user_data["date_time"] = update.message.text
    
    await update.message.reply_text(
        "12. Total Amount Lost:\n"
        "Please specify both in crypto amount and approximate USD value."
    )
    return AMOUNT_LOST

async def get_amount_lost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store amount and ask how loss occurred."""
    context.user_data["amount_lost"] = update.message.text
    
    keyboard = [
        ['Phishing link', 'Fake investment platform'],
        ['Rug pull', 'Fake wallet app'],
        ['Social engineering', 'Unauthorized transfer'],
        ['Other']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "13. How did the loss occur?",
        reply_markup=reply_markup
    )
    return HOW_OCCURRED

async def get_how_occurred(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store how loss occurred and ask about proof of ownership."""
    if update.message.text == 'Other':
        await update.message.reply_text(
            "Please specify how the loss occurred:",
            reply_markup=ReplyKeyboardRemove()
        )
        return HOW_OCCURRED_OTHER
    
    context.user_data["how_occurred"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📋 Section D – Evidence & Proof\n\n"
        "14. Do you have proof of ownership of the assets?",
        reply_markup=reply_markup
    )
    return PROOF_OWNERSHIP

async def get_how_occurred_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store custom how occurred and ask about proof of ownership."""
    context.user_data["how_occurred"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📋 Section D – Evidence & Proof\n\n"
        "14. Do you have proof of ownership of the assets?",
        reply_markup=reply_markup
    )
    return PROOF_OWNERSHIP

async def get_proof_ownership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store proof ownership and ask about transaction IDs."""
    context.user_data["proof_ownership"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "15. Do you have transaction IDs (TXIDs) from the blockchain?",
        reply_markup=reply_markup
    )
    return TRANSACTION_IDS

async def get_transaction_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store transaction IDs and ask about evidence."""
    context.user_data["transaction_ids"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "16. Do you have chat screenshots, emails, or scammer contact details?",
        reply_markup=reply_markup
    )
    return EVIDENCE

async def get_evidence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store evidence and ask about police report."""
    context.user_data["evidence"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📋 Section E – Additional Information\n\n"
        "17. Have you reported the case to local police or cybercrime authorities?\n"
        "If yes, please mention the case reference number in the next question.",
        reply_markup=reply_markup
    )
    return POLICE_REPORT

async def get_police_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store police report info and ask about other services."""
    context.user_data["police_report"] = update.message.text
    
    keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "18. Have you tried any other recovery services?",
        reply_markup=reply_markup
    )
    return OTHER_SERVICES

async def get_other_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store other services info and ask for additional details."""
    context.user_data["other_services"] = update.message.text
    
    await update.message.reply_text(
        "19. Any additional details you believe are important?\n"
        "Please provide any other relevant information that might help with your case.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ADDITIONAL_INFO

async def get_additional_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store additional info and send complete case to admin."""
    context.user_data["additional_info"] = update.message.text

    # Send comprehensive data to admin (replace with your Telegram user ID)
    admin_id = 1227132183
    user_data = context.user_data
    
    message = (
        f"🚨 NEW CRYPTO RECOVERY CASE SUBMISSION 🚨\n\n"
        f"📋 SECTION A - BASIC CONTACT INFORMATION:\n"
        f"👤 Name: {user_data['name']}\n"
        f"📧 Email: {user_data['email']}\n"
        f"📱 Phone: {user_data['phone']}\n"
        f"🌍 Location: {user_data['location']}\n\n"
        
        f"📋 SECTION B - INCIDENT OVERVIEW:\n"
        f"🔍 Incident Type: {user_data['incident_type']}\n"
        f"📝 Description: {user_data['incident_description']}\n\n"
        
        f"📋 SECTION C - CASE DETAILS:\n"
        f"🏦 Exchange/Platform: {user_data['exchange']}\n"
        f"💰 Crypto Type: {user_data['crypto_type']}\n"
        f"🔗 Network: {user_data['network']}\n"
        f"🔑 Wallet Addresses: {user_data['wallet_addresses']}\n"
        f"📅 Date/Time: {user_data['date_time']}\n"
        f"💸 Amount Lost: {user_data['amount_lost']}\n"
        f"❓ How Occurred: {user_data['how_occurred']}\n\n"
    )
    
    # Send first part
    await context.bot.send_message(chat_id=admin_id, text=message)
    
    # Send second part with evidence info
    evidence_message = (
        f"📋 SECTION D - EVIDENCE & PROOF:\n"
        f"📄 Proof of Ownership: {user_data['proof_ownership']}\n"
        f"🔍 Transaction IDs: {user_data['transaction_ids']}\n"
        f"🗂 Evidence Available: {user_data['evidence']}\n\n"
        
        f"📋 SECTION E - ADDITIONAL INFO:\n"
        f"🚔 Police Report: {user_data['police_report']}\n"
        f"🔄 Other Services: {user_data['other_services']}\n"
        f"ℹ️ Additional Details: {user_data['additional_info']}\n\n"
        f"⚠️ MINIMUM CLAIM: USD $1,000+"
    )
    
    await context.bot.send_message(chat_id=admin_id, text=evidence_message)

    keyboard = [['Start New Case']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "✅ Thank you for providing the details!\n\n"
        "Our investigation team will review your case and get in touch via email/Telegram.\n\n"
        "📅 Please note: This process is strictly confidential and reviewed manually by our specialists.\n"
        "We aim to respond within 24–48 hours.\n\n"
        "💼 Important: Minimum claim size is USD $1,000 and above.\n\n"
        "You can start a new case by pressing 'Start New Case' or using /start command.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation."""
    keyboard = [['Start New Case']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "❌ Process cancelled.\n"
        "You can start a new case anytime by pressing 'Start New Case' or using /start command.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Timeout handler."""
    keyboard = [['Start New Case']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "⏰ Session timed out due to inactivity.\n"
        "You can start a new case anytime by pressing 'Start New Case' or using /start command.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

def main():
    """Run the bot."""
    # Replace with your bot token
    app = ApplicationBuilder().token("7551799880:AAFYztXvznFoUDGof1mlmtU_4Nc5nMqVSoc").build()

    # Add conversation handler with all new states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex('^Start New Case$'), start)
        ],
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
            ],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            INCIDENT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_incident_type)],
            INCIDENT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_incident_description)],
            EXCHANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_exchange)],
            CRYPTO_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_crypto_type)],
            NETWORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_network)],
            NETWORK_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_network_other)],
            WALLET_ADDRESSES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_wallet_addresses)],
            DATE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date_time)],
            AMOUNT_LOST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount_lost)],
            HOW_OCCURRED: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_how_occurred)],
            HOW_OCCURRED_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_how_occurred_other)],
            PROOF_OWNERSHIP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_proof_ownership)],
            TRANSACTION_IDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transaction_ids)],
            EVIDENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_evidence)],
            POLICE_REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_police_report)],
            OTHER_SERVICES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_other_services)],
            ADDITIONAL_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_additional_info)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.Regex('^Start New Case$'), start)
        ],
        conversation_timeout=600  # Extended timeout to 10 minutes due to more questions
    )

    app.add_handler(conv_handler)
    
    # Start the bot
    print("🚀 Enhanced Crypto Recovery Bot is running...")
    print("📋 Now collecting comprehensive case details as per PDF requirements")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()