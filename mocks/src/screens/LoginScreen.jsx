import React, { useState } from 'react'
import { colors, glassMorphism, typography, spacing } from '../theme'

const LoginScreen = ({ onSendOTP }) => {
  const [phone, setPhone] = useState('')

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    padding: spacing.lg,
    background: `linear-gradient(135deg, ${colors.background} 0%, ${colors.surface} 100%)`
  }

  const cardStyle = {
    ...glassMorphism,
    borderRadius: '24px',
    padding: spacing.xl,
    maxWidth: '400px',
    width: '100%'
  }

  const logoStyle = {
    ...typography.title,
    color: colors.primary,
    textAlign: 'center',
    marginBottom: spacing.xl,
    fontWeight: '700'
  }

  const inputGroupStyle = {
    marginBottom: spacing.lg
  }

  const labelStyle = {
    ...typography.caption,
    color: colors.textSecondary,
    marginBottom: spacing.sm,
    display: 'block'
  }

  const inputContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    ...glassMorphism,
    borderRadius: '12px',
    padding: spacing.sm,
    border: `2px solid ${colors.primary}20`
  }

  const prefixStyle = {
    ...typography.body,
    color: colors.textPrimary,
    fontWeight: '600',
    marginRight: spacing.sm
  }

  const inputStyle = {
    flex: 1,
    border: 'none',
    background: 'transparent',
    ...typography.body,
    color: colors.textPrimary,
    outline: 'none'
  }

  const buttonStyle = {
    width: '100%',
    padding: spacing.md,
    backgroundColor: colors.primary,
    color: colors.surface,
    ...typography.subheading,
    fontWeight: '600',
    borderRadius: '12px',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: `0 4px 16px ${colors.primary}40`
  }

  const handleSubmit = () => {
    if (phone.length === 10) {
      onSendOTP(phone)
    }
  }

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <div style={logoStyle}>Epicura</div>
        <div style={inputGroupStyle}>
          <label style={labelStyle}>Phone Number</label>
          <div style={inputContainerStyle}>
            <span style={prefixStyle}>+91</span>
            <input
              type="tel"
              maxLength={10}
              value={phone}
              onChange={e => setPhone(e.target.value.replace(/\D/g, ''))}
              placeholder="98765 43210"
              style={inputStyle}
            />
          </div>
        </div>
        <button
          onClick={handleSubmit}
          disabled={phone.length !== 10}
          style={{
            ...buttonStyle,
            opacity: phone.length === 10 ? 1 : 0.5,
            cursor: phone.length === 10 ? 'pointer' : 'not-allowed'
          }}
          onMouseEnter={e => {
            if (phone.length === 10) {
              e.target.style.backgroundColor = colors.primaryVariant
            }
          }}
          onMouseLeave={e => {
            e.target.style.backgroundColor = colors.primary
          }}
        >
          Send OTP
        </button>
      </div>
    </div>
  )
}

export default LoginScreen
