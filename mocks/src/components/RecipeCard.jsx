import React from 'react'
import { Clock } from 'lucide-react'
import { colors, glassMorphism, typography, spacing } from '../theme'

const RecipeCard = ({ recipe, onClick }) => {
  const cardStyle = {
    ...glassMorphism,
    borderRadius: '16px',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
    ':hover': {
      transform: 'translateY(-4px)'
    }
  }

  const imageStyle = {
    width: '100%',
    height: '140px',
    objectFit: 'cover',
    display: 'block'
  }

  const contentStyle = {
    padding: spacing.md
  }

  const nameStyle = {
    ...typography.subheading,
    color: colors.textPrimary,
    marginBottom: spacing.xs
  }

  const badgeContainerStyle = {
    display: 'flex',
    gap: spacing.sm,
    marginTop: spacing.sm
  }

  const badgeStyle = (bgColor) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    padding: '4px 8px',
    borderRadius: '8px',
    backgroundColor: bgColor,
    ...typography.small,
    color: colors.surface,
    fontWeight: '600'
  })

  const difficultyColor = {
    'Easy': colors.success,
    'Medium': colors.warning,
    'Hard': colors.emergency
  }

  return (
    <div style={cardStyle} onClick={onClick}>
      <img src={recipe.image} alt={recipe.name} style={imageStyle} />
      <div style={contentStyle}>
        <div style={nameStyle}>{recipe.name}</div>
        <div style={badgeContainerStyle}>
          <div style={badgeStyle(colors.primary)}>
            <Clock size={12} />
            {recipe.time_minutes} min
          </div>
          <div style={badgeStyle(difficultyColor[recipe.difficulty])}>
            {recipe.difficulty}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RecipeCard
