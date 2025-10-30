# Teste Técnico: Pipeline de Dados com Arquitetura Medalhão no GCP

**Status:** ✅ Projeto Concluído ✅

---

## 🎯 Objetivo do Projeto

Este projeto implementa uma arquitetura de dados Medalhão (Bronze, Silver, Gold) de ponta a ponta no Google Cloud Platform, como parte do processo de avaliação técnica para a posição de Engenheiro de Dados. O objetivo é demonstrar a capacidade de ingerir, limpar, transformar e modelar dados de e-commerce, seguindo as melhores práticas de engenharia e os padrões de desenvolvimento da empresa.

---

## 🏛️ Arquitetura e Metodologia

[cite_start]O pipeline foi construído utilizando **Dataform** para orquestração e transformação, seguindo o padrão de **Arquitetura Medalhão** para garantir rastreabilidade, escalabilidade e governança dos dados[cite: 2824].

- [cite_start]**🥉 Camada Bronze:** Réplica dos dados brutos do dataset público `thelook_ecommerce`, com a adição de uma coluna de metadados `data_ingestao` para controle de carga[cite: 2755]. Esta camada serve como a fonte única da verdade, garantindo que os dados originais estejam sempre disponíveis.

- [cite_start]**🥈 Camada Silver:** Camada de limpeza e conformidade, onde regras de negócio são aplicadas para garantir a qualidade e a consistência dos dados[cite: 2768]. As transformações incluem remoção de registros inválidos, padronização de campos (ex: `UPPER(category)`) e criação de colunas derivadas (ex: `idade_estimada_atual`).

- [cite_start]**🥇 Camada Gold:** Camada de negócio, com tabelas e views desnormalizadas e agregadas, prontas para consumo por dashboards e análises[cite: 2792]. Esta camada é otimizada para performance de consulta e responde diretamente a perguntas de negócio.

---

## 📝 Decisões Técnicas e Raciocínio

[cite_start]Durante a implementação, foram tomadas decisões de engenharia para aumentar a robustez e o valor de negócio do pipeline[cite: 2826]:

1.  **Cálculo de Idade Estimada (Tabela `slv_ecommerce_users`):**
    * **Problema:** A coluna `age` da fonte é um dado estático.
    * **Solução:** Criei a coluna `idade_estimada_atual` reconstruindo uma data de nascimento estimada a partir da `age` e da `created_at`.
    * **Valor:** Transforma um dado impreciso em uma métrica dinâmica e sempre atualizada, crucial para segmentações de clientes por faixa etária.

2.  **Deduplicação Robusta (Tabela `slv_ecommerce_order_items`):**
    * **Problema:** Garantir a unicidade dos itens de pedido.
    * **Solução:** Utilizei a window function `ROW_NUMBER() OVER(PARTITION BY id ...)` para remover duplicatas de sistema, preservando a contagem correta de itens em um mesmo pedido.

3.  **Cálculo de Margem Agregada (Tabela `gld_ecommerce_top_produtos`):**
    * **Problema:** A "média da margem" (`AVG(margem)`) é uma métrica analiticamente incorreta.
    * **Solução:** Calculei a margem percentual agregada `(SUM(margem_bruta) / SUM(custo_total))`, que é uma métrica ponderada e muito mais precisa para o negócio.

4.  **Uso de `LEFT JOIN` na Camada Gold:**
    * **Problema:** `INNER JOIN` pode esconder problemas de integridade de dados (ex: uma venda de um produto que foi deletado do catálogo).
    * **Solução:** Optei por `LEFT JOIN` na criação da `fato_vendas` para garantir que nenhuma venda seja perdida na análise, mantendo a integridade da receita.

---

## [cite_start]⚙️ Como Executar os Scripts [cite: 2828]

O projeto é orquestrado pelo Dataform. Para executar o pipeline completo:
1.  Garanta que as permissões do Agente de Serviço do Dataform estejam corretas no IAM.
2.  No ambiente Dataform, selecione a opção "Executar".
3.  Escolha "Todas as ações" para que o Dataform analise as dependências e execute as tabelas na ordem correta (Bronze → Silver → Gold).

---

## [cite_start]💡 Insights de Negócio [cite: 2830]

A análise das tabelas da Camada Gold permite extrair os seguintes insights:

1.  **Insight 1 (Exemplo):** A categoria **[Ex: 'Tops & Tees']**, apesar de não ser a de maior receita, possui a maior margem percentual média (~XX%), sugerindo que campanhas de marketing focadas nesta categoria podem ter um alto retorno sobre o investimento. *(Baseado em `metricas_mensais_categoria`)*.
2.  **Insight 2 (Exemplo):** Identificamos um segmento de clientes "Campeões" (alta frequência e valor, com compra recente) que representa apenas X% da base de clientes, mas gera Y% da receita total. Um programa de fidelidade para este grupo poderia ser altamente eficaz. *(Baseado em `rfm_clientes`)*.
3.  **Insight 3 (Exemplo):** O produto **[Ex: 'Solid Brass Paperweight']** é o item mais vendido em quantidade, mas sua margem de lucro é uma das mais baixas. Isso pode indicar uma oportunidade de otimização de preço ou de criar combos com produtos de maior margem. *(Baseado em `top_produtos`)*.

---

## [cite_start]쿼리 Consultas de Exemplo [cite: 2832]

Abaixo estão exemplos de como as tabelas Gold podem ser usadas para responder a perguntas de negócio.

**1. Performance de Vendas por Categoria no Último Trimestre:**
```sql
SELECT
  product_category,
  SUM(receita_total) as receita_trimestral,
  AVG(margem_total_percentual) as margem_media
FROM
  `datascience-451918.gld_ecommerce.metricas_mensais_categoria`
WHERE
  -- Exemplo para o último trimestre de 2023 no dataset
  ano_pedido = 2023 AND mes_pedido IN (10, 11, 12)
GROUP BY 1
ORDER BY 2 DESC;