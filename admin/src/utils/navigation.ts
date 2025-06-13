import apiService from '../services/api.service';

export const getPath = (path: string): string => {
  const adminPrefix = apiService.getAdminPrefix();
  // Remove leading slash if present to avoid double slashes
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return `${adminPrefix}/${cleanPath}`;
};

export const navigateTo = (path: string): void => {
  window.location.href = getPath(path);
};

export const getCurrentPath = (): string => {
  const adminPrefix = apiService.getAdminPrefix();
  const path = window.location.pathname;
  // Remove admin prefix from path if in production
  return path.startsWith(adminPrefix) ? path.slice(adminPrefix.length) : path;
}; 