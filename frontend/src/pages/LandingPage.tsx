
import { ArrowRight, FileText, DollarSign, TrendingUp } from 'lucide-react';
import { Link } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => (
  <div className="outline-card flex flex-col items-center">
    <div className="text-sbi-cyan mb-4">{icon}</div>
    <h3 className="text-xl font-semibold mb-2 text-sbi-blue">{title}</h3>
    <p className="text-center text-sbi-gray">{description}</p>
  </div>
);

const Testimonial = ({ quote, author, role, avatar }: { quote: string, author: string, role: string, avatar: string }) => (
  <div className="bg-white p-6 rounded-lg shadow-md">
    <div className="mb-4">
      <svg className="h-8 w-8 text-sbi-cyan mb-2" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
        <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z" />
      </svg>
      <p className="text-sbi-gray">{quote}</p>
    </div>
    <div className="flex items-center">
      <img className="h-10 w-10 rounded-full mr-3" src={avatar} alt={author} />
      <div>
        <p className="font-semibold text-sbi-blue">{author}</p>
        <p className="text-sm text-sbi-gray">{role}</p>
      </div>
    </div>
  </div>
);

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="gradient-cyan-white py-20 md:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="text-center max-w-3xl mx-auto">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-sbi-blue">
                AI-Powered Insurance Tailored to You
              </h1>
              <p className="text-xl text-sbi-gray mb-8">
                Revolutionizing insurance with artificial intelligence for personalized coverage, 
                dynamic pricing, and intelligent strategy recommendations.
              </p>
              <Link to="/login" className="primary-button inline-flex items-center">
                Get Started <ArrowRight className="ml-2" size={18} />
              </Link>
            </div>
          </div>
        </section>
        
        {/* Features Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-3xl font-bold text-center mb-12">Our AI-Powered Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <FeatureCard 
                icon={<FileText size={42} />}
                title="Personalized Policy Recommendation"
                description="Our AI analyzes your data to recommend the perfect insurance policy tailored to your specific needs and risk profile."
              />
              <FeatureCard 
                icon={<DollarSign size={42} />}
                title="Dynamic Pricing Engine"
                description="Get competitive real-time pricing based on your unique profile, market conditions, and risk assessment."
              />
              <FeatureCard 
                icon={<TrendingUp size={42} />}
                title="AI-Driven Upselling Strategy"
                description="Discover additional coverage options that make sense for your situation, with clear explanations of their benefits."
              />
            </div>
          </div>
        </section>
        
        {/* Testimonials Section */}
        <section className="py-16 bg-sbi-light-gray">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-3xl font-bold text-center mb-12">What Our Customers Say</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Testimonial 
                quote="InsuraWise transformed how I approach insurance. Their AI recommended coverage options I hadn't even considered but desperately needed."
                author="Priya Sharma"
                role="Small Business Owner"
                avatar="https://randomuser.me/api/portraits/women/32.jpg"
              />
              <Testimonial 
                quote="The dynamic pricing saved me thousands on my premiums. The platform is incredibly easy to use and the recommendations are spot on."
                author="Rajesh Kumar"
                role="IT Professional"
                avatar="https://randomuser.me/api/portraits/men/45.jpg"
              />
              <Testimonial 
                quote="After using InsuraWise, I finally understand my coverage. The AI explanations are clear and the personalized approach made all the difference."
                author="Ananya Patel"
                role="Healthcare Worker"
                avatar="https://randomuser.me/api/portraits/women/68.jpg"
              />
            </div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section className="py-16 bg-sbi-blue text-white">
          <div className="container mx-auto px-4 md:px-6 text-center">
            <h2 className="text-3xl font-bold text-white mb-6">Ready to Transform Your Insurance Experience?</h2>
            <p className="text-xl mb-8 text-white/90 max-w-2xl mx-auto">
              Join thousands of satisfied customers who have discovered the power of AI-driven insurance solutions.
            </p>
            <Link to="/login" className="bg-white text-sbi-blue px-6 py-3 rounded-md hover:bg-white/90 transition-colors focus-ring inline-flex items-center">
              Get Started <ArrowRight className="ml-2" size={18} />
            </Link>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default LandingPage;
