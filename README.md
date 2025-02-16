# COGS219_Assignments
This is a repository for COGS219 Assignments.

## 1. Figure Assignment
The figure I reproduced is taken from [this paper](https://www.nature.com/articles/s41467-021-25500-y). 
I used the source data provided in [the OSF repository](https://osf.io/pb3v2), and recreated it using R. 
The source code for the plot was not provided in the repository.

1. A short list of strengths and weaknesses of the original figure:  

The [original figure](Figure_assignment/Figures/original_figure.jpg) shows how the performance of different models increases by the number of hidden layers increases in that model.
Colors effectively differentiate different types of models, which are the configurations of activation functions in the encoder and decoder layers (linear, tanh, sigmoid, rectified linear activation unit, L1-norm regularization). For example, for 'AE-linear-linear' model, it means an autoencoder model with linear encoder and decoder layers.
The authors also applied L1-norm regularization to 'AE-linear-linear' model and also displayed how the performance changes by the regularization parameter. However, this means the differences between the 'AE-linear-linear' model is not necessarily due to the model configuration difference, but rather is due to the regularization. Their figure fail to provide additional distinction between models with different configurations vs within-model variation according to the regularization parameter.

2. Your figure (along with any tweaks/ improvements) and a caption describing what the figure represents.  

On top of the the information that the original figure provides, [my figure](Figure_assignment/Figures/revised_figure.jpg) provides additional distinction between models with different configurations vs within-model variation according to the regularization parameter.
I added differences in the shape of the geom_point to indicate whether it's within-model variation by regularization for 'AE-linear-linear' model (triangle shape), or other models with different configurations.

3. Your code (ideally a GitHub repository)  

My code is in [this folder](Figure_assignment/Data_and_codes).

## 2. Psychopy Assignment