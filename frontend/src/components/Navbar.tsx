
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import ProfileMenu from './ProfileMenu';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user } = useAuth();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-white shadow-sm py-4 sticky top-0 z-50">
      <div className="container mx-auto px-4 md:px-6">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-sbi-blue font-bold text-2xl">InsuraWise</div>
          </Link>
          
          <button 
            onClick={toggleMenu}
            className="md:hidden focus:outline-none"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          
          {/* Desktop navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-sbi-blue hover:text-sbi-cyan transition-colors">
              Home
            </Link>
            <Link to="/about" className="text-sbi-blue hover:text-sbi-cyan transition-colors">
              About
            </Link>
            {user ? (
              <ProfileMenu />
            ) : (
              <>
                <Link to="/login" className="text-sbi-blue hover:text-sbi-cyan transition-colors">
                  Login
                </Link>
                <Link to="/create-account" className="primary-button">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
        
        {/* Mobile navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 flex flex-col space-y-4 pb-4">
            <Link 
              to="/" 
              className="text-sbi-blue hover:text-sbi-cyan transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </Link>
            <Link 
              to="/about" 
              className="text-sbi-blue hover:text-sbi-cyan transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              About
            </Link>
            {user ? (
              <div className="flex justify-center">
                <ProfileMenu />
              </div>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="text-sbi-blue hover:text-sbi-cyan transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Login
                </Link>
                <Link 
                  to="/create-account" 
                  className="primary-button w-full text-center"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
