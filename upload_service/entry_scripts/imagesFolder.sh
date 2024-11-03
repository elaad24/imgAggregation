#!/bin/sh



#  directory scripts 
IMAGE_FOLDER="/app/imagesFolder"
PRE_SORT_FOLDER="$IMAGE_FOLDER/preSort"
SORTED_FOLDER="$IMAGE_FOLDER/sorted"

# defults directorys for storing data in them
DUCUMENTS_FOLDER="$IMAGE_FOLDER/sorted/documents"
EXPLORATION_FOLDER="$IMAGE_FOLDER/sorted/exploration"
RECUPES_FOLDER="$IMAGE_FOLDER/sorted/recipes"
RESUMES_FOLDER="$IMAGE_FOLDER/sorted/resumes"

# info.json file 
JSON_FILE="$SORTED_FOLDER/info.json"


# Check if /app/imagesFolder/preSort exists, if not, create it
if [ ! -d "$PRE_SORT_FOLDER" ]; then 
echo "creating $PRE_SORT_FOLDER"
mkdir -p "$PRE_SORT_FOLDER"
fi 

# check if /app/imagesFolder/sorted exists, if not, create it 
if [ ! -d "$SORTED_FOLDER" ]; then
echo "creating $SORTED_FOLDER"
mkdir -p "$SORTED_FOLDER"
fi

# check if /app/imagesFolder/sorted/info.json exists, if not, create it 
if [ ! -d "$JSON_FILE" ]; then
echo "creating $JSON_FILE file"

echo '{
 "documents": {
  "description": "Formal or official papers with structured information or communication.",
  "common_words": [
   "agreement",
   "contract",
   "policy",
   "report",
   "invoice",
   "statement",
   "letter",
   "application",
   "summary",
   "meeting",
   "analysis"
  ]
 },
 "recipes": {
  "description": "Instructions and ingredients for preparing food or drinks.",
  "common_words": [
   "ingredients",
   "preheat",
   "bake",
   "cook",
   "mix",
   "stir",
   "chop",
   "servings",
   "dish",
   "boil",
   "season",
   "garnish"
  ]
 },
 "resumes": {
  "description": "A document summarizing a persons skills, education, and work experience.",
  "common_words": [
   "experience",
   "skills",
   "education",
   "position",
   "responsibilities",
   "achievements",
   "projects",
   "certifications",
   "languages",
   "degree",
   "references"
  ]
 },
 "exploration": {
  "description": "A collection of files related to software exploration, including tests and service images.",
  "common_words": [
   "explorer",
   "classify",
   "tests",
   "images",
   "upload",
   "service",
   "docker",
   "cache",
   "venv",
   "repository"
  ]
 }
}' > "$JSON_FILE"


echo "created $JSON_FILE file"
fi

# check if /app/imagesFolder/sorted/documents exists, if not, create it 
if [ ! -d "$DUCUMENTS_FOLDER" ]; then
echo "creating $DUCUMENTS_FOLDER"
mkdir -p "$DUCUMENTS_FOLDER"
fi

# check if /app/imagesFolder/sorted/exploration exists, if not, create it 
if [ ! -d "$EXPLORATION_FOLDER" ]; then
echo "creating $EXPLORATION_FOLDER"
mkdir -p "$EXPLORATION_FOLDER"
fi

# check if /app/imagesFolder/sorted/recipes exists, if not, create it 
if [ ! -d "$RECUPES_FOLDER" ]; then
echo "creating $RECUPES_FOLDER"
mkdir -p "$RECUPES_FOLDER"
fi

# check if /app/imagesFolder/sorted/resumes exists, if not, create it 
if [ ! -d "$RESUMES_FOLDER" ]; then
echo "creating $RESUMES_FOLDER"
mkdir -p "$RESUMES_FOLDER"
fi

echo "Initialization complete. Starting main application..."

# After ensuring directories exist, start the application (use exec to forward signals properly)
exec "$@"
