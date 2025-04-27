import { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Eye, EyeOff, User, Mail, Key } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuth } from '@/contexts/AuthContext';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useNavigate } from 'react-router-dom';

const CreateAccountPage = () => {
  const navigate = useNavigate();
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const newErrors = {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
    let isValid = true;
    
    if (!formData.name) {
      newErrors.name = 'Name is required';
      isValid = false;
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
      isValid = false;
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
      isValid = false;
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
      isValid = false;
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
      isValid = false;
    }
    
    setErrors(newErrors);
    
    if (isValid) {
      setIsLoading(true);
      try {
        await signUp(formData.email, formData.password, formData.name);
        // Remove navigation from here - AuthContext will handle it
      } catch (error) {
        console.error('Signup error:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-sbi-light-gray">
      <Navbar />
      
      <main className="flex-grow flex items-center justify-center py-12 px-4">
        <div className="bg-white rounded-lg shadow-md max-w-md w-full p-8">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-sbi-blue">Create an Account</h1>
            <p className="text-sbi-gray mt-2">Join InsuraWise today</p>
          </div>
          
          <form onSubmit={handleSignUp}>
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-sbi-blue mb-1">
                  Full Name
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-sbi-gray">
                    <User size={18} />
                  </div>
                  <Input
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="pl-10 form-input"
                    placeholder="John Doe"
                    aria-invalid={errors.name ? 'true' : 'false'}
                  />
                </div>
                {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
              </div>
              
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-sbi-blue mb-1">
                  Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-sbi-gray">
                    <Mail size={18} />
                  </div>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="pl-10 form-input"
                    placeholder="your@email.com"
                    aria-invalid={errors.email ? 'true' : 'false'}
                  />
                </div>
                {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
              </div>
              
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-sbi-blue mb-1">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-sbi-gray">
                    <Key size={18} />
                  </div>
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={handleChange}
                    className="pl-10 pr-10 form-input"
                    aria-invalid={errors.password ? 'true' : 'false'}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
              </div>
              
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-sbi-blue mb-1">
                  Confirm Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-sbi-gray">
                    <Key size={18} />
                  </div>
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="pl-10 pr-10 form-input"
                    aria-invalid={errors.confirmPassword ? 'true' : 'false'}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                  >
                    {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                {errors.confirmPassword && <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>}
              </div>
              
              <Button type="submit" className="w-full bg-sbi-cyan hover:bg-sbi-cyan/90">
                Sign Up
              </Button>
            </div>
          </form>
          
          <p className="text-center mt-6 text-sbi-gray">
            Already have an account?{' '}
            <Link to="/login" className="text-sbi-cyan hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default CreateAccountPage;
