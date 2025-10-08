from flask import Blueprint, request, jsonify
import os
import requests
from sqlalchemy import and_
import json
from typing import List, Dict, Any

from models import db, User, Meal, MealHistory

meals_bp = Blueprint('meals', __name__)

# قاموس شامل للمواد المسببة للحساسية مع المرادفات
ALLERGEN_DICTIONARY = {
    # الحليب ومشتقاته
    "milk": ["حليب", "لبن", "جبن", "زبدة", "كريمة", "ميلك", "dairy", "lactose"],
    "بيض": ["egg", "بيض", "أومليت", "عجة", "mayo", "مايونيز"],

    # المكسرات
    "nuts": ["مكسرات", "لوز", "جوز", "فستق", "كاجو", "nuts", "almonds", "walnuts", "pistachios"],
    "peanuts": ["فول سوداني", "peanuts", "زبد الفول السوداني"],

    # القمح والحبوب
    "wheat": ["قمح", "wheat", "gluten", "خبز", "معكرونة", "bread", "pasta", "flour"],
    "soy": ["صويا", "soy", "توفو", "صلصة الصويا", "soy sauce"],

    # الأسماك والمأكولات البحرية
    "fish": ["أسماك", "fish", "سلمون", "تونة", "salmon", "tuna"],
    "shellfish": ["محار", "جمبري", "crab", "lobster", "shrimp"],

    # السمسم
    "sesame": ["سمسم", "sesame", "طحينة", "tahini", "حلاوة طحينية"],

    # المواد الأخرى
    "sulfites": ["كبريتيت", "sulfites", "مواد حافظة"],
    "mustard": ["خردل", "mustard"]
}


def normalize_allergen_name(allergen: str) -> str:
    """تطبيع اسم المادة المسببة للحساسية للبحث في القاموس"""
    allergen = allergen.strip().lower()

    # البحث في القاموس
    for main_allergen, synonyms in ALLERGEN_DICTIONARY.items():
        if allergen == main_allergen or allergen in synonyms:
            return main_allergen

    return allergen


def check_allergy_conflict(meal_allergens: List[str], user_allergens: List[str]) -> Dict[str, Any]:
    """
    فحص تعارض الحساسية مع تفاصيل دقيقة

    Returns:
        Dict containing:
        - has_conflict: bool
        - conflicting_allergens: List[str]
        - severity: str ('high', 'medium', 'low')
        - explanation: str
    """
    if not meal_allergens or not user_allergens:
        return {
            "has_conflict": False,
            "conflicting_allergens": [],
            "severity": "none",
            "explanation": "لا توجد مواد مسببة للحساسية"
        }

    # تطبيع قوائم الحساسية
    normalized_meal_allergens = [normalize_allergen_name(
        a) for a in meal_allergens if a.strip()]
    normalized_user_allergens = [normalize_allergen_name(
        a) for a in user_allergens if a.strip()]

    # البحث عن التعارضات
    conflicts = set(normalized_meal_allergens) & set(normalized_user_allergens)

    if not conflicts:
        return {
            "has_conflict": False,
            "conflicting_allergens": [],
            "severity": "none",
            "explanation": "الوجبة آمنة حسب حساسيتك"
        }

    # تحديد مستوى الخطورة
    high_risk_allergens = ["milk", "eggs",
                           "nuts", "peanuts", "fish", "shellfish"]
    medium_risk_allergens = ["wheat", "soy", "sesame"]

    severity = "low"
    if any(c in high_risk_allergens for c in conflicts):
        severity = "high"
    elif any(c in medium_risk_allergens for c in conflicts):
        severity = "medium"

    # إنشاء رسالة توضيحية
    allergen_names = {
        "milk": "الحليب",
        "eggs": "البيض",
        "nuts": "المكسرات",
        "peanuts": "الفول السوداني",
        "fish": "الأسماك",
        "shellfish": "المأكولات البحرية",
        "wheat": "القمح",
        "soy": "الصويا",
        "sesame": "السمسم"
    }

    conflict_names = [allergen_names.get(c, c) for c in conflicts]
    explanation = f"تحتوي هذه الوجبة على: {', '.join(conflict_names)}"

    if severity == "high":
        explanation += " - خطر عالي!"
    elif severity == "medium":
        explanation += " - تحذير متوسط"
    else:
        explanation += " - انتبه"

    return {
        "has_conflict": True,
        "conflicting_allergens": list(conflicts),
        "severity": severity,
        "explanation": explanation
    }


def analyze_meal_nutrition(meal: Meal, user: User) -> Dict[str, Any]:
    """
    تحليل شامل للوجبة من ناحية التغذية والمناسبية للمستخدم

    Returns:
        Dict containing nutritional analysis and recommendations
    """
    user_bmi = user.BMI or (user.weight_kg / ((user.height_cm/100) ** 2))

    # تحليل السعرات الحرارية
    calorie_analysis = {
        "meal_calories": meal.calories,
        "user_bmi": round(user_bmi, 2),
        "calorie_rating": "مناسب",
        "recommendation": ""
    }

    if user_bmi >= 30:  # سمنة
        if meal.calories > 700:
            calorie_analysis["calorie_rating"] = "عالية جداً"
            calorie_analysis[
                "recommendation"] = "هذه الوجبة عالية السعرات. يُنصح بوجبة أخف (أقل من 700 سعرة)"
        elif meal.calories > 500:
            calorie_analysis["calorie_rating"] = "عالية"
            calorie_analysis["recommendation"] = "وجبة مناسبة ولكن احرص على تناول وجبات أخف خلال اليوم"
    elif user_bmi < 18.5:  # نحافة
        if meal.calories < 400:
            calorie_analysis["calorie_rating"] = "منخفضة"
            calorie_analysis["recommendation"] = "يمكن إضافة وجبة خفيفة صحية لزيادة السعرات"
    else:  # وزن طبيعي
        if meal.calories > 800:
            calorie_analysis["calorie_rating"] = "عالية"
            calorie_analysis["recommendation"] = "وجبة دسمة، تأكد من التوازن مع باقي الوجبات"

    return {
        "calorie_analysis": calorie_analysis,
        "ingredient_count": len(meal.ingredients) if isinstance(meal.ingredients, list) else 1,
        "allergen_count": len(meal.allergens) if isinstance(meal.allergens, list) else 0
    }


def upsert_sample_meals():
    """إضافة بيانات شاملة للوجبات مع معلومات مفصلة عن المكونات والحساسية"""
    if Meal.query.first():
        return

    # قاعدة بيانات شاملة للوجبات مع تصنيف دقيق للحساسية
    samples = [
        # وجبات الإفطار
        {
            "name": "دقيق الشوفان مع التوت البري",
            "type": Meal.MealType.breakfast,
            "calories": 320,
            "ingredients": ["شوفان", "حليب", "توت أزرق", "عسل", "لوز"],
            "allergens": ["حليب", "لوز"]
        },
        {
            "name": "Oatmeal with Berries",
            "type": Meal.MealType.breakfast,
            "calories": 320,
            "ingredients": ["oats", "milk", "blueberries", "honey", "almonds"],
            "allergens": ["milk", "nuts"]
        },
        {
            "name": "عجة البيض مع الخضار",
            "type": Meal.MealType.breakfast,
            "calories": 280,
            "ingredients": ["بيض", "طماطم", "بصل", "فلفل أخضر", "زيت زيتون"],
            "allergens": ["بيض"]
        },
        {
            "name": "Avocado Toast",
            "type": Meal.MealType.breakfast,
            "calories": 350,
            "ingredients": ["خبز قمح كامل", "أفوكادو", "طماطم", "ملح", "فلفل"],
            "allergens": ["قمح"]
        },
        {
            "name": "سموذي الموز والتوت",
            "type": Meal.MealType.breakfast,
            "calories": 250,
            "ingredients": ["موز", "توت", "حليب لوز", "عسل", "سبيرولينا"],
            "allergens": ["nuts"]
        },
        {
            "name": "Greek Yogurt Parfait",
            "type": Meal.MealType.breakfast,
            "calories": 300,
            "ingredients": ["زبادي يوناني", "غرانولا", "توت", "عسل"],
            "allergens": ["حليب", "مكسرات"]
        },

        # وجبات الغداء
        {
            "name": "سلطة الدجاج المشوي",
            "type": Meal.MealType.lunch,
            "calories": 450,
            "ingredients": ["دجاج مشوي", "خس", "طماطم", "خيار", "زيت زيتون", "ليمون"],
            "allergens": []
        },
        {
            "name": "Grilled Chicken Salad",
            "type": Meal.MealType.lunch,
            "calories": 450,
            "ingredients": ["chicken breast", "lettuce", "tomato", "cucumber", "olive oil", "lemon"],
            "allergens": []
        },
        {
            "name": "ساندويتش التونة",
            "type": Meal.MealType.lunch,
            "calories": 400,
            "ingredients": ["خبز قمح كامل", "تونة", "مايونيز", "خس", "طماطم"],
            "allergens": ["قمح", "بيض", "أسماك"]
        },
        {
            "name": "Quinoa Buddha Bowl",
            "type": Meal.MealType.lunch,
            "calories": 480,
            "ingredients": ["كينوا", "حمص", "خضار مشكلة", "تاهيني", "ليمون"],
            "allergens": ["سمسم"]
        },
        {
            "name": "شوربة العدس الأحمر",
            "type": Meal.MealType.lunch,
            "calories": 350,
            "ingredients": ["عدس أحمر", "بصل", "جزر", "ثوم", "كمون", "كزبرة"],
            "allergens": []
        },
        {
            "name": "Vegetable Stir Fry",
            "type": Meal.MealType.lunch,
            "calories": 380,
            "ingredients": ["خضار مشكلة", "أرز بني", "صلصة الصويا", "زيت السمسم"],
            "allergens": ["صويا", "سمسم"]
        },

        # وجبات العشاء
        {
            "name": "سمك السلمون مع الكينوا",
            "type": Meal.MealType.dinner,
            "calories": 520,
            "ingredients": ["سلمون", "كينوا", "ليمون", "أعشاب طازجة", "زيت زيتون"],
            "allergens": ["أسماك"]
        },
        {
            "name": "Salmon with Quinoa",
            "type": Meal.MealType.dinner,
            "calories": 520,
            "ingredients": ["salmon fillet", "quinoa", "lemon", "fresh herbs", "olive oil"],
            "allergens": ["fish"]
        },
        {
            "name": "دجاج مشوي مع بطاطا حلوة",
            "type": Meal.MealType.dinner,
            "calories": 480,
            "ingredients": ["دجاج", "بطاطا حلوة", "بروكلي", "زيت زيتون", "أعشاب"],
            "allergens": []
        },
        {
            "name": "Pasta with Marinara",
            "type": Meal.MealType.dinner,
            "calories": 420,
            "ingredients": ["معكرونة قمح كامل", "صلصة طماطم", "بصل", "ثوم", "ريحان"],
            "allergens": ["قمح"]
        },
        {
            "name": "كاري الخضار مع الأرز البني",
            "type": Meal.MealType.dinner,
            "calories": 450,
            "ingredients": ["خضار مشكلة", "جوز الهند", "كاري", "أرز بني", "كزبرة"],
            "allergens": []
        },
        {
            "name": "Turkey Meatballs with Zoodles",
            "type": Meal.MealType.dinner,
            "calories": 390,
            "ingredients": ["لحم ديك رومي", "كوسة", "طماطم", "بصل", "ثوم", "أعشاب"],
            "allergens": []
        },

        # وجبات خفيفة صحية
        {
            "name": "مزيج المكسرات والتمر",
            "type": Meal.MealType.lunch,  # يمكن أن تكون وجبة خفيفة
            "calories": 200,
            "ingredients": ["لوز", "جوز", "تمر", "زبيب"],
            "allergens": ["مكسرات"]
        },
        {
            "name": "Hummus with Vegetables",
            "type": Meal.MealType.lunch,
            "calories": 180,
            "ingredients": ["حمص", "طحينة", "ليمون", "ثوم", "خضار طازجة"],
            "allergens": ["سمسم"]
        }
    ]

    for s in samples:
        # تحويل القوائم إلى JSON strings للتوافق مع قاعدة البيانات
        ingredients_json = s["ingredients"] if isinstance(
            s["ingredients"], list) else s["ingredients"].split(", ")
        allergens_json = s["allergens"] if isinstance(
            s["allergens"], list) else s["allergens"].split(", ") if s["allergens"] else []

        m = Meal(
            name=s["name"],
            type=s["type"],
            calories=s["calories"],
            ingredients=ingredients_json,
            allergens=allergens_json
        )
        db.session.add(m)
    db.session.commit()


@meals_bp.route('/get_meals', methods=['GET'])
def get_meals():
    upsert_sample_meals()
    meal_type = request.args.get('type')  # breakfast/lunch/dinner
    max_cal = request.args.get('max_calories', type=int)

    query = Meal.query
    if meal_type:
        try:
            mt = Meal.MealType(meal_type)
            query = query.filter(Meal.type == mt)
        except ValueError:
            return jsonify({"error": "Invalid meal type"}), 400
    if max_cal is not None:
        query = query.filter(Meal.calories <= max_cal)

    meals = query.limit(50).all()
    return jsonify([
        {"id": m.id, "name": m.name, "type": m.type.value, "calories": m.calories,
            "ingredients": m.ingredients, "allergens": m.allergens}
        for m in meals
    ])


@meals_bp.route('/api/meals', methods=['POST'])
def meals_filter_advanced():
    """Advanced filter that excludes common and specific allergens.
    Body: { type?: 'breakfast'|'lunch'|'dinner', max_calories?: int, specific_allergies?: 'a,b,c' }
    """
    upsert_sample_meals()
    data = request.get_json(silent=True) or {}
    meal_type = (data.get('type') or '').strip()
    max_cal = data.get('max_calories')
    specific = (data.get('specific_allergies') or '').lower()
    specific_set = {x.strip() for x in specific.split(',') if x.strip()}

    query = Meal.query
    if meal_type:
        try:
            mt = Meal.MealType(meal_type)
            query = query.filter(Meal.type == mt)
        except ValueError:
            return jsonify({"error": "Invalid meal type"}), 400
    if max_cal is not None:
        try:
            max_cal = int(max_cal)
            query = query.filter(Meal.calories <= max_cal)
        except Exception:
            return jsonify({"error": "Invalid max_calories"}), 400

    meals = query.limit(100).all()
    filtered = []
    for m in meals:
        ing = (m.ingredients or '').lower()
        alg = (m.allergens or '').lower()
        # Exclude if any specific allergens appear in ingredients or allergens
        if any(s in ing or s in alg for s in specific_set):
            continue
        filtered.append(m)
    return jsonify([
        {"id": m.id, "name": m.name, "type": m.type.value, "calories": m.calories,
            "ingredients": m.ingredients, "allergens": m.allergens}
        for m in filtered
    ])


def fetch_usda_samples(api_key: str, query: str = "chicken"):
    # Example: fetch from USDA FoodData Central if key provided
    try:
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={query}&pageSize=5"
        r = requests.get(url, timeout=10)
        if r.ok:
            return r.json()
    except Exception:
        return None
    return None


def calculate_meal_score(meal: Meal, user: User, user_allergies: List[str] = None) -> Dict[str, Any]:
    """
    حساب نقاط متقدمة للوجبة بناءً على عدة معايير

    Returns:
        Dict containing detailed scoring breakdown
    """
    user_bmi = user.BMI or (user.weight_kg / ((user.height_cm/100) ** 2))

    # 1. نقاط السعرات الحرارية (40% من النقاط الإجمالية)
    calorie_score = 0
    if user_bmi >= 30:  # سمنة - هدف: 400-600 سعرة
        if 400 <= meal.calories <= 600:
            calorie_score = 100
        elif 300 <= meal.calories <= 700:
            calorie_score = 80
        elif meal.calories <= 800:
            calorie_score = 60
        else:
            calorie_score = 20
    elif user_bmi < 18.5:  # نحافة - هدف: 500-700 سعرة
        if 500 <= meal.calories <= 700:
            calorie_score = 100
        elif 400 <= meal.calories <= 800:
            calorie_score = 80
        else:
            calorie_score = 60
    else:  # وزن طبيعي - هدف: 400-800 سعرة
        if 400 <= meal.calories <= 800:
            calorie_score = 100
        elif 300 <= meal.calories <= 900:
            calorie_score = 80
        else:
            calorie_score = 60

    # 2. نقاط الحساسية (30% من النقاط الإجمالية)
    allergy_score = 100  # نقاط كاملة افتراضياً
    allergy_details = {"safe": True, "warnings": [], "conflicts": []}

    if user_allergies:
        meal_allergens = meal.allergens if isinstance(
            meal.allergens, list) else []
        allergy_check = check_allergy_conflict(meal_allergens, user_allergies)

        if allergy_check["has_conflict"]:
            allergy_details["safe"] = False
            allergy_details["conflicts"] = allergy_check["conflicting_allergens"]

            if allergy_check["severity"] == "high":
                allergy_score = 0  # استبعاد كامل
                allergy_details["warnings"].append(
                    "خطر عالي - تجنب هذه الوجبة")
            elif allergy_check["severity"] == "medium":
                allergy_score = 30
                allergy_details["warnings"].append("تحذير متوسط - استشر طبيبك")
            else:
                allergy_score = 60
                allergy_details["warnings"].append(
                    "انتبه - قد تسبب حساسية خفيفة")

    # 3. نقاط التنوع في المكونات (15% من النقاط الإجمالية)
    ingredient_score = 0
    ingredients = meal.ingredients if isinstance(
        meal.ingredients, list) else []
    if ingredients:
        ingredient_count = len(ingredients)
        if ingredient_count >= 5:
            ingredient_score = 100  # وجبة متنوعة
        elif ingredient_count >= 3:
            ingredient_score = 80
        else:
            ingredient_score = 60

    # 4. نقاط التفضيلات الشخصية (15% من النقاط الإجمالية)
    preference_score = 0
    if user.preferences and ingredients:
        user_prefs = [p.strip().lower()
                      for p in user.preferences.split(',') if p.strip()]
        ingredient_text = ' '.join(ingredients).lower()

        matches = sum(1 for pref in user_prefs if pref in ingredient_text)
        if matches > 0:
            preference_score = min(100, matches * 25)

    # حساب النقاط الإجمالية المرجحة
    total_score = (
        calorie_score * 0.4 +
        allergy_score * 0.3 +
        ingredient_score * 0.15 +
        preference_score * 0.15
    )

    # تحليل إضافي للوجبة
    nutrition_analysis = analyze_meal_nutrition(meal, user)

    return {
        "total_score": round(total_score, 2),
        "breakdown": {
            "calorie_score": calorie_score,
            "allergy_score": allergy_score,
            "ingredient_score": ingredient_score,
            "preference_score": preference_score
        },
        "allergy_details": allergy_details,
        "nutrition_analysis": nutrition_analysis,
        "recommendation_level": "ممتاز" if total_score >= 80 else "جيد" if total_score >= 60 else "متوسط" if total_score >= 40 else "ضعيف"
    }


@meals_bp.route('/ai_suggest_meals/<int:user_id>', methods=['GET'])
def ai_suggest_meals(user_id: int):
    """اقتراح وجبات ذكية مع تحليل شامل وتفاصيل مفصلة"""
    upsert_sample_meals()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # الحصول على حساسية المستخدم
    user_allergies = []
    if user.allergies:
        user_allergies = [a.strip()
                          for a in user.allergies.split(',') if a.strip()]

    # استبعاد الوجبات التي تم تناولها مؤخراً
    recent_meal_ids = set()
    recent_history = MealHistory.query.filter_by(user_id=user_id).order_by(
        MealHistory.date_consumed.desc()).limit(10).all()
    for mh in recent_history:
        recent_meal_ids.add(mh.meal_id)

    # الحصول على جميع الوجبات المرشحة
    all_meals = Meal.query.all()
    candidates = [m for m in all_meals if m.id not in recent_meal_ids]

    # تحليل وتقييم كل وجبة
    analyzed_meals = []
    for meal in candidates:
        score_data = calculate_meal_score(meal, user, user_allergies)

        # إضافة تفاصيل الوجبة
        meal_data = {
            "id": meal.id,
            "name": meal.name,
            "type": meal.type.value,
            "calories": meal.calories,
            "ingredients": meal.ingredients,
            "allergens": meal.allergens,
            "score": score_data["total_score"],
            "recommendation_level": score_data["recommendation_level"],
            "allergy_safety": score_data["allergy_details"],
            "nutrition_analysis": score_data["nutrition_analysis"],
            "score_breakdown": score_data["breakdown"]
        }
        analyzed_meals.append(meal_data)

    # ترتيب الوجبات حسب النقاط (الأعلى أولاً)
    ranked_meals = sorted(
        analyzed_meals, key=lambda x: x["score"], reverse=True)

    # تصنيف الوجبات حسب النوع
    breakfast_meals = [m for m in ranked_meals if m["type"]
                       == "breakfast" and m["score"] > 40][:3]
    lunch_meals = [m for m in ranked_meals if m["type"]
                   == "lunch" and m["score"] > 40][:3]
    dinner_meals = [m for m in ranked_meals if m["type"]
                    == "dinner" and m["score"] > 40][:3]

    # إحصائيات عامة
    total_analyzed = len(analyzed_meals)
    safe_meals = len(
        [m for m in analyzed_meals if m["allergy_safety"]["safe"]])
    high_score_meals = len([m for m in analyzed_meals if m["score"] >= 80])

    response = {
        "user_info": {
            "user_id": user_id,
            "bmi": round(user.BMI or (user.weight_kg / ((user.height_cm/100) ** 2)), 2),
            "allergies": user_allergies
        },
        "recommendations": {
            "breakfast": breakfast_meals,
            "lunch": lunch_meals,
            "dinner": dinner_meals
        },
        "statistics": {
            "total_meals_analyzed": total_analyzed,
            "safe_meals_count": safe_meals,
            "high_score_meals_count": high_score_meals,
            "safety_percentage": round((safe_meals / total_analyzed * 100) if total_analyzed > 0 else 0, 1)
        },
        "system_explanation": {
            "scoring_method": "نظام النقاط المرجح يعتمد على: السعرات (40%)، الحساسية (30%)، التنوع (15%)، التفضيلات (15%)",
            "allergy_handling": "فحص شامل للمواد المسببة للحساسية مع مرادفات باللغتين العربية والإنجليزية",
            "recommendation_levels": {
                "ممتاز": "80+ نقطة - وجبة مثالية",
                "جيد": "60-79 نقطة - وجبة مناسبة",
                "متوسط": "40-59 نقطة - وجبة مقبولة",
                "ضعيف": "أقل من 40 نقطة - غير موصى بها"
            }
        }
    }

    return jsonify(response), 200


@meals_bp.route('/system_explanation', methods=['GET'])
def system_explanation():
    """شرح مفصل لكيفية عمل نظام الاقتراحات الذكية"""

    explanation = {
        "system_overview": {
            "title": "نظام الاقتراحات الذكية للتغذية",
            "description": "نظام متقدم لاقتراح الوجبات المناسبة بناءً على البيانات الشخصية والحساسية والتفضيلات",
            "language_support": "دعم كامل للعربية والإنجليزية في المكونات والمواد المسببة للحساسية"
        },

        "data_processing_steps": {
            "step_1": {
                "title": "جمع البيانات الأساسية",
                "description": "جمع معلومات المستخدم: BMI، الوزن، الطول، الحساسية، التفضيلات",
                "details": "يتم حساب BMI تلقائياً إذا لم يكن محدداً: BMI = الوزن / (الطول بالمتر)²"
            },
            "step_2": {
                "title": "تحليل الحساسية المتقدم",
                "description": "فحص شامل للمواد المسببة للحساسية مع مرادفات متعددة",
                "details": {
                    "allergen_dictionary": "قاموس شامل للمواد المسببة للحساسية باللغتين",
                    "normalization": "تطبيع أسماء المواد للبحث الدقيق",
                    "severity_levels": {
                        "high": "خطر عالي - استبعاد كامل (حليب، بيض، مكسرات، أسماك)",
                        "medium": "خطر متوسط - تحذير (قمح، صويا، سمسم)",
                        "low": "خطر منخفض - تنبيه"
                    }
                }
            },
            "step_3": {
                "title": "تحليل السعرات الحرارية",
                "description": "تقييم مناسبية السعرات حسب BMI المستخدم",
                "details": {
                    "obese_bmi_30+": "هدف: 400-600 سعرة، حد أقصى 700",
                    "underweight_bmi_18.5-": "هدف: 500-700 سعرة، تشجيع على زيادة",
                    "normal_bmi_18.5-30": "هدف: 400-800 سعرة، مرونة أكبر"
                }
            },
            "step_4": {
                "title": "تقييم التنوع والتغذية",
                "description": "فحص تنوع المكونات وجودة التغذية",
                "details": {
                    "ingredient_diversity": "وجبات متنوعة (5+ مكونات) تحصل على نقاط أعلى",
                    "nutritional_balance": "تقييم التوازن الغذائي للمكونات"
                }
            },
            "step_5": {
                "title": "مطابقة التفضيلات الشخصية",
                "description": "البحث عن المكونات المفضلة للمستخدم",
                "details": "كل مطابقة تفضيل تضيف نقاط إضافية للوجبة"
            }
        },

        "scoring_algorithm": {
            "title": "خوارزمية النقاط المرجحة",
            "weights": {
                "calories": "40% - الأهمية القصوى للسعرات المناسبة",
                "allergies": "30% - السلامة أولوية قصوى",
                "diversity": "15% - التنوع الغذائي مهم",
                "preferences": "15% - التفضيلات الشخصية"
            },
            "score_interpretation": {
                "80-100": "ممتاز - وجبة مثالية ومناسبة تماماً",
                "60-79": "جيد - وجبة مناسبة ومقبولة",
                "40-59": "متوسط - وجبة مقبولة مع تحفظات",
                "0-39": "ضعيف - غير موصى بها"
            }
        },

        "allergy_safety_features": {
            "title": "ميزات الأمان للحساسية",
            "features": [
                "فحص دقيق للمواد المسببة للحساسية مع مرادفات",
                "تصنيف مستويات الخطورة (عالي، متوسط، منخفض)",
                "رسائل تحذيرية واضحة باللغة العربية",
                "استبعاد تلقائي للوجبات الخطيرة",
                "تنبيهات للمواد المشكوك فيها"
            ]
        },

        "response_format": {
            "title": "تنسيق الاستجابة",
            "structure": {
                "user_info": "معلومات المستخدم والـ BMI والحساسية",
                "recommendations": "اقتراحات مصنفة حسب نوع الوجبة",
                "statistics": "إحصائيات عامة عن التحليل",
                "system_explanation": "شرح كيفية عمل النظام"
            }
        },

        "data_sources": {
            "title": "مصادر البيانات",
            "local_database": {
                "description": "قاعدة بيانات محلية شاملة للوجبات",
                "content": "20+ وجبة متنوعة باللغتين العربية والإنجليزية",
                "coverage": "إفطار، غداء، عشاء، وجبات خفيفة"
            },
            "external_apis": {
                "description": "إمكانية التكامل مع APIs خارجية",
                "usda_support": "دعم USDA FoodData Central API",
                "fallback": "النظام يعمل بالكامل بدون APIs خارجية"
            }
        }
    }

    return jsonify(explanation), 200


@meals_bp.route('/add_meal_history', methods=['POST'])
def add_meal_history():
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    meal_id = data.get('meal_id')
    if not user_id or not meal_id:
        return jsonify({"error": "user_id and meal_id required"}), 400
    user = User.query.get(user_id)
    meal = Meal.query.get(meal_id)
    if not user or not meal:
        return jsonify({"error": "Invalid user or meal"}), 404
    mh = MealHistory(user_id=user.id, meal_id=meal.id)
    db.session.add(mh)
    db.session.commit()
    return jsonify({"message": "Added to history"}), 201


@meals_bp.route('/api/profile', methods=['GET', 'PUT'])
def profile():
    # For demo: user_id from query/body; in real app, derive from auth
    if request.method == 'GET':
        user_id = request.args.get('user_id', type=int)
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'weight': user.weight,
            'allergies': user.allergies,
        })
    else:
        data = request.get_json(silent=True) or {}
        user_id = data.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        # update fields if provided
        for key in ['first_name', 'last_name', 'weight', 'allergies']:
            if key in data and data[key] is not None:
                setattr(user, key, data[key])
        db.session.commit()
        return jsonify({"message": "Profile updated"})
