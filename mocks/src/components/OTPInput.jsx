import React, { useRef, useState, useEffect } from 'react'
import { colors, glassMorphism, spacing } from '../theme'

const OTPInput = ({ length = 6, value, onChange }) => {
  const inputRefs = useRef([])
  const [otp, setOtp] = useState(value ? value.split('') : Array(length).fill(''))

  useEffect(() => {
    if (value && value.length === length) {
      setOtp(value.split(''))
    }
  }, [value, length])

  const handleChange = (index, digit) => {
    if (!/^\d*$/.test(digit)) return

    const newOtp = [...otp]
    newOtp[index] = digit
    setOtp(newOtp)
    onChange(newOtp.join(''))

    if (digit && index < length - 1) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const containerStyle = {
    display: 'flex',
    gap: spacing.sm,
    justifyContent: 'center'
  }

  const inputBoxStyle = {
    width: '48px',
    height: '56px',
    ...glassMorphism,
    borderRadius: '12px',
    textAlign: 'center',
    fontSize: '24px',
    fontWeight: '600',
    color: colors.textPrimary,
    border: `2px solid ${colors.primary}20`,
    transition: 'all 0.3s ease'
  }

  return (
    <div style={containerStyle}>
      {Array(length).fill(0).map((_, index) => (
        <input
          key={index}
          ref={el => inputRefs.current[index] = el}
          type="text"
          maxLength={1}
          value={otp[index]}
          onChange={e => handleChange(index, e.target.value)}
          onKeyDown={e => handleKeyDown(index, e)}
          style={inputBoxStyle}
          onFocus={e => e.target.style.borderColor = colors.primary}
          onBlur={e => e.target.style.borderColor = `${colors.primary}20`}
        />
      ))}
    </div>
  )
}

export default OTPInput
