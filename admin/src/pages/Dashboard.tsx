import PageLoadingOverlay from '../components/ui/PageLoadingOverlay';
import { Activity, AlertCircle, ArrowDownRight, ArrowUpRight, Shield, Users } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import {
  Area,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '../components/ui/card';
import monitoringService, { PerformanceData, SystemMetrics } from '../services/monitoring.service';

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [performanceData, setPerformanceData] = useState<PerformanceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [metricsData, performanceData] = await Promise.all([
          monitoringService.getSystemMetrics(),
          monitoringService.getPerformanceData()
        ]);

        setMetrics(metricsData);
        setPerformanceData(performanceData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-red-500 text-center p-6 rounded-lg bg-red-50">
          <AlertCircle className="h-8 w-8 mx-auto mb-2" />
          <p className="text-base font-medium">{error}</p>
        </div>
      </div>
    );
  }

  return loading ? (
    <PageLoadingOverlay />
  ) : (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
          Dashboard
        </h1>
        <div className="text-xs text-muted-foreground">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* System Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Active Users</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Users className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{metrics?.activeUsers.toLocaleString()}</div>
            <div className="flex items-center text-xs text-green-600 mt-0.5">
              <ArrowUpRight className="h-3 w-3 mr-0.5" />
              <span>12% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Total Brokers</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Shield className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{metrics?.totalBrokers.toLocaleString()}</div>
            <div className="flex items-center text-xs text-green-600 mt-0.5">
              <ArrowUpRight className="h-3 w-3 mr-0.5" />
              <span>8% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Recent Leads</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Activity className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{metrics?.recentLeads.toLocaleString()}</div>
            <div className="flex items-center text-xs text-red-600 mt-0.5">
              <ArrowDownRight className="h-3 w-3 mr-0.5" />
              <span>3% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">System Health</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <AlertCircle className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className={`text-xl font-bold capitalize ${metrics?.systemHealth === 'healthy' ? 'text-green-600' :
              metrics?.systemHealth === 'warning' ? 'text-yellow-600' :
                'text-red-600'
              }`}>
              {metrics?.systemHealth}
            </div>
            <div className="text-xs text-muted-foreground mt-0.5">
              All systems operational
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="p-3">
            <CardTitle className="text-base font-semibold">API Performance</CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={performanceData}>
                  <defs>
                    <linearGradient id="apiPerformanceGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0284c7" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#0284c7" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="time"
                    className="text-xs text-muted-foreground"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <YAxis
                    className="text-xs text-muted-foreground"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--background))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: 'var(--radius)'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="responseTime"
                    stroke="false"
                    fillOpacity={1}
                    fill="url(#apiPerformanceGradient)"
                  />
                  <Line
                    type="monotone"
                    dataKey="responseTime"
                    stroke="#0284c7"
                    name="Response Time (ms)"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="p-3">
            <CardTitle className="text-base font-semibold">Cache Performance</CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={performanceData}>
                  <defs>
                    <linearGradient id="cachePerformanceGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0284c7" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#0284c7" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="time"
                    className="text-xs text-muted-foreground"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <YAxis
                    className="text-xs text-muted-foreground"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--background))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: 'var(--radius)'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="hitRate"
                    stroke="false"
                    fillOpacity={1}
                    fill="url(#cachePerformanceGradient)"
                  />
                  <Line
                    type="monotone"
                    dataKey="hitRate"
                    stroke="#0284c7"
                    name="Hit Rate"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-3">
          <CardTitle className="text-base font-semibold">Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="p-3 pt-0">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-primary-200 bg-primary-50 hover:bg-primary-100 text-primary-700 h-10 px-4 py-2">
              <Shield className="h-4 w-4 mr-2" />
              Manage Cache
            </button>
            <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-primary-200 bg-primary-50 hover:bg-primary-100 text-primary-700 h-10 px-4 py-2">
              <Activity className="h-4 w-4 mr-2" />
              Check System Health
            </button>
            <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-primary-200 bg-primary-50 hover:bg-primary-100 text-primary-700 h-10 px-4 py-2">
              <AlertCircle className="h-4 w-4 mr-2" />
              View Security Events
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard; 