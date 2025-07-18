// Common form fields for Replicate tools
export const commonReplicateFormFields = [
    {
        name: 'api_token',
        label: 'Replicate API Token',
        labelFR: 'Token API Replicate',
        type: 'password',
        required: true,
        placeholder: 'r8_...',
        placeholderFR: 'r8_...',
        description: 'Your Replicate API token from https://replicate.com/account',
        descriptionFR: 'Votre token API Replicate depuis https://replicate.com/account',
    },
];

// Common plans for Replicate tools
export const commonReplicatePlans = ['free', 'pro', 'business', 'enterprise'];

export const replicateIndividualTools = [
    {
        name: 'Replicate - List Models',
        nameFR: 'Replicate - Lister les Modèles',
        slug: 'replicate_list_models',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'List available AI models on Replicate platform with pagination support.',
        descriptionFR: 'Lister les modèles IA disponibles sur la plateforme Replicate avec support de pagination.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Model',
        nameFR: 'Replicate - Obtenir un Modèle',
        slug: 'replicate_get_model',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Get detailed information about a specific AI model including schema and versions.',
        descriptionFR: 'Obtenir des informations détaillées sur un modèle IA spécifique incluant le schéma et les versions.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Search Models',
        nameFR: 'Replicate - Rechercher des Modèles',
        slug: 'replicate_search_models',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Search for AI models on Replicate platform using keywords.',
        descriptionFR: 'Rechercher des modèles IA sur la plateforme Replicate en utilisant des mots-clés.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Model Versions',
        nameFR: 'Replicate - Obtenir les Versions du Modèle',
        slug: 'replicate_get_model_versions',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Get all versions of a specific AI model with version details.',
        descriptionFR: 'Obtenir toutes les versions d\'un modèle IA spécifique avec les détails des versions.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Version Details',
        nameFR: 'Replicate - Obtenir les Détails de la Version',
        slug: 'replicate_get_version_details',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Get detailed information about a specific model version including input/output schema.',
        descriptionFR: 'Obtenir des informations détaillées sur une version spécifique du modèle incluant le schéma d\'entrée/sortie.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Create Prediction',
        nameFR: 'Replicate - Créer une Prédiction',
        slug: 'replicate_create_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Create a new prediction using an AI model with custom input parameters.',
        descriptionFR: 'Créer une nouvelle prédiction en utilisant un modèle IA avec des paramètres d\'entrée personnalisés.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Prediction',
        nameFR: 'Replicate - Obtenir une Prédiction',
        slug: 'replicate_get_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Get the status and results of a prediction with detailed output.',
        descriptionFR: 'Obtenir le statut et les résultats d\'une prédiction avec une sortie détaillée.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Cancel Prediction',
        nameFR: 'Replicate - Annuler une Prédiction',
        slug: 'replicate_cancel_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Cancel a running prediction to stop processing and free resources.',
        descriptionFR: 'Annuler une prédiction en cours pour arrêter le traitement et libérer les ressources.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - List Predictions',
        nameFR: 'Replicate - Lister les Prédictions',
        slug: 'replicate_list_predictions',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'List all your predictions with status and metadata.',
        descriptionFR: 'Lister toutes vos prédictions avec le statut et les métadonnées.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Prediction Logs',
        nameFR: 'Replicate - Obtenir les Logs de Prédiction',
        slug: 'replicate_get_prediction_logs',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Get logs and error information from a prediction for debugging.',
        descriptionFR: 'Obtenir les logs et informations d\'erreur d\'une prédiction pour le débogage.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Generate Code',
        nameFR: 'Replicate - Générer du Code',
        slug: 'replicate_generate_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Generate code in various programming languages using AI models.',
        descriptionFR: 'Générer du code dans différents langages de programmation en utilisant des modèles IA.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Generate Python Code',
        nameFR: 'Replicate - Générer du Code Python',
        slug: 'replicate_generate_python',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Generate Python code with specific formatting, comments, and style guidelines.',
        descriptionFR: 'Générer du code Python avec un formatage spécifique, des commentaires et des directives de style.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Generate JavaScript Code',
        nameFR: 'Replicate - Générer du Code JavaScript',
        slug: 'replicate_generate_javascript',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Generate JavaScript code with framework support and ES version targeting.',
        descriptionFR: 'Générer du code JavaScript avec support de framework et ciblage de version ES.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Generate API Code',
        nameFR: 'Replicate - Générer du Code API',
        slug: 'replicate_generate_api_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Generate API integration code for REST, GraphQL, and WebSocket APIs.',
        descriptionFR: 'Générer du code d\'intégration API pour les APIs REST, GraphQL et WebSocket.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Code Completion',
        nameFR: 'Replicate - Complétion de Code',
        slug: 'replicate_code_completion',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/replicate-logo.png',
        description: 'Complete partial code snippets using AI models with context awareness.',
        descriptionFR: 'Compléter des extraits de code partiels en utilisant des modèles IA avec conscience du contexte.',
        formFields: commonReplicateFormFields,
    },
];

export default replicateIndividualTools;