# RISE-README.md

These are notes on how to continue training sBert on MedSTS data.

MedSTS is available in `DATA_ROOT / data/projects/<deviations>/ClinicalSTS`

## TODO

* MedSTS currently consists of a train set and a test set; for the purpose of continued sBert training, we also need
a dev set: **Split the train set into a train and dev set.** Are there already such splits in use? **No, it appears not!** 
Although BLUE (https://github.com/ncbi-nlp/BLUE_Benchmark) reports on using a dev MedSTS data set of 75 sentences, apparently
taken from the train set. But there are no details as to how the split was made. **Perhaps in the code?**
* The test set does not contain scores. **Align clinicalSTS.test.txt with clinicalSTS.test.gs.sim.txt to produce a file
that is similar in format to clinicalSTS.train.txt.**
* Use `examples/training_stsbenchmark_continue_training.py` as base and create program to train on MedSTS.