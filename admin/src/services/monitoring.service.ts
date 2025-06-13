import apiService from './api.service';

export interface SystemMetrics {
  activeUsers: number;
  totalBrokers: number;
  recentLeads: number;
  systemHealth: 'healthy' | 'warning' | 'critical';
  apiResponseTime: number;
  cacheHitRate: number;
  errorRate: number;
}

export interface PerformanceData {
  time: string;
  responseTime: number;
  hitRate: number;
}

interface AnalyticsResponse {
  summary: {
    total_api_requests: number;
    financial_analysis_requests: number;
    cache_hit_rate_percentage: number;
  };
  detailed_analytics: {
    api_request: {
      daily: Array<{
        date: string;
        count: number;
      }>;
    };
  };
}

interface PerformanceMetricsResponse {
  performance_metrics: {
    api: {
      total_requests_24h: number;
      error_rate_percentage: number;
    };
    cache: {
      hit_rate: number;
    };
  };
}

interface SystemStatusResponse {
  system_status: {
    overall_status: 'healthy' | 'warning' | 'critical';
  };
}

class MonitoringService {
  async getSystemMetrics(): Promise<SystemMetrics> {
    try {
      const [analytics, performance, systemStatus] = await Promise.all([
        apiService.get<AnalyticsResponse>('/monitoring/analytics'),
        apiService.get<PerformanceMetricsResponse>('/monitoring/performance-metrics'),
        apiService.get<SystemStatusResponse>('/monitoring/system-status')
      ]);

      // Transform the data to match our frontend interface
      return {
        activeUsers: analytics.summary.total_api_requests || 0,
        totalBrokers: analytics.summary.financial_analysis_requests || 0,
        recentLeads: analytics.summary.total_api_requests || 0,
        systemHealth: systemStatus.system_status.overall_status,
        apiResponseTime: performance.performance_metrics.api.total_requests_24h || 0,
        cacheHitRate: performance.performance_metrics.cache.hit_rate || 0,
        errorRate: performance.performance_metrics.api.error_rate_percentage || 0
      };
    } catch (error) {
      console.error('Error fetching system metrics:', error);
      throw error;
    }
  }

  async getPerformanceData(): Promise<PerformanceData[]> {
    try {
      const [analytics, performance] = await Promise.all([
        apiService.get<AnalyticsResponse>('/monitoring/analytics'),
        apiService.get<PerformanceMetricsResponse>('/monitoring/performance-metrics')
      ]);

      // Transform the data into time series format
      const dailyData = analytics.detailed_analytics.api_request.daily || [];
      return dailyData.map((day) => ({
        time: new Date(day.date).toLocaleTimeString(),
        responseTime: day.count || 0,
        hitRate: performance.performance_metrics.cache.hit_rate || 0
      }));
    } catch (error) {
      console.error('Error fetching performance data:', error);
      throw error;
    }
  }

  async getSecurityEvents() {
    try {
      return await apiService.get('/monitoring/security-events');
    } catch (error) {
      console.error('Error fetching security events:', error);
      throw error;
    }
  }

  async getCacheStats() {
    try {
      return await apiService.get('/monitoring/cache-stats');
    } catch (error) {
      console.error('Error fetching cache stats:', error);
      throw error;
    }
  }
}

export default new MonitoringService(); 