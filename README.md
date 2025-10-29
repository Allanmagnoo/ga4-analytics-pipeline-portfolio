# Teste Técnico: Pipeline de Dados com Arquitetura Medalhão no GCP

**Status:** 🚀 Sprint 2 em Execução: Construção da Camada Silver 🚀

---

## 🎯 Objetivo do Projeto

Este projeto implementa uma arquitetura de dados Medalhão (Bronze, Silver, Gold) no Google Cloud Platform, como parte do processo de avaliação técnica para a posição de Engenheiro de Dados. O objetivo é demonstrar a capacidade de ingerir, limpar, transformar e modelar dados de e-commerce, seguindo as melhores práticas de engenharia e os padrões de desenvolvimento da empresa.

---

## 🏛️ Arquitetura e Metodologia

O pipeline foi construído utilizando **Dataform** para orquestração e transformação, seguindo o padrão de **Arquitetura Medalhão**:

- **🥉 Camada Bronze:** Réplica dos dados brutos com adição de metadados de ingestão, garantindo a rastreabilidade.
- **🥈 Camada Silver:** Camada de limpeza e conformidade, onde regras de negócio são aplicadas para garantir a qualidade e a consistência dos dados.
- **🥇 Camada Gold:** Camada de negócio, com tabelas e views agregadas, prontas para consumo por dashboards e análises.

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
| | `slv_ecommerce_order_items` | ⏳ Em Andamento |
| | `slv_ecommerce_products` | ⬜ A Fazer |
| | `slv_ecommerce_users` | ⬜ A Fazer |
| **Gold** | `fato_vendas` | ⬜ A Fazer |
| | `metricas_mensais_categoria` | ⬜ A Fazer |
| | `top_produtos` | ⬜ A Fazer |

---

## 🚀 Tech Stack

- **Cloud Provider:** Google Cloud Platform (GCP)
- **Data Warehouse:** Google BigQuery
- **Orquestração e Transformação:** Dataform
- **Versionamento de Código:** Git & GitHub

---

**Autor:** Allan Magno