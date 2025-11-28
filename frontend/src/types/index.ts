// Schedule types
export interface Schedule {
  id: string;
  date_saisie: string;
  heure_debut: string;
  heure_debut_pause: string;
  heure_fin_pause: string;
  heure_depart_calculee: string;
  duree_pause_minutes?: number;
}

export interface CreateScheduleInput {
  heure_debut: string;
  heure_debut_pause: string;
  heure_fin_pause: string;
}

export interface UpdateScheduleInput extends Partial<CreateScheduleInput> {
  id: string;
}

// Configuration types
export interface Config {
  duree_travail_heures: number;
  duree_travail_minutes: number;
  seuil_pause_minutes: number;
  format_heure: string;
  format_date: string;
}

export interface UpdateConfigInput {
  duree_travail_heures?: number;
  duree_travail_minutes?: number;
  seuil_pause_minutes?: number;
}

// Statistics types
export interface Statistics {
  moyenne_arrivee: string;
  moyenne_depart: string;
  moyenne_pause_minutes: number;
  total_entrees: number;
}

export interface ChartDataPoint {
  date: string;
  heure_debut?: string;
  heure_depart?: string;
  duree_pause?: number;
  moyenne?: string;
}

export interface ChartsData {
  arrivee: ChartDataPoint[];
  depart: ChartDataPoint[];
  pause: ChartDataPoint[];
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface ApiError {
  message: string;
  status: number;
  details?: string;
}
