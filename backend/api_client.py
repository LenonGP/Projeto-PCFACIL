
import google.generativeai as genai
import json

# CONFIGURAÇÃO DA API GEMINI


GEMINI_API_KEY = "insira_sua_chave_aqui "


def montar_prompt_para_ia(diagnosticos):
    """
    Cria a instrução (prompt) que será enviada para a IA.
    """
    mensagens_problemas = [d['mensagem'] for d in diagnosticos]
    texto_problemas = "\n- ".join(mensagens_problemas)
    prompt = f"""
    Você é o "PC Fácil", um assistente técnico de informática extremamente amigável e didático. 
    Sua missão é ajudar usuários totalmente leigos a resolverem problemas em seus computadores.
    
    Um scan automático detectou os seguintes problemas no computador do usuário:
    - {texto_problemas}
    
    Baseado APENAS nestes problemas, forneça uma solução curta, clara e em formato de passo a passo. 
    Use uma linguagem simples, sem jargões técnicos. Fale diretamente com o usuário (ex: "Seu computador...").
    Se o diagnóstico for "Nenhum problema crítico detectado", apenas dê uma mensagem positiva e encorajadora.
    """
    return prompt

# FUNÇÃO PRINCIPAL DE ENVIO

def enviar_relatorio_para_ia(relatorio_json):
    """
    Envia o relatório para a API do Gemini e retorna a resposta da IA.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "insira_sua_chave_aqui ":
        print("[ERRO] A chave de API do Gemini não foi definida no arquivo api_client.py!")
        return None

    try:
        print("Configurando e enviando relatório para a IA do Gemini...")
        
       
        genai.configure(api_key=GEMINI_API_KEY)
        
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        relatorio_dict = json.loads(relatorio_json)
        diagnosticos = relatorio_dict.get('diagnostico_problemas', [])
        prompt_usuario = montar_prompt_para_ia(diagnosticos)
        
        response = model.generate_content(prompt_usuario)
        
        print("Resposta recebida do Gemini com sucesso!")
        
        return response.text

    except Exception as e:
        
        print(f"\n[ERRO] Falha ao se comunicar com a API do Gemini: {e}")
        return None