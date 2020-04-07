# lab7_superyideng

Name: Yi Deng
Email: dengyi@usc.edu

For KNN part:
1. My code of KNN part is in knn.py, and the results were written in knn_results.txt and knn_results_sklearn.txt.

2. Please use $python3 in command line instead of $python, because I use python3 to write the code, just in case that there would be some problem using python.

3. Sample command for my code:
	$ python3 knn.py 5 100 900 data_batch_1
   Since we use a full SVD solver to build the PCA embeddings, the component number should between 0 to minimum of sample number and feature numbers.
   Also, the path to file should be "data_batch_1" since I just put data_batch_1 in the folder in stead of the whole CIFAR-10 dataset.

4. The accuracy of results generated from both myKNN and KNN in sklearn package are 0.14.


For Gaussian Naive Bayes part:
1. My code of Naive Bayes part is in naive_bayes.py

2. Generated results:
My Naive Bayes:
Training acc: 85.71%  Training time: 0.012032032012939453 s
Testing acc: 90.48%  Testing time: 0.0025501251220703125 s
Sklearn Naive Bayes:
Training acc: 89.29%  Training time: 0.0006272792816162109 s
Testing acc: 97.62%  Testing time: 0.0003941059112548828 s
Sklearn SVM:
Training acc: 89.29%  Training time: 0.013493061065673828 s
Testing acc: 97.62%  Testing time: 0.0005888938903808594 s

3. Please also use $python3 instead of $python. Sample command for my code:
	$ python3 naive_bayes.py