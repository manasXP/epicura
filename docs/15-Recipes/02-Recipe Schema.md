
The entities are needed to define a recipe

1. Recipe
2. Ingredient
3. Cooking Instruction 

Each Recipe has an ID  (Primary Key, UINT16), Recipe Name, Protein in gm, Carbs in gm, Fats in gm and Calories in kCal. It can have at least one cuisine.  Cuisines include American, Thai, Indian, Japanese, Korean, Italian, Chinese, and Global. Category include Vegetarian, Protein Rich, Vegan, Quick Recipe. Recipe can represent any of those category and when no category is mentioned it is non-vegetarian implicitly. 

Each Recipe has a list of ingredients. Ingredients are delivered via SLD, p-ASD and CID. SLD ingredient can be oil or water and specified quantity for each is ml. pASD has 6 dispensing box to deliver in increments of 1/4 tsp of each ingredient. Boxes are numbered Box1, Box2, Box3, Box4, Box5, Box6. CID is delivered slotwise. Total 5 slots Slot1, Slot2, Slot3, Slot4, Slot5. 

Cooking Instructions are given in form of Segments for each Recipe ID. Each recipe has upto 5 cooking segments. In each cooking segment, the following attributes are provided. Segment ID (1 to 5), Pot surface temperature to start, SLD ingredient type and quantity in ml, pASD Box id and multiple of 1/4 tsp, CID Slot ID. Heat Profile of the cooking surface as power input to Induction surface enumerated Low, Low Medium, Medium, Medium High, and High. Also, how many seconds is the heat applied?  Stirring Profile is Rotation (Slow, Normal, Fast), Direction (Forward, Reverse, Alternating), and Stirring duration in seconds.  
