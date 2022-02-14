# Debugging Deep Learning

## Under Fitting

1. Make mdoel bigger (more layers)
2. Reduce regularization
3. Error analysis
   1. Reduce train error
   2. Reduce validation error
   3. Reduce test error
4. Choose different tool LeNet -> ResNet
5. Tune hyper-params
6. Add Features

## Over Fitting

1. Add more training data
2. Add normaliztion (batch, layer)
3. Data augmentation
4. Regularization (dropout, L2 weight decay)
5. Error analysis
6. Choose different model
7. Tune hyper-params
8. Not recommended
   1. Early stopping
   2. Reduce features
   3. Reduce model size

## Eliminating Errors

1. Analyze test/validation errors
2. Apply domain adaptations

## Hyper param selection

1. Grid search (slow)
2. Random search
3. Coarse-to-fine selection (best)
4. Bayesian

## Debugging Tools

- ipdb.self_trace
- tfdb and tf.data for TensorFlow
