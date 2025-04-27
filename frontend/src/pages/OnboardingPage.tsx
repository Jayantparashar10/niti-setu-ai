import { Widget } from '@typeform/embed-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useState, useEffect } from 'react';

const OnboardingPage = () => {
  const navigate = useNavigate();
  const { supabase, user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  // Redirect to dashboard if already onboarded
  useEffect(() => {
    if (user?.user_metadata?.onboarded) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const handleOnboardingComplete = async () => {
    setIsLoading(true);
    try {
      await supabase.auth.updateUser({
        data: { onboarded: true }
      });
      navigate('/dashboard');
    } catch (error) {
      console.error('Error updating user metadata:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="h-screen flex items-center justify-center">
      <Widget
        id="YOUR_TYPEFORM_ID"
        style={{ width: '100%', height: '100vh' }}
        hidden={{ userId: user?.id, email: user?.email }}
        onSubmit={handleOnboardingComplete}
      />
    </div>
  );
};

export default OnboardingPage;
