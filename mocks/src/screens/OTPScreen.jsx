import React, { useState, useEffect } from 'react'
import OTPInput from '../components/OTPInput'
import { colors, glassMorphism, typography, spacing } from '../theme'

const OTPScreen = ({ phone, onVerify }) => {
  const [otp, setOtp] = useState('')
  const [autoFilled, setAutoFilled] = useState(false)

  useEffect(() => {
    // Auto-fill after 3 seconds
    const timer = setTimeout(() => {
      setOtp('123456')
      setAutoFilled(true)
    }, 3000)

    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    // Auto-verify after OTP is filled
    if (autoFilled && otp === '123456') {
      setTimeout(() => {
        onVerify()
      }, 500)
    }
  }, [autoFilled, otp, onVerify])

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

  const titleStyle = {
    ...typography.heading,
    color: colors.textPrimary,
    textAlign: 'center',
    marginBottom: spacing.sm
  }

  const subtitleStyle = {
    ...typography.body,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.xl
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
    boxShadow: `0 4px 16px ${colors.primary}40`,
    marginTop: spacing.lg
  }

  const formatPhone = (phoneNumber) => {
    return phoneNumber.replace(/(\d{5})(\d{5})/, '$1 $2')
  }

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <div style={titleStyle}>Enter OTP</div>
        <div style={subtitleStyle}>
          Enter the OTP sent to +91 {formatPhone(phone)}
        </div>
        <OTPInput value={otp} onChange={setOtp} />
        <button
          onClick={onVerify}
          disabled={otp.length !== 6}
          style={{
            ...buttonStyle,
            opacity: otp.length === 6 ? 1 : 0.5,
            cursor: otp.length === 6 ? 'pointer' : 'not-allowed'
          }}
          onMouseEnter={e => {
            if (otp.length === 6) {
              e.target.style.backgroundColor = colors.primaryVariant
            }
          }}
          onMouseLeave={e => {
            e.target.style.backgroundColor = colors.primary
          }}
        >
          Verify
        </button>
      </div>
    </div>
  )
}

export default OTPScreen
