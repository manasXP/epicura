import React from 'react'
import { colors, glassMorphism, typography, spacing } from '../theme'

const MiniProgress = ({ session }) => {
  const containerStyle = {
    ...glassMorphism,
    borderRadius: '16px',
    padding: spacing.md,
    marginBottom: spacing.md
  }

  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm
  }

  const recipeNameStyle = {
    ...typography.subheading,
    color: colors.textPrimary,
    display: 'flex',
    alignItems: 'center',
    gap: spacing.sm
  }

  const liveIndicatorStyle = {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: colors.success,
    animation: 'pulse 2s infinite'
  }

  const timeStyle = {
    ...typography.caption,
    color: colors.textSecondary
  }

  const stageStyle = {
    ...typography.body,
    color: colors.textPrimary,
    marginBottom: spacing.sm
  }

  const tempContainerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm
  }

  const tempStyle = {
    ...typography.caption,
    color: colors.textSecondary
  }

  const progressBarContainerStyle = {
    width: '100%',
    height: '6px',
    backgroundColor: 'rgba(230, 81, 0, 0.2)',
    borderRadius: '3px',
    overflow: 'hidden'
  }

  const progressBarFillStyle = {
    width: `${session.progress * 100}%`,
    height: '100%',
    backgroundColor: colors.primary,
    transition: 'width 0.5s ease',
    borderRadius: '3px'
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <>
      <style>
        {`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
          }
        `}
      </style>
      <div style={containerStyle}>
        <div style={headerStyle}>
          <div style={recipeNameStyle}>
            <div style={liveIndicatorStyle}></div>
            {session.recipeName}
          </div>
          <div style={timeStyle}>{formatTime(session.timeRemaining)} left</div>
        </div>
        <div style={stageStyle}>{session.currentStage}</div>
        <div style={tempContainerStyle}>
          <div style={tempStyle}>
            Temperature: {session.temperature}°C / {session.targetTemp}°C
          </div>
        </div>
        <div style={progressBarContainerStyle}>
          <div style={progressBarFillStyle}></div>
        </div>
      </div>
    </>
  )
}

export default MiniProgress
