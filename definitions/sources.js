// Arquivo: definitions/sources.js

// Este código não cria nada.
// Ele apenas "registra" uma tabela ou view que já existe no BigQuery
// como uma fonte de dados oficial para o nosso projeto Dataform.

declare({
  schema: "brz_ga4",
  name: "raw_ga_sessions"
});