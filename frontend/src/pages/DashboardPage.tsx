import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FileText, DollarSign, TrendingUp } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import AgentResultCard from '@/components/AgentResultCard';

interface RecommendationResult {
  policy_name: string;
  explanation: string;
}

interface PricingResult {
  price_inr: number;
  breakdown: { name: string; value: number }[];
}

interface UpsellResult {
  upsell_name: string;
  explanation: string;
}

type AgentResult = RecommendationResult | PricingResult | UpsellResult;

const DashboardPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AgentResult | null>(null);
  
  // Get feature from URL query parameter
  const feature = new URLSearchParams(location.search).get('feature') || 'recommendation';
  
  useEffect(() => {
    const fetchAgentResult = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // In a real app, this would be an actual API call
        // For the prototype, we'll simulate with mock data
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
        
        let mockResult: AgentResult;
        
        switch (feature) {
          case 'recommendation':
            mockResult = {
              policy_name: "Comprehensive Health Shield Pro",
              explanation: "Based on your health profile, family history, and coverage preferences, our AI recommends the Comprehensive Health Shield Pro plan. This policy provides extensive coverage for hospitalization, critical illness, and preventive care with a lower deductible that suits your risk profile."
            };
            break;
          case 'pricing':
            mockResult = {
              price_inr: 25750,
              breakdown: [
                { name: "Base Coverage", value: 15000 },
                { name: "Add-ons", value: 5500 },
                { name: "Risk Assessment", value: 3250 },
                { name: "Administrative Fees", value: 2000 }
              ]
            };
            break;
          case 'upsell':
            mockResult = {
              upsell_name: "Critical Illness Rider",
              explanation: "Given your family medical history, adding the Critical Illness Rider would provide an additional ₹10,00,000 coverage specifically for 30+ critical conditions. This would increase your premium by only ₹350/month but significantly enhance your financial protection against serious health events."
            };
            break;
          default:
            throw new Error("Invalid feature type");
        }
        
        setResult(mockResult);
      } catch (err) {
        setError("Failed to fetch agent result. Please try again later.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAgentResult();
  }, [feature]);
  
  const getFeatureTitle = () => {
    switch (feature) {
      case 'recommendation':
        return "Policy Recommendation";
      case 'pricing':
        return "Dynamic Pricing";
      case 'upsell':
        return "Upsell Strategy";
      default:
        return "Insurance Insights";
    }
  };
  
  const getFeatureIcon = () => {
    switch (feature) {
      case 'recommendation':
        return <FileText size={24} />;
      case 'pricing':
        return <DollarSign size={24} />;
      case 'upsell':
        return <TrendingUp size={24} />;
      default:
        return <FileText size={24} />;
    }
  };
  
  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-sbi-cyan border-solid mx-auto mb-4"></div>
            <p className="text-sbi-gray">Analyzing your data...</p>
          </div>
        </div>
      );
    }
    
    if (error) {
      return (
        <div className="bg-red-50 border border-red-200 rounded-md p-6 text-center">
          <p className="text-red-600">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-sbi-blue text-white rounded-md hover:bg-sbi-blue/90 transition-colors"
          >
            Try Again
          </button>
        </div>
      );
    }
    
    if (!result) {
      return <div>No results available.</div>;
    }
    
    switch (feature) {
      case 'recommendation': {
        const typedResult = result as RecommendationResult;
        return (
          <div>
            <h3 className="text-xl font-semibold text-sbi-blue mb-3">{typedResult.policy_name}</h3>
            <p className="text-sbi-gray">{typedResult.explanation}</p>
            <div className="mt-6 bg-sbi-light-gray p-4 rounded-md">
              <h4 className="text-lg font-medium text-sbi-blue mb-2">Key Benefits</h4>
              <ul className="list-disc pl-5 text-sbi-gray space-y-1">
                <li>Comprehensive coverage for hospitalization</li>
                <li>Critical illness protection</li>
                <li>Preventive care benefits</li>
                <li>Lower deductible</li>
                <li>Network of 5000+ hospitals</li>
              </ul>
            </div>
          </div>
        );
      }
      case 'pricing': {
        const typedResult = result as PricingResult;
        const COLORS = ['#00B5EF', '#36A2EB', '#4C6FFF', '#292075'];
        
        return (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-sbi-blue">Annual Premium</h3>
              <div className="text-2xl font-bold text-sbi-blue">₹{typedResult.price_inr.toLocaleString()}</div>
            </div>
            
            <h4 className="text-lg font-medium text-sbi-blue mb-4">Premium Breakdown</h4>
            
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={typedResult.breakdown}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    nameKey="name"
                  >
                    {typedResult.breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value: number) => [`₹${value.toLocaleString()}`, 'Amount']}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="mt-4">
              <table className="w-full text-left">
                <thead>
                  <tr>
                    <th className="pb-2 text-sbi-blue">Component</th>
                    <th className="pb-2 text-right text-sbi-blue">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {typedResult.breakdown.map((item, index) => (
                    <tr key={index} className="border-t border-sbi-gray/20">
                      <td className="py-2 text-sbi-gray">{item.name}</td>
                      <td className="py-2 text-right text-sbi-gray">₹{item.value.toLocaleString()}</td>
                    </tr>
                  ))}
                  <tr className="border-t border-sbi-gray/20 font-bold">
                    <td className="py-2 text-sbi-blue">Total</td>
                    <td className="py-2 text-right text-sbi-blue">
                      ₹{typedResult.price_inr.toLocaleString()}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        );
      }
      case 'upsell': {
        const typedResult = result as UpsellResult;
        return (
          <div>
            <h3 className="text-xl font-semibold text-sbi-blue mb-3">Recommended Add-on: {typedResult.upsell_name}</h3>
            <p className="text-sbi-gray mb-6">{typedResult.explanation}</p>
            
            <div className="bg-sbi-light-gray p-5 rounded-md">
              <h4 className="text-lg font-medium text-sbi-blue mb-3">Why This Matters</h4>
              <p className="text-sbi-gray mb-4">
                Critical illness coverage provides financial protection when you need it most. 
                Treatment for serious conditions often requires specialized care and may impact your ability to work.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center sm:justify-between gap-4 bg-white p-4 rounded-md">
                <div>
                  <div className="text-sm text-sbi-gray">Monthly Cost</div>
                  <div className="text-xl font-semibold text-sbi-blue">₹350</div>
                </div>
                
                <div>
                  <div className="text-sm text-sbi-gray">Coverage Amount</div>
                  <div className="text-xl font-semibold text-sbi-blue">₹10,00,000</div>
                </div>
                
                <button className="primary-button">Add to Policy</button>
              </div>
            </div>
          </div>
        );
      }
      default:
        return <div>Select a feature to get started.</div>;
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow py-12 px-4 bg-sbi-light-gray">
        <div className="container mx-auto max-w-4xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-sbi-blue mb-2">Your Insurance Dashboard</h1>
            <p className="text-sbi-gray">
              Here's your personalized {getFeatureTitle().toLowerCase()} from our AI engine
            </p>
          </div>
          
          <AgentResultCard title={getFeatureTitle()} icon={getFeatureIcon()}>
            {renderContent()}
          </AgentResultCard>
          
          <div className="mt-8 flex justify-between">
            <button
              onClick={() => window.history.back()}
              className="secondary-button"
            >
              Back
            </button>
            
            <button
              onClick={() => navigate('/select-feature')}
              className="primary-button"
            >
              Try Another Feature
            </button>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default DashboardPage;
