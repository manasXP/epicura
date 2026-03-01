import React, { useState } from 'react'
import { Clock, Flame, ChefHat, CheckCircle, XCircle } from 'lucide-react'
import { colors, typography, spacing, glassMorphism } from '../theme'
import { activeCookingSession } from '../data/mockData'

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// ─── Pulsing live indicator (reused across all variants) ────────────────────
const LiveDot = ({ size = 8, color = '#34C759' }) => (
  <div style={{
    width: `${size}px`,
    height: `${size}px`,
    borderRadius: '50%',
    backgroundColor: color,
    animation: 'livePulse 2s ease-in-out infinite',
    flexShrink: 0
  }} />
)

// ─── Temperature arc gauge (SVG) ────────────────────────────────────────────
const TempGauge = ({ current, target, size = 60 }) => {
  const ratio = Math.min(current / target, 1)
  const radius = (size - 8) / 2
  const circumference = Math.PI * radius // half circle
  const offset = circumference * (1 - ratio)

  return (
    <svg width={size} height={size / 2 + 8} viewBox={`0 0 ${size} ${size / 2 + 8}`}>
      <path
        d={`M 4 ${size / 2 + 4} A ${radius} ${radius} 0 0 1 ${size - 4} ${size / 2 + 4}`}
        fill="none"
        stroke="rgba(230,81,0,0.15)"
        strokeWidth="6"
        strokeLinecap="round"
      />
      <path
        d={`M 4 ${size / 2 + 4} A ${radius} ${radius} 0 0 1 ${size - 4} ${size / 2 + 4}`}
        fill="none"
        stroke={colors.primary}
        strokeWidth="6"
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        style={{ transition: 'stroke-dashoffset 0.6s ease' }}
      />
      <text
        x={size / 2}
        y={size / 2}
        textAnchor="middle"
        fill={colors.textPrimary}
        fontSize="12"
        fontWeight="700"
      >
        {current}°
      </text>
    </svg>
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// iOS Lock Screen Live Activity
// ═══════════════════════════════════════════════════════════════════════════════
const IOSLockScreenActivity = ({ session, state = 'cooking' }) => {
  const isEnded = state === 'completed' || state === 'failed'

  return (
    <div style={{
      background: 'rgba(30, 30, 30, 0.85)',
      backdropFilter: 'blur(40px)',
      WebkitBackdropFilter: 'blur(40px)',
      borderRadius: '20px',
      padding: '16px',
      color: '#fff',
      fontFamily: '-apple-system, SF Pro Display, system-ui, sans-serif',
      maxWidth: '360px',
      width: '100%'
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '28px', height: '28px', borderRadius: '8px',
            background: 'linear-gradient(135deg, #E65100, #FF8A65)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <ChefHat size={16} color="#fff" />
          </div>
          <span style={{ fontSize: '13px', fontWeight: '600', opacity: 0.7 }}>Epicura</span>
        </div>
        {!isEnded && <LiveDot size={8} color="#34C759" />}
      </div>

      {isEnded ? (
        // ─── End state ─────────────────────────────────────────────────
        <div style={{ textAlign: 'center', padding: '8px 0' }}>
          {state === 'completed' ? (
            <>
              <CheckCircle size={36} color="#34C759" style={{ marginBottom: '8px' }} />
              <div style={{ fontSize: '17px', fontWeight: '600' }}>{session.recipeName}</div>
              <div style={{ fontSize: '13px', opacity: 0.6, marginTop: '4px' }}>Cooking complete — ready to serve!</div>
            </>
          ) : (
            <>
              <XCircle size={36} color="#FF453A" style={{ marginBottom: '8px' }} />
              <div style={{ fontSize: '17px', fontWeight: '600' }}>{session.recipeName}</div>
              <div style={{ fontSize: '13px', color: '#FF453A', marginTop: '4px' }}>Session stopped — check the robot</div>
            </>
          )}
        </div>
      ) : (
        // ─── Active cooking state ──────────────────────────────────────
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '17px', fontWeight: '600', marginBottom: '4px' }}>{session.recipeName}</div>
              <div style={{ fontSize: '13px', opacity: 0.6 }}>{session.currentStage}</div>
            </div>
            <TempGauge current={session.temperature} target={session.targetTemp} size={56} />
          </div>

          {/* Progress bar */}
          <div style={{ marginTop: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span style={{ fontSize: '13px', opacity: 0.6 }}>
                <Flame size={12} style={{ verticalAlign: 'middle', marginRight: '3px' }} />
                {session.temperature}°C / {session.targetTemp}°C
              </span>
              <span style={{ fontSize: '13px', fontWeight: '600', fontVariantNumeric: 'tabular-nums' }}>
                {formatTime(session.timeRemaining)} left
              </span>
            </div>
            <div style={{ height: '4px', borderRadius: '2px', background: 'rgba(255,255,255,0.15)', overflow: 'hidden' }}>
              <div style={{
                width: `${session.progress * 100}%`,
                height: '100%',
                borderRadius: '2px',
                background: 'linear-gradient(90deg, #E65100, #FF8A65)',
                transition: 'width 0.5s ease'
              }} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// Dynamic Island — Compact (pill)
// ═══════════════════════════════════════════════════════════════════════════════
const DynamicIslandCompact = ({ session }) => (
  <div style={{
    background: '#000',
    borderRadius: '36px',
    padding: '8px 16px 8px 12px',
    color: '#fff',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '10px',
    fontFamily: '-apple-system, SF Pro Display, system-ui, sans-serif',
    minWidth: '200px',
    maxWidth: '320px'
  }}>
    <div style={{
      width: '24px', height: '24px', borderRadius: '50%',
      background: 'linear-gradient(135deg, #E65100, #FF8A65)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
    }}>
      <ChefHat size={13} color="#fff" />
    </div>
    <span style={{ fontSize: '13px', fontWeight: '500', flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
      {session.recipeName}
    </span>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <LiveDot size={6} color="#34C759" />
      <span style={{ fontSize: '13px', fontWeight: '700', fontVariantNumeric: 'tabular-nums' }}>
        {formatTime(session.timeRemaining)}
      </span>
    </div>
  </div>
)

// ═══════════════════════════════════════════════════════════════════════════════
// Dynamic Island — Expanded
// ═══════════════════════════════════════════════════════════════════════════════
const DynamicIslandExpanded = ({ session }) => (
  <div style={{
    background: '#000',
    borderRadius: '44px',
    padding: '20px 24px',
    color: '#fff',
    fontFamily: '-apple-system, SF Pro Display, system-ui, sans-serif',
    maxWidth: '370px',
    width: '100%'
  }}>
    {/* Top row */}
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '50%',
          background: 'linear-gradient(135deg, #E65100, #FF8A65)',
          display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          <ChefHat size={16} color="#fff" />
        </div>
        <div>
          <div style={{ fontSize: '15px', fontWeight: '600' }}>{session.recipeName}</div>
          <div style={{ fontSize: '12px', opacity: 0.5 }}>{session.currentStage}</div>
        </div>
      </div>
      <TempGauge current={session.temperature} target={session.targetTemp} size={48} />
    </div>

    {/* Progress */}
    <div style={{ height: '4px', borderRadius: '2px', background: 'rgba(255,255,255,0.12)', overflow: 'hidden', marginBottom: '10px' }}>
      <div style={{
        width: `${session.progress * 100}%`,
        height: '100%',
        borderRadius: '2px',
        background: 'linear-gradient(90deg, #E65100, #FF8A65)',
        transition: 'width 0.5s ease'
      }} />
    </div>

    {/* Bottom row */}
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
        <LiveDot size={6} color="#34C759" />
        <span style={{ fontSize: '12px', opacity: 0.5 }}>Live</span>
      </div>
      <span style={{ fontSize: '22px', fontWeight: '700', fontVariantNumeric: 'tabular-nums' }}>
        {formatTime(session.timeRemaining)}
      </span>
    </div>
  </div>
)

// ═══════════════════════════════════════════════════════════════════════════════
// Android Glance Widget — Small (2×1)
// ═══════════════════════════════════════════════════════════════════════════════
const AndroidGlanceSmall = ({ session, state = 'cooking' }) => {
  const isEnded = state === 'completed' || state === 'failed'

  return (
    <div style={{
      background: '#F5F0EB',
      borderRadius: '28px',
      padding: '14px 16px',
      fontFamily: '"Google Sans", Roboto, system-ui, sans-serif',
      width: '200px',
      border: '1px solid rgba(0,0,0,0.06)'
    }}>
      {isEnded ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {state === 'completed'
            ? <CheckCircle size={20} color={colors.success} />
            : <XCircle size={20} color={colors.emergency} />
          }
          <div>
            <div style={{ fontSize: '14px', fontWeight: '500', color: '#1C1B1F' }}>{session.recipeName}</div>
            <div style={{ fontSize: '11px', color: '#49454F' }}>
              {state === 'completed' ? 'Done' : 'Failed'}
            </div>
          </div>
        </div>
      ) : (
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <LiveDot size={6} color={colors.success} />
              <span style={{ fontSize: '14px', fontWeight: '500', color: '#1C1B1F' }}>{session.recipeName}</span>
            </div>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
            <span style={{ fontSize: '11px', color: '#49454F' }}>{session.currentStage}</span>
            <span style={{ fontSize: '13px', fontWeight: '600', color: '#1C1B1F', fontVariantNumeric: 'tabular-nums' }}>
              {formatTime(session.timeRemaining)}
            </span>
          </div>
          <div style={{ height: '4px', borderRadius: '2px', background: 'rgba(28,27,31,0.08)', marginTop: '8px', overflow: 'hidden' }}>
            <div style={{
              width: `${session.progress * 100}%`,
              height: '100%',
              borderRadius: '2px',
              background: colors.primary,
              transition: 'width 0.5s ease'
            }} />
          </div>
        </>
      )}
    </div>
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// Android Glance Widget — Medium (3×2)
// ═══════════════════════════════════════════════════════════════════════════════
const AndroidGlanceMedium = ({ session, state = 'cooking' }) => {
  const isEnded = state === 'completed' || state === 'failed'

  return (
    <div style={{
      background: '#F5F0EB',
      borderRadius: '28px',
      padding: '20px',
      fontFamily: '"Google Sans", Roboto, system-ui, sans-serif',
      width: '320px',
      border: '1px solid rgba(0,0,0,0.06)'
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '28px', height: '28px', borderRadius: '14px',
            background: colors.primary,
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <ChefHat size={14} color="#fff" />
          </div>
          <span style={{ fontSize: '12px', color: '#49454F', fontWeight: '500' }}>Epicura</span>
        </div>
        {!isEnded && <LiveDot size={7} color={colors.success} />}
      </div>

      {isEnded ? (
        <div style={{ textAlign: 'center', padding: '12px 0' }}>
          {state === 'completed' ? (
            <>
              <CheckCircle size={32} color={colors.success} style={{ marginBottom: '8px' }} />
              <div style={{ fontSize: '16px', fontWeight: '500', color: '#1C1B1F' }}>{session.recipeName}</div>
              <div style={{ fontSize: '12px', color: '#49454F', marginTop: '4px' }}>Cooking complete</div>
            </>
          ) : (
            <>
              <XCircle size={32} color={colors.emergency} style={{ marginBottom: '8px' }} />
              <div style={{ fontSize: '16px', fontWeight: '500', color: '#1C1B1F' }}>{session.recipeName}</div>
              <div style={{ fontSize: '12px', color: colors.emergency, marginTop: '4px' }}>Session stopped</div>
            </>
          )}
        </div>
      ) : (
        <>
          <div style={{ fontSize: '16px', fontWeight: '500', color: '#1C1B1F', marginBottom: '4px' }}>{session.recipeName}</div>
          <div style={{ fontSize: '12px', color: '#49454F', marginBottom: '14px' }}>{session.currentStage}</div>

          {/* Stats row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Flame size={14} color={colors.primary} />
              <span style={{ fontSize: '13px', color: '#1C1B1F' }}>{session.temperature}°C / {session.targetTemp}°C</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Clock size={14} color="#49454F" />
              <span style={{ fontSize: '20px', fontWeight: '600', color: '#1C1B1F', fontVariantNumeric: 'tabular-nums' }}>
                {formatTime(session.timeRemaining)}
              </span>
            </div>
          </div>

          {/* Progress */}
          <div style={{ height: '6px', borderRadius: '3px', background: 'rgba(28,27,31,0.08)', overflow: 'hidden' }}>
            <div style={{
              width: `${session.progress * 100}%`,
              height: '100%',
              borderRadius: '3px',
              background: colors.primary,
              transition: 'width 0.5s ease'
            }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px' }}>
            <span style={{ fontSize: '11px', color: '#49454F' }}>{Math.round(session.progress * 100)}%</span>
          </div>
        </>
      )}
    </div>
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// Showcase Screen
// ═══════════════════════════════════════════════════════════════════════════════
const GlanceScreen = () => {
  const [endState, setEndState] = useState('cooking') // 'cooking' | 'completed' | 'failed'
  const session = activeCookingSession

  const sectionLabelStyle = {
    ...typography.small,
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: '1.5px',
    marginBottom: spacing.sm,
    marginTop: spacing.lg
  }

  const chipStyle = (active) => ({
    padding: '6px 14px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: '600',
    cursor: 'pointer',
    border: 'none',
    background: active ? colors.primary : 'rgba(0,0,0,0.06)',
    color: active ? '#fff' : colors.textPrimary,
    transition: 'all 0.2s ease'
  })

  return (
    <div style={{
      minHeight: '100vh',
      background: colors.background,
      padding: `${spacing.lg} ${spacing.md}`,
      paddingBottom: '100px'
    }}>
      <style>{`
        @keyframes livePulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>

      <div style={{ ...typography.title, color: colors.textPrimary, marginBottom: spacing.xs }}>
        Live Activity & Glance
      </div>
      <div style={{ ...typography.caption, color: colors.textSecondary, marginBottom: spacing.md }}>
        Cooking progress widgets for iOS and Android
      </div>

      {/* State toggle */}
      <div style={{ display: 'flex', gap: spacing.sm, marginBottom: spacing.lg }}>
        {['cooking', 'completed', 'failed'].map((s) => (
          <button key={s} style={chipStyle(endState === s)} onClick={() => setEndState(s)}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {/* ── iOS Section ─────────────────────────────────────────────── */}
      <div style={sectionLabelStyle}>iOS — Dynamic Island (Compact)</div>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: spacing.lg }}>
        <DynamicIslandCompact session={session} />
      </div>

      <div style={sectionLabelStyle}>iOS — Dynamic Island (Expanded)</div>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: spacing.lg }}>
        <DynamicIslandExpanded session={session} />
      </div>

      <div style={sectionLabelStyle}>iOS — Lock Screen Live Activity</div>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: spacing.lg }}>
        <IOSLockScreenActivity session={session} state={endState} />
      </div>

      {/* ── Android Section ──────────────────────────────────────────── */}
      <div style={sectionLabelStyle}>Android — Glance Widget (Small 2×1)</div>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: spacing.lg }}>
        <AndroidGlanceSmall session={session} state={endState} />
      </div>

      <div style={sectionLabelStyle}>Android — Glance Widget (Medium 3×2)</div>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: spacing.lg }}>
        <AndroidGlanceMedium session={session} state={endState} />
      </div>
    </div>
  )
}

export default GlanceScreen
