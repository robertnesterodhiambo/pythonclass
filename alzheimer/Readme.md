# last code section in calcusl.ipynb is a nn   model for classifying alzheimers images from an MRI scan.

#   Task 3 – Neural Networks (35%)

##  Part 1 (25 marks):

The dataset provided on blackboard contains images of MRI scans from patients diagnosed
with Alzheimer's, separated into four classes; 0: Mild Demented, 1: Moderate Demented, 2:
NonDemented, 3: Very Mild Demented.
Using the datasets provided on Blackboard:
1. Create two basic* Neural Networks. The first should be a Simple Neural Network.
The second, a Convolutional Neural Network.
2. Create two improved* Neural Networks. The first should be a Simple Neural
Network. The second, a Convolutional Neural Network.
You should then conduct a comparative analysis of the two improved models, discussing
the changes you made and how they’ve improved on the basic models.
•
•
A “basic” neural network is “A functional neural network, that contains the
necessary features to constitute as that type of neural network, however may
not produce the best results.”.
An “improved” neural network is “A neural network where changes/adaptations
have been made to the model structure, or training algorithm, to improve the
results delivered by the model.”.

##  Part 2 (10 marks):
1. Using only your optimized Convolutional Neural Network you’ve created. Test a
learning rate of 0.00000001 vs a learning rate of 10 (using the SGD optimizer from
the learning material & keeping all other parameters in your model the same).
Discuss what happens when these values are used and why. Furthermore, discuss in
detail, the advantages and disadvantages of a higher & lower learning rate, and its
impact.
2. Secondly, discuss in detail, the advantages and disadvantages of a higher & lower
batch size.