import apiService from './api.service';

export interface MarketTrends {
  location: string;
  averageLoanAmount: number;
  totalLeads: number;
  conversionRate: number;
  topBrokers: Array<{
    id: string;
    name: string;
    successRate: number;
  }>;
}

export interface LeadAnalysis {
  leadId: string;
  financialProfile: {
    creditScore: number;
    income: number;
    expenses: number;
    debtToIncomeRatio: number;
    loanAmount: number;
  };
  riskAssessment: {
    riskLevel: 'low' | 'medium' | 'high';
    confidence: number;
    factors: string[];
  };
  recommendations: string[];
}

export interface FinancialAnalysis {
  marketTrends: MarketTrends[];
  leadAnalysis: LeadAnalysis[];
  totalAnalyzed: number;
  averageConversionRate: number;
}

class FinancialAnalysisService {
  // Mock data for development
  private static mockMarketTrends: MarketTrends[] = [
    {
      location: 'Sydney',
      averageLoanAmount: 750000,
      totalLeads: 150,
      conversionRate: 35,
      topBrokers: [
        { id: '1', name: 'John Smith', successRate: 0.85 },
        { id: '2', name: 'Sarah Johnson', successRate: 0.78 },
        { id: '3', name: 'Michael Brown', successRate: 0.72 },
        { id: '4', name: 'Emma Wilson', successRate: 0.68 },
      ]
    },
    {
      location: 'Melbourne',
      averageLoanAmount: 680000,
      totalLeads: 120,
      conversionRate: 32,
      topBrokers: [
        { id: '5', name: 'David Lee', successRate: 0.82 },
        { id: '6', name: 'Lisa Chen', successRate: 0.75 },
        { id: '7', name: 'James Wilson', successRate: 0.70 },
      ]
    },
    {
      location: 'Brisbane',
      averageLoanAmount: 620000,
      totalLeads: 90,
      conversionRate: 28,
      topBrokers: [
        { id: '8', name: 'Robert Taylor', successRate: 0.80 },
        { id: '9', name: 'Maria Garcia', successRate: 0.73 },
        { id: '10', name: 'Peter Anderson', successRate: 0.67 },
      ]
    }
  ];

  private static mockLeadAnalysis: LeadAnalysis[] = [
    {
      leadId: 'L001',
      financialProfile: {
        creditScore: 780,
        income: 120000,
        expenses: 45000,
        debtToIncomeRatio: 0.28,
        loanAmount: 850000
      },
      riskAssessment: {
        riskLevel: 'low',
        confidence: 0.92,
        factors: ['High credit score', 'Stable employment', 'Low debt ratio']
      },
      recommendations: [
        'Consider premium loan products',
        'Eligible for rate discounts',
        'Fast-track application process'
      ]
    },
    {
      leadId: 'L002',
      financialProfile: {
        creditScore: 650,
        income: 85000,
        expenses: 38000,
        debtToIncomeRatio: 0.45,
        loanAmount: 550000
      },
      riskAssessment: {
        riskLevel: 'medium',
        confidence: 0.75,
        factors: ['Moderate credit score', 'Higher debt ratio', 'Stable income']
      },
      recommendations: [
        'Consider debt consolidation',
        'Review spending patterns',
        'Standard loan products recommended'
      ]
    },
    {
      leadId: 'L003',
      financialProfile: {
        creditScore: 580,
        income: 65000,
        expenses: 35000,
        debtToIncomeRatio: 0.62,
        loanAmount: 420000
      },
      riskAssessment: {
        riskLevel: 'high',
        confidence: 0.85,
        factors: ['Low credit score', 'High debt ratio', 'Limited savings']
      },
      recommendations: [
        'Improve credit score',
        'Reduce existing debt',
        'Consider smaller loan amount'
      ]
    }
  ];

  private static mockFinancialAnalysis: FinancialAnalysis = {
    marketTrends: FinancialAnalysisService.mockMarketTrends,
    leadAnalysis: FinancialAnalysisService.mockLeadAnalysis,
    totalAnalyzed: 360,
    averageConversionRate: 31.7
  };

  async getMarketTrends(location?: string, daysBack: number = 30): Promise<MarketTrends[]> {
    try {
      // When backend is ready, uncomment this:
      // const params = new URLSearchParams();
      // if (location) params.append('location', location);
      // params.append('days_back', daysBack.toString());
      // return await apiService.get<MarketTrends[]>(`/financial-analysis/market-trends?${params}`);
      
      // For now, return mock data
      return Promise.resolve(FinancialAnalysisService.mockMarketTrends);
    } catch (error) {
      console.error('Error fetching market trends:', error);
      throw error;
    }
  }

  async analyzeLead(leadData: any): Promise<LeadAnalysis> {
    try {
      // When backend is ready, uncomment this:
      // return await apiService.post<LeadAnalysis>('/financial-analysis/analyze-lead', leadData);
      
      // For now, return mock data
      return Promise.resolve(FinancialAnalysisService.mockLeadAnalysis[0]);
    } catch (error) {
      console.error('Error analyzing lead:', error);
      throw error;
    }
  }

  async getMyFinancialAnalysis(): Promise<FinancialAnalysis> {
    try {
      // When backend is ready, uncomment this:
      // return await apiService.get<FinancialAnalysis>('/financial-analysis/my-financial-analysis');
      
      // For now, return mock data
      return Promise.resolve(FinancialAnalysisService.mockFinancialAnalysis);
    } catch (error) {
      console.error('Error fetching financial analysis:', error);
      throw error;
    }
  }

  async batchAnalyzeLeads(leadIds: string[]): Promise<{
    success: boolean;
    batch_results: Array<{
      lead_id: string;
      success: boolean;
      analysis?: LeadAnalysis;
      error?: string;
    }>;
  }> {
    try {
      // When backend is ready, uncomment this:
      // return await apiService.post('/financial-analysis/batch-analyze', { lead_ids: leadIds });
      
      // For now, return mock data
      return Promise.resolve({
        success: true,
        batch_results: leadIds.map(id => ({
          lead_id: id,
          success: true,
          analysis: FinancialAnalysisService.mockLeadAnalysis[0]
        }))
      });
    } catch (error) {
      console.error('Error in batch analysis:', error);
      throw error;
    }
  }
}

export default new FinancialAnalysisService(); 