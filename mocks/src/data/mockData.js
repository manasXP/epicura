export const recipes = [
  {
    id: 1,
    name: 'Dal Tadka',
    image: 'https://placehold.co/400x300/E65100/white?text=Dal+Tadka',
    category: 'Dal',
    cuisine: 'Indian',
    difficulty: 'Easy',
    time_minutes: 30,
    servings: 4,
    tags: ['Vegetarian', 'Dal', 'Quick'],
    isFavourite: true
  },
  {
    id: 2,
    name: 'Paneer Butter Masala',
    image: 'https://placehold.co/400x300/2E7D32/white?text=Paneer+Butter+Masala',
    category: 'Curry',
    cuisine: 'Indian',
    difficulty: 'Medium',
    time_minutes: 45,
    servings: 4,
    tags: ['Vegetarian', 'Paneer'],
    isFavourite: true
  },
  {
    id: 3,
    name: 'Jeera Rice',
    image: 'https://placehold.co/400x300/FFB300/white?text=Jeera+Rice',
    category: 'Rice',
    cuisine: 'Indian',
    difficulty: 'Easy',
    time_minutes: 20,
    servings: 4,
    tags: ['Vegetarian', 'Rice', 'Quick'],
    isFavourite: false
  },
  {
    id: 4,
    name: 'Chicken Biryani',
    image: 'https://placehold.co/400x300/BF360C/white?text=Chicken+Biryani',
    category: 'Rice',
    cuisine: 'Indian',
    difficulty: 'Hard',
    time_minutes: 90,
    servings: 6,
    tags: ['Non-Vegetarian', 'Rice', 'Chicken'],
    isFavourite: true
  },
  {
    id: 5,
    name: 'Aloo Gobi',
    image: 'https://placehold.co/400x300/43A047/white?text=Aloo+Gobi',
    category: 'Vegetable',
    cuisine: 'Indian',
    difficulty: 'Easy',
    time_minutes: 35,
    servings: 4,
    tags: ['Vegetarian', 'Quick'],
    isFavourite: false
  },
  {
    id: 6,
    name: 'Rajma',
    image: 'https://placehold.co/400x300/D50000/white?text=Rajma',
    category: 'Dal',
    cuisine: 'Indian',
    difficulty: 'Medium',
    time_minutes: 60,
    servings: 4,
    tags: ['Vegetarian', 'Dal'],
    isFavourite: false
  },
  {
    id: 7,
    name: 'Chole',
    image: 'https://placehold.co/400x300/6D4C41/white?text=Chole',
    category: 'Curry',
    cuisine: 'Indian',
    difficulty: 'Medium',
    time_minutes: 50,
    servings: 4,
    tags: ['Vegetarian'],
    isFavourite: false
  },
  {
    id: 8,
    name: 'Sambar',
    image: 'https://placehold.co/400x300/E65100/white?text=Sambar',
    category: 'Dal',
    cuisine: 'South Indian',
    difficulty: 'Easy',
    time_minutes: 40,
    servings: 4,
    tags: ['Vegetarian', 'Dal'],
    isFavourite: false
  }
]

export const sessions = [
  {
    id: 1,
    recipeId: 1,
    recipeName: 'Dal Tadka',
    date: '2026-02-16T18:30:00',
    duration_s: 1800,
    status: 'completed'
  },
  {
    id: 2,
    recipeId: 4,
    recipeName: 'Chicken Biryani',
    date: '2026-02-15T12:00:00',
    duration_s: 5400,
    status: 'completed'
  },
  {
    id: 3,
    recipeId: 2,
    recipeName: 'Paneer Butter Masala',
    date: '2026-02-14T19:00:00',
    duration_s: 2700,
    status: 'completed'
  },
  {
    id: 4,
    recipeId: 6,
    recipeName: 'Rajma',
    date: '2026-02-13T13:30:00',
    duration_s: 1200,
    status: 'failed'
  },
  {
    id: 5,
    recipeId: 3,
    recipeName: 'Jeera Rice',
    date: '2026-02-12T20:00:00',
    duration_s: 1200,
    status: 'completed'
  }
]

export const user = {
  name: 'Manas Pradhan',
  phone: '+91 98765 43210',
  avatar: 'https://placehold.co/120x120/E65100/white?text=MP',
  preferences: {
    spiceLevel: 3,
    defaultServings: 4,
    dietaryTags: ['Vegetarian']
  }
}

export const activeCookingSession = {
  recipeName: 'Dal Tadka',
  currentStage: 'Tempering spices',
  temperature: 165,
  targetTemp: 180,
  timeRemaining: 420,
  progress: 0.65
}
