import { Widget } from '@typeform/embed-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function OnboardingPage() {
  const { user, supabase } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="h-screen flex items-center justify-center">
      <Widget
        id="YOUR_TYPEFORM_ID"
        style={{ width: '100%', height: '100vh' }}
        hidden={{ userId: user.id }}
        onSubmit={async () => {
          // mark onboarded
          await supabase
            .from('profiles')
            .update({ onboarded: true })
            .eq('id', user.id)
          navigate('/select-feature')
        }}
      />
    </div>
  )
}
