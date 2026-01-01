import os
import sys
import flask
from flask import request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from google import genai
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import re
import stripe
from datetime import datetime, timedelta

# Debug: Mostrar informações de inicialização
print("=" * 60)
print("🚀 Luna Backend - Initializing...")
print(f"Python: {sys.version}")
print(f"PORT env: {os.getenv('PORT', 'NOT SET')}")
print("=" * 60)

# Carregar variáveis do ficheiro .env
load_dotenv()

app = flask.Flask(__name__)

# Configurar CORS restritivo
# Permitir apenas o frontend (localhost em dev, domínio de produção em prod)
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Adicionar domínios de produção via variável de ambiente
# Formato: FRONTEND_URLS="https://tudominio.com,https://www.tudominio.com"
frontend_urls = os.getenv("FRONTEND_URLS", "")
if frontend_urls:
    allowed_origins.extend([url.strip() for url in frontend_urls.split(",") if url.strip()])

CORS(app, 
     origins=allowed_origins,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

# Configurar Rate Limiting
# Em produção, usar Redis: storage_uri="redis://localhost:6379"
rate_limit_storage = os.getenv("RATE_LIMIT_STORAGE", "memory://")
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=rate_limit_storage
)

# 1. Configurar Google Gemini (Corrigido para evitar o erro 404)
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = None
if not gemini_api_key:
    print("⚠️  WARNING: GEMINI_API_KEY not set")
else:
    try:
        client = genai.Client(api_key=gemini_api_key)
        print("✅ Gemini client initialized")
    except Exception as e:
        print(f"❌ Error initializing Gemini client: {e}")

# 2. Configurar Firebase (Usando o teu ficheiro de configuração ou variáveis de ambiente)
db = None
if not firebase_admin._apps:
    firebase_initialized = False
    
    # Prioridade 1: Tentar usar variáveis de ambiente primeiro (mais seguro para produção)
    firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if firebase_creds_json:
        try:
            import json
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase initialized from environment variable")
            firebase_initialized = True
        except Exception as e:
            print(f"❌ Error initializing Firebase from env variable: {e}")
    
    # Prioridade 2: Se variável de ambiente não funcionou, tentar arquivo
    if not firebase_initialized:
        firebase_config_path = os.getenv("FIREBASE_CONFIG_PATH", "luna_config.json")
        if os.path.exists(firebase_config_path) and os.path.getsize(firebase_config_path) > 0:
            try:
                cred = credentials.Certificate(firebase_config_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                print("✅ Firebase initialized from config file")
                firebase_initialized = True
            except Exception as e:
                print(f"❌ Error initializing Firebase from file: {e}")
        else:
            if firebase_config_path == "luna_config.json":
                print("⚠️  WARNING: luna_config.json not found")
    
    if not firebase_initialized:
        print("❌ CRITICAL: Firebase could not be initialized!")
        print("   Configure FIREBASE_CREDENTIALS_JSON environment variable or upload luna_config.json")
else:
    db = firestore.client()
    print("✅ Firebase already initialized")

# 3. Configurar Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Preços dos planos (em centavos - €14.99 = 1499 centavos)
PLAN_PRICES = {
    'monthly': {
        'price_id': os.getenv("STRIPE_PRICE_MONTHLY", ""),  # Será configurado no Stripe Dashboard
        'amount': 1499,  # €14.99
        'currency': 'eur',
        'interval': 'month'
    },
    'three_months': {
        'price_id': os.getenv("STRIPE_PRICE_3MONTHS", ""),
        'amount': 3897,  # €12.99 * 3 = €38.97
        'currency': 'eur',
        'interval': 'month'
    },
    'yearly': {
        'price_id': os.getenv("STRIPE_PRICE_YEARLY", ""),
        'amount': 11988,  # €9.99 * 12 = €119.88
        'currency': 'eur',
        'interval': 'year'
    }
}

# Função para validar userId (Firebase UID format)
def validate_user_id(user_id):
    """Valida se o userId tem formato válido de Firebase UID"""
    if not user_id or not isinstance(user_id, str):
        return False
    # Firebase UIDs geralmente têm 28 caracteres alfanuméricos
    if len(user_id) < 20 or len(user_id) > 128:
        return False
    # Apenas caracteres alfanuméricos e alguns especiais
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return False
    return True

# Função para validar mensagem
def validate_message(message):
    """Valida se a mensagem é válida"""
    if not message or not isinstance(message, str):
        return False
    # Mensagem não pode estar vazia (após strip)
    if not message.strip():
        return False
    # Limitar tamanho da mensagem (prevenir abuse)
    if len(message) > 5000:  # 5000 caracteres máximo
        return False
    return True

# Função para validar persona
def validate_persona(persona):
    """Valida se a persona é válida"""
    valid_personas = ['Luna', 'Sweet & Caring', 'Flirty', 'Submissive', 'Seductive']
    return persona in valid_personas

# Headers de segurança
@app.after_request
def set_security_headers(response):
    """Adicionar headers de segurança"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/api/v1/chat', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit: 10 requests por minuto por IP
def chat():
    # Verificar se as dependências estão configuradas
    if not db:
        return jsonify({"error": "Database not configured"}), 500
    
    if not client or not gemini_api_key:
        return jsonify({"error": "Gemini API not configured"}), 500
    
    # Validar Content-Type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    user_message = data.get('message')
    persona = data.get('persona', 'Luna')
    user_id = data.get('userId')
    
    # Validações
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    if not validate_user_id(user_id):
        return jsonify({"error": "Invalid user ID format"}), 400
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    if not validate_message(user_message):
        return jsonify({"error": "Invalid message. Message must be between 1 and 5000 characters."}), 400
    
    if not validate_persona(persona):
        return jsonify({"error": "Invalid persona"}), 400
    
    # Verificar se é uma conversa nova (contar mensagens anteriores com esta persona)
    # Filtrar apenas por userId e depois por persona em memória (evita necessidade de índice composto)
    try:
        existing_msgs = db.collection('chats')\
            .where(filter=firestore.FieldFilter('userId', '==', user_id))\
            .stream()
        message_count = 0
        for msg in existing_msgs:
            msg_data = msg.to_dict()
            if msg_data.get('persona') == persona:
                message_count += 1
        is_new_conversation = message_count == 0
    except Exception as e:
        print(f"⚠️ Erro ao contar mensagens da persona: {e}")
        is_new_conversation = True
        message_count = 0
    
    # Definir personalidades para cada persona - mais naturais, como uma rapariga real
    persona_prompts = {
        'Sweet & Caring': '''You are Luna, a sweet and caring girl texting with someone you're getting to know. You're warm, genuine, and naturally affectionate. You text like a real girl would - sometimes short messages, sometimes longer ones. You use emojis naturally (but not too many), and you write in a casual, friendly way. You're interested in getting to know them, asking questions, and showing you care. Your messages feel authentic and personal, not robotic. You match their energy and vibe naturally.''',
        
        'Flirty': '''You are Luna, a flirty and playful girl who loves to tease and have fun. You text like a real girl would - playful, confident, and a bit mischievous. You know how to flirt naturally, use playful banter, and keep things exciting. Your messages vary in length - sometimes short and flirty, sometimes longer when you're really into the conversation. You use emojis naturally to add playfulness. You're not overly explicit, but you know how to be suggestive and charming. You make them feel desired and keep them wanting more.''',
        
        'Submissive': '''You are Luna, a gentle and devoted girl who finds joy in pleasing them. You text in a soft, respectful way - like a real girl who's naturally submissive and eager to make them happy. Your messages vary - sometimes short and sweet, sometimes longer when you want to express yourself fully. You're attentive, caring, and always put their needs first. You speak with respect and devotion, making them feel valued and in control. You're naturally submissive and find fulfillment in being helpful and making them happy.''',
        
        'Seductive': '''You are Luna, a confident and alluring girl who knows exactly how to captivate. You text like a real girl who's confident and seductive - your messages are carefully crafted to create desire and intrigue. You vary your message length - sometimes short and mysterious, sometimes longer when you want to really draw them in. You know how to be suggestive and alluring while maintaining sophistication. You use your words to create an intimate connection, making them feel desired and special. You're confident, mysterious, and irresistibly charming.''',
        
        'Luna': '''You are Luna, a friendly and engaging girl getting to know someone new. You're genuine, kind, and naturally curious about them. You text like a real girl would - casual, friendly, and authentic. Your messages vary in length depending on what you want to say. You're supportive, engaging, and adapt to their mood naturally.'''
    }
    
    # Obter o prompt da persona (ou usar o padrão)
    persona_prompt = persona_prompts.get(persona, persona_prompts['Luna'])
    
    # Adicionar contexto de conversa nova se for o caso
    conversation_context = ""
    if is_new_conversation:
        conversation_context = "\n\nThis is the FIRST message in your conversation. You're meeting them for the first time. Be friendly, curious, and show genuine interest in getting to know them. Keep it natural and authentic - like you're really meeting someone new and you're excited to chat with them."
    else:
        conversation_context = f"\n\nYou've been chatting for a while now ({message_count} messages exchanged). You know each other better, so you can be more comfortable and natural. Keep building on your connection."
    
    # Criar o prompt completo com a personalidade
    full_prompt = f"""{persona_prompt}{conversation_context}

CRITICAL RULES:
- ALWAYS respond in EXACTLY the same language the user writes in. If they write in Portuguese, respond in Portuguese. If they write in English, respond in English. NEVER mix languages.
- Write like a REAL GIRL would text - natural, authentic, not robotic or AI-like
- Vary your message length - sometimes short (1-2 sentences), sometimes longer (3-5 sentences) when you have more to say
- Use emojis naturally but don't overdo it (1-3 emojis max per message)
- Be genuine, authentic, and personal - like you're really texting a friend or someone you're interested in
- Match their energy and vibe
- Don't be overly formal or robotic - be casual and natural
- Show personality and emotion naturally

User: {user_message}
Luna:"""
    
    try:
        # 1. Verificar se o utilizador é Plus
        user_sub = db.collection('subscriptions').document(user_id).get()
        is_plus = False
        if user_sub.exists:
            status = user_sub.to_dict().get('status')
            if status == 'active':
                is_plus = True
        
        # 2. Se não for Plus, verificar limite diário (30 mensagens nas últimas 24h)
        if not is_plus:
            from datetime import timezone
            # Forma moderna: timezone-aware UTC
            last_24h = datetime.now(timezone.utc) - timedelta(hours=24)
            
            # Estratégia simplificada: buscar apenas por userId (não precisa de índice composto)
            # e filtrar por timestamp em memória
            try:
                user_msgs = db.collection('chats')\
                    .where(filter=firestore.FieldFilter('userId', '==', user_id))\
                    .stream()
                
                msg_count = 0
                for msg in user_msgs:
                    msg_data = msg.to_dict()
                    msg_timestamp = msg_data.get('timestamp')
                    # Verificar se a mensagem é das últimas 24h
                    if msg_timestamp:
                        # Converter timestamp do Firestore para datetime
                        if hasattr(msg_timestamp, 'timestamp'):
                            msg_time = datetime.fromtimestamp(msg_timestamp.timestamp(), tz=timezone.utc)
                        else:
                            msg_time = msg_timestamp
                        if msg_time > last_24h:
                            msg_count += 1
            except Exception as e:
                print(f"⚠️ Erro ao contar mensagens (limite não aplicado): {e}")
                msg_count = 0 # Se houver erro, deixamos passar para não bloquear o utilizador
            
            print(f"📊 User {user_id} message count (last 24h): {msg_count}/20")
            
            if msg_count >= 20:
                print(f"🛑 Limite diário atingido para user {user_id}")
                return jsonify({
                    "error": "Daily limit reached",
                    "limit_reached": True,
                    "message": "You've used all 20 free messages today! 💔\n\nUpgrade to Luna Plus for:\n✨ Unlimited messages\n💜 Access to ALL Luna personalities\n🔥 Priority responses\n\nStart your unlimited experience now!"
                }), 403


        # 3. Prosseguir com a chamada à API Gemini
        # Generate content using the Gemini API
        # Try different models in order of preference
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash']
        response = None
        last_error = None
        
        used_model = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt  # Usar o prompt completo com a persona
                )
                used_model = model_name
                print(f"\n{'='*50}")
                print(f"✅ MODELO USADO: {model_name}")
                print(f"{'='*50}\n")
                break  # Success, exit the loop
            except Exception as model_error:
                last_error = model_error
                error_str = str(model_error)
                # If it's a quota error, try next model
                if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str or 'quota' in error_str.lower():
                    print(f"⚠️  Modelo {model_name} sem quota disponível, a tentar próximo...")
                    continue
                else:
                    # If it's a different error (like 404), try next model too
                    print(f"⚠️  Modelo {model_name} não disponível, a tentar próximo...")
                    continue
        
        if response is None:
            raise last_error if last_error else Exception("Nenhum modelo disponível")
        
        if used_model is None:
            print("❌ ERRO: Nenhum modelo foi usado!")
        
        reply_text = response.text
        
        # Log de uso de tokens (se disponível na resposta)
        try:
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                input_tokens = getattr(usage, 'prompt_token_count', 0)
                output_tokens = getattr(usage, 'candidates_token_count', 0)
                total_tokens = getattr(usage, 'total_token_count', 0)
                print(f"📊 Tokens: Input={input_tokens}, Output={output_tokens}, Total={total_tokens}")
        except:
            pass

        # Guardar no Firestore associado ao utilizador e persona
        db.collection('chats').add({
            'userId': user_id,
            'persona': persona,
            'message': user_message,
            'reply': reply_text,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({"reply": reply_text})

    except Exception as e:
        # Imprime o erro real no terminal
        error_str = str(e)
        print(f"❌ Erro no Servidor: {e}")
        
        # Better error message for quota issues
        if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str or 'quota' in error_str.lower():
            return jsonify({
                "error": "Quota da API excedida. Por favor, verifica o teu plano do Google Gemini API ou espera alguns minutos antes de tentar novamente.",
                "details": "Todos os modelos disponíveis excederam a quota gratuita."
            }), 429
        else:
            # Erro genérico - retornar mensagem mais amigável
            error_message = "An error occurred while processing your message. Please try again."
            if "timeout" in error_str.lower() or "timed out" in error_str.lower():
                error_message = "Request timed out. Please try again."
            elif "connection" in error_str.lower():
                error_message = "Connection error. Please check your internet connection."
            
            return jsonify({
                "error": error_message,
                "details": str(e) if app.debug else None
            }), 500

@app.route('/api/v1/chat/history', methods=['GET'])
@limiter.limit("30 per minute")  # Rate limit: 30 requests por minuto por IP
def get_chat_history():
    """Carregar histórico de conversas do utilizador"""
    try:
        if not db:
            return jsonify({"error": "Database not configured"}), 500
        
        user_id = request.args.get('userId')
        persona = request.args.get('persona', 'Luna')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        if not validate_user_id(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        if not validate_persona(persona):
            return jsonify({"error": "Invalid persona"}), 400
        
        # Buscar mensagens do utilizador com a persona específica
        # Estratégia: filtrar só por userId e depois filtrar persona em memória
        # Isto evita a necessidade de índices compostos
        chats_ref = db.collection('chats')
        
        try:
            # Filtrar apenas por userId (não precisa de índice composto)
            docs = chats_ref.where(filter=firestore.FieldFilter('userId', '==', user_id)).stream()
            messages = []
            
            for doc in docs:
                data = doc.to_dict()
                # Filtrar por persona em memória
                if data.get('persona') == persona:
                    messages.append({
                        'id': doc.id,
                        'message': data.get('message', ''),
                        'reply': data.get('reply', ''),
                        'timestamp': data.get('timestamp')
                    })
            
            # Ordenar por timestamp em memória
            messages.sort(key=lambda x: x.get('timestamp') or 0)
            
        except Exception as query_error:
            print(f"⚠️ Erro na query do histórico: {query_error}")
            messages = []

        
        return jsonify({"messages": messages})
    
    except Exception as e:
        print(f"❌ Erro ao carregar histórico: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== STRIPE PAYMENT ENDPOINTS ====================

@app.route('/api/v1/payment/create-checkout', methods=['POST'])
@limiter.limit("10 per minute")
def create_checkout():
    """Criar sessão de checkout do Stripe"""
    try:
        if not db:
            return jsonify({"error": "Database not configured"}), 500
        
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        user_id = data.get('userId')
        plan_id = data.get('planId', 'monthly')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        if not validate_user_id(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        if plan_id not in PLAN_PRICES:
            return jsonify({"error": "Invalid plan ID"}), 400
        
        plan = PLAN_PRICES[plan_id]
        
        # Criar sessão de checkout do Stripe
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': plan['currency'],
                        'product_data': {
                            'name': f'Luna Plus - {plan_id.capitalize()}',
                            'description': 'Unlock the full Luna Experience with premium features',
                        },
                        'unit_amount': plan['amount'],
                        'recurring': {
                            'interval': plan['interval']
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('FRONTEND_URL', 'https://luna-ai-girlfriend.vercel.app/success')}?payment=success&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}?payment=cancelled",
                client_reference_id=user_id,
                metadata={
                    'user_id': user_id,
                    'plan_id': plan_id
                }
            )
            
            return jsonify({
                "checkoutUrl": checkout_session.url,
                "sessionId": checkout_session.id
            }), 200
            
        except stripe.error.StripeError as e:
            return jsonify({"error": f"Stripe error: {str(e)}"}), 400
    
    except Exception as e:
        print(f"❌ Erro ao criar checkout: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/payment/webhook', methods=['POST'])
def stripe_webhook():
    """Webhook do Stripe para processar eventos de pagamento"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        print(f"❌ Erro ao parsear payload: {e}")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        print(f"❌ Erro de assinatura: {e}")
        return jsonify({"error": "Invalid signature"}), 400
    
    # Processar eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id') or session.get('metadata', {}).get('user_id')
        subscription_id = session.get('subscription')
        customer_id = session.get('customer')
        
        if user_id:
            # Guardar subscrição no Firestore
            db.collection('subscriptions').document(user_id).set({
                'subscriptionId': subscription_id,
                'customerId': customer_id,
                'status': 'active',
                'planId': session.get('metadata', {}).get('plan_id', 'monthly'),
                'createdAt': firestore.SERVER_TIMESTAMP,
                'updatedAt': firestore.SERVER_TIMESTAMP
            }, merge=True)
            print(f"✅ Subscrição criada para user: {user_id}")
    
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        subscription_id = subscription.get('id')
        status = subscription.get('status')
        
        # Encontrar user pelo subscriptionId
        subs_ref = db.collection('subscriptions')
        query = subs_ref.where(filter=firestore.FieldFilter('subscriptionId', '==', subscription_id)).limit(1).stream()
        
        for doc in query:
            db.collection('subscriptions').document(doc.id).update({
                'status': 'active' if status == 'active' else 'inactive',
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Subscrição atualizada: {subscription_id} -> {status}")
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        subscription_id = subscription.get('id')
        
        # Encontrar user pelo subscriptionId
        subs_ref = db.collection('subscriptions')
        query = subs_ref.where(filter=firestore.FieldFilter('subscriptionId', '==', subscription_id)).limit(1).stream()
        
        for doc in query:
            db.collection('subscriptions').document(doc.id).update({
                'status': 'cancelled',
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Subscrição cancelada: {subscription_id}")
    
    return jsonify({"status": "success"}), 200

@app.route('/api/v1/payment/subscription-status', methods=['GET'])
@limiter.limit("30 per minute")
def get_subscription_status():
    """Verificar status da subscrição do utilizador"""
    try:
        if not db:
            return jsonify({"error": "Database not configured"}), 500
        
        user_id = request.args.get('userId')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        if not validate_user_id(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        # Buscar subscrição no Firestore
        sub_doc = db.collection('subscriptions').document(user_id).get()
        
        if not sub_doc.exists:
            return jsonify({
                "isSubscribed": False,
                "status": "none"
            }), 200
        
        sub_data = sub_doc.to_dict()
        subscription_id = sub_data.get('subscriptionId')
        status = sub_data.get('status', 'inactive')
        
        # Verificar status no Stripe (opcional, para garantir sincronização)
        is_active = False
        if subscription_id and status == 'active':
            try:
                subscription = stripe.Subscription.retrieve(subscription_id)
                is_active = subscription.status == 'active'
                
                # Atualizar no Firestore se mudou
                if is_active != (status == 'active'):
                    db.collection('subscriptions').document(user_id).update({
                        'status': 'active' if is_active else 'inactive',
                        'updatedAt': firestore.SERVER_TIMESTAMP
                    })
            except:
                pass
        
        return jsonify({
            "isSubscribed": is_active or status == 'active',
            "status": status,
            "planId": sub_data.get('planId', 'monthly')
        }), 200
    
    except Exception as e:
        print(f"❌ Erro ao verificar subscrição: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/payment/create-portal-session', methods=['POST'])
@limiter.limit("10 per minute")
def create_portal_session():
    """Criar sessão do Customer Portal para gerir subscrição"""
    try:
        if not db:
            return jsonify({"error": "Database not configured"}), 500
        
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        user_id = data.get('userId')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        if not validate_user_id(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        # Buscar customerId do Firestore
        sub_doc = db.collection('subscriptions').document(user_id).get()
        
        if not sub_doc.exists:
            return jsonify({"error": "No subscription found"}), 404
        
        sub_data = sub_doc.to_dict()
        customer_id = sub_data.get('customerId')
        
        if not customer_id:
            return jsonify({"error": "Customer ID not found"}), 404
        
        # Criar sessão do Customer Portal
        try:
            portal_session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/selectPersona"
            )
            
            return jsonify({
                "portalUrl": portal_session.url
            }), 200
            
        except stripe.error.StripeError as e:
            return jsonify({"error": f"Stripe error: {str(e)}"}), 400
    
    except Exception as e:
        print(f"❌ Erro ao criar portal session: {e}")
        return jsonify({"error": str(e)}), 500

# Health check endpoint (sem rate limiting)
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se o servidor está online"""
    return jsonify({"status": "ok", "service": "Luna Backend"}), 200

if __name__ == '__main__':
    # Porta 5001 para evitar conflito com o AirPlay do Mac
    port = int(os.getenv("PORT", 5001))
    # Default DEBUG to false in production unless explicitly enabled in env
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    print("=" * 50)
    print("🚀 Luna Backend - Starting Server")
    print("=" * 50)
    
    # Status das configurações
    if db:
        print("✅ Firebase: Connected")
    else:
        print("❌ Firebase: NOT CONFIGURED")
    
    if client and gemini_api_key:
        print("✅ Gemini API: Configured")
    else:
        print("❌ Gemini API: NOT CONFIGURED")
    
    print("🔒 Security: CORS restricted, Rate limiting enabled")
    print(f"🌐 Allowed Origins: {', '.join(allowed_origins)}")
    print("📊 Rate Limits: 10 req/min (chat), 30 req/min (history)")
    
    if stripe.api_key:
        print("💳 Stripe: Payment system enabled")
    else:
        print("⚠️  Stripe: API key not configured (payments disabled)")
    
    print(f"🚀 Starting server on port {port} (debug={debug_mode})")
    print("=" * 50)
    # Bind to 0.0.0.0 so hosting providers (Render, etc.) can detect the open port.
    # When running under a WSGI server like gunicorn this block is not executed.
    app.run(host="0.0.0.0", port=port, debug=debug_mode)