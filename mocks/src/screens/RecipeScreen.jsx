import React, { useState } from 'react'
import { Search } from 'lucide-react'
import RecipeCard from '../components/RecipeCard'
import { recipes } from '../data/mockData'
import { colors, glassMorphism, typography, spacing } from '../theme'

const RecipeScreen = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeFilters, setActiveFilters] = useState(['All'])

  const filters = [
    { id: 'All', label: 'All' },
    { id: 'Vegetarian', label: 'Vegetarian' },
    { id: 'Quick', label: 'Quick <30min' },
    { id: 'Rice', label: 'Rice' },
    { id: 'Dal', label: 'Dal' }
  ]

  const toggleFilter = (filterId) => {
    if (filterId === 'All') {
      setActiveFilters(['All'])
    } else {
      const newFilters = activeFilters.filter(f => f !== 'All')
      if (activeFilters.includes(filterId)) {
        const filtered = newFilters.filter(f => f !== filterId)
        setActiveFilters(filtered.length === 0 ? ['All'] : filtered)
      } else {
        setActiveFilters([...newFilters, filterId])
      }
    }
  }

  const filteredRecipes = recipes.filter(recipe => {
    const matchesSearch = recipe.name.toLowerCase().includes(searchQuery.toLowerCase())

    if (activeFilters.includes('All')) return matchesSearch

    const matchesFilter = activeFilters.some(filter => {
      if (filter === 'Quick') return recipe.time_minutes < 30
      return recipe.tags.includes(filter)
    })

    return matchesSearch && matchesFilter
  })

  const containerStyle = {
    padding: spacing.md,
    paddingBottom: '100px',
    maxWidth: '1200px',
    margin: '0 auto'
  }

  const searchContainerStyle = {
    ...glassMorphism,
    borderRadius: '12px',
    padding: spacing.sm,
    display: 'flex',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.md
  }

  const searchInputStyle = {
    flex: 1,
    border: 'none',
    background: 'transparent',
    ...typography.body,
    color: colors.textPrimary,
    outline: 'none'
  }

  const filterContainerStyle = {
    display: 'flex',
    gap: spacing.sm,
    overflowX: 'auto',
    marginBottom: spacing.lg,
    paddingBottom: spacing.sm
  }

  const filterChipStyle = (isActive) => ({
    padding: '8px 16px',
    borderRadius: '20px',
    ...typography.caption,
    fontWeight: '600',
    whiteSpace: 'nowrap',
    transition: 'all 0.3s ease',
    backgroundColor: isActive ? colors.primary : 'rgba(255, 255, 255, 0.7)',
    color: isActive ? colors.surface : colors.textPrimary,
    border: `2px solid ${isActive ? colors.primary : 'rgba(230, 81, 0, 0.2)'}`,
    cursor: 'pointer',
    backdropFilter: 'blur(10px)'
  })

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
    gap: spacing.md
  }

  return (
    <div style={containerStyle}>
      <div style={searchContainerStyle}>
        <Search size={20} color={colors.textSecondary} />
        <input
          type="text"
          placeholder="Search recipes..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          style={searchInputStyle}
        />
      </div>

      <div style={filterContainerStyle}>
        {filters.map(filter => (
          <button
            key={filter.id}
            onClick={() => toggleFilter(filter.id)}
            style={filterChipStyle(activeFilters.includes(filter.id))}
          >
            {filter.label}
          </button>
        ))}
      </div>

      <div style={gridStyle}>
        {filteredRecipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} onClick={() => console.log('Recipe clicked:', recipe.name)} />
        ))}
      </div>
    </div>
  )
}

export default RecipeScreen
