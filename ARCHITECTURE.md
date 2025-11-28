# Architecture Frontend Next.js + API Backend

Documentation de l'architecture moderne de l'application Gestion des Horaires.

## 🏗️ Vue d'Ensemble

L'application adopte une architecture **API + Frontend** séparant complètement:
- **Backend**: API REST (à implémenter)
- **Frontend**: Application Next.js moderne avec TypeScript et shadcn/ui

```
┌─────────────────────────────────────────────────────────┐
│                    UTILISATEUR                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (Next.js 15+)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Pages (App Router)                              │  │
│  │  - Dashboard (/)                                 │  │
│  │  - Horaires (/schedules)                        │  │
│  │  - Statistiques (/statistics)                   │  │
│  │  - Configuration (/config)                      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Composants                                      │  │
│  │  - UI (shadcn/ui)                               │  │
│  │  - Forms                                        │  │
│  │  - Charts (Recharts)                           │  │
│  │  - Layouts                                      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Lib                                            │  │
│  │  - API Client                                   │  │
│  │  - Validations (Zod)                           │  │
│  │  - Utils                                        │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND API (à implémenter)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Endpoints REST                                  │  │
│  │  - /api/schedules                               │  │
│  │  - /api/statistics                              │  │
│  │  - /api/config                                  │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Business Logic                                  │  │
│  │  - Calculs des horaires                        │  │
│  │  - Statistiques                                 │  │
│  │  - Gestion de config                           │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Data Layer                                      │  │
│  │  - CSV Handler                                  │  │
│  │  - Config Handler                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PERSISTANCE                                │
│  - horaires.csv                                        │
│  - config.json                                         │
└─────────────────────────────────────────────────────────┘
```

## 📁 Structure du Projet

```
calcule-heure-app/
├── frontend/                   # Application Next.js
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   │   ├── layout.tsx     # Layout global
│   │   │   ├── page.tsx       # Dashboard
│   │   │   ├── schedules/     # Page horaires
│   │   │   ├── statistics/    # Page stats
│   │   │   └── config/        # Page config
│   │   │
│   │   ├── components/        # Composants React
│   │   │   ├── ui/           # shadcn/ui
│   │   │   ├── forms/        # Formulaires
│   │   │   ├── charts/       # Graphiques
│   │   │   └── layouts/      # Layouts
│   │   │
│   │   ├── lib/              # Bibliothèques
│   │   │   ├── api.ts        # Client API
│   │   │   ├── utils.ts      # Utilitaires
│   │   │   └── validations.ts # Zod schemas
│   │   │
│   │   └── types/            # Types TS
│   │       └── index.ts
│   │
│   ├── public/               # Assets statiques
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── tailwind.config.ts
│
└── backend/                   # API Backend (à créer)
    ├── api/
    │   ├── routes/
    │   │   ├── schedules.py
    │   │   ├── statistics.py
    │   │   └── config.py
    │   ├── models/
    │   └── services/
    │
    └── calcule_Heure/        # Module existant
        ├── csv_handler.py
        ├── config.py
        └── ...
```

## 🔌 Contrat API

### Endpoints Schedules

#### `GET /api/schedules`
Liste tous les horaires.

**Response:**
```json
[
  {
    "id": "uuid",
    "date_saisie": "2024-11-28T10:00:00",
    "heure_debut": "08:00",
    "heure_debut_pause": "12:00",
    "heure_fin_pause": "13:00",
    "heure_depart_calculee": "16:10",
    "duree_pause_minutes": 60
  }
]
```

#### `POST /api/schedules`
Crée un nouvel horaire.

**Request Body:**
```json
{
  "heure_debut": "08:00",
  "heure_debut_pause": "12:00",
  "heure_fin_pause": "13:00"
}
```

**Response:**
```json
{
  "id": "uuid",
  "date_saisie": "2024-11-28T10:00:00",
  "heure_debut": "08:00",
  "heure_debut_pause": "12:00",
  "heure_fin_pause": "13:00",
  "heure_depart_calculee": "16:10",
  "duree_pause_minutes": 60
}
```

#### `GET /api/schedules/{id}`
Récupère un horaire spécifique.

#### `PUT /api/schedules/{id}`
Modifie un horaire existant.

**Request Body:**
```json
{
  "heure_debut": "08:30",
  "heure_debut_pause": "12:30",
  "heure_fin_pause": "13:30"
}
```

#### `DELETE /api/schedules/{id}`
Supprime un horaire.

### Endpoints Statistics

#### `GET /api/statistics`
Récupère les statistiques moyennes.

**Response:**
```json
{
  "moyenne_arrivee": "08:15",
  "moyenne_depart": "16:25",
  "moyenne_pause_minutes": 55,
  "total_entrees": 42
}
```

#### `GET /api/statistics/charts`
Récupère les données pour les graphiques.

**Response:**
```json
{
  "arrivee": [
    {
      "date": "2024-11-01",
      "heure_debut": "08:00",
      "moyenne": "08:15"
    }
  ],
  "depart": [
    {
      "date": "2024-11-01",
      "heure_depart": "16:10",
      "moyenne": "16:25"
    }
  ],
  "pause": [
    {
      "date": "2024-11-01",
      "duree_pause": 60
    }
  ]
}
```

### Endpoints Config

#### `GET /api/config`
Récupère la configuration actuelle.

**Response:**
```json
{
  "duree_travail_heures": 7,
  "duree_travail_minutes": 10,
  "seuil_pause_minutes": 45,
  "format_heure": "%H:%M",
  "format_date": "%Y-%m-%d %H:%M:%S"
}
```

#### `PUT /api/config`
Met à jour la configuration.

**Request Body:**
```json
{
  "duree_travail_heures": 8,
  "duree_travail_minutes": 0,
  "seuil_pause_minutes": 60
}
```

#### `POST /api/config/reset`
Réinitialise la configuration aux valeurs par défaut.

### Health Check

#### `GET /api/health`
Vérifie l'état de l'API.

**Response:**
```json
{
  "status": "ok"
}
```

## 🎨 Stack Technique Frontend

### Core
- **Next.js 15+** - Framework React avec App Router
- **React 19** - Bibliothèque UI
- **TypeScript 5.7** - Typage statique

### UI & Styling
- **shadcn/ui** - Composants UI accessibles
- **TailwindCSS 3.4** - Framework CSS utility-first
- **Radix UI** - Primitives UI accessibles
- **Lucide React** - Icônes SVG

### Data & Charts
- **Recharts 2.13** - Bibliothèque de graphiques
- **date-fns** - Manipulation de dates
- **Zod 3.24** - Validation de schémas

### Utilities
- **class-variance-authority** - Variantes de classes
- **clsx** - Utilitaire de classes conditionnelles
- **tailwind-merge** - Fusion de classes Tailwind

## 🔄 Flux de Données

### 1. Ajout d'un Horaire

```
User Input → Form Validation (Zod) → API Client → POST /api/schedules
                                                          ↓
User Interface ← Schedule Object ← Response ← Backend Calculation
```

### 2. Affichage des Statistiques

```
Page Load → API Client → GET /api/statistics + /api/statistics/charts
                                     ↓
              Statistics Component ← Data Processing
                                     ↓
              Recharts ← Formatted Data
```

### 3. Configuration

```
Config Form → Validation → API Client → PUT /api/config
                                             ↓
Config State Update ← Response ← Backend Update
```

## 🎯 Fonctionnalités par Page

### Dashboard (`/`)
- **Composants:**
  - Statistics Cards (4 métriques)
  - Schedule Form (ajout rapide)
  - Recent Schedules (5 derniers)

- **API Calls:**
  - `GET /api/statistics`
  - `GET /api/schedules`
  - `POST /api/schedules` (form submit)

### Horaires (`/schedules`)
- **Composants:**
  - Schedules Table (tous les horaires)
  - Delete buttons

- **API Calls:**
  - `GET /api/schedules`
  - `DELETE /api/schedules/{id}`

### Statistiques (`/statistics`)
- **Composants:**
  - Statistics Summary
  - Arrival Chart (Recharts Line)
  - Departure Chart (Recharts Line)
  - Pause Chart (Recharts Bar)

- **API Calls:**
  - `GET /api/statistics`
  - `GET /api/statistics/charts`
  - `GET /api/config` (seuil pause)

### Configuration (`/config`)
- **Composants:**
  - Config Form
  - Current Config Display
  - Reset Button

- **API Calls:**
  - `GET /api/config`
  - `PUT /api/config`
  - `POST /api/config/reset`

## 🔒 Validation des Données

### Côté Client (Zod)

```typescript
// Schedule validation
const scheduleSchema = z.object({
  heure_debut: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
  heure_debut_pause: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
  heure_fin_pause: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
}).refine(data => {
  // Les heures doivent être dans l'ordre croissant
  return parseTime(data.heure_debut) < parseTime(data.heure_debut_pause) &&
         parseTime(data.heure_debut_pause) < parseTime(data.heure_fin_pause);
});

// Config validation
const configSchema = z.object({
  duree_travail_heures: z.number().min(0).max(24),
  duree_travail_minutes: z.number().min(0).max(59),
  seuil_pause_minutes: z.number().min(0).max(180),
});
```

### Côté Backend (à implémenter)

Les mêmes règles de validation doivent être implémentées côté backend pour garantir l'intégrité des données.

## 🚀 Prochaines Étapes

### Phase 1: Backend API
1. Créer l'API REST avec FastAPI ou Flask
2. Implémenter les endpoints définis dans le contrat
3. Intégrer le module existant `calcule_Heure`
4. Ajouter la gestion CORS
5. Tests unitaires et d'intégration

### Phase 2: Intégration
1. Connecter le frontend à l'API backend
2. Tester tous les flux
3. Gérer les erreurs API
4. Optimiser les performances

### Phase 3: Déploiement
1. Dockeriser frontend et backend
2. Configuration CI/CD
3. Variables d'environnement de production
4. Monitoring et logs

### Phase 4: Améliorations
1. Authentification utilisateur
2. Multi-tenancy
3. Export de données (PDF, Excel)
4. Notifications
5. Dark mode
6. PWA (Progressive Web App)

## 📊 Avantages de l'Architecture

### Séparation des Préoccupations
- Frontend: Interface utilisateur et expérience
- Backend: Logique métier et données
- Facilite la maintenance et l'évolution

### Scalabilité
- Frontend et backend peuvent scaler indépendamment
- Possibilité d'ajouter plusieurs frontends (mobile, desktop)

### Technologies Modernes
- Next.js avec App Router pour les performances
- TypeScript pour la sécurité des types
- shadcn/ui pour une UI moderne et accessible

### Développement
- Hot reload rapide avec Next.js
- Type safety bout en bout
- Composants réutilisables
- Validation centralisée

## 🔧 Configuration Recommandée

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (à définir)
```env
CORS_ORIGINS=http://localhost:3000
CSV_PATH=./calcule_Heure/horaires.csv
CONFIG_PATH=./calcule_Heure/config.json
```

## 📚 Documentation Complémentaire

- [Frontend README](./frontend/README.md)
- [API Contract](./API_CONTRACT.md) (à créer)
- [Deployment Guide](./DEPLOYMENT.md) (à créer)

---

**Version:** 2.0.0
**Date:** 2024-11-28
**Auteur:** Architecture moderne API + Frontend
