import psutil
import platform
import json
import api_client 


def coletar_informacoes_sistema():
    """
    Coleta as informações do sistema e as retorna em um dicionário Python.
    """
    dados_sistema = {
        'cpu': { 'uso_percentual': psutil.cpu_percent(interval=1) },
        'memoria': { 'total_gb': round(psutil.virtual_memory().total / (1024**3), 2), 'uso_percentual': psutil.virtual_memory().percent },
        'disco': { 'total_gb': round(psutil.disk_usage('/').total / (1024**3), 2), 'uso_percentual': psutil.disk_usage('/').percent },
        'sistema_operacional': { 'nome': platform.system(), 'versao': platform.version() }
    }
    return dados_sistema

def analisar_saude_sistema(dados_sistema):
    """
    Recebe os dados do sistema e cria uma lista de diagnósticos com base em regras.
    """
    diagnosticos = []
    if dados_sistema['cpu']['uso_percentual'] > 90:
        diagnosticos.append({
            'tipo': 'ALERTA_CPU', 'nivel': 'critico',
            'mensagem': f"Uso de CPU extremamente alto ({dados_sistema['cpu']['uso_percentual']}%). O computador pode estar travando ou muito lento."
        })
    if dados_sistema['memoria']['uso_percentual'] > 85:
        diagnosticos.append({
            'tipo': 'ALERTA_MEMORIA', 'nivel': 'alerta',
            'mensagem': f"Uso de Memória RAM elevado ({dados_sistema['memoria']['uso_percentual']}%). Fechar aplicativos pesados pode ajudar."
        })
    if dados_sistema['disco']['uso_percentual'] > 90:
        diagnosticos.append({
            'tipo': 'ALERTA_DISCO', 'nivel': 'alerta',
            'mensagem': f"Pouco espaço livre em disco ({dados_sistema['disco']['uso_percentual']}% usado). É recomendável fazer uma limpeza de arquivos."
        })
    if not diagnosticos:
        diagnosticos.append({
            'tipo': 'SISTEMA_SAUDAVEL', 'nivel': 'ok',
            'mensagem': 'Nenhum problema crítico detectado. O sistema parece estar saudável.'
        })
    return diagnosticos

def gerar_relatorio_json(dados_sistema, diagnosticos):
    """
    Estrutura o relatório final em um formato de dicionário e o converte para JSON.
    """
    relatorio = { 'status_geral': 'Analise Concluida', 'snapshot_sistema': dados_sistema, 'diagnostico_problemas': diagnosticos }
    return json.dumps(relatorio, indent=4)


if __name__ == "__main__":
    print("Iniciando diagnóstico do PC Fácil...")
    dados_coletados = coletar_informacoes_sistema()
    diagnostico_final = analisar_saude_sistema(dados_coletados)
    relatorio_json = gerar_relatorio_json(dados_coletados, diagnostico_final)
    
    print("Relatório local gerado. Conectando com a IA...")
    
    # envia o relatório e recebe a resposta de texto da IA
    resposta_formatada_ia = api_client.enviar_relatorio_para_ia(relatorio_json)
    
    # exibe a resposta final para o usuário
    if resposta_formatada_ia:
        print("\n=============== Resposta do Assistente PC Fácil ===============\n")
        print(resposta_formatada_ia)
        print("\n===============================================================")
    else:
        print("\n[FALHA] Não foi possível obter uma resposta do assistente de IA.")