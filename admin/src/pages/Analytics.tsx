import { Activity, AlertCircle, ArrowUpRight, Shield, TrendingUp, Users } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import {
  Area,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
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
import financialAnalysisService, { FinancialAnalysis } from '../services/financial-analysis.service';
import monitoringService, { PerformanceData, SystemMetrics } from '../services/monitoring.service';
import PageLoadingOverlay from '../components/ui/PageLoadingOverlay';

const COLORS = ['#0284c7', '#0ea5e9', '#38bdf8', '#7dd3fc', '#bae6fd'];

const Analytics: React.FC = () => {
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [performanceData, setPerformanceData] = useState<PerformanceData[]>([]);
  const [financialData, setFinancialData] = useState<FinancialAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const [metrics, perfData, finData] = await Promise.all([
          monitoringService.getSystemMetrics(),
          monitoringService.getPerformanceData(),
          financialAnalysisService.getMyFinancialAnalysis()
        ]);

        setSystemMetrics(metrics);
        setPerformanceData(perfData);
        setFinancialData(finData);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
        setError('Failed to load analytics data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <PageLoadingOverlay />
    );
  }

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

  if (!systemMetrics || !financialData) {
    return null;
  }

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low': return '#00C49F';
      case 'medium': return '#FFBB28';
      case 'high': return '#FF8042';
      default: return '#8884D8';
    }
  };

  // Default values for safety
  const averageConversionRate = financialData?.averageConversionRate ?? 0;
  const marketTrends = financialData?.marketTrends ?? [];
  const leadAnalysis = financialData?.leadAnalysis ?? [];

  return (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
          Analytics Dashboard
        </h1>
        <div className="text-xs text-muted-foreground">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Active Users</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Users className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{systemMetrics?.activeUsers.toLocaleString()}</div>
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
            <div className="text-xl font-bold">{systemMetrics?.totalBrokers.toLocaleString()}</div>
            <div className="flex items-center text-xs text-green-600 mt-0.5">
              <ArrowUpRight className="h-3 w-3 mr-0.5" />
              <span>8% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Conversion Rate</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <TrendingUp className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{averageConversionRate.toFixed(1)}%</div>
            <div className="flex items-center text-xs text-green-600 mt-0.5">
              <ArrowUpRight className="h-3 w-3 mr-0.5" />
              <span>5% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">System Health</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Activity className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className={`text-xl font-bold capitalize ${systemMetrics?.systemHealth === 'healthy' ? 'text-green-600' :
              systemMetrics?.systemHealth === 'warning' ? 'text-yellow-600' :
                'text-red-600'
              }`}>
              {systemMetrics?.systemHealth}
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
            <CardTitle className="text-base font-semibold">System Performance</CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={performanceData}>
                  <defs>
                    <linearGradient id="performanceGradient" x1="0" y1="0" x2="0" y2="1">
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
                    fill="url(#performanceGradient)"
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
            <CardTitle className="text-base font-semibold">Market Trends</CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={marketTrends}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="location"
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
                  <Bar dataKey="averageLoanAmount" fill="#0284c7" name="Average Loan Amount" />
                  <Bar dataKey="totalLeads" fill="#0ea5e9" name="Total Leads" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Risk Analysis */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-3">
          <CardTitle className="text-base font-semibold">Risk Analysis Overview</CardTitle>
        </CardHeader>
        <CardContent className="p-3 pt-0">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {leadAnalysis.map((analysis) => (
              <div
                key={analysis.leadId}
                className="p-4 rounded-lg border border-border hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-medium text-sm">Lead {analysis.leadId}</h3>
                  <div
                    className="px-2 py-1 rounded-full text-xs font-medium"
                    style={{
                      backgroundColor: `${getRiskColor(analysis.riskAssessment.riskLevel)}20`,
                      color: getRiskColor(analysis.riskAssessment.riskLevel)
                    }}
                  >
                    {analysis.riskAssessment.riskLevel.toUpperCase()}
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Credit Score</span>
                    <span className="font-medium">{analysis.financialProfile.creditScore}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Loan Amount</span>
                    <span className="font-medium">${analysis.financialProfile.loanAmount.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Confidence</span>
                    <span className="font-medium">{(analysis.riskAssessment.confidence * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Top Brokers */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-3">
          <CardTitle className="text-base font-semibold">Top Performing Brokers</CardTitle>
        </CardHeader>
        <CardContent className="p-3 pt-0">
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={marketTrends[0]?.topBrokers || []}
                  dataKey="successRate"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                >
                  {(marketTrends[0]?.topBrokers || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: 'var(--radius)'
                  }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

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
    </div>
  );
};

export default Analytics; 