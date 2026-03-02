import React from 'react'
import { Grid, Heart, Clock, User } from 'lucide-react'
import { colors, glassMorphism, typography } from '../theme'

const TabBar = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'recipe', label: 'Recipe', icon: Grid },
    { id: 'favourite', label: 'Favourite', icon: Heart },
    { id: 'session', label: 'Session', icon: Clock },
    { id: 'profile', label: 'Profile', icon: User }
  ]

  const containerStyle = {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: '12px 0',
    ...glassMorphism,
    borderTop: '1px solid rgba(255, 255, 255, 0.5)',
    zIndex: 1000
  }

  const tabStyle = (isActive) => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '4px',
    padding: '8px 16px',
    background: 'transparent',
    color: isActive ? colors.primary : colors.textSecondary,
    transition: 'all 0.3s ease'
  })

  const labelStyle = {
    ...typography.small,
    fontWeight: '600'
  }

  return (
    <div style={containerStyle}>
      {tabs.map(tab => {
        const Icon = tab.icon
        const isActive = activeTab === tab.id
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            style={tabStyle(isActive)}
          >
            <Icon size={24} strokeWidth={isActive ? 2.5 : 2} />
            <span style={labelStyle}>{tab.label}</span>
          </button>
        )
      })}
    </div>
  )
}

export default TabBar
