# Frontend Next.js - Gestion des Horaires

Application web moderne pour la gestion et l'analyse des horaires de travail, construite avec Next.js 15, TypeScript, shadcn/ui et Recharts.

## 🚀 Technologies

- **Next.js 15+** - Framework React avec App Router
- **TypeScript** - Type safety et meilleure expérience développeur
- **shadcn/ui** - Composants UI modernes et accessibles
- **TailwindCSS** - Styling utilitaire
- **Recharts** - Graphiques interactifs
- **Zod** - Validation de schémas
- **Lucide React** - Icônes modernes

## 📋 Prérequis

- Node.js 18+
- npm, yarn ou pnpm

## 🔧 Installation

```bash
# Installer les dépendances
npm install

# Copier le fichier d'environnement
cp .env.example .env.local

# Configurer l'URL de l'API dans .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎯 Démarrage

### Mode Développement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:3000`

### Mode Production

```bash
# Build l'application
npm run build

# Démarrer le serveur de production
npm start
```

## 📁 Structure du Projet

```
frontend/
├── src/
│   ├── app/                    # Pages Next.js (App Router)
│   │   ├── layout.tsx         # Layout principal
│   │   ├── page.tsx           # Dashboard / Page d'accueil
│   │   ├── schedules/         # Page des horaires
│   │   ├── statistics/        # Page des statistiques
│   │   └── config/            # Page de configuration
│   │
│   ├── components/            # Composants React
│   │   ├── ui/               # Composants shadcn/ui
│   │   ├── forms/            # Formulaires
│   │   ├── charts/           # Graphiques Recharts
│   │   └── layouts/          # Layouts
│   │
│   ├── lib/                  # Bibliothèques et utilitaires
│   │   ├── api.ts           # Client API
│   │   ├── utils.ts         # Fonctions utilitaires
│   │   └── validations.ts   # Schémas Zod
│   │
│   └── types/               # Types TypeScript
│       └── index.ts
│
├── public/                  # Fichiers statiques
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.ts
```

## 🎨 Pages

### 1. Dashboard (`/`)
- Vue d'ensemble des statistiques
- Formulaire d'ajout rapide d'horaire
- Affichage des 5 derniers horaires

### 2. Horaires (`/schedules`)
- Liste complète de tous les horaires
- Tableau avec toutes les données
- Suppression d'horaires

### 3. Statistiques (`/statistics`)
- Graphique d'évolution des heures d'arrivée
- Graphique d'évolution des heures de départ
- Graphique des durées de pause avec code couleur
- Moyennes calculées

### 4. Configuration (`/config`)
- Réglage de la durée de travail
- Réglage du seuil de pause
- Réinitialisation aux valeurs par défaut

## 🔌 API Endpoints

Le frontend communique avec l'API backend via les endpoints suivants:

```typescript
// Schedules
GET    /api/schedules              // Liste tous les horaires
POST   /api/schedules              // Créer un nouvel horaire
GET    /api/schedules/{id}         // Détail d'un horaire
PUT    /api/schedules/{id}         // Modifier un horaire
DELETE /api/schedules/{id}         // Supprimer un horaire

// Statistics
GET    /api/statistics             // Statistiques (moyennes)
GET    /api/statistics/charts      // Données pour graphiques

// Config
GET    /api/config                 // Configuration actuelle
PUT    /api/config                 // Mettre à jour la config
POST   /api/config/reset           // Réinitialiser la config

// Health
GET    /api/health                 // Health check
```

## 🎨 Composants UI Disponibles

Le projet utilise shadcn/ui avec les composants suivants:

- `Button` - Boutons avec variantes
- `Card` - Cartes de contenu
- `Input` - Champs de saisie
- `Label` - Labels de formulaire
- `Tabs` - Onglets

## 🔧 Scripts Disponibles

```bash
# Développement
npm run dev

# Build pour production
npm run build

# Démarrage en production
npm start

# Linting
npm run lint

# Type checking
npm run type-check
```

## 🌐 Variables d'Environnement

Créez un fichier `.env.local` avec:

```env
# URL de l'API backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# ou pour la production
NEXT_PUBLIC_API_URL=https://api.votre-domaine.com
```

## 📝 Validation des Données

Le projet utilise Zod pour la validation:

```typescript
// Validation d'horaire
scheduleSchema.parse({
  heure_debut: "08:00",
  heure_debut_pause: "12:00",
  heure_fin_pause: "13:00"
});

// Validation de config
configSchema.parse({
  duree_travail_heures: 7,
  duree_travail_minutes: 10,
  seuil_pause_minutes: 45
});
```

## 🎯 Fonctionnalités

- ✅ Ajout d'horaires avec calcul automatique de l'heure de départ
- ✅ Visualisation de tous les horaires en tableau
- ✅ Graphiques interactifs (arrivée, départ, pause)
- ✅ Statistiques moyennes
- ✅ Configuration personnalisable
- ✅ Validation des données côté client
- ✅ Interface responsive
- ✅ Mode sombre (prévu dans shadcn/ui)

## 🔒 Type Safety

Le projet est entièrement typé avec TypeScript en mode strict:

```typescript
// Types d'API
interface Schedule {
  id: string;
  date_saisie: string;
  heure_debut: string;
  heure_debut_pause: string;
  heure_fin_pause: string;
  heure_depart_calculee: string;
  duree_pause_minutes?: number;
}
```

## 🎨 Personnalisation

### Modifier le thème

Éditez `tailwind.config.ts` et `src/app/globals.css` pour personnaliser:
- Couleurs
- Espacements
- Polices
- Animations

### Ajouter des composants shadcn/ui

```bash
# Ajouter un nouveau composant
npx shadcn@latest add [component-name]
```

## 🐛 Dépannage

### Port déjà utilisé
```bash
# Utiliser un autre port
PORT=3001 npm run dev
```

### Erreurs de build TypeScript
```bash
# Vérifier les erreurs
npm run type-check
```

### Erreurs de connexion API
- Vérifier que l'API backend est démarrée
- Vérifier l'URL dans `.env.local`
- Vérifier les CORS sur le backend

## 📚 Ressources

- [Documentation Next.js](https://nextjs.org/docs)
- [Documentation shadcn/ui](https://ui.shadcn.com/)
- [Documentation Recharts](https://recharts.org/)
- [Documentation TailwindCSS](https://tailwindcss.com/docs)
- [Documentation TypeScript](https://www.typescriptlang.org/docs/)

## 🤝 Contribution

1. Forker le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Committer (`git commit -m 'Add AmazingFeature'`)
4. Pousser (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.
