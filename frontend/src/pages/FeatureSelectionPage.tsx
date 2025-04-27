
import { useNavigate } from 'react-router-dom';
import { FileText, DollarSign, TrendingUp } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  featureType: string;
  onClick: (feature: string) => void;
}

const FeatureCard = ({ icon, title, description, featureType, onClick }: FeatureCardProps) => (
  <Card 
    className="border border-sbi-gray/20 p-6 rounded-lg hover:shadow-md transition-all cursor-pointer flex flex-col h-full"
    onClick={() => onClick(featureType)}
    role="button"
    tabIndex={0}
    onKeyDown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onClick(featureType);
      }
    }}
  >
    <div className="text-sbi-cyan mb-4 flex justify-center">{icon}</div>
    <h3 className="text-xl font-semibold mb-2 text-sbi-blue text-center">{title}</h3>
    <p className="text-sbi-gray text-center mb-6">{description}</p>
    <Button 
      className="mt-auto bg-sbi-cyan hover:bg-sbi-cyan/90 w-full"
      onClick={(e) => {
        e.stopPropagation();
        onClick(featureType);
      }}
    >
      Select
    </Button>
  </Card>
);

const FeatureSelectionPage = () => {
  const navigate = useNavigate();
  
  const handleFeatureSelect = (feature: string) => {
    navigate(`/dashboard?feature=${feature}`);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow py-12 px-4 bg-sbi-light-gray">
        <div className="container mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h1 className="text-3xl font-bold text-sbi-blue mb-4">Choose Your AI Insurance Feature</h1>
            <p className="text-sbi-gray text-lg">
              Select one of our powerful AI tools to optimize your insurance experience.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <FeatureCard 
              icon={<FileText size={48} />}
              title="Policy Recommendation"
              description="Get personalized insurance policy recommendations based on your profile and needs."
              featureType="recommendation"
              onClick={handleFeatureSelect}
            />
            
            <FeatureCard 
              icon={<DollarSign size={48} />}
              title="Dynamic Pricing"
              description="See real-time pricing estimates for different policy configurations."
              featureType="pricing"
              onClick={handleFeatureSelect}
            />
            
            <FeatureCard 
              icon={<TrendingUp size={48} />}
              title="Upsell Strategy"
              description="Discover additional coverage options that provide better protection for your specific situation."
              featureType="upsell"
              onClick={handleFeatureSelect}
            />
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default FeatureSelectionPage;
