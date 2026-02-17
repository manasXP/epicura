import React, { useState } from 'react'
import { Heart } from 'lucide-react'
import { recipes as initialRecipes } from '../data/mockData'
import { colors, glassMorphism, typography, spacing } from '../theme'

const FavouriteScreen = () => {
  const [recipes, setRecipes] = useState(initialRecipes)

  const favouriteRecipes = recipes.filter(r => r.isFavourite)

  const toggleFavourite = (recipeId) => {
    setRecipes(recipes.map(r =>
      r.id === recipeId ? { ...r, isFavourite: !r.isFavourite } : r
    ))
  }

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

  const recipeItemStyle = {
    ...glassMorphism,
    borderRadius: '16px',
    padding: spacing.md,
    marginBottom: spacing.md,
    display: 'flex',
    alignItems: 'center',
    gap: spacing.md
  }

  const recipeImageStyle = {
    width: '80px',
    height: '80px',
    borderRadius: '12px',
    objectFit: 'cover'
  }

  const recipeInfoStyle = {
    flex: 1
  }

  const recipeNameStyle = {
    ...typography.subheading,
    color: colors.textPrimary,
    marginBottom: spacing.xs
  }

  const recipeMetaStyle = {
    ...typography.caption,
    color: colors.textSecondary
  }

  const heartButtonStyle = {
    background: 'transparent',
    padding: spacing.sm,
    cursor: 'pointer'
  }

  return (
    <div style={containerStyle}>
      <div style={titleStyle}>Favourite Recipes</div>

      {favouriteRecipes.length === 0 ? (
        <div style={emptyStateStyle}>
          <Heart size={64} color={colors.textSecondary} style={emptyIconStyle} />
          <div style={emptyTextStyle}>
            No favourite recipes yet.<br />
            Start adding your favourites from the Recipe tab!
          </div>
        </div>
      ) : (
        favouriteRecipes.map(recipe => (
          <div key={recipe.id} style={recipeItemStyle}>
            <img src={recipe.image} alt={recipe.name} style={recipeImageStyle} />
            <div style={recipeInfoStyle}>
              <div style={recipeNameStyle}>{recipe.name}</div>
              <div style={recipeMetaStyle}>
                {recipe.time_minutes} min • {recipe.difficulty} • {recipe.cuisine}
              </div>
            </div>
            <button
              onClick={() => toggleFavourite(recipe.id)}
              style={heartButtonStyle}
            >
              <Heart
                size={24}
                color={colors.primary}
                fill={recipe.isFavourite ? colors.primary : 'none'}
              />
            </button>
          </div>
        ))
      )}
    </div>
  )
}

export default FavouriteScreen
