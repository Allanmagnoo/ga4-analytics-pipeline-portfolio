# Arquivo: /scripts/ingest_crm_data.py

import pandas as pd
from google.cloud import bigquery
import os

# --- CONFIGURAÇÕES - ALTERE ESTAS VARIÁVEIS ---
PROJECT_ID = "datascience-473223"  # Substitua pelo ID do seu projeto GCP
DATASET_ID = "brz_crm"
TABLE_ID = "raw_customers"
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'marketing_campaign.csv')
# ----------------------------------------------

def ingest_crm_data():
    """
    Lê dados de um arquivo CSV e os carrega para uma tabela no BigQuery.
    A tabela será substituída se já existir.
    """
    print("Iniciando a ingestão de dados do CRM...")

    # 1. Inicializa o cliente do BigQuery.
    #    O cliente usará suas credenciais do gcloud CLI que já devem estar configuradas.
    client = bigquery.Client(project=PROJECT_ID)

    # 2. Lê o arquivo CSV para um DataFrame do Pandas.
    #    O separador '\t' é específico para este arquivo do Kaggle.
    try:
        df = pd.read_csv(CSV_FILE_PATH, sep='\t')
        print(f"Arquivo CSV '{CSV_FILE_PATH}' lido com sucesso. {len(df)} linhas encontradas.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo CSV não encontrado em '{CSV_FILE_PATH}'. Verifique o caminho.")
        return

    # 3. Define o nome completo da tabela no BigQuery.
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # 4. Configura o "job" de carregamento.
    #    - write_disposition='WRITE_TRUNCATE': Se a tabela existir, ela será apagada e recriada.
    #    - source_format: Especifica que estamos carregando de um DataFrame.
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    # 5. Executa o job de carregamento e aguarda a conclusão.
    print(f"Carregando dados para a tabela '{table_ref}' no BigQuery...")
    job = client.load_table_from_dataframe(
        df, table_ref, job_config=job_config
    )
    job.result()  # Aguarda o job terminar.

    # 6. Verifica o resultado e imprime uma mensagem de sucesso.
    table = client.get_table(table_ref)
    print(
        f"Ingestão concluída com sucesso. A tabela '{table_ref}' agora tem {table.num_rows} linhas."
    )

if __name__ == "__main__":
    # Para rodar o script, certifique-se de que você está autenticado no gcloud:
    # No seu terminal, rode: gcloud auth application-default login
    ingest_crm_data()