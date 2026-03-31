-- Table: Ingredient
CREATE TABLE Ingredient (
    Item VARCHAR(255),
    Type VARCHAR(100),
    Unit VARCHAR(50),
    Calories INT,
    Protein INT,
    Carbs INT
);

-- Table: Inventory
CREATE TABLE Inventory (
    Item VARCHAR(255),
    ExpirationDate DATE,
    Location VARCHAR(100),
    RestockThreshold INT,
    Price DECIMAL(10, 2)
);

-- Table: Recipe
CREATE TABLE Recipe (
    Item VARCHAR(255),
    Steps TEXT,
    Servings INT,
    DairyFree BOOLEAN
);

-- Table: RecipeIngredients
CREATE TABLE RecipeIngredients (
    Quantity DECIMAL(10, 2),
    Unit VARCHAR(50)
);

-- Table: Meals
CREATE TABLE Meals (
    Day DATE,
    Type VARCHAR(100),
    Servings INT
);