# Teste Técnico: Pipeline de Dados com Arquitetura Medalhão no GCP

**Status:** ✅ Projeto Concluído ✅

## 🎯 Objetivo do Projeto

Este projeto implementa uma arquitetura de dados Medalhão (Bronze, Silver, Gold) de ponta a ponta no Google Cloud Platform. O objetivo é demonstrar a capacidade de ingerir, limpar, transformar e modelar dados de um e-commerce (`bigquery-public-data.thelook_ecommerce`), seguindo as melhores práticas de engenharia de dados e os padrões de desenvolvimento da Hagens.

O pipeline foi construído com foco em robustez, escalabilidade e valor de negócio, transformando dados brutos em insights acionáveis e prontos para o consumo pelo time de Business Intelligence e Marketing.

## 🏛️ Arquitetura e Metodologia

O pipeline foi construído utilizando **Dataform** para orquestração e transformação, seguindo o padrão de **Arquitetura Medalhão**:

* **🥉 Camada Bronze (`brz_ecommerce`):** É a camada de ingestão. Funciona como uma réplica dos dados brutos da fonte (`thelook_ecommerce`), com a adição de uma coluna de metados (`data_ingestao`) para controle de carga e rastreabilidade. Esta camada é a "fonte única da verdade" imutável.

* **🥈 Camada Silver (`slv_ecommerce`):** É a camada de limpeza, padronização e enriquecimento. É aqui que as regras de negócio são aplicadas para garantir a qualidade dos dados. As transformações incluem remoção de registros inválidos (ex: pedidos cancelados), padronização de campos (ex: `UPPER(category)`) e criação de colunas de valor agregado (ex: `idade_estimada_atual`).

* **🥇 Camada Gold (`gld_ecommerce`):** É a camada de negócio (Business Layer). Contém tabelas e views desnormalizadas e pré-agregadas, otimizadas para performance de consulta. Ela entrega respostas prontas para as perguntas do negócio e alimenta diretamente os dashboards analíticos.

## 🚀 Tech Stack

* **Cloud Provider:** Google Cloud Platform (GCP)
* **Data Warehouse:** Google BigQuery
* **Orquestração e Transformação (ELT):** Dataform
* **Versionamento de Código:** Git & GitHub
* **Business Intelligence (Consumidor):** Looker Studio, Power BI

## 📊 Dashboard (Looker Studio)

Para demonstrar a aplicação prática e o valor de negócio dos dados da Camada Gold, um dashboard interativo foi criado no Looker Studio. Este painel permite a exploração dos KPIs de negócio, análise de rentabilidade de produtos e segmentação de clientes (RFM).

[**Clique aqui para acessar o Dashboard Interativo**](https://lookerstudio.google.com/u/0/reporting/3f5e8dde-6737-45af-8922-31273f9de921/page/p_2jccde8nxd)

## 📝 Decisões Técnicas e Raciocínio (O "Porquê?")

Durante a implementação, foram tomadas decisões de engenharia para aumentar a robustez e o valor de negócio do pipeline:

1.  **Cálculo de Idade Estimada (Tabela `slv_ecommerce_users`):**
    > **Desafio:** A coluna `age` da fonte é um dado estático (idade no momento do cadastro), tornando-se obsoleta.
    >
    > **Solução:** Criei uma coluna `idade_atual_estimada` reconstruindo uma data de nascimento estimada (`DATE_SUB(created_at, INTERVAL age YEAR)`) e, em seguida, calculando a idade atual dinamicamente (`DATE_DIFF(CURRENT_DATE(), ...)`).
    >
    > **Valor:** Transforma um dado impreciso em uma métrica dinâmica e sempre precisa, crucial para segmentações de clientes por faixa etária.

2.  **Cálculo de Margem Agregada (Tabela `gld_ecommerce_top_produtos`):**
    > **Desafio:** O teste pedia a "margem média". Calcular `AVG(margem_percentual)` é analiticamente incorreto, pois distorce o resultado.
    >
    > **Solução:** Calculei a margem percentual agregada real: `SAFE_DIVIDE(SUM(margem_bruta_item), SUM(custo_total_item))`.
    >
    > **Valor:** Esta é uma métrica ponderada e muito mais precisa para a tomada de decisão do negócio sobre a rentabilidade real dos produtos.

3.  **Correção de `NULL`s na Camada Gold (Tabela `gld_ecommerce_fato_vendas`):**
    > **Desafio:** A tabela `gld_metricas_mensais_categoria` exibia uma grande linha com datas nulas, apesar de os dados na Bronze estarem completos.
    >
    > **Investigação:** A causa raiz foi um `LEFT JOIN` na `fato_vendas` que mantinha itens de pedidos `Cancelled` (que foram filtrados da `slv_orders`), gerando `NULL`s em todas as colunas de data.
    >
    > **Solução:** Mudei o `LEFT JOIN` para um `INNER JOIN` entre `slv_ecommerce_order_items` e `slv_ecommerce_orders`, garantindo que a `fato_vendas` contenha apenas vendas de pedidos válidos.
    >
    > **Valor:** Esta decisão de modelagem garante a integridade analítica de toda a Camada Gold.

4.  **Enriquecimento da Tabela de Fatos (Tabela `gld_ecommerce_fato_vendas`):**
    > **Desafio:** O time de performance precisa de segmentações que exigem `JOIN`s complexos na ferramenta de BI, causando lentidão.
    >
    > **Solução:** Enriqueci a `fato_vendas` diretamente no Dataform com dimensões pré-calculadas, como `user_faixa_etaria`, `tipo_cliente` ('Novo Cliente' vs. 'Recorrente', via `ROW_NUMBER()`) e `user_country`.
    >
    > **Valor:** Isso torna o dashboard extremamente rápido e centraliza a lógica de negócio no DWH, garantindo consistência em todas as análises.

5.  **Otimização de BI (Tabela `gld_ecommerce_rfm_analise_categoria`):**
    > **Desafio:** Responder "O que meus melhores clientes compram?" exigiria um "Data Blending" (mesclagem) complexo e lento no Looker Studio.
    >
    > **Solução:** Criei uma tabela Gold adicional que já cruza os segmentos RFM com as categorias de produtos que eles compraram, entregando a resposta pronta.
    >
    > **Valor:** O dashboard carrega instantaneamente, e a lógica de segmentação fica centralizada, padronizada e reutilizável.

## 🚧 Principais Desafios Encontrados

Durante o desenvolvimento do pipeline, o principal desafio não foi técnico, mas sim de **qualidade de dados na fonte**.

> **Descoberta:** Após a construção da Camada Gold, a tabela `gld_ecommerce_top_produtos` revelou margens de lucro percentuais impossíveis (ex: 8.000% a 14.000%).
>
> **Investigação:** A análise da fórmula de margem (`(Receita - Custo) / Custo`) provou que o **cálculo estava correto**. O problema residia nos dados da fonte: produtos com alto preço de venda (ex: R\$ 78,58) tinham um `cost` registrado de centavos (ex: R\$ 0,55).
>
> **Conclusão:** O pipeline funcionou com sucesso, pois seu resultado expôs uma falha crítica de qualidade nos dados de custo do catálogo. Em um cenário real, este insight seria levado ao time de Compras/Catálogo para a correção dos dados de origem, provando o valor do pipeline como uma ferramenta de auditoria de dados.

## ⚙️ Como Executar os Scripts

O projeto é orquestrado pelo Dataform e foi configurado para ser executado de forma unificada.

1.  Garanta que as permissões do Agente de Serviço do Dataform (`service-<ID>@gcp-sa-dataform.iam.gserviceaccount.com`) tenham os papéis de "Editor de Dados do BigQuery" e "Usuário de Job do BigQuery" no IAM.
2.  No ambiente Dataform, clique no botão principal **"Start Execution"**.
3.  Selecione a opção **"All actions"**.
4.  Clique em **"Start execution"**. O Dataform analisará o grafo de dependências e executará todas as tabelas na ordem correta (Bronze → Silver → Gold).

## 💡 Insights de Negócio (Baseado na Camada Gold)

Abaixo estão os 3 principais insights extraídos da análise dos dashboards e das tabelas Gold, baseados nos fatos encontrados nos dados.

1.  **Insight de Qualidade de Dados (Ação Imediata):**
    > **Observação:** O pipeline expôs uma falha crítica na qualidade dos dados de custo (`cost`) da fonte. A análise da tabela `gld_top_produtos` revela margens de lucro irreais (ex: 14.000%) para produtos de alto volume, como "Pendleton Men's Pajama Set".
    >
    > **Ação Sugerida:** A prioridade número um é **auditar e corrigir os dados de custo na fonte** (`products`). Sem dados de custo confiáveis, qualquer análise de lucratividade da empresa estará fundamentalmente errada. O pipeline de dados provou seu valor como uma ferramenta de auditoria.

2.  **Insight de Segmentação (Onde está o Valor):**
    > **Observação:** A análise RFM (`gld_ecommerce_rfm_clientes`) revelou que os segmentos de clientes ativos de maior valor (ex: "Clientes Leais", "Em Risco") representam uma fatia minúscula da base total de clientes (menos de 7,3%), mas geram uma receita desproporcionalmente grande (somados, são **16,9%** de toda a receita).
    >
    > **Ação Sugerida:** O segmento "Clientes Leais" sozinho, embora seja uma pequena fração de clientes, gera **6,3%** da receita, tornando-os em média **3x a 6x mais valiosos** que um cliente comum. A prioridade de marketing não deve ser apenas reativar os "Adormecidos" (65.5% dos clientes), mas garantir a retenção VIP e o crescimento (up-sell) deste pequeno e hiper-valioso grupo de clientes leais.

3.  **Insight de Risco (Recuperação de Clientes):**
    > **Observação:** O segmento "Em Risco (Leais que sumiram)" é o segundo grupo mais valioso, responsável por **5.5%** da receita. Eles eram clientes leais que agora estão em risco de abandono.
    >
    > **Ação Sugerida:** Este segmento é o alvo perfeito para uma campanha de reativação imediata. Uma consulta de exemplo mostra que seu ticket médio era historicamente alto. Sugere-se uma campanha de e-mail direcionada oferecendo um desconto de "Estamos com saudades" para tentar recuperar esses clientes de alto valor antes que sejam perdidos para a concorrência.

## 쿼리 Consultas de Exemplo (Para o Negócio)

Abaixo estão exemplos de como as tabelas Gold podem ser usadas para responder a perguntas de negócio complexas de forma simples.

**1. Identificar Clientes "Campeões" em Risco para Reativação Imediata:**

```sql
-- Identifica clientes de alto valor (top 20% em gastos) que eram leais
-- (frequência > 5) mas não compram há mais de 90 dias.
SELECT
  user_id,
  recencia_dias,
  frequencia,
  valor_monetaria_total
FROM
  `datascience-451918.gld_ecommerce.gld_ecommerce_rfm_clientes`
WHERE
  recencia_dias > 90
  AND frequencia > 5
  AND valor_monetaria_total > (
    -- Define "alto valor" como clientes no 80º percentil de gastos
    SELECT
      APPROX_QUANTILES(valor_monetaria_total, 100)[OFFSET(80)]
    FROM
      `datascience-451918.gld_ecommerce.gld_ecommerce_rfm_clientes`
  )
ORDER BY
  valor_monetaria_total DESC;

2. Performance de Vendas (Receita vs. Margem) para a Faixa Etária "25-34" por Categoria:

'''sql
-- Analisa quais categorias são mais lucrativas vs. mais populares
-- para a faixa etária de marketing mais cobiçada.
SELECT
  product_category,
  SUM(valor_total_vendido) AS receita_total,
  SAFE_DIVIDE(SUM(margem_bruta_item), SUM(custo_total_item)) * 100 AS margem_percentual_agregada
FROM
  `datascience-451918.gld_ecommerce.gld_ecommerce_fato_vendas`
WHERE
  user_faixa_etaria = '25-34'
GROUP BY
  1
ORDER BY
  receita_total DESC;

## 📈 Diagrama de Fluxo

<img width="1968" height="575" alt="image" src="https://github.com/user-attachments/assets/947600ec-c73d-4796-8c1e-20073aebc0d0" />

Fluxo Conceitual:

[Fonte: bigquery-public-data.thelook_ecommerce] → [Camada Bronze (4 tabelas)] → [Camada Silver (4 tabelas)] → [Camada Gold (Fatos e Agregações)]