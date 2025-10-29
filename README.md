# Projeto de Portfólio: Pipeline de Dados de Marketing com GCP e Dataform

**Status:** 🚧 Em Desenvolvimento 🚧

---

## 🎯 Charter do Projeto (Objetivo)

Este projeto serve como uma prova de conceito completa para a construção de um pipeline de dados ELT (Extract, Load, Transform) no Google Cloud Platform. O objetivo é demonstrar proficiência técnica e raciocínio de negócio alinhados às melhores práticas de Engenharia de Dados, replicando uma arquitetura de Data Lake Medalhão para processar dados públicos do Google Analytics.

Este trabalho visa demonstrar, de forma prática, as competências essenciais para a vaga de Engenheiro de Dados, incluindo:
- **Domínio de GCP e BigQuery:** Modelagem de dados, otimização de performance e consultas complexas.
- **Orquestração com Dataform:** Construção de um pipeline de dados com dependências, testes e versionamento.
- **Mentalidade de Negócio:** Foco na transformação de dados brutos em insights acionáveis para a área de Marketing.
- **Qualidade e Documentação:** Implementação de testes automatizados (assertions) e manutenção de uma documentação clara e objetiva.

---

## 🏛️ Arquitetura Proposta

O pipeline segue o padrão de **Arquitetura Medalhão**, garantindo rastreabilidade, escalabilidade e governança dos dados:

- **🥉 Camada Bronze:** Tabelas com dados brutos, padronizados e limpos, servindo como a fonte única da verdade (Single Source of Truth).
- **🥈 Camada Silver:** Tabelas agregadas por entidades de negócio (ex: sessões), prontas para análises exploratórias.
- **🥇 Camada Gold:** Tabelas otimizadas para consumo, com KPIs e métricas de negócio prontas para alimentar dashboards e relatórios.

---

## 🚀 Tech Stack

- **Cloud Provider:** Google Cloud Platform (GCP)
- **Data Warehouse:** Google BigQuery
- **Orquestração e Transformação:** Dataform
- **Versionamento de Código:** Git & GitHub
- **Business Intelligence:** Looker Studio & Power BI (a ser implementado)

---

## 📂 Estrutura do Projeto

O repositório segue a estrutura padrão do Dataform para organização e clareza:

- `definitions/sources.js`: Declaração das fontes de dados externas.
- `definitions/01_bronze/`: Scripts da camada Bronze.
- `definitions/02_silver/`: Scripts da camada Silver.
- `definitions/03_gold/`: Scripts da camada Gold.
- `definitions/assertions/`: Scripts de testes de qualidade de dados.

---
## 💻 Progresso do Projeto

| Camada | Tabela / Tarefa | Status |
| :--- | :--- | :--- |
| **Setup** | Criação de Datasets (brz, slv, gld, qa) | ✅ Concluído |
| | Declaração de Fontes (`sources.js`) | ✅ Concluído |
| **Bronze**| `brz_ecommerce_orders` | ✅ Concluído |
| | `brz_ecommerce_order_items` | ✅ Concluído |
| | `brz_ecommerce_products` | ✅ Concluído |
| | `brz_ecommerce_users` | ✅ Concluído |
| **Silver** | `slv_ecommerce_orders` | ✅ Concluído |
| | `slv_ecommerce_order_items` | ✅ Concluído |
| | `slv_ecommerce_products` | ⏳ Em Andamento |
| | `slv_ecommerce_users` | ⬜ A Fazer |
| **Gold** | `fato_vendas` | ⬜ A Fazer |
| | `metricas_mensais_categoria` | ⬜ A Fazer |
| | `top_produtos` | ⬜ A Fazer |

**Autor:** Allan Magno

