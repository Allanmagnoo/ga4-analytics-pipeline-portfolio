# Projeto de Portfólio: Visão 360 do Cliente com GCP, Dataform e Python

**Status:** 🚀 Sprint 1 em Execução: Ingestão Multi-Fonte & Qualidade de Dados 🚀

---

## 🎯 Charter do Projeto (Objetivo)

Este projeto serve como uma prova de conceito completa para a construção de um **pipeline de dados unificado**, que integra dados de comportamento web (Google Analytics) com dados transacionais e demográficos de um CRM. O objetivo é ir além da análise de canais e criar uma **Visão 360º do Cliente**, permitindo a segmentação avançada e a descoberta de insights de negócio profundos.

Este trabalho visa demonstrar, de forma prática, as competências essenciais para a vaga de Engenheiro de Dados, incluindo:
- **Domínio de GCP e BigQuery:** Modelagem de dados para múltiplas fontes, otimização de performance e consultas complexas.
- **Ingestão de Dados Heterogêneos:** Uso de Python (`pandas`) para ingestão de arquivos CSV e simulação de ingestão via Data Transfer Service (`VIEWs`).
- **Orquestração com Dataform:** Construção de um pipeline com dependências entre diferentes fontes de dados.
- **Mentalidade de Negócio:** Foco na transformação de dados brutos em um ativo estratégico (a Visão 360) para responder a perguntas complexas de Marketing e Vendas.
- **Qualidade e Documentação:** Implementação de testes automatizados (assertions) para todas as fontes de dados.

---

## ❓ Perguntas de Negócio a Serem Respondidas

Este projeto foi desenhado para responder a perguntas que só a unificação de dados permite:

1.  Quais são as características demográficas (educação, renda, estado civil) dos clientes que geram mais receita online?
2.  Clientes que responderam positivamente a campanhas de marketing anteriores (`Campanha X`) demonstram maior engajamento (mais pageviews, maior tempo de sessão) no site?
3.  Podemos criar "Personas" de clientes (ex: "Amantes de Vinho", "Famílias com Crianças") e analisar a jornada de compra online de cada uma?
4.  Qual é o verdadeiro Lifetime Value (LTV) de um cliente, somando suas compras online e offline (simuladas pelo CRM)?

---

## 🏛️ Arquitetura Proposta

O pipeline segue o padrão de **Arquitetura Medalhão**, agora aplicado a múltiplas fontes de dados:

- **Fonte de Dados:**
    - Google Analytics (via `VIEW` sobre dataset público)
    - CRM (via ingestão de CSV com Python)
- **🥉 Camada Bronze:** Tabelas com dados brutos, padronizados e limpos para cada fonte (`brz_ga4`, `brz_crm`), servindo como a fonte única da verdade.
- **🥈 Camada Silver:** Camada de integração, onde os dados de GA4 e CRM são unidos para criar a tabela `slv_customer_360`, a nossa Visão 360 do Cliente.
- **🥇 Camada Gold:** Tabelas otimizadas para consumo, com KPIs e métricas de negócio baseadas na visão unificada (ex: `gld_persona_performance`).

---

## 🚀 Tech Stack

- **Cloud Provider:** Google Cloud Platform (GCP)
- **Data Warehouse:** Google BigQuery
- **Orquestração e Transformação:** Dataform
- **Ingestão de Dados:** Python 3 (`pandas`, `google-cloud-bigquery`)
- **Versionamento de Código:** Git & GitHub
- **Business Intelligence:** Looker Studio & Power BI

---

## 📊 Fontes de Dados

- **Google Analytics:** [Google Analytics Sample Dataset for BigQuery](https://support.google.com/analytics/answer/7586738?hl=pt-PT)
- **CRM:** [Customer Personality Analysis Dataset on Kaggle](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)

---

## 📂 Estrutura do Projeto

- `/scripts/ingest_crm_data.py`: Script Python para ingestão do dataset do Kaggle.
- `definitions/sources.js`: Declaração das fontes de dados externas para o Dataform.
- `definitions/01_bronze/`: Scripts da camada Bronze para cada fonte (`/ga4`, `/crm`).
- `definitions/02_silver/`: Scripts da camada Silver, onde a unificação ocorre.
- `definitions/03_gold/`: Scripts da camada Gold, com as métricas de negócio finais.
- `definitions/assertions/`: Scripts de testes de qualidade para todas as fontes de dados.

---

**Autor:** [Seu Nome Completo]
**LinkedIn:** [Link para seu perfil no LinkedIn]

**Autor:** Allan Magno

