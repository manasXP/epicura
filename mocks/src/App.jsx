import React, { useState } from 'react'
import LoginScreen from './screens/LoginScreen'
import OTPScreen from './screens/OTPScreen'
import RecipeScreen from './screens/RecipeScreen'
import FavouriteScreen from './screens/FavouriteScreen'
import SessionScreen from './screens/SessionScreen'
import ProfileScreen from './screens/ProfileScreen'
import TabBar from './components/TabBar'

const App = () => {
  const [appState, setAppState] = useState('login') // 'login' | 'otp' | 'app'
  const [phoneNumber, setPhoneNumber] = useState('')
  const [activeTab, setActiveTab] = useState('recipe')

  const handleSendOTP = (phone) => {
    setPhoneNumber(phone)
    setAppState('otp')
  }

  const handleVerifyOTP = () => {
    setAppState('app')
  }

  const renderScreen = () => {
    switch (activeTab) {
      case 'recipe':
        return <RecipeScreen />
      case 'favourite':
        return <FavouriteScreen />
      case 'session':
        return <SessionScreen />
      case 'profile':
        return <ProfileScreen />
      default:
        return <RecipeScreen />
    }
  }

  if (appState === 'login') {
    return <LoginScreen onSendOTP={handleSendOTP} />
  }

  if (appState === 'otp') {
    return <OTPScreen phone={phoneNumber} onVerify={handleVerifyOTP} />
  }

  return (
    <>
      {renderScreen()}
      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
    </>
  )
}

export default App
