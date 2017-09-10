# Quora pairs
### Issue
- Many people ask similarly worded questions
- Multiple questions with the same intent can cause seekers to spend more time finding the best answer to their question
- Make writers feel they need to answer multiple versions of the same question.

Quora values canonical questions because they provide a better experience to active seekers and writers, and offer more value to both of these groups in the long term.

### Current technique
Quora uses a Random Forest model to identify duplicate questions

### Goal
Classify whether question pairs are duplicates or not.

## 1. Data exploration
According to the description:
- __id__: the id of a training set question pair
- __qid1__, __qid2__: unique ids of each question (only available in train.csv)
- __question1__, __question2__: the full text of each question
- __is_duplicate__: the target variable, set to 1 if question1 and question2 have essentially the same meaning, and 0 otherwise.

## 2. Features
For features:
- __Distance Measure__:
    - __Jaccard Similarity__: ratio of number of shared terms against total number of terms.
- __Shared__:
    - __words (unigrams)__
    - __bigrams__
    - __trigrams__
- __NLP-specific__:
    - __Word movers distance__: semantic similarity between the questions
    - __TD-IDF__: similarity between 2 strings from a corpus (google news here)
- __Other__:
    - __Same final words__: Last words might carry weights
    - __Length of questions__: similar questions would have similar length
    - __Ratio of length between questions__: normalized measure for the length
    - __Question frequency__: a question asked often will be likely to be a duplicate

Everything will be processed without stop words.

## 3. Gradient boosted decision trees

XGBoost is used for supervised learning problems, where we use the training data (with multiple features) __X__ (here _x_train_ with features as columns) to predict a target variable __Y__ (here _y_train_ with 'is_duplicate').

The model is set up with:
- 'binary:logistic' because we expect a binary output (duplicate or no)
- the evaluation metric is 'logloss'
