// Arquivo: definitions/sources.js

// Este código não cria nada.
// Ele apenas "registra" uma tabela ou view que já existe no BigQuery
// como uma fonte de dados oficial para o nosso projeto Dataform.

declare({
    schema: "brz_ga4",
    name: "raw_ga_sessions"
});

// 2. Declara a tabela de clientes brutos do CRM
declare({
  schema: "brz_crm", // O schema do seu sistema de CRM
  name: "raw_customers"
});