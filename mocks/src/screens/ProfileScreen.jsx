import React, { useState } from 'react'
import { User, Wifi, Bell, Globe, LogOut, ChevronRight } from 'lucide-react'
import { user } from '../data/mockData'
import { colors, glassMorphism, typography, spacing } from '../theme'

const ProfileScreen = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true)
  const [language, setLanguage] = useState('English')

  const containerStyle = {
    padding: spacing.md,
    paddingBottom: '100px',
    maxWidth: '1200px',
    margin: '0 auto'
  }

  const profileHeaderStyle = {
    ...glassMorphism,
    borderRadius: '20px',
    padding: spacing.lg,
    marginBottom: spacing.lg,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center'
  }

  const avatarStyle = {
    width: '100px',
    height: '100px',
    borderRadius: '50%',
    backgroundColor: colors.primary,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: colors.surface,
    ...typography.title,
    fontWeight: '700',
    marginBottom: spacing.md
  }

  const nameStyle = {
    ...typography.heading,
    color: colors.textPrimary,
    marginBottom: spacing.xs
  }

  const phoneStyle = {
    ...typography.body,
    color: colors.textSecondary
  }

  const sectionStyle = {
    ...glassMorphism,
    borderRadius: '16px',
    padding: spacing.md,
    marginBottom: spacing.md
  }

  const sectionTitleStyle = {
    ...typography.caption,
    color: colors.textSecondary,
    fontWeight: '600',
    marginBottom: spacing.md,
    textTransform: 'uppercase',
    letterSpacing: '0.5px'
  }

  const preferenceRowStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: `${spacing.sm} 0`,
    borderBottom: `1px solid rgba(62, 39, 35, 0.1)`
  }

  const preferenceRowLastStyle = {
    ...preferenceRowStyle,
    borderBottom: 'none'
  }

  const preferenceLabelStyle = {
    ...typography.body,
    color: colors.textPrimary
  }

  const preferenceValueStyle = {
    ...typography.body,
    color: colors.textSecondary,
    fontWeight: '600'
  }

  const spiceDotsContainerStyle = {
    display: 'flex',
    gap: '6px'
  }

  const spiceDotStyle = (filled) => ({
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    backgroundColor: filled ? colors.primary : 'rgba(230, 81, 0, 0.2)'
  })

  const deviceCardStyle = {
    ...glassMorphism,
    borderRadius: '12px',
    padding: spacing.md,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  }

  const deviceInfoStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: spacing.sm
  }

  const deviceNameStyle = {
    ...typography.subheading,
    color: colors.textPrimary
  }

  const statusBadgeStyle = {
    padding: '4px 12px',
    borderRadius: '12px',
    backgroundColor: colors.success,
    color: colors.surface,
    ...typography.small,
    fontWeight: '600'
  }

  const settingItemStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    cursor: 'pointer',
    borderBottom: `1px solid rgba(62, 39, 35, 0.1)`
  }

  const settingItemLastStyle = {
    ...settingItemStyle,
    borderBottom: 'none'
  }

  const settingLabelStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: spacing.sm,
    ...typography.body,
    color: colors.textPrimary
  }

  const toggleStyle = (enabled) => ({
    width: '48px',
    height: '28px',
    borderRadius: '14px',
    backgroundColor: enabled ? colors.success : 'rgba(62, 39, 35, 0.2)',
    position: 'relative',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease'
  })

  const toggleKnobStyle = (enabled) => ({
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    backgroundColor: colors.surface,
    position: 'absolute',
    top: '2px',
    left: enabled ? '22px' : '2px',
    transition: 'left 0.3s ease',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
  })

  const logoutButtonStyle = {
    width: '100%',
    padding: spacing.md,
    backgroundColor: colors.emergency,
    color: colors.surface,
    ...typography.subheading,
    fontWeight: '600',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    cursor: 'pointer',
    transition: 'opacity 0.3s ease'
  }

  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase()
  }

  return (
    <div style={containerStyle}>
      <div style={profileHeaderStyle}>
        <div style={avatarStyle}>{getInitials(user.name)}</div>
        <div style={nameStyle}>{user.name}</div>
        <div style={phoneStyle}>{user.phone}</div>
      </div>

      <div style={sectionStyle}>
        <div style={sectionTitleStyle}>Preferences</div>
        <div style={preferenceRowStyle}>
          <div style={preferenceLabelStyle}>Spice Level</div>
          <div style={spiceDotsContainerStyle}>
            {[1, 2, 3, 4, 5].map(level => (
              <div key={level} style={spiceDotStyle(level <= user.preferences.spiceLevel)} />
            ))}
          </div>
        </div>
        <div style={preferenceRowStyle}>
          <div style={preferenceLabelStyle}>Default Servings</div>
          <div style={preferenceValueStyle}>{user.preferences.defaultServings} people</div>
        </div>
        <div style={preferenceRowLastStyle}>
          <div style={preferenceLabelStyle}>Dietary Preference</div>
          <div style={preferenceValueStyle}>{user.preferences.dietaryTags.join(', ')}</div>
        </div>
      </div>

      <div style={sectionStyle}>
        <div style={sectionTitleStyle}>Device</div>
        <div style={deviceCardStyle}>
          <div style={deviceInfoStyle}>
            <User size={20} color={colors.primary} />
            <div style={deviceNameStyle}>Kitchen Epicura</div>
          </div>
          <div style={statusBadgeStyle}>Online</div>
        </div>
      </div>

      <div style={sectionStyle}>
        <div style={sectionTitleStyle}>Settings</div>
        <div style={settingItemStyle}>
          <div style={settingLabelStyle}>
            <Bell size={20} color={colors.textSecondary} />
            Notifications
          </div>
          <div
            style={toggleStyle(notificationsEnabled)}
            onClick={() => setNotificationsEnabled(!notificationsEnabled)}
          >
            <div style={toggleKnobStyle(notificationsEnabled)} />
          </div>
        </div>
        <div style={settingItemLastStyle}>
          <div style={settingLabelStyle}>
            <Globe size={20} color={colors.textSecondary} />
            Language
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: spacing.xs }}>
            <span style={preferenceValueStyle}>{language}</span>
            <ChevronRight size={20} color={colors.textSecondary} />
          </div>
        </div>
      </div>

      <button
        style={logoutButtonStyle}
        onMouseEnter={e => e.target.style.opacity = '0.9'}
        onMouseLeave={e => e.target.style.opacity = '1'}
      >
        <LogOut size={20} />
        Logout
      </button>
    </div>
  )
}

export default ProfileScreen
