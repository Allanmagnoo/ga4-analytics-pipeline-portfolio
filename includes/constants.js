// Project Constants
const PROJECT_ID = "datascience-473223";

// Dataset Names
const DATASETS = {
    BRONZE: "brz_ecommerce",
    SILVER: "slv_ecommerce",
    GOLD: "gld_ecommerce",
    ASSERTIONS: "qa_assertions"
};

// Business Logic Constants
const BUSINESS_LOGIC = {
    INCREMENTAL_WINDOW_DAYS: 7,
    HIGH_VALUE_THRESHOLD: 500,
    VIP_ORDER_COUNT: 5
};

module.exports = {
    PROJECT_ID,
    DATASETS,
    BUSINESS_LOGIC
};
