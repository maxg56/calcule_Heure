/**
 * API Client for Calcule Heure Backend
 * Handles all HTTP requests to the FastAPI backend
 */

import type {
  Schedule,
  CreateScheduleInput,
  UpdateScheduleInput,
  Config,
  UpdateConfigInput,
  Statistics,
  ChartsData,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api';

/**
 * Custom error class for API errors
 */
class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Helper function to handle API responses
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    let errorDetails;

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
      errorDetails = errorData;
    } catch {
      // If response is not JSON, use status text
    }

    throw new ApiError(errorMessage, response.status, errorDetails);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return null as T;
  }

  try {
    return await response.json();
  } catch {
    throw new ApiError('Invalid JSON response from server', response.status);
  }
}

/**
 * Helper function to make API requests
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${API_PREFIX}${endpoint}`;

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  const response = await fetch(url, config);
  return handleResponse<T>(response);
}

/**
 * Schedule API endpoints
 */
export const scheduleApi = {
  /**
   * Get all schedules
   */
  async getAll(): Promise<Schedule[]> {
    return request<Schedule[]>('/schedules/');
  },

  /**
   * Get a single schedule by ID
   */
  async getById(id: string): Promise<Schedule> {
    return request<Schedule>(`/schedules/${id}`);
  },

  /**
   * Create a new schedule
   */
  async create(data: CreateScheduleInput): Promise<Schedule> {
    return request<Schedule>('/schedules/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing schedule
   */
  async update(id: string, data: UpdateScheduleInput): Promise<Schedule> {
    return request<Schedule>(`/schedules/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a schedule
   */
  async delete(id: string): Promise<void> {
    return request<void>(`/schedules/${id}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Statistics API endpoints
 */
export const statisticsApi = {
  /**
   * Get statistics summary
   */
  async getSummary(): Promise<Statistics> {
    return request<Statistics>('/statistics/');
  },

  /**
   * Get charts data
   */
  async getChartsData(): Promise<ChartsData> {
    return request<ChartsData>('/statistics/charts');
  },
};

/**
 * Config API endpoints
 */
export const configApi = {
  /**
   * Get current configuration
   */
  async get(): Promise<Config> {
    return request<Config>('/config/');
  },

  /**
   * Update configuration
   */
  async update(data: UpdateConfigInput): Promise<Config> {
    return request<Config>('/config/', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Reset configuration to defaults
   */
  async reset(): Promise<Config> {
    return request<Config>('/config/reset', {
      method: 'POST',
    });
  },
};

/**
 * Main API object - backwards compatible with existing code
 */
export const api = {
  // Schedule methods
  getSchedules: scheduleApi.getAll,
  getSchedule: scheduleApi.getById,
  createSchedule: scheduleApi.create,
  updateSchedule: scheduleApi.update,
  deleteSchedule: scheduleApi.delete,

  // Statistics methods
  getStatistics: statisticsApi.getSummary,
  getChartsData: statisticsApi.getChartsData,

  // Config methods
  getConfig: configApi.get,
  updateConfig: configApi.update,
  resetConfig: configApi.reset,
};

export default api;
