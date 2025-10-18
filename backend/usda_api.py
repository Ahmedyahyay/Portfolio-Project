import requests
import json
import time
import logging
from typing import List, Dict, Optional
from models import db, Meal, FoodCategory

logger = logging.getLogger(__name__)

class USDANutritionFetcher:
    """USDA FoodData Central API integration following copilot health-centric patterns"""
    
    def __init__(self, api_key: str = 'DEMO_KEY'):
        self.api_key = api_key
        self.base_url = 'https://api.nal.usda.gov/fdc/v1'
        self.session = requests.Session()
        
    def fetch_suitable_meals(self, target_count: int = 75) -> List[Dict]:
        """Fetch meals suitable for BMI >= 30 demographic following copilot business rules"""
        logger.info(f"🔍 Fetching {target_count} suitable meals from USDA FoodData Central")
        
        # Search terms optimized for BMI >= 30 demographic
        search_terms = [
            # High-protein breakfast options
            'greek yogurt plain', 'oatmeal steel cut', 'egg white scrambled',
            'cottage cheese low fat', 'protein smoothie', 'whole grain toast',
            
            # Lean proteins for main meals
            'chicken breast grilled', 'salmon baked', 'turkey breast roasted',
            'cod fillet baked', 'lean ground turkey', 'tuna canned water',
            'tofu firm', 'tempeh', 'lentils cooked', 'black beans cooked',
            
            # Nutrient-dense vegetables and sides
            'broccoli steamed', 'spinach fresh', 'kale massaged',
            'asparagus grilled', 'cauliflower roasted', 'brussels sprouts',
            'sweet potato baked', 'quinoa cooked', 'brown rice cooked',
            
            # Healthy fats and snacks
            'avocado fresh', 'almonds raw', 'walnuts', 'hummus',
            'olive oil extra virgin', 'chia seeds', 'flaxseed ground',
            
            # Low-calorie, high-volume foods
            'cucumber fresh', 'celery raw', 'carrot raw', 'bell pepper',
            'tomato fresh', 'lettuce romaine', 'cabbage raw',
            
            # Fiber-rich options
            'apple fresh', 'pear fresh', 'berries mixed', 'beans kidney',
            'chickpeas cooked', 'edamame', 'artichoke hearts'
        ]
        
        meals = []
        processed_count = 0
        
        for search_term in search_terms:
            if processed_count >= target_count:
                break
                
            try:
                # Rate limiting to respect API guidelines
                time.sleep(0.5)
                
                food_data = self._search_foods(search_term, limit=2)
                
                for food in food_data:
                    if processed_count >= target_count:
                        break
                        
                    meal_data = self._parse_food_to_meal(food, search_term)
                    if meal_data and self._validate_meal_for_target_demographic(meal_data):
                        meals.append(meal_data)
                        processed_count += 1
                        logger.info(f"✅ Added: {meal_data['name']} (Score: {meal_data.get('nutrition_score', 0):.1f})")
                        
            except Exception as e:
                logger.warning(f"⚠️ Failed to fetch {search_term}: {e}")
                continue
        
        # Add fallback meals if API quota exceeded
        if len(meals) < 25:
            logger.info("📝 Adding fallback sample meals due to API limitations")
            meals.extend(self._get_fallback_meals()[:(target_count - len(meals))])
        
        logger.info(f"✅ Total meals fetched: {len(meals)}")
        return meals
    
    def _search_foods(self, search_term: str, limit: int = 2) -> List[Dict]:
        """Search USDA database for specific foods"""
        search_url = f"{self.base_url}/foods/search"
        params = {
            'api_key': self.api_key,
            'query': search_term,
            'dataType': ['Foundation', 'SR Legacy'],
            'pageSize': limit,
            'sortBy': 'dataType.keyword',
            'sortOrder': 'asc'
        }
        
        response = self.session.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get('foods', [])
    
    def _parse_food_to_meal(self, food_data: Dict, search_term: str) -> Optional[Dict]:
        """Parse USDA food data to meal format following copilot health-centric model"""
        try:
            food_id = food_data.get('fdcId')
            description = food_data.get('description', search_term)
            
            # Clean up food name
            name = self._clean_food_name(description)
            
            # Extract nutrients
            nutrients = self._extract_nutrients(food_data.get('foodNutrients', []))
            
            # Determine meal type based on search term
            meal_type = self._determine_meal_type(name, search_term)
            
            # Determine allergens
            allergens = self._determine_allergens(name, food_data)
            
            # Generate ingredients description
            ingredients = self._generate_ingredients(name, food_data)
            
            meal_data = {
                'name': name,
                'type': meal_type,
                'calories': nutrients.get('calories', 0),
                'protein': nutrients.get('protein', 0.0),
                'carbs': nutrients.get('carbs', 0.0),
                'fat': nutrients.get('fat', 0.0),
                'fiber': nutrients.get('fiber', 0.0),
                'sugar': nutrients.get('sugar', 0.0),
                'sodium': nutrients.get('sodium', 0.0),
                'ingredients': ingredients,
                'allergens': allergens,
                'usda_id': str(food_id),
                'serving_size': self._determine_serving_size(nutrients.get('calories', 100))
            }
            
            # Calculate nutrition score following copilot patterns
            meal_data['nutrition_score'] = self._calculate_nutrition_score(meal_data)
            
            return meal_data
            
        except Exception as e:
            logger.error(f"Error parsing food data: {e}")
            return None
    
    def _extract_nutrients(self, food_nutrients: List[Dict]) -> Dict:
        """Extract nutrition values from USDA nutrient data"""
        nutrients = {
            'calories': 0,
            'protein': 0.0,
            'carbs': 0.0,
            'fat': 0.0,
            'fiber': 0.0,
            'sugar': 0.0,
            'sodium': 0.0
        }
        
        for nutrient in food_nutrients:
            nutrient_name = nutrient.get('nutrientName', '').lower()
            value = float(nutrient.get('value', 0))
            
            # Map USDA nutrient names to our fields
            if 'energy' in nutrient_name and 'kcal' in nutrient_name:
                nutrients['calories'] = int(value)
            elif 'protein' in nutrient_name:
                nutrients['protein'] = round(value, 1)
            elif 'carbohydrate' in nutrient_name and 'fiber' not in nutrient_name:
                nutrients['carbs'] = round(value, 1)
            elif 'total lipid' in nutrient_name or ('fat' in nutrient_name and 'fatty' not in nutrient_name):
                nutrients['fat'] = round(value, 1)
            elif 'fiber' in nutrient_name and 'total dietary' in nutrient_name:
                nutrients['fiber'] = round(value, 1)
            elif 'sugars' in nutrient_name and 'total' in nutrient_name:
                nutrients['sugar'] = round(value, 1)
            elif 'sodium' in nutrient_name:
                nutrients['sodium'] = round(value, 1)
        
        return nutrients
    
    def _clean_food_name(self, description: str) -> str:
        """Clean USDA food descriptions for better readability"""
        # Remove common USDA suffixes and prefixes
        cleanups = [
            ', raw', ', cooked', ', boiled', ', steamed', ', baked', ', grilled',
            ', roasted', ', canned', ', frozen', ', dried', ', fresh',
            'usda commodity', ', no salt added', ', drained solids'
        ]
        
        name = description.lower()
        for cleanup in cleanups:
            name = name.replace(cleanup, '')
        
        # Capitalize properly and limit length
        name = ' '.join(word.capitalize() for word in name.split())
        return name[:50] + '...' if len(name) > 50 else name
    
    def _determine_meal_type(self, name: str, search_term: str) -> str:
        """Determine meal type following copilot health-centric patterns"""
        combined_text = (name + ' ' + search_term).lower()
        
        if any(word in combined_text for word in ['oatmeal', 'yogurt', 'egg', 'toast', 'breakfast']):
            return 'breakfast'
        elif any(word in combined_text for word in ['chicken', 'salmon', 'turkey', 'beef', 'dinner']):
            return 'dinner'
        elif any(word in combined_text for word in ['salad', 'soup', 'sandwich', 'lunch']):
            return 'lunch'
        else:
            return 'snack'
    
    def _determine_allergens(self, name: str, food_data: Dict) -> str:
        """Determine allergens based on food name and data"""
        allergens = []
        text = (name + ' ' + str(food_data)).lower()
        
        allergen_keywords = {
            'Dairy': ['milk', 'cheese', 'yogurt', 'cream', 'butter', 'whey'],
            'Nuts': ['almond', 'peanut', 'walnut', 'pecan', 'cashew', 'hazelnut'],
            'Fish': ['salmon', 'tuna', 'cod', 'fish', 'seafood'],
            'Eggs': ['egg', 'eggs', 'albumin'],
            'Gluten': ['wheat', 'barley', 'rye', 'bread', 'pasta'],
            'Soy': ['soy', 'tofu', 'tempeh', 'soybean', 'edamame']
        }
        
        for allergen, keywords in allergen_keywords.items():
            if any(keyword in text for keyword in keywords):
                allergens.append(allergen)
        
        return ', '.join(allergens) if allergens else 'None'
    
    def _generate_ingredients(self, name: str, food_data: Dict) -> str:
        """Generate ingredients description from food name and data"""
        # Check if actual ingredients are provided
        if 'ingredients' in food_data:
            return food_data['ingredients']
        
        # Generate based on food name
        name_lower = name.lower()
        if 'yogurt' in name_lower:
            return 'cultured milk, live active cultures'
        elif 'oatmeal' in name_lower:
            return 'steel cut oats, water'
        elif 'salmon' in name_lower:
            return 'atlantic salmon fillet'
        elif 'chicken' in name_lower:
            return 'boneless skinless chicken breast'
        else:
            return name.lower()
    
    def _determine_serving_size(self, calories: int) -> str:
        """Determine appropriate serving size based on calories"""
        if calories <= 100:
            return '100g'
        elif calories <= 200:
            return '150g'
        elif calories <= 400:
            return '200g'
        else:
            return '250g'
    
    def _calculate_nutrition_score(self, meal_data: Dict) -> float:
        """Calculate nutrition score following copilot health-centric patterns"""
        score = 0.0
        
        # Protein scoring (higher is better for weight management)
        protein = meal_data.get('protein', 0)
        if protein:
            score += min(protein / 30 * 20, 20)
        
        # Fiber scoring (higher is better)
        fiber = meal_data.get('fiber', 0)
        if fiber:
            score += min(fiber / 10 * 15, 15)
        
        # Calorie density scoring (lower is better for volume eating)
        calories = meal_data.get('calories', 0)
        if calories <= 200:
            score += 15
        elif calories <= 400:
            score += 10
        else:
            score += 5
        
        return min(score, 50.0)
    
    def _validate_meal_for_target_demographic(self, meal_data: Dict) -> bool:
        """Validate meal suitability for BMI >= 30 demographic"""
        # Must have reasonable calorie count
        calories = meal_data.get('calories', 0)
        if not (50 <= calories <= 600):
            return False
        
        # Must have nutrition score above minimum threshold
        nutrition_score = meal_data.get('nutrition_score', 0)
        if nutrition_score < 10:
            return False
        
        # Must have valid name
        if not meal_data.get('name', '').strip():
            return False
        
        return True
    
    def _get_fallback_meals(self) -> List[Dict]:
        """Fallback meals if USDA API is unavailable"""
        return [
            {
                'name': 'Grilled Chicken Breast',
                'type': 'lunch',
                'calories': 285,
                'protein': 35.2,
                'carbs': 0.0,
                'fat': 12.8,
                'fiber': 0.0,
                'sugar': 0.0,
                'sodium': 140.0,
                'ingredients': 'boneless skinless chicken breast, olive oil, herbs',
                'allergens': 'None',
                'usda_id': '171077',
                'serving_size': '150g'
            },
            {
                'name': 'Greek Yogurt Plain',
                'type': 'breakfast',
                'calories': 195,
                'protein': 18.2,
                'carbs': 22.5,
                'fat': 4.8,
                'fiber': 3.2,
                'sugar': 18.0,
                'sodium': 85.0,
                'ingredients': 'cultured pasteurized grade a nonfat milk',
                'allergens': 'Dairy',
                'usda_id': '170900',
                'serving_size': '200g'
            },
            # ... more fallback meals
        ]

def populate_usda_meals(target_count: int = 75):
    """Populate database with USDA meals following copilot health-centric patterns"""
    logger.info("🍽️ Starting USDA meal population for BMI >= 30 demographic")
    
    # Check if meals already exist
    existing_count = Meal.query.count()
    if existing_count >= target_count:
        logger.info(f"✅ Database already has {existing_count} meals, skipping population")
        return existing_count
    
    # Initialize USDA fetcher
    fetcher = USDANutritionFetcher()
    
    # Fetch meals from API
    meal_data_list = fetcher.fetch_suitable_meals(target_count)
    
    # Add meals to database
    added_count = 0
    for meal_data in meal_data_list:
        try:
            # Check if meal already exists by USDA ID
            if meal_data.get('usda_id'):
                existing = Meal.query.filter_by(usda_id=meal_data['usda_id']).first()
                if existing:
                    continue
            
            # Create new meal
            meal = Meal(
                name=meal_data['name'],
                type=meal_data['type'],
                calories=meal_data['calories'],
                protein=meal_data['protein'],
                carbs=meal_data['carbs'],
                fat=meal_data['fat'],
                fiber=meal_data['fiber'],
                sugar=meal_data['sugar'],
                sodium=meal_data['sodium'],
                ingredients=meal_data['ingredients'],
                allergens=meal_data['allergens'],
                usda_id=meal_data['usda_id'],
                serving_size=meal_data['serving_size']
            )
            
            db.session.add(meal)
            added_count += 1
            
        except Exception as e:
            logger.error(f"Error adding meal {meal_data.get('name', 'Unknown')}: {e}")
            continue
    
    # Commit all changes
    try:
        db.session.commit()
        logger.info(f"✅ Successfully added {added_count} USDA meals to database")
        
        # Add food categories
        _populate_food_categories()
        
        return added_count + existing_count
        
    except Exception as e:
        logger.error(f"Error committing meals to database: {e}")
        db.session.rollback()
        return existing_count

def _populate_food_categories():
    """Populate food categories following copilot health-centric patterns"""
    categories = [
        {
            'name': 'High Protein',
            'description': 'Foods with ≥15g protein per serving, ideal for muscle preservation',
            'color_code': '#FF5722'
        },
        {
            'name': 'High Fiber',
            'description': 'Foods with ≥3g fiber per serving, promoting satiety',
            'color_code': '#4CAF50'
        },
        {
            'name': 'Low Calorie Dense',
            'description': 'Foods with ≤200 calories per serving, supporting volume eating',
            'color_code': '#2196F3'
        },
        {
            'name': 'BMI ≥30 Optimized',
            'description': 'Meals specifically optimized for obesity management',
            'color_code': '#9C27B0'
        }
    ]
    
    for cat_data in categories:
        if not FoodCategory.query.filter_by(name=cat_data['name']).first():
            category = FoodCategory(**cat_data)
            db.session.add(category)
    
    try:
        db.session.commit()
        logger.info("✅ Food categories populated")
    except Exception as e:
        logger.error(f"Error adding food categories: {e}")
        db.session.rollback()
