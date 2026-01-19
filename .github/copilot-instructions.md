# DarkIris Bot - AI Agent Instructions

## Project Overview
**DarkIris** is a Telegram bot with AI reasoning capabilities. It's a **stateful, context-aware conversational agent** that remembers user interactions and adapts responses based on conversation history and execution context.

### Core Architecture
```
User Message (Telegram) → Message Handler → Memory Loader → AI Reasoning → Response + Memory Save
```

The bot operates in three contexts:
- **Private DMs**: Full AI responses with memory integration
- **Group @mention**: Triggered by `@darkiris` or `@iris` name triggers
- **Group keywords**: Auto-responds to commercial keywords (preço, valor, stock, etc.)

## Critical Patterns & Implementation Details

### 1. Memory System (Supabase)
- **Table**: `darkiris_memory` stores (user_id, role, content, created_at)
- **Load pattern**: Always fetch full conversation history before calling OpenRouter
  ```python
  history = load_memory(user_id)  # Returns list of {role, content}
  messages = [{"role": "system", "content": SYSTEM_PROMPT}]
  messages.extend(history)  # Prepend to build full context
  ```
- **Save pattern**: Save both user input AND assistant response separately
  ```python
  save_memory(user_id, "user", user_text)
  save_memory(user_id, "assistant", reply)
  ```
- **Limitation**: Default limit=10 messages per history load (configurable)

### 2. Message Routing Logic
The bot uses **priority-based triggering** in groups:
1. **Reply detection**: Only responds to replies to bot messages
2. **Name triggers**: Regex patterns in `NAME_TRIGGERS` (case-insensitive)
3. **Keyword matching**: Simple substring check against `GROUP_KEYWORDS`

When ANY condition is true in a group, invoke `respond_ai()` with `group_mode=True` to append: `"\n\n🖤 No privado consigo orientar melhor."`

### 3. AI Configuration
- **Provider**: OpenRouter with `openai/gpt-4o-mini` (configurable via `OPENROUTER_MODEL`)
- **Temperature**: 0.6 (balanced creativity/consistency)
- **Max tokens**: 300 (concise responses optimized for Telegram)
- **System prompt**: Located in `SYSTEM_PROMPT` constant—defines "DarkIris" personality (feminine, strategic, discrete)

### 4. Environment Variables
Required:
- `BOT_TOKEN`: Telegram bot token
- `OPENROUTER_API_KEY`: OpenRouter authentication
- `SUPABASE_URL`: Database connection
- `SUPABASE_SERVICE_KEY`: Supabase admin key

Optional:
- `OPENROUTER_MODEL`: Defaults to `openai/gpt-4o-mini`

## Development Workflows

### Local Setup
```bash
pip install -r requirements.txt
# Set .env with required variables
python main.py
```

### Deployment
Automatic via Railway (GitHub webhook). Push to trigger.

### Testing
1. **Private DM testing**: Add bot, message directly, check memory via Supabase dashboard
2. **Group testing**: Add bot to group, use triggers or keywords
3. **Memory verification**: Query `darkiris_memory` table for user_id to validate save/load

## File Structure & Responsibility
- **main.py**: Core bot logic, handlers, memory ops, AI integration
- **menus.py**: Telegram inline keyboard definitions (WIP—currently skeleton)
- **requirements.txt**: Dependencies
- **README.md**: High-level architecture diagram

## Common AI Agent Tasks

### Adding New Features
1. **New handlers**: Add to `Application` in `main()` (e.g., CommandHandler, MessageHandler)
2. **New triggers**: Extend `NAME_TRIGGERS` or `GROUP_KEYWORDS`
3. **Personality tuning**: Modify `SYSTEM_PROMPT` constant
4. **Response logic**: All happens in `respond_ai()` after AI call—modify before `await message.reply_text()`

### Debugging Message Flow
- Check message `chat_type` (private/group/supergroup)
- Verify regex patterns in `NAME_TRIGGERS` case-insensitively
- For groups, confirm bot has message permissions
- Memory issues? Query Supabase directly—check user_id format (string from `message.from_user.id`)

### Modifying AI Behavior
- Adjust `temperature` for consistency (lower) vs. creativity (higher)
- Reduce `max_tokens` if responses are too long for Telegram (280 char limit per message)
- Tweak `SYSTEM_PROMPT` for personality; test with `/start` then private messages

## Dependencies & External Services
- **python-telegram-bot 21.6**: Official Telegram API wrapper
- **OpenRouter**: LLM provider (abstracts multiple models)
- **Supabase**: PostgreSQL + real-time database
- **OpenAI client library**: Used for OpenRouter compatibility
- **python-dotenv**: Environment variable loading (not explicitly imported but required)

## Important Constraints & Gotchas
1. **User ID consistency**: Always convert to string (`str(message.from_user.id)`) for Supabase queries
2. **Group vs. Private**: `group_mode=True` appends recommendation text; private bypasses this
3. **Telegram message limits**: Max 4096 characters per message; 300 tokens may truncate
4. **Memory ordering**: `load_memory()` returns reversed (oldest first) for chat context—always use `reversed()` on raw Supabase data
5. **Missing dependencies**: `supabase` package not in requirements.txt—needs to be added

## Code Conventions
- **Sections**: Marked with `# ========================` dividers (ENV, CLIENTS, CONFIG, MEMORY, HANDLERS, AI CORE, MAIN)
- **Async patterns**: All handlers are `async`; use `await` for all I/O
- **Naming**: snake_case for functions/vars; SCREAMING_SNAKE_CASE for constants
- **Comments**: Sparse; code is self-documenting. Add only for non-obvious logic.
