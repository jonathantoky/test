#!/bin/bash

# 🚀 Script de migration des outils Replicate vers SynsLab/ai-powered-todolist
# Ce script copie tous les fichiers nécessaires depuis le repository test

echo "🚀 Migration des outils Replicate vers SynsLab/ai-powered-todolist"
echo "================================================================="

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier qu'on est dans le bon repository
if [[ ! -d ".git" ]]; then
    print_error "Ce script doit être exécuté depuis la racine d'un repository git"
    exit 1
fi

print_info "Vérification du repository..."
REPO_URL=$(git remote get-url origin 2>/dev/null)
if [[ "$REPO_URL" != *"SynsLab/ai-powered-todolist"* ]]; then
    print_warning "Attention: Ce ne semble pas être le repository SynsLab/ai-powered-todolist"
    print_info "Repository actuel: $REPO_URL"
    read -p "Continuer quand même? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Vérifier qu'on est sur la bonne branche
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$CURRENT_BRANCH" != "feature/replicate-agent-tools" ]]; then
    print_info "Branche actuelle: $CURRENT_BRANCH"
    print_info "Création de la branche feature/replicate-agent-tools..."
    
    # S'assurer qu'on est sur staging
    git checkout staging
    git pull origin staging
    
    # Créer la nouvelle branche
    git checkout -b feature/replicate-agent-tools
    print_status "Branche feature/replicate-agent-tools créée"
fi

# Créer les dossiers nécessaires
print_info "Création des dossiers..."
mkdir -p agent_tools/replicate
mkdir -p client
mkdir -p tests
mkdir -p seeds

print_status "Dossiers créés"

# Instructions pour copier les fichiers
print_info "📋 INSTRUCTIONS DE MIGRATION"
echo "=============================="
echo ""
print_warning "ÉTAPE 1: Copiez les fichiers suivants depuis le repository test:"
echo ""
echo "  📁 agent_tools/replicate/"
echo "    ├── __init__.py                 (Package initialization)"
echo "    ├── replicate_tools.py          (Main tools orchestrator - 15 tools)"
echo "    ├── models.py                   (Model management tools - 5 tools)"
echo "    ├── predictions.py              (Prediction execution tools - 5 tools)"
echo "    └── code_generation.py          (AI code generation tools - 5 tools)"
echo ""
echo "  📁 client/"
echo "    ├── __init__.py                 (Client package initialization)"
echo "    ├── replicate_auth.py           (Authentication system)"
echo "    └── config.py                   (Configuration management)"
echo ""
echo "  📁 tests/"
echo "    └── test_replicate_tools.py     (Comprehensive test suite)"
echo ""
echo "  📁 seeds/"
echo "    └── replicate.ts                (TypeScript tool definitions)"
echo ""
echo "  📄 Fichiers racine:"
echo "    ├── load_tools.py               (Integration examples)"
echo "    ├── pr_description.md           (Pull request description)"
echo "    └── README_REPLICATE.md         (Documentation des outils Replicate)"
echo ""

print_warning "ÉTAPE 2: Une fois tous les fichiers copiés, appuyez sur Entrée..."
read -p "Fichiers copiés? Appuyez sur Entrée pour continuer..."

# Vérifier que les fichiers essentiels sont présents
REQUIRED_FILES=(
    "agent_tools/replicate/__init__.py"
    "agent_tools/replicate/replicate_tools.py"
    "agent_tools/replicate/models.py"
    "agent_tools/replicate/predictions.py"
    "agent_tools/replicate/code_generation.py"
    "client/__init__.py"
    "client/replicate_auth.py"
    "client/config.py"
    "tests/test_replicate_tools.py"
    "seeds/replicate.ts"
    "load_tools.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        MISSING_FILES+=("$file")
    fi
done

if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
    print_error "Fichiers manquants:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    print_warning "Veuillez copier tous les fichiers requis avant de continuer."
    exit 1
fi

print_status "Tous les fichiers requis sont présents"

# Ajouter les fichiers à git
print_info "Ajout des fichiers à git..."
git add .

# Vérifier les changements
if git diff --cached --quiet; then
    print_warning "Aucun changement détecté. Les fichiers sont peut-être déjà commitées."
else
    print_status "Fichiers ajoutés à git"
fi

# Commit des changements
print_info "Commit des changements..."
COMMIT_MESSAGE="feat: Add comprehensive Replicate agent tools

- Add model management tools (list, get, create, versions)
- Add prediction execution tools (create, monitor, cancel, run)
- Add AI-powered code generation tools (generate, optimize, debug, dockerfile, requirements)
- Add authentication system with token management
- Add configuration system with environment support
- Add comprehensive test suite
- Add TypeScript seed definitions
- Add integration examples and documentation

Features:
✅ 15 comprehensive Replicate tools
✅ Model management capabilities
✅ Prediction execution and monitoring
✅ AI-powered code generation
✅ Authentication and token management
✅ Configuration management
✅ Comprehensive testing
✅ LangChain integration ready
✅ Full documentation

Repository: SynsLab/ai-powered-todolist
Target branch: staging"

git commit -m "$COMMIT_MESSAGE"
print_status "Changements commitées"

# Push vers origin
print_info "Push vers origin..."
if git push origin feature/replicate-agent-tools; then
    print_status "Branch pushée vers origin avec succès"
else
    print_error "Erreur lors du push. Vérifiez vos permissions."
    exit 1
fi

# Instructions pour créer la PR
echo ""
print_status "🎉 Migration terminée avec succès!"
echo "=================================="
echo ""
print_info "📋 PROCHAINES ÉTAPES:"
echo "1. 🌐 Allez sur: https://github.com/SynsLab/ai-powered-todolist"
echo "2. 🔄 Cliquez sur 'New Pull Request' ou 'Compare & pull request'"
echo "3. ⚙️  Configurez la PR:"
echo "   - Base repository: SynsLab/ai-powered-todolist"
echo "   - Base branch: staging"
echo "   - Head repository: SynsLab/ai-powered-todolist"
echo "   - Compare branch: feature/replicate-agent-tools"
echo "4. 📝 Titre: feat: Add Comprehensive Replicate Agent Tools"
echo "5. 📄 Description: Utilisez le contenu de pr_description.md"
echo ""
print_info "📊 RÉSUMÉ DE LA MIGRATION:"
echo "✅ 15 outils Replicate ajoutés"
echo "✅ Système d'authentification inclus"
echo "✅ Système de configuration inclus"
echo "✅ Tests complets ajoutés"
echo "✅ Définitions TypeScript incluses"
echo "✅ Documentation complète fournie"
echo "✅ Intégration LangChain prête"
echo ""
print_status "🚀 Prêt pour la review et le merge!"
echo ""
print_info "🔗 Lien direct pour créer la PR:"
echo "https://github.com/SynsLab/ai-powered-todolist/compare/staging...feature/replicate-agent-tools"