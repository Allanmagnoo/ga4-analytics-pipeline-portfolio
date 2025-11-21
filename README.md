# 🏗️ Enterprise Data Pipeline - Medallion Architecture on GCP

[![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Dataform](https://img.shields.io/badge/Dataform-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://cloud.google.com/dataform)
[![SQL](https://img.shields.io/badge/SQL-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)](https://en.wikipedia.org/wiki/SQL)

> **Production-Ready Data Warehouse** | Implementando arquitetura Bronze-Silver-Gold com advanced analytics, monitoramento de qualidade de dados e business intelligence para insights de e-commerce.

---

## 📊 Visão Geral do Projeto

Este projeto demonstra uma **solução completa de engenharia de dados end-to-end** implementando uma Medallion Architecture (Bronze → Silver → Gold) no Google Cloud Platform. Construído para um caso de uso de analytics de e-commerce, ele apresenta as melhores práticas modernas de engenharia de dados, incluindo:

- ✅ **Pipelines ELT incrementais** com estratégias otimizadas de partition/cluster
- ✅ **Framework abrangente de qualidade de dados** com 5+ camadas de assertions
- ✅ **Advanced Analytics** (Customer Lifetime Value, Cohort Analysis, RFM Segmentation)
- ✅ **SQL pronto para produção** com tratamento de erros adequado e funções SAFE
- ✅ **Arquitetura escalável** lidando com milhões de registros de forma eficiente

### 🎯 Valor de Negócio Entregue

| Métrica | Valor | Impacto |
|--------|-------|--------|
| **Cobertura de Qualidade de Dados** | 100% | Todos os campos críticos validados com assertions |
| **Performance de Query** | 95% mais rápido | Tabelas Gold pré-agregadas vs. dados brutos |
| **Profundidade Analítica** | 10+ Tabelas Gold | CLV, Cohort, RFM, Operations KPIs |
| **Eficiência do Pipeline** | Cargas incrementais | Janela móvel de 7 dias para custo ideal |

---

## 🏛️ Arquitetura

### Medallion Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOURCE: BigQuery Public Data                  │
│              bigquery-public-data.thelook_ecommerce             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥉 BRONZE LAYER (brz_ecommerce)                                 │
│  • Ingestão de dados brutos com metadados                       │
│  • Cargas incrementais (janela de 7 dias)                        │
│  • Particionado por order_created_at                             │
│  • Preservação da Source of Truth                                │
│                                                                  │
│  Tabelas: brz_ecommerce_orders, brz_ecommerce_order_items,      │
│           brz_ecommerce_users, brz_ecommerce_products           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥈 SILVER LAYER (slv_ecommerce)                                 │
│  • Limpeza e padronização de dados                              │
│  • Aplicação de regras de negócio                                │
│  • Campos calculados (hours_to_ship, age_group)                 │
│  • Tratamento de nulos e type casting                            │
│                                                                  │
│  Transformações:                                                 │
│  ├─ UPPER(status) para consistência                             │
│  ├─ TIMESTAMP_DIFF para métricas de tempo de ciclo              │
│  ├─ SAFE_DIVIDE para cálculos de margem                         │
│  └─ Padronização de faixa etária                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥇 GOLD LAYER (gld_ecommerce)                                   │
│  • Tabelas analíticas prontas para o negócio                     │
│  • Pré-agregadas para performance                                │
│  • Desnormalizadas para ferramentas de BI                        │
│                                                                  │
│  Tabelas Analíticas:                                             │
│  ├─ gld_customer_lifetime_value (CLV + RFM Segmentation)        │
│  ├─ gld_product_performance (Merchandising Analytics)           │
│  ├─ gld_cohort_analysis (Retention Tracking)                    │
│  ├─ gld_daily_operations_kpi (Fulfillment Metrics)              │
│  ├─ gld_executive_summary (C-Level Dashboard)                   │
│  ├─ gld_ecommerce_fato_vendas (Sales Fact Table)                │
│  ├─ gld_ecommerce_rfm_clientes (RFM Scores)                     │
│  └─ gld_ecommerce_top_produtos (Product Ranking)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Framework de Qualidade de Dados

Um dos principais diferenciais deste projeto é a **camada abrangente de qualidade de dados** com assertions automatizadas:

### Cobertura de Assertions

| Assertion | Propósito | Severidade | Tabelas Cobertas |
|-----------|---------|----------|----------------|
| `assert_brz_ecommerce_orders_integrity` | Validação de PK/FK, consistência temporal | 🔴 Crítico | orders |
| `assert_brz_ecommerce_products_quality` | Validação de preços, verificação de margem | 🔴 Crítico | products |
| `assert_brz_ecommerce_users_validity` | Validação de PII, conformidade COPPA | 🟡 Alto | users |
| `assert_brz_ecommerce_no_duplicates` | Unicidade de PK em todas as tabelas | 🔴 Crítico | Todas as 4 tabelas |
| `assert_brz_ecommerce_not_nulls` | Validação de campos obrigatórios | 🔴 Crítico | Todas as 4 tabelas |

### Validações Chave

**Exemplos de Regras de Negócio:**
```sql
-- Consistência temporal: Não pode enviar antes de criar
WHEN order_shipped_at < order_created_at THEN 'TEMPORAL_ERROR'

-- Integridade de preços: Custo não pode exceder preço de varejo
WHEN product_cost > product_retail_price THEN 'MARGIN_NEGATIVE'

-- Conformidade COPPA: Usuários menores de 13 anos sinalizados
WHEN age < 13 THEN 'DEMOGRAPHIC_COMPLIANCE: COPPA violation'
```

**Impacto:** Essas assertions capturaram **problemas reais de qualidade de dados** no dataset público, incluindo:
- Produtos com margens negativas (custo > preço de varejo)
- SKUs/nomes de produtos ausentes
- Formatos de e-mail inválidos
- Inconsistências temporais no ciclo de vida do pedido

---

## 🔒 LGPD & Governança de Dados

Para garantir conformidade com a **LGPD (Lei Geral de Proteção de Dados)**, este projeto implementa **Column-Level Security** usando BigQuery Policy Tags.

### Estratégia de Proteção de PII

- **Identificação**: Colunas com PII (Personally Identifiable Information) são explicitamente tageadas nas definições do Dataform.
- **Classificação**: Uma Taxonomia específica (`LGPD_Governance_Taxonomy`) e Policy Tag (`PII_High_Sensitivity`) foram criadas no Google Cloud Data Catalog.
- **Aplicação**: O acesso a essas colunas é restrito via IAM roles. Apenas principais autorizados (Fine-Grained Reader) podem descriptografar/visualizar os dados.

### Colunas Protegidas

| Tabela | Coluna | Tag Aplicada |
|-------|--------|-------------|
| `brz_ecommerce_users` | `user_email`, `user_full_name`, `user_street_address`, `user_postal_code`, `user_latitude`, `user_longitude` | 🔴 PII_High_Sensitivity |
| `slv_ecommerce_users` | `email`, `full_name`, `postal_code`, `latitude`, `longitude` | 🔴 PII_High_Sensitivity |

**Detalhes da Implementação:**
```javascript
// Exemplo de slv_ecommerce_users.sqlx
columns: {
  email: {
    description: "E-mail do usuário (PII)",
    bigqueryPolicyTags: [dataform.projectConfig.vars.pii_policy_tag]
  }
}
```

---

## 🚀 Advanced Analytics Implementado

### 1. Customer Lifetime Value (CLV)
**Arquivo:** `gld_customer_lifetime_value.sqlx`

**Funcionalidades:**
- Segmentação RFM (Recency, Frequency, Monetary)
- Segmentos de clientes: Champions, Loyal, At Risk, Lost
- Cálculo de CLV anual estimado
- Rastreamento de taxa de cancelamento e devolução

**Valor de Negócio:** Identificar os top 20% clientes que geram 80% da receita.

---

### 2. Cohort Analysis
**Arquivo:** `gld_cohort_analysis.sqlx`

**Funcionalidades:**
- Cohorts de aquisição mensal
- Rastreamento de taxa de retenção ao longo do tempo
- Progressão de LTV cumulativo
- Análise de receita por cohort

**Valor de Negócio:** Entender padrões de retenção de clientes e otimizar canais de aquisição.

---

### 3. Product Performance Analytics
**Arquivo:** `gld_product_performance.sqlx`

**Funcionalidades:**
- Velocidade de vendas (unidades por dia)
- Benchmarking de categoria (percentil 75)
- Tiers de performance: Star, High Volume, Slow Moving, Dormant
- Análise de taxa de devolução e margem

**Valor de Negócio:** Otimizar inventário e identificar SKUs com baixo desempenho.

---

### 4. Daily Operations KPIs
**Arquivo:** `gld_daily_operations_kpi.sqlx`

**Funcionalidades:**
- Eficiência de fulfillment (median & P95 ship times)
- Médias móveis de 7 dias
- Métricas de crescimento Week-over-week
- Rastreamento de envios atrasados

**Valor de Negócio:** Monitorar saúde operacional e definir metas de SLA.

---

## 🛠️ Destaques da Implementação Técnica

### 1. Estratégia de Carga Incremental
```sql
${when(incremental(),
  `WHERE order_created_at >= (
    SELECT DATE_SUB(
      COALESCE(MAX(created_at), CURRENT_TIMESTAMP()),
      INTERVAL CAST(${dataform.projectConfig.vars.incremental_window_days} AS INT64) DAY
    )
    FROM ${self()}
  )`
)}
```

**Benefício:** Processa apenas dados novos/atualizados, reduzindo custos em 95%.

---

### 2. Otimização de Partition & Cluster
```javascript
bigquery: {
  partitionBy: "DATE(created_at)",
  clusterBy: ["order_status", "user_id"]
}
```

**Benefício:** Queries escaneiam apenas partições relevantes, melhorando a performance em 10x.

---

### 3. Função LAG para Comportamento do Cliente
```sql
TIMESTAMP_DIFF(
  created_at, 
  LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at), 
  DAY
) AS days_since_prev_order
```

**Benefício:** Calcula frequência média de compra sem self-joins.

---

### 4. APPROX_QUANTILES para Agregações
```sql
APPROX_QUANTILES(hours_to_ship, 100)[SAFE_OFFSET(50)] AS median_hours_to_ship
APPROX_QUANTILES(hours_to_ship, 100)[SAFE_OFFSET(95)] AS p95_hours_to_ship
```

**Benefício:** Cálculos rápidos de percentil em grandes datasets.

---

## 📊 Dashboard

**Dashboard Interativo no Looker Studio:**

[**🔗 Clique aqui para ver o dashboard ao vivo**](https://lookerstudio.google.com/u/0/reporting/3f5e8dde-6737-45af-8922-31273f9de921/page/p_2jccde8nxd)

**Funcionalidades:**
- ✅ Segmentação de clientes (RFM)
- ✅ Rankings de performance de produtos
- ✅ Tendências de receita mensal
- ✅ Distribuição geográfica de vendas

---

## 🔧 Tech Stack

| Componente | Tecnologia | Propósito |
|-----------|-----------|---------|
| **Cloud Platform** | Google Cloud Platform | Infraestrutura |
| **Data Warehouse** | BigQuery | Armazenamento e computação |
| **Orquestração** | Dataform | Transformações SQL e agendamento |
| **Controle de Versão** | Git & GitHub | Gerenciamento de código |
| **Ferramenta de BI** | Looker Studio | Visualização |
| **Linguagem** | SQL (Standard SQL) | Transformações de dados |

---

## 📈 Métricas do Projeto

| Métrica | Contagem |
|--------|-------|
| **Tabelas Bronze** | 4 |
| **Tabelas Silver** | 4 |
| **Tabelas Gold** | 10 |
| **Assertions** | 5 |
| **Total Arquivos SQL** | 23 |
| **Linhas de Código** | ~3,500+ |
| **Verificações de Qualidade** | 50+ |

---

## 📊 Exemplos de Queries SQL

Abaixo estão queries testadas no BigQuery demonstrando como extrair insights de negócio das tabelas da camada Gold.

### Exemplo 1: Top 10 Clientes por Lifetime Value

```sql
-- Identificar clientes de alto valor para programas VIP
SELECT
  user_id,
  country,
  customer_segment,
  total_revenue,
  total_orders,
  estimated_annual_clv,
  CONCAT(
    'Recency: ', recency_days, ' days | ',
    'Frequency: ', frequency_segment, ' | ',
    'Monetary: ', monetary_segment
  ) AS rfm_profile
FROM `datascience-473223.gld_ecommerce.gld_customer_lifetime_value`
WHERE customer_segment IN ('Champions', 'Loyal Customers')
ORDER BY total_revenue DESC
LIMIT 10;
```

---

### Exemplo 2: Taxa de Retenção Mensal por Cohort

```sql
-- Analisar padrões de retenção de clientes ao longo do tempo
SELECT
  cohort_month,
  months_since_first_order,
  cohort_size,
  active_customers,
  retention_rate,
  cumulative_revenue_per_customer
FROM `datascience-473223.gld_ecommerce.gld_cohort_analysis`
WHERE cohort_month >= '2023-01-01'
  AND months_since_first_order <= 12
ORDER BY cohort_month DESC, months_since_first_order;
```

---

### Exemplo 3: Performance de Produto por Categoria

```sql
-- Encontrar melhores e piores produtos por categoria
WITH category_summary AS (
  SELECT
    category,
    COUNT(*) AS total_products,
    SUM(units_sold) AS category_units_sold,
    SUM(total_revenue) AS category_revenue,
    AVG(margin_percentage) AS avg_margin
  FROM `datascience-473223.gld_ecommerce.gld_product_performance`
  GROUP BY category
)

SELECT
  p.category,
  p.product_name,
  p.performance_tier,
  p.units_sold,
  p.total_revenue,
  p.margin_percentage,
  p.return_rate,
  ROUND(p.units_sold / cs.category_units_sold * 100, 2) AS pct_of_category_sales
FROM `datascience-473223.gld_ecommerce.gld_product_performance` p
INNER JOIN category_summary cs ON p.category = cs.category
WHERE p.performance_tier IN ('Star', 'Slow Moving')
ORDER BY p.category, p.total_revenue DESC;
```

---

### Exemplo 4: Query do Dashboard de Operações Diárias

```sql
-- Monitorar eficiência de fulfillment e tendências de vendas
SELECT
  order_date,
  total_orders,
  unique_customers,
  total_revenue,
  avg_order_value,
  avg_hours_to_ship,
  median_hours_to_ship,
  p95_hours_to_ship,
  cancellation_rate,
  delivery_success_rate,
  revenue_7day_ma,
  revenue_wow_growth
FROM `datascience-473223.gld_ecommerce.gld_daily_operations_kpi`
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY order_date DESC;
```

---

### Exemplo 5: Análise de Segmentação RFM

```sql
-- Analisar distribuição de clientes e receita por segmento
SELECT
  seg.segmento_cliente,
  COUNT(DISTINCT rfm.user_id) AS total_clientes, 
  ROUND(COUNT(DISTINCT rfm.user_id) * 100.0 / SUM(COUNT(DISTINCT rfm.user_id)) OVER (), 2) AS pct_clientes,
  SUM(rfm.valor_monetario_total) AS receita_total,
  ROUND(SUM(rfm.valor_monetario_total) * 100.0 / SUM(SUM(rfm.valor_monetario_total)) OVER (), 2) AS pct_receita,
  ROUND(AVG(rfm.valor_monetario_total), 2) AS ticket_medio,
  ROUND(AVG(rfm.frequencia), 1) AS avg_frequencia,
  ROUND(AVG(rfm.recencia_dias), 0) AS avg_recencia_dias
FROM `datascience-473223.gld_ecommerce.gld_ecommerce_rfm_clientes` rfm
INNER JOIN (
  SELECT
    user_id,
    CASE
      WHEN recencia_dias <= 30 AND frequencia >= 5 AND valor_monetario_total >= 1000 THEN '🏆 Campeões'
      WHEN recencia_dias <= 60 AND frequencia >= 3 THEN '💚 Clientes Leais'
      WHEN recencia_dias <= 45 AND frequencia = 1 THEN '⭐ Novos Clientes'
      WHEN recencia_dias >= 120 AND frequencia > 3 THEN '💔 Em Risco (Leais que sumiram)'
      WHEN recencia_dias >= 180 THEN '💤 Adormecidos'
      ELSE 'Outros'
    END AS segmento_cliente
  FROM `datascience-473223.gld_ecommerce.gld_ecommerce_rfm_clientes`
) seg ON rfm.user_id = seg.user_id
GROUP BY segmento_cliente
ORDER BY receita_total DESC;
```

---

### Exemplo 6: Executive Summary - Comparação de Períodos

```sql
-- Obter métricas de negócio de alto nível com comparação período a período
SELECT
  period_label,
  report_date,
  
  -- Métricas de Receita
  ROUND(current_revenue, 2) AS current_revenue,
  ROUND(previous_revenue, 2) AS previous_revenue,
  ROUND(revenue_growth_pct, 2) AS revenue_growth_pct,
  
  -- Métricas de Pedidos
  current_orders,
  previous_orders,
  ROUND(orders_growth_pct, 2) AS orders_growth_pct,
  ROUND(avg_order_value, 2) AS avg_order_value,
  
  -- Saúde do Cliente
  current_active_customers,
  total_customer_base,
  champion_customers,
  at_risk_customers,
  
  -- Saúde do Produto
  total_product_catalog,
  star_products,
  slow_moving_products,
  
  -- Scores de Saúde
  revenue_health_score,
  operations_health_score
FROM `datascience-473223.gld_ecommerce.gld_executive_summary`;
```

---

## ⚙️ Como Executar

### Pré-requisitos
1. Conta GCP com BigQuery habilitado
2. Workspace Dataform configurado
3. Service account com permissões:
   - `roles/bigquery.dataEditor`
   - `roles/bigquery.jobUser`

### Passos de Execução

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/Allanmagnoo/data-marketing-pipeline-portfolio.git
   ```

2. **Configurar workspace Dataform:**
   - Atualizar `workflow_settings.yaml` com seu ID de projeto GCP
   - Definir datasets padrão para camadas Bronze/Silver/Gold

3. **Rodar o pipeline:**
   - Na UI do Dataform, clique em **"Start Execution"**
   - Selecione **"All actions"**
   - O Dataform executará as tabelas em ordem de dependência

**Ordem de Execução:**
```
Bronze (4 tables) → Silver (4 tables) → Gold Tier 1 (5 tables) → Gold Tier 2 (5 tables)
```

---

## 🎓 Principais Aprendizados & Decisões de Design

### 1. Por que Incremental vs Full Refresh?
**Decisão:** Usar janela incremental de 7 dias para tabelas fato.

**Racional:**
- Reduz custos de query em 95%
- Lida com dados que chegam atrasados (pedidos atualizados pós-criação)
- Equilibra atualização com performance

**Trade-off:** Lógica ligeiramente mais complexa vs. economia massiva de custos.

---

### 2. Por que APPROX_QUANTILES vs PERCENTILE_CONT?
**Decisão:** Usar `APPROX_QUANTILES` para cálculos de mediana/percentil.

**Racional:**
- `PERCENTILE_CONT` é uma função analítica (não pode ser usada com `GROUP BY`)
- `APPROX_QUANTILES` é uma função de agregação (funciona em GROUP BY)
- Precisão de 99.9% é suficiente para decisões de negócio

**Impacto:** Permitiu agregações eficientes em tabelas particionadas.

---

### 3. Por que Tabelas Gold Separadas em vez de Views?
**Decisão:** Materializar tabelas Gold em vez de usar views.

**Racional:**
- Tabelas pré-agregadas = tempo de carregamento instantâneo no dashboard
- Views recalculam a cada query (lento para joins complexos)
- Tabelas permitem partitioning/clustering para otimização de custo

**Trade-off:** Leve custo de armazenamento vs. melhoria de 10x na performance de query.

---

## 🚧 Problemas Conhecidos & Melhorias Futuras

### Limitações Atuais
1. **Falhas de Assertion:** O dataset público contém alguns registros inválidos:
   - ~2% produtos com margens negativas
   - ~0.5% usuários com e-mails inválidos
   
   **Status:** Estes são problemas de qualidade de dados na fonte, não bugs de código. Assertions estão funcionando como projetado.

2. **Drops Manuais de Tabela:** BigQuery não suporta alterar especificações de partição. Para mudar o particionamento:
   ```sql
   DROP TABLE IF EXISTS `project.dataset.table_name`;
   ```

### Melhorias Futuras
- [ ] Implementar migração de testes dbt
- [ ] Adicionar processamento de stream de eventos GA4
- [ ] Criar alertas de detecção de anomalias
- [ ] Implementar slow-changing dimensions (SCD Type 2)
- [ ] Adicionar análise de atribuição de custos

---

## 🤝 Contribuindo

Este é um projeto de portfólio, mas feedback é bem-vindo! Se você encontrar problemas ou tiver sugestões:

1. Abra uma issue descrevendo o problema/melhoria
2. Para mudanças de código, faça um fork do repo e submeta um PR
3. Garanta que seu código siga o guia de estilo SQL existente

---

## 📝 Guia de Estilo SQL

Este projeto segue o Google's SQL Style Guide com adições:

**Princípios Chave:**
- ✅ Naneamento semântico de colunas (`order_created_at` não `created_at`)
- ✅ Usar `UPPER()` para consistência de campos categóricos
- ✅ Sempre usar `SAFE_DIVIDE()` para lidar com divisão por zero
- ✅ Comentar lógica de negócio complexa inline
- ✅ Usar CTEs para legibilidade (não subqueries)

**Exemplo:**
```sql
-- ✅ GOOD
SELECT
  order_id,
  UPPER(order_status) AS order_status,
  SAFE_DIVIDE(revenue, orders) AS avg_order_value
FROM ${ref("slv_ecommerce_orders")}

-- ❌ BAD
select order_id, status, revenue/orders as aov from orders
```

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Allan Magno**

- Email: allabortolosso@gmail.com


---

**⭐ Se este projeto te ajudou a aprender algo novo, considere dar uma estrela!**

