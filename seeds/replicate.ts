import { ToolFormField, ToolPlan } from '../types/tools';

// Common form fields for Replicate tools
export const commonReplicateFormFields: ToolFormField[] = [
    {
        name: 'api_token',
        label: 'Replicate API Token',
        labelFR: 'Token API Replicate',
        type: 'password',
        required: true,
        placeholder: 'r8_xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        placeholderFR: 'r8_xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        description: 'Your Replicate API token for authentication',
        descriptionFR: 'Votre token API Replicate pour l\'authentification',
        validation: {
            minLength: 40,
            pattern: '^r8_[a-zA-Z0-9]{32}$'
        }
    }
];

// Common plans for Replicate tools
export const commonReplicatePlans: ToolPlan[] = [
    'FREE',
    'STARTER',
    'PROFESSIONAL',
    'ENTERPRISE'
];

// Individual Replicate tools
export const replicateIndividualTools = [
    // Model Management Tools
    {
        name: 'Replicate - List Models',
        nameFR: 'Replicate - Lister les Modèles',
        slug: 'replicate_list_models',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/list-models.png',
        description: 'List available Replicate models with pagination support.',
        descriptionFR: 'Lister les modèles Replicate disponibles avec support de pagination.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Model',
        nameFR: 'Replicate - Obtenir un Modèle',
        slug: 'replicate_get_model',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/get-model.png',
        description: 'Get detailed information about a specific Replicate model.',
        descriptionFR: 'Obtenir des informations détaillées sur un modèle Replicate spécifique.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Create Model',
        nameFR: 'Replicate - Créer un Modèle',
        slug: 'replicate_create_model',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/create-model.png',
        description: 'Create a new Replicate model with specified configuration.',
        descriptionFR: 'Créer un nouveau modèle Replicate avec la configuration spécifiée.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Update Model',
        nameFR: 'Replicate - Mettre à Jour un Modèle',
        slug: 'replicate_update_model',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/update-model.png',
        description: 'Update an existing Replicate model\'s configuration.',
        descriptionFR: 'Mettre à jour la configuration d\'un modèle Replicate existant.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Delete Model',
        nameFR: 'Replicate - Supprimer un Modèle',
        slug: 'replicate_delete_model',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/delete-model.png',
        description: 'Delete a Replicate model permanently.',
        descriptionFR: 'Supprimer définitivement un modèle Replicate.',
        formFields: commonReplicateFormFields,
    },

    // Prediction Management Tools
    {
        name: 'Replicate - Create Prediction',
        nameFR: 'Replicate - Créer une Prédiction',
        slug: 'replicate_create_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/create-prediction.png',
        description: 'Create a new prediction using a Replicate model.',
        descriptionFR: 'Créer une nouvelle prédiction en utilisant un modèle Replicate.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Get Prediction',
        nameFR: 'Replicate - Obtenir une Prédiction',
        slug: 'replicate_get_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/get-prediction.png',
        description: 'Get the status and results of a specific Replicate prediction.',
        descriptionFR: 'Obtenir le statut et les résultats d\'une prédiction Replicate spécifique.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Cancel Prediction',
        nameFR: 'Replicate - Annuler une Prédiction',
        slug: 'replicate_cancel_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/cancel-prediction.png',
        description: 'Cancel a running Replicate prediction.',
        descriptionFR: 'Annuler une prédiction Replicate en cours d\'exécution.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - List Predictions',
        nameFR: 'Replicate - Lister les Prédictions',
        slug: 'replicate_list_predictions',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/list-predictions.png',
        description: 'List your Replicate predictions with pagination support.',
        descriptionFR: 'Lister vos prédictions Replicate avec support de pagination.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Stream Prediction',
        nameFR: 'Replicate - Diffuser une Prédiction',
        slug: 'replicate_stream_prediction',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/stream-prediction.png',
        description: 'Stream a Replicate prediction and wait for completion.',
        descriptionFR: 'Diffuser une prédiction Replicate et attendre la completion.',
        formFields: commonReplicateFormFields,
    },

    // Code Generation Tools
    {
        name: 'Replicate - Generate Code',
        nameFR: 'Replicate - Générer du Code',
        slug: 'replicate_generate_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/generate-code.png',
        description: 'Generate code using AI models on Replicate.',
        descriptionFR: 'Générer du code en utilisant des modèles IA sur Replicate.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Optimize Code',
        nameFR: 'Replicate - Optimiser le Code',
        slug: 'replicate_optimize_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/optimize-code.png',
        description: 'Optimize code for performance, readability, or other aspects using AI.',
        descriptionFR: 'Optimiser le code pour la performance, la lisibilité ou d\'autres aspects avec l\'IA.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Debug Code',
        nameFR: 'Replicate - Déboguer le Code',
        slug: 'replicate_debug_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/debug-code.png',
        description: 'Debug code and find solutions to errors using AI.',
        descriptionFR: 'Déboguer le code et trouver des solutions aux erreurs avec l\'IA.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Explain Code',
        nameFR: 'Replicate - Expliquer le Code',
        slug: 'replicate_explain_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/explain-code.png',
        description: 'Get detailed explanations of code functionality using AI.',
        descriptionFR: 'Obtenir des explications détaillées sur la fonctionnalité du code avec l\'IA.',
        formFields: commonReplicateFormFields,
    },
    {
        name: 'Replicate - Convert Code',
        nameFR: 'Replicate - Convertir le Code',
        slug: 'replicate_convert_code',
        plans: commonReplicatePlans,
        imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/convert-code.png',
        description: 'Convert code from one programming language to another using AI.',
        descriptionFR: 'Convertir le code d\'un langage de programmation à un autre avec l\'IA.',
        formFields: commonReplicateFormFields,
    },
];

// Grouped tools by category
export const replicateToolCategories = {
    models: {
        name: 'Model Management',
        nameFR: 'Gestion des Modèles',
        description: 'Tools for managing Replicate models',
        descriptionFR: 'Outils pour gérer les modèles Replicate',
        tools: replicateIndividualTools.slice(0, 5), // First 5 tools
    },
    predictions: {
        name: 'Prediction Management',
        nameFR: 'Gestion des Prédictions',
        description: 'Tools for executing and managing predictions',
        descriptionFR: 'Outils pour exécuter et gérer les prédictions',
        tools: replicateIndividualTools.slice(5, 10), // Next 5 tools
    },
    codeGeneration: {
        name: 'Code Generation',
        nameFR: 'Génération de Code',
        description: 'AI-powered code generation and optimization tools',
        descriptionFR: 'Outils de génération et d\'optimisation de code alimentés par l\'IA',
        tools: replicateIndividualTools.slice(10, 15), // Last 5 tools
    },
};

// Complete Replicate toolkit
export const replicateToolkit = {
    name: 'Replicate AI Toolkit',
    nameFR: 'Boîte à Outils IA Replicate',
    slug: 'replicate_toolkit',
    plans: commonReplicatePlans,
    imageUrl: 'https://static.swiftask.ai/swiftaskagent/replicate/toolkit.png',
    description: 'Complete toolkit for Replicate AI platform with model management, predictions, and code generation.',
    descriptionFR: 'Boîte à outils complète pour la plateforme IA Replicate avec gestion des modèles, prédictions et génération de code.',
    formFields: commonReplicateFormFields,
    categories: replicateToolCategories,
    totalTools: 15,
};

// Export all tools
export default replicateIndividualTools;

// Additional exports for specific use cases
export {
    commonReplicateFormFields,
    commonReplicatePlans,
    replicateToolCategories,
    replicateToolkit,
};

// Tool metadata for documentation
export const replicateToolsMetadata = {
    version: '1.0.0',
    author: 'Jonathan Toky',
    description: 'Comprehensive Replicate AI tools for model management, predictions, and code generation',
    documentation: 'https://docs.replicate.com',
    repository: 'https://github.com/jonathantoky/replicate-agent-tools',
    license: 'MIT',
    keywords: ['replicate', 'ai', 'machine-learning', 'code-generation', 'predictions'],
    categories: ['AI/ML', 'Code Generation', 'Model Management'],
    requirements: {
        python: '>=3.8',
        packages: ['requests', 'langchain-core', 'pydantic'],
    },
    features: [
        'Model management (list, get, create, update, delete)',
        'Prediction execution and monitoring',
        'AI-powered code generation',
        'Code optimization and debugging',
        'Code explanation and conversion',
        'Real-time streaming support',
        'Comprehensive error handling',
        'Full test coverage',
    ],
};