"""
This example loads the pre-trained bert-base-nli-mean-tokens models from the server.
It then fine-tunes this model for some epochs on the STS benchmark dataset.
"""
from torch.utils.data import DataLoader
import math
from sentence_transformers import SentenceTransformer, SentencesDataset, LoggingHandler, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import STSDataReader
import logging
from datetime import datetime
from rise.common import get_data_root

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

# Read the dataset
model_name = 'bert-base-nli-stsb-mean-tokens'
train_batch_size = 16
num_epochs = 4

medsts_root = get_data_root() / "data/projects/az-deviations/ClinicalSTS"
model_root = get_data_root() / "data/projects/az-deviations/resources/sbert"
dev_file_name = "rise-clinicalSTS-dev.csv"
train_file_name = "rise-clinicalSTS-train.csv"


model_save_path = str(model_root) + '/training_stsbenchmark_continue_training-' + model_name + '-' + datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S")
sts_reader = STSDataReader(str(medsts_root), normalize_scores=True, s1_col_idx=0, s2_col_idx=1, score_col_idx=2)

# Load a pre-trained sentence transformer model
model = SentenceTransformer(model_name)

# Convert the dataset to a DataLoader ready for training
logging.info("Read STSbenchmark train dataset")
train_data = SentencesDataset(sts_reader.get_examples(train_file_name), model)
train_dataloader = DataLoader(train_data, shuffle=True, batch_size=train_batch_size)
train_loss = losses.CosineSimilarityLoss(model=model)

logging.info("Read STSbenchmark dev dataset")
dev_data = SentencesDataset(examples=sts_reader.get_examples(dev_file_name), model=model)
dev_dataloader = DataLoader(dev_data, shuffle=False, batch_size=train_batch_size)
evaluator = EmbeddingSimilarityEvaluator(dev_dataloader)

# Configure the training. We skip evaluation in this example
warmup_steps = math.ceil(len(train_data) * num_epochs / train_batch_size * 0.1)  # 10% of train data for warm-up
logging.info("Warmup-steps: {}".format(warmup_steps))

# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=1000,
          warmup_steps=warmup_steps,
          output_path=model_save_path)

##############################################################################
#
# Load the stored model and evaluate its performance on STS benchmark dataset
#
##############################################################################
"""
# The test data file does not exist yet.
model = SentenceTransformer(model_save_path)
test_data = SentencesDataset(examples=sts_reader.get_examples("sts-test.csv"), model=model)
test_dataloader = DataLoader(test_data, shuffle=False, batch_size=train_batch_size)
evaluator = EmbeddingSimilarityEvaluator(test_dataloader)
model.evaluate(evaluator)
"""