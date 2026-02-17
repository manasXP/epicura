import React from 'react'
import { Clock } from 'lucide-react'
import MiniProgress from '../components/MiniProgress'
import { sessions, activeCookingSession } from '../data/mockData'
import { colors, glassMorphism, typography, spacing } from '../theme'

const SessionScreen = () => {
  const hasActiveSession = true // Change to false to see empty state

  const containerStyle = {
    padding: spacing.md,
    paddingBottom: '100px',
    maxWidth: '1200px',
    margin: '0 auto'
  }

  const titleStyle = {
    ...typography.heading,
    color: colors.textPrimary,
    marginBottom: spacing.lg
  }

  const sessionItemStyle = {
    ...glassMorphism,
    borderRadius: '16px',
    padding: spacing.md,
    marginBottom: spacing.md
  }

  const sessionHeaderStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'start',
    marginBottom: spacing.sm
  }

  const sessionNameStyle = {
    ...typography.subheading,
    color: colors.textPrimary
  }

  const statusBadgeStyle = (status) => {
    const statusColors = {
      'completed': colors.success,
      'failed': colors.emergency,
      'in_progress': colors.warning
    }

    return {
      padding: '4px 12px',
      borderRadius: '12px',
      backgroundColor: statusColors[status],
      color: colors.surface,
      ...typography.small,
      fontWeight: '600',
      textTransform: 'capitalize'
    }
  }

  const sessionMetaStyle = {
    ...typography.caption,
    color: colors.textSecondary,
    display: 'flex',
    flexDirection: 'column',
    gap: spacing.xs
  }

  const emptyStateStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '60vh',
    textAlign: 'center'
  }

  const emptyIconStyle = {
    marginBottom: spacing.md
  }

  const emptyTextStyle = {
    ...typography.body,
    color: colors.textSecondary
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60)
    return `${mins} minutes`
  }

  return (
    <div style={containerStyle}>
      <div style={titleStyle}>Cooking Sessions</div>

      {hasActiveSession && (
        <>
          <div style={{ ...typography.caption, color: colors.textSecondary, marginBottom: spacing.sm, fontWeight: '600' }}>
            LIVE NOW
          </div>
          <MiniProgress session={activeCookingSession} />
        </>
      )}

      <div style={{ ...typography.caption, color: colors.textSecondary, marginBottom: spacing.sm, marginTop: spacing.lg, fontWeight: '600' }}>
        PAST SESSIONS
      </div>

      {sessions.length === 0 ? (
        <div style={emptyStateStyle}>
          <Clock size={64} color={colors.textSecondary} style={emptyIconStyle} />
          <div style={emptyTextStyle}>
            No cooking sessions yet.<br />
            Start your first recipe to see sessions here!
          </div>
        </div>
      ) : (
        sessions.map(session => (
          <div key={session.id} style={sessionItemStyle}>
            <div style={sessionHeaderStyle}>
              <div style={sessionNameStyle}>{session.recipeName}</div>
              <div style={statusBadgeStyle(session.status)}>
                {session.status.replace('_', ' ')}
              </div>
            </div>
            <div style={sessionMetaStyle}>
              <span>{formatDate(session.date)}</span>
              <span>Duration: {formatDuration(session.duration_s)}</span>
            </div>
          </div>
        ))
      )}
    </div>
  )
}

export default SessionScreen
